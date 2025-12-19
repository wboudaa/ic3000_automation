#!/usr/bin/env python3
"""
IC3000 Software Upgrade API Client
Handles firmware/software upgrades via REST API
"""

import os
import sys
import requests
from typing import Tuple, Any
from ic3000_api_client import IC3000APIClient

class IC3000UpgradeClient(IC3000APIClient):
    """Extended API client for software upgrades"""
    
    def upload_firmware(self, firmware_path: str) -> Tuple[bool, str]:
        """
        Upload firmware file to device
        
        Args:
            firmware_path: Path to .bin firmware file
            
        Returns:
            (success: bool, message: str)
        """
        if not self.authenticated or not self.auth_token:
            return False, "Not authenticated"
        
        # Validate file exists
        if not os.path.exists(firmware_path):
            return False, f"File not found: {firmware_path}"
        
        # Get filename and size
        filename = os.path.basename(firmware_path)
        filesize = os.path.getsize(firmware_path)
        filesize_mb = filesize / (1024 * 1024)
        
        print(f"      Uploading: {filename} ({filesize_mb:.1f} MB)")
        
        try:
            # Read file content
            with open(firmware_path, 'rb') as f:
                file_content = f.read()
            
            # Upload file
            # Discovered API: POST /file/upload with raw binary content
            response = self.session.post(
                f"{self.base_url}/file/upload",
                data=file_content,
                headers={
                    "X-IDA-AUTH-TOKEN": self.auth_token,
                    "Content-Type": "x-www-form-urlencoded",
                    "Content-Disposition": filename,
                    "Origin": f"https://{self.ip}:8443",
                    "Referer": f"https://{self.ip}:8443/"
                },
                timeout=300  # 5 minutes timeout for large files
            )
            
            if response.status_code in [200, 201, 204]:
                return True, f"Upload successful ({filesize_mb:.1f} MB transferred)"
            else:
                return False, f"Upload failed (status: {response.status_code}): {response.text[:200]}"
                
        except Exception as e:
            return False, f"Upload error: {str(e)}"
    
    def install_firmware(self, filename: str) -> Tuple[bool, str]:
        """
        Trigger firmware installation after upload
        
        Args:
            filename: Name of the uploaded firmware file
            
        Returns:
            (success: bool, message: str)
        """
        if not self.authenticated or not self.auth_token:
            return False, "Not authenticated"
        
        try:
            # Trigger installation
            # Discovered API: POST /firmware/install
            # Note: Device may start installing immediately without sending response
            response = self.session.post(
                f"{self.base_url}/firmware/install",
                headers={
                    "X-IDA-AUTH-TOKEN": self.auth_token,
                    "Content-Disposition": filename,
                    "Origin": f"https://{self.ip}:8443",
                    "Referer": f"https://{self.ip}:8443/"
                },
                timeout=60  # Increased timeout
            )
            
            if response.status_code in [200, 201, 204]:
                return True, "Installation initiated successfully"
            else:
                return False, f"Installation failed (status: {response.status_code}): {response.text[:200]}"
                
        except requests.exceptions.ReadTimeout:
            # Timeout is actually OK - device likely started installing
            return True, "Installation initiated (device started installing, connection timed out - this is normal)"
        except requests.exceptions.ConnectionError as e:
            # Connection error might also mean device started rebooting
            if "Connection aborted" in str(e) or "Remote end closed" in str(e):
                return True, "Installation initiated (device started installing/rebooting - this is normal)"
            return False, f"Connection error: {str(e)[:100]}"
        except Exception as e:
            return False, f"Installation error: {str(e)[:100]}"
    
    def upgrade_firmware(self, firmware_path: str) -> Tuple[bool, str]:
        """
        Complete firmware upgrade: upload + install
        
        Args:
            firmware_path: Path to .bin firmware file
            
        Returns:
            (success: bool, message: str)
        """
        filename = os.path.basename(firmware_path)
        
        # Step 1: Upload
        print(f"      [1/2] Uploading firmware...")
        success, message = self.upload_firmware(firmware_path)
        if not success:
            return False, f"Upload failed: {message}"
        
        print(f"      ✓ {message}")
        
        # Step 2: Install
        print(f"      [2/2] Triggering installation...")
        success, message = self.install_firmware(filename)
        if not success:
            return False, f"Installation failed: {message}"
        
        print(f"      ✓ {message}")
        
        return True, "Firmware upgrade completed successfully"


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='IC3000 Software Upgrade via REST API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Upload and install firmware
  python3 ic3000_upgrade_api.py 192.168.69.142 admin password \\
      --firmware IC3000-K9-1.5.1.SPA
  
  # Just upload (no install)
  python3 ic3000_upgrade_api.py 192.168.69.142 admin password \\
      --firmware IC3000-K9-1.5.1.SPA --upload-only
  
  # Just install (already uploaded)
  python3 ic3000_upgrade_api.py 192.168.69.142 admin password \\
      --install IC3000-K9-1.5.1.SPA

Warning:
  - Firmware upgrade will reboot the device!
  - Ensure you have the correct firmware file
  - Device will be unavailable during upgrade (~5-10 minutes)
  - Have console access in case of issues
        """
    )
    
    parser.add_argument('ip', help='Device IP address')
    parser.add_argument('username', help='Username')
    parser.add_argument('password', help='Password')
    
    parser.add_argument('--firmware', help='Path to firmware .bin file')
    parser.add_argument('--upload-only', action='store_true',
                       help='Only upload, do not trigger installation')
    parser.add_argument('--install', help='Install already uploaded firmware (filename)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.firmware and not args.install:
        print("✗ Error: Must specify --firmware or --install")
        parser.print_help()
        sys.exit(1)
    
    print("="*70)
    print("IC3000 SOFTWARE UPGRADE")
    print("="*70)
    print(f"Target: {args.ip}")
    print(f"User: {args.username}")
    
    if args.firmware:
        if not os.path.exists(args.firmware):
            print(f"\n✗ Error: Firmware file not found: {args.firmware}")
            sys.exit(1)
        
        filesize_mb = os.path.getsize(args.firmware) / (1024 * 1024)
        print(f"Firmware: {os.path.basename(args.firmware)} ({filesize_mb:.1f} MB)")
    
    print("="*70)
    print()
    
    # Create client
    client = IC3000UpgradeClient(args.ip, args.username, args.password)
    
    # Step 1: Authenticate
    print("[1/3] Authenticating...")
    success, message = client.login()
    
    if not success:
        print(f"      ✗ {message}")
        sys.exit(1)
    
    print(f"      ✓ Authenticated (token: {client.auth_token[:8]}...)")
    
    # Step 2: Upload firmware
    if args.firmware:
        print(f"\n[2/3] Uploading firmware...")
        print(f"      This may take several minutes for large files...")
        
        success, message = client.upload_firmware(args.firmware)
        
        if not success:
            print(f"      ✗ {message}")
            sys.exit(1)
        
        print(f"      ✓ {message}")
        
        filename = os.path.basename(args.firmware)
    else:
        print(f"\n[2/3] Skipping upload (using already uploaded file)")
        filename = args.install
    
    # Step 3: Install firmware
    if args.upload_only:
        print(f"\n[3/3] Skipping installation (--upload-only specified)")
        print("\n✓ Upload complete. To install later, run:")
        print(f"  python3 ic3000_upgrade_api.py {args.ip} {args.username} <password> \\")
        print(f"      --install {filename}")
    else:
        print(f"\n[3/3] Triggering installation...")
        print(f"      ⚠️  Device will reboot during installation!")
        
        success, message = client.install_firmware(filename)
        
        if not success:
            print(f"      ✗ {message}")
            sys.exit(1)
        
        print(f"      ✓ {message}")
        
        print("\n" + "="*70)
        print("FIRMWARE UPGRADE INITIATED")
        print("="*70)
        print("\n⚠️  Important:")
        print("  - Device is now installing firmware")
        print("  - Device will automatically reboot")
        print("  - Upgrade takes approximately 5-10 minutes")
        print("  - Device will be unavailable during this time")
        print("  - Do NOT power off the device during upgrade")
        print("\nWait 10 minutes, then verify:")
        print(f"  1. Device is accessible: https://{args.ip}:8443")
        print(f"  2. Check firmware version in web UI")
        print("="*70)
    
    print()

if __name__ == '__main__':
    main()

