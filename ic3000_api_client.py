#!/usr/bin/env python3
"""
IC3000 REST API Client - Uses port 8444 REST API instead of web scraping
Discovered via browser DevTools showing XHR requests on port 8444
"""

import os
import requests
import urllib3
import json
import sys
from typing import Dict, Any, Tuple, Optional

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def _default_timeout() -> int:
    """Request timeout in seconds; use env IC3000_REQUEST_TIMEOUT for slow devices."""
    try:
        return int(os.environ.get("IC3000_REQUEST_TIMEOUT", "30"))
    except ValueError:
        return 30


class IC3000APIClient:
    """REST API client for IC3000 devices"""
    
    def __init__(self, ip: str, username: str, password: str, timeout: Optional[int] = None):
        self.ip = ip
        self.username = username
        self.password = password
        self.timeout = timeout if timeout is not None else _default_timeout()
        self.session = requests.Session()
        self.session.verify = False
        self.base_url = f"https://{ip}:8444"  # API port, not web UI port (8443)
        self.auth_url = f"https://{ip}:8443"  # Auth endpoint on port 8443
        self.authenticated = False
        self.auth_token = None  # X-IDA-AUTH-TOKEN
    
    def login(self) -> Tuple[bool, str]:
        """
        Authenticate with the device
        
        Authentication flow discovered via browser DevTools:
        1. Login to web UI on port 8443 (establish session)
        2. POST to /iox/api/v2/hosting/tokenservice with that session + Basic Auth
        3. Receive X-IDA-AUTH-TOKEN in response
        4. Use token in X-IDA-AUTH-TOKEN header for API calls on port 8444
        
        Returns: (success: bool, message: str)
        """
        try:
            # Step 1: Login to web UI on port 8443 to establish session
            login_payload = {
                'j_username': self.username,
                'j_password': self.password,
                'action': 'login',
                'flashVersion': '9.0.47.0',
                'hasCorrectFlashVersion': 'false'
            }
            
            login_response = self.session.post(
                self.auth_url,  # https://IP:8443
                data=login_payload,
                timeout=self.timeout,
                allow_redirects=True
            )
            
            # Verify we can access admin page (validates session)
            admin_check = self.session.get(
                f"{self.auth_url}/admin",
                timeout=self.timeout
            )
            
            if admin_check.status_code != 200:
                return False, f"Web UI login failed (status: {admin_check.status_code})"
            
            # Step 2: Get authentication token from tokenservice using the authenticated session
            import base64
            
            # Create Basic Auth header
            credentials = f"{self.username}:{self.password}"
            b64_credentials = base64.b64encode(credentials.encode()).decode()
            
            # Request token from tokenservice endpoint with authenticated session
            token_response = self.session.post(
                f"{self.auth_url}/iox/api/v2/hosting/tokenservice",
                headers={
                    "Authorization": f"Basic {b64_credentials}",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-Requested-With": "XMLHttpRequest"
                },
                timeout=self.timeout
            )
            
            if token_response.status_code != 200:
                return False, f"Token service failed (status: {token_response.status_code})"
            
            # Step 3: Extract token from response
            try:
                token_data = token_response.json()
                
                # The actual response format: {"token": {"id": "uuid"}}
                if isinstance(token_data, dict):
                    # Try nested structure first: token.id
                    if 'token' in token_data and isinstance(token_data['token'], dict):
                        token_value = token_data['token'].get('id')
                    else:
                        # Try flat structure as fallback
                        token_value = (
                            token_data.get('id') or
                            token_data.get('token') or 
                            token_data.get('authToken') or 
                            token_data.get('idaAuthToken') or
                            token_data.get('X-IDA-AUTH-TOKEN')
                        )
                    
                    # Ensure we have a string, not a dict or other object
                    if token_value:
                        self.auth_token = str(token_value)
                    else:
                        return False, f"No token field in response: {token_response.text[:100]}"
                        
                elif isinstance(token_data, str):
                    # Sometimes the response is just the token as a string
                    self.auth_token = token_data.strip('"')
                else:
                    return False, f"Unexpected token response format: {type(token_data)}"
                
                if not self.auth_token:
                    return False, f"Empty token in response: {token_response.text[:100]}"
                    
            except ValueError as e:
                # JSON parsing failed, try to extract UUID pattern from text
                import re
                uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
                match = re.search(uuid_pattern, token_response.text, re.IGNORECASE)
                
                if match:
                    self.auth_token = match.group(0)
                else:
                    return False, f"Cannot parse JSON or extract token: {token_response.text[:100]}"
            except Exception as e:
                return False, f"Error extracting token: {str(e)}"
            
            # Step 4: Test the token by accessing the API
            # Include all headers that the browser sends
            test_response = self.session.get(
                f"{self.base_url}/ntp",
                headers={
                    "X-IDA-AUTH-TOKEN": self.auth_token,
                    "Content-Type": "application/json",
                    "Origin": f"https://{self.ip}:8443",
                    "Referer": f"https://{self.ip}:8443/"
                },
                timeout=self.timeout
            )
            
            if test_response.status_code == 200:
                self.authenticated = True
                return True, f"Authentication successful (token: {self.auth_token[:8]}...)"
            else:
                return False, f"Token validation failed (status: {test_response.status_code})"
                
        except requests.exceptions.ConnectionError as e:
            return False, f"Connection failed: {str(e)[:100]}"
        except requests.exceptions.Timeout:
            return False, "Connection timeout"
        except Exception as e:
            return False, f"Login error: {str(e)[:100]}"
    
    def check_api_availability(self) -> Tuple[bool, str]:
        """
        Check if the REST API is available on port 8444
        Note: The API requires session authentication, so we check if the endpoint responds
        Returns: (available: bool, message: str)
        """
        try:
            # Try to access the NTP endpoint (actual discovered endpoint)
            response = self.session.get(
                f"{self.base_url}/ntp",
                timeout=min(10, self.timeout)
            )
            
            # Even if we get 401 (unauthorized), it means the API is there
            if response.status_code in [200, 401, 403]:
                return True, f"API is available (status: {response.status_code})"
            else:
                return False, f"API responded with status {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            return False, "Cannot connect to port 8444"
        except requests.exceptions.Timeout:
            return False, "Connection timeout"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_ntp_config(self) -> Tuple[bool, Any]:
        """
        Get current NTP configuration
        Actual endpoint discovered: GET /ntp (not /config/ntp)
        Returns: (success: bool, config: dict or error message)
        """
        if not self.authenticated or not self.auth_token:
            return False, "Not authenticated"
        
        try:
            # Use the actual endpoint discovered in browser DevTools
            # Must include X-IDA-AUTH-TOKEN header and other required headers
            response = self.session.get(
                f"{self.base_url}/ntp",
                headers={
                    "X-IDA-AUTH-TOKEN": self.auth_token,
                    "Content-Type": "application/json",
                    "Origin": f"https://{self.ip}:8443",
                    "Referer": f"https://{self.ip}:8443/"
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                try:
                    config = response.json()
                    return True, config
                except Exception:
                    # If not JSON, return raw text
                    return True, response.text
            else:
                return False, f"GET failed with status {response.status_code}: {response.text[:200]}"
                
        except Exception as e:
            return False, f"GET error: {str(e)}"
    
    def set_ntp_config(self, ntp_server: str) -> Tuple[bool, str]:
        """
        Set NTP server configuration
        Uses the actual payload structure discovered in browser DevTools
        
        Args:
            ntp_server: NTP server address (e.g., "pool.ntp.org" or "192.168.1.1")
                       Can be comma-separated for multiple servers: "192.168.1.1, 192.168.1.2"
        Returns: (success: bool, message: str)
        """
        if not self.authenticated or not self.auth_token:
            return False, "Not authenticated"
        
        try:
            # Support multiple NTP servers (comma-separated)
            if ',' in ntp_server:
                ntp_servers = [s.strip() for s in ntp_server.split(',')]
            else:
                ntp_servers = [ntp_server]
            
            # Build ntpServerConfig array with multiple servers
            ntp_server_config = [{"NTPServer": server} for server in ntp_servers]
            
            # Build payload using EXACT structure from browser DevTools
            # Original: [{"ntpConfig":{"autoGet":false,"minPoll":6,"maxPoll":10,"ntpServerConfig":[{"NTPServer":"192.168.69.16"}],"ntpAuthConfig":[]}}]
            payload = [{
                "ntpConfig": {
                    "autoGet": False,
                    "minPoll": 6,
                    "maxPoll": 10,
                    "ntpServerConfig": ntp_server_config,
                    "ntpAuthConfig": []
                }
            }]
            
            # Send PUT request with all required headers
            response = self.session.put(
                f"{self.base_url}/config/ntp",
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "X-IDA-AUTH-TOKEN": self.auth_token,
                    "Origin": f"https://{self.ip}:8443",
                    "Referer": f"https://{self.ip}:8443/"
                },
                timeout=self.timeout
            )
            
            if response.status_code in [200, 201, 204]:
                server_list = ', '.join(ntp_servers) if len(ntp_servers) > 1 else ntp_servers[0]
                return True, f"NTP configured: {server_list}"
            else:
                # Try to get error details from response
                try:
                    error_detail = response.json()
                    return False, f"PUT failed ({response.status_code}): {error_detail}"
                except:
                    return False, f"PUT failed with status {response.status_code}: {response.text[:200]}"
                    
        except Exception as e:
            return False, f"PUT error: {str(e)}"
    
    def get_system_info(self) -> Tuple[bool, Any]:
        """
        Get system information
        Returns: (success: bool, info: dict or error message)
        """
        if not self.authenticated or not self.auth_token:
            return False, "Not authenticated"
        
        endpoints = [
            '/system/info',
            '/system',
            '/info',
            '/status',
        ]
        
        for endpoint in endpoints:
            try:
                response = self.session.get(
                    f"{self.base_url}{endpoint}",
                    headers={
                        "X-IDA-AUTH-TOKEN": self.auth_token,
                        "Content-Type": "application/json",
                        "Origin": f"https://{self.ip}:8443",
                        "Referer": f"https://{self.ip}:8443/"
                    },
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    try:
                        return True, response.json()
                    except Exception:
                        return True, response.text
            except Exception:
                continue
        
        return False, "Could not retrieve system info"


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='IC3000 REST API Client - Port 8444',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check if API is available
  python3 ic3000_api_client.py 192.168.69.142 --check
  
  # Get current NTP configuration
  python3 ic3000_api_client.py 192.168.69.142 admin password --get-ntp
  
  # Set NTP server
  python3 ic3000_api_client.py 192.168.69.142 admin password --set-ntp pool.ntp.org
  
  # Slow device: use 60s timeout (or set IC3000_REQUEST_TIMEOUT=60)
  python3 ic3000_api_client.py 192.168.69.142 admin password --set-ntp pool.ntp.org --timeout 60
  
  # Get system information
  python3 ic3000_api_client.py 192.168.69.142 admin password --system-info
        """
    )
    
    parser.add_argument('ip', help='Device IP address')
    parser.add_argument('username', nargs='?', help='Username (if authentication required)')
    parser.add_argument('password', nargs='?', help='Password (if authentication required)')
    
    parser.add_argument('--timeout', type=int, default=None,
                        help='Request timeout in seconds (default: 30 or IC3000_REQUEST_TIMEOUT). Use 60+ for slow devices.')
    
    parser.add_argument('--check', action='store_true',
                       help='Check if REST API is available on port 8444')
    parser.add_argument('--get-ntp', action='store_true',
                       help='Get current NTP configuration')
    parser.add_argument('--set-ntp', metavar='SERVER',
                       help='Set NTP server')
    parser.add_argument('--system-info', action='store_true',
                       help='Get system information')
    
    args = parser.parse_args()
    
    # Create client (optional timeout for slow devices)
    client = IC3000APIClient(
        args.ip,
        args.username or '',
        args.password or '',
        timeout=args.timeout
    )
    
    print("="*70)
    print("IC3000 REST API CLIENT")
    print("="*70)
    print(f"Target: https://{args.ip}:8444")
    print("="*70)
    print()
    
    # Check API availability (no auth required)
    if args.check:
        print("Checking API availability...")
        success, message = client.check_api_availability()
        
        if success:
            print(f"✓ {message}")
            print("\nThe REST API is available on port 8444!")
            print("You can now use --get-ntp and --set-ntp commands with credentials.")
        else:
            print(f"✗ {message}")
            print("\nThe REST API is NOT available on port 8444.")
            print("This device may not support the REST API.")
        
        sys.exit(0 if success else 1)
    
    # All other commands require authentication
    if not args.username or not args.password:
        print("✗ Error: Username and password required for this operation")
        print("\nUsage: python3 ic3000_api_client.py <ip> <username> <password> <command>")
        sys.exit(1)
    
    # Authenticate
    print(f"[1/2] Authenticating as '{args.username}'...")
    success, message = client.login()
    
    if not success:
        print(f"      ✗ {message}")
        sys.exit(1)
    
    print(f"      ✓ {message}")
    
    # Execute requested command
    print(f"\n[2/2] Executing command...")
    
    if args.get_ntp:
        success, result = client.get_ntp_config()
        
        if success:
            print("      ✓ NTP configuration retrieved:\n")
            if isinstance(result, dict):
                print(json.dumps(result, indent=2))
            else:
                print(result)
        else:
            print(f"      ✗ {result}")
            sys.exit(1)
    
    elif args.set_ntp:
        ntp_server = args.set_ntp
        print(f"      Setting NTP server to: {ntp_server}")
        
        success, message = client.set_ntp_config(ntp_server)
        
        if success:
            print(f"      ✓ {message}")
            
            # Verify the change
            print("\n      Verifying configuration...")
            success, config = client.get_ntp_config()
            if success:
                print("      New configuration:")
                if isinstance(config, dict):
                    print(json.dumps(config, indent=2))
                else:
                    print(config)
        else:
            print(f"      ✗ {message}")
            sys.exit(1)
    
    elif args.system_info:
        success, info = client.get_system_info()
        
        if success:
            print("      ✓ System information:\n")
            if isinstance(info, dict):
                print(json.dumps(info, indent=2))
            else:
                print(info)
        else:
            print(f"      ✗ {info}")
            sys.exit(1)
    
    else:
        print("      No command specified. Use --get-ntp, --set-ntp, or --system-info")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("DONE")
    print("="*70)

if __name__ == '__main__':
    main()

