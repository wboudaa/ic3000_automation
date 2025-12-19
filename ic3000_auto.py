#!/usr/bin/env python3
# IC3000 Device Manager - Unified NTP and Software Upgrade Tool

import os
import sys
import csv
import yaml
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
import argparse

# Import our API clients
from ic3000_api_client import IC3000APIClient
from ic3000_upgrade_api import IC3000UpgradeClient


class IC3000Config:
    def __init__(self, config_file='ic3000_config.yaml'):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        if not os.path.exists(self.config_file):
            print(f'Warning: Config file not found: {self.config_file}')
            print('Using default configuration')
            return self.default_config()
        
        try:
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            print(f'Error loading config: {e}')
            print('Using default configuration')
            return self.default_config()
    
    def default_config(self):
        return {
            'devices_csv': 'ic3000_devices.csv',
            'software': {'firmware_path': '', 'firmware_name': ''},
            'ntp': {'default_server': '192.168.69.254'},
            'parallel': {'max_workers_upgrade': 3, 'max_workers_ntp': 10, 'batch_size': 0, 'batch_delay': 60},
            'timeouts': {'connection': 30, 'upload': 600, 'install': 120},
            'output': {'results_dir': 'results', 'verbose': True, 'show_progress': True},
            'safety': {'require_confirmation': True, 'test_mode_default': False, 'prompt_between_batches': True}
        }
    
    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value


class IC3000Manager:
    def __init__(self, config):
        self.config = config
        self.results_dir = config.get('output.results_dir', 'results')
        os.makedirs(self.results_dir, exist_ok=True)
    
    def load_devices(self, csv_file=None, test_mode=False, limit=None):
        if csv_file is None:
            csv_file = self.config.get('devices_csv', 'ic3000_devices.csv')
        
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f'Device CSV not found: {csv_file}')
        
        with open(csv_file, 'r') as f:
            devices = list(csv.DictReader(f))
        
        if test_mode:
            devices = devices[:3]
            print(f'\nTEST MODE: Processing only {len(devices)} devices\n')
        elif limit:
            devices = devices[:limit]
            print(f'\nLimited to {len(devices)} devices\n')
        
        return devices
    
    def configure_ntp(self, device):
        device_name = device.get('DeviceName') or device.get('Hostname') or device['IPAddress']
        ip = device['IPAddress']
        username = device['Username']
        password = device['Password']
        
        # Support multiple NTP servers: comma-separated
        ntp_server = device.get('NTPServer', self.config.get('ntp.default_server'))
        
        result = {
            'DeviceName': device_name,
            'IPAddress': ip,
            'Operation': 'NTP',
            'Target': ntp_server,  # Keep full list for display
            'Status': 'Failed',
            'Message': ''
        }
        
        try:
            client = IC3000APIClient(ip, username, password)
            success, message = client.login()
            if not success:
                result['Message'] = f'Auth: {message}'
                return result
            
            success, message = client.set_ntp_config(ntp_server)
            if not success:
                result['Message'] = message
                return result
            
            success, config = client.get_ntp_config()
            if success:
                result['Status'] = 'Success'
                result['Message'] = 'NTP configured and verified'
            else:
                result['Status'] = 'Warning'
                result['Message'] = 'Configured but verification failed'
        
        except Exception as e:
            result['Message'] = f'Exception: {str(e)[:100]}'
        
        return result
    
    def upgrade_firmware(self, device, firmware_path):
        device_name = device.get('DeviceName') or device.get('Hostname') or device['IPAddress']
        ip = device['IPAddress']
        username = device['Username']
        password = device['Password']
        
        filename = os.path.basename(firmware_path)
        
        result = {
            'DeviceName': device_name,
            'IPAddress': ip,
            'Operation': 'Upgrade',
            'Target': filename,
            'Status': 'Failed',
            'Message': ''
        }
        
        try:
            client = IC3000UpgradeClient(ip, username, password)
            success, message = client.login()
            if not success:
                result['Message'] = f'Auth: {message}'
                return result
            
            success, message = client.upload_firmware(firmware_path)
            if not success:
                result['Message'] = f'Upload: {message}'
                return result
            
            success, message = client.install_firmware(filename)
            if not success:
                result['Status'] = 'Warning'
                result['Message'] = f'Uploaded but install failed: {message}'
                return result
            
            result['Status'] = 'Success'
            result['Message'] = 'Upgrade initiated (device will reboot)'
        
        except Exception as e:
            result['Message'] = f'Exception: {str(e)[:100]}'
        
        return result
    
    def process_batch(self, devices, operation, **kwargs):
        max_workers = kwargs.get('max_workers', 5)
        firmware_path = kwargs.get('firmware_path')
        
        results = []
        completed = 0
        total = len(devices)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            if operation == 'ntp':
                futures = {executor.submit(self.configure_ntp, device): device for device in devices}
            elif operation == 'upgrade':
                futures = {executor.submit(self.upgrade_firmware, device, firmware_path): device for device in devices}
            else:
                raise ValueError(f'Unknown operation: {operation}')
            
            for future in as_completed(futures):
                device = futures[future]
                try:
                    result = future.result(timeout=kwargs.get('timeout', 600))
                    results.append(result)
                    completed += 1
                    
                    status_icon = '✓' if result['Status'] == 'Success' else '✗'
                    target_info = f' → {result["Target"]}' if 'Target' in result else ''
                    print(f'[{completed}/{total}] {status_icon} {result["DeviceName"]} ({result["IPAddress"]}){target_info}')
                    if result['Status'] != 'Success' and result['Message']:
                        print(f'            {result["Message"][:70]}')
                
                except Exception as e:
                    device_name = device.get('DeviceName') or device.get('Hostname') or device['IPAddress']
                    print(f'[{completed+1}/{total}] FAIL {device_name} - {str(e)[:50]}')
                    results.append({
                        'DeviceName': device_name,
                        'IPAddress': device['IPAddress'],
                        'Operation': operation,
                        'Status': 'Failed',
                        'Message': str(e)[:100]
                    })
                    completed += 1
        
        return results
    
    def save_results(self, results, operation):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.results_dir, f'ic3000_{operation}_{timestamp}.csv')
        
        if not results:
            return None
        
        fieldnames = list(results[0].keys())
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        return filename
    
    def run(self, operation, **kwargs):
        test_mode = kwargs.get('test_mode', self.config.get('safety.test_mode_default', False))
        devices = self.load_devices(kwargs.get('csv_file'), test_mode, kwargs.get('limit'))
        
        if not devices:
            print('No devices to process')
            return
        
        batch_size = kwargs.get('batch_size', self.config.get('parallel.batch_size', 0))
        batch_delay = kwargs.get('batch_delay', self.config.get('parallel.batch_delay', 60))
        
        if operation == 'ntp':
            max_workers = kwargs.get('max_workers', self.config.get('parallel.max_workers_ntp', 10))
            op_desc = 'NTP Configuration'
        elif operation == 'upgrade':
            max_workers = kwargs.get('max_workers', self.config.get('parallel.max_workers_upgrade', 3))
            op_desc = 'Software Upgrade'
            firmware_path = kwargs.get('firmware_path') or self.config.get('software.firmware_path')
            if not firmware_path or not os.path.exists(firmware_path):
                print(f'Firmware file not found: {firmware_path}')
                return
            kwargs['firmware_path'] = firmware_path
        else:
            print(f'Unknown operation: {operation}')
            return
        
        print('='*80)
        print(f'IC3000 {op_desc.upper()}')
        print('='*80)
        if operation == 'upgrade' and kwargs.get('firmware_path'):
            fw_name = os.path.basename(kwargs['firmware_path'])
            fw_size = os.path.getsize(kwargs['firmware_path']) / (1024 * 1024)
            print(f'Firmware: {fw_name} ({fw_size:.1f} MB)')
        print(f'Total Devices: {len(devices)}')
        print(f'Parallel Workers: {max_workers}')
        if batch_size > 0:
            print(f'Batch Size: {batch_size} devices per batch')
            print(f'Batch Delay: {batch_delay}s between batches')
        print('='*80)
        print()
        
        print('Devices to configure:')
        for i, d in enumerate(devices[:5], 1):
            name = d.get('DeviceName') or d.get('Hostname') or d['IPAddress']
            if operation == 'ntp':
                ntp = d.get('NTPServer', self.config.get('ntp.default_server'))
                # Show multiple NTP servers if present
                if ',' in ntp:
                    ntp_list = [s.strip() for s in ntp.split(',')]
                    ntp_display = ', '.join(ntp_list)
                    print(f'  {i}. {name} ({d["IPAddress"]}) → NTP: {ntp_display}')
                else:
                    print(f'  {i}. {name} ({d["IPAddress"]}) → NTP: {ntp}')
            else:
                print(f'  {i}. {name} ({d["IPAddress"]})')
        if len(devices) > 5:
            print(f'  ... and {len(devices) - 5} more')
        print()
        
        if self.config.get('safety.require_confirmation', True) and not test_mode:
            confirm = input(f'Proceed with {op_desc} on {len(devices)} devices? [y/N]: ')
            if confirm.lower() not in ['y', 'yes']:
                print('Cancelled')
                return
        
        print('\n' + '='*80)
        print(f'STARTING {op_desc.upper()}')
        print('='*80)
        print()
        
        start_time = datetime.now()
        all_results = []
        
        if batch_size > 0 and batch_size < len(devices):
            batches = [devices[i:i+batch_size] for i in range(0, len(devices), batch_size)]
            
            for batch_num, batch in enumerate(batches, 1):
                print(f'\n--- BATCH {batch_num}/{len(batches)} ({len(batch)} devices) ---\n')
                
                batch_results = self.process_batch(batch, operation, max_workers=max_workers, **kwargs)
                all_results.extend(batch_results)
                
                if batch_num < len(batches):
                    if self.config.get('safety.prompt_between_batches', True):
                        input(f'\nBatch {batch_num} complete. Press Enter to continue...')
                    else:
                        print(f'\nWaiting {batch_delay} seconds before next batch...')
                        time.sleep(batch_delay)
        else:
            all_results = self.process_batch(devices, operation, max_workers=max_workers, **kwargs)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        success_count = sum(1 for r in all_results if r['Status'] == 'Success')
        warning_count = sum(1 for r in all_results if r['Status'] == 'Warning')
        failed_count = sum(1 for r in all_results if r['Status'] == 'Failed')
        
        print('\n' + '='*80)
        print(f'{op_desc.upper()} COMPLETE')
        print('='*80)
        print(f'Total Devices: {len(devices)}')
        print(f'Success: {success_count}')
        if warning_count > 0:
            print(f'Warning: {warning_count}')
        print(f'Failed: {failed_count}')
        print(f'Duration: {duration:.1f}s ({duration/60:.1f} minutes)')
        if len(devices) > 0:
            print(f'Avg per Device: {duration/len(devices):.1f}s')
            print(f'Success Rate: {success_count/len(devices)*100:.1f}%')
        print('='*80)
        print()
        
        # Show detailed results for small sets
        if len(devices) <= 20:
            print('DETAILED RESULTS:')
            print('-' * 80)
            print(f'{"Device":<25} {"IP":<18} {"Status":<10} {"Target"}')
            print('-' * 80)
            for r in all_results:
                name = r['DeviceName'][:24]
                ip = r['IPAddress']
                status = r['Status']
                target = r.get('Target', '')
                # Truncate target if too long, but show multiple servers
                if len(target) > 35:
                    target_display = target[:32] + '...'
                else:
                    target_display = target
                print(f'{name:<25} {ip:<18} {status:<10} {target_display}')
            print()
        
        result_file = self.save_results(all_results, operation)
        if result_file:
            print(f'✓ Detailed results saved: {result_file}')
        
        failures = [r for r in all_results if r['Status'] == 'Failed']
        if failures and len(failures) <= 10:
            print('\n' + '='*80)
            print(f'FAILED DEVICES ({len(failures)}):')
            print('='*80)
            for f in failures:
                print(f'\n{f["DeviceName"]} ({f["IPAddress"]})')
                print(f'  Error: {f["Message"]}')


def main():
    parser = argparse.ArgumentParser(description='IC3000 Device Manager')
    parser.add_argument('operation', choices=['ntp', 'upgrade'], help='Operation to perform')
    parser.add_argument('--config', default='ic3000_config.yaml', help='Configuration file')
    parser.add_argument('--csv', dest='csv_file', help='Device CSV file')
    parser.add_argument('--firmware', help='Firmware file path')
    parser.add_argument('--batch-size', type=int, help='Process devices in batches')
    parser.add_argument('--batch-delay', type=int, help='Seconds between batches')
    parser.add_argument('--workers', type=int, dest='max_workers', help='Max parallel workers')
    parser.add_argument('--test', action='store_true', dest='test_mode', help='Test mode (3 devices)')
    parser.add_argument('--limit', type=int, help='Limit to N devices')
    parser.add_argument('--yes', action='store_true', help='Skip confirmation')
    
    args = parser.parse_args()
    
    config = IC3000Config(args.config)
    
    if args.yes:
        config.config['safety']['require_confirmation'] = False
        config.config['safety']['prompt_between_batches'] = False
    
    manager = IC3000Manager(config)
    
    kwargs = {
        'test_mode': args.test_mode,
        'csv_file': args.csv_file,
        'limit': args.limit,
    }
    
    if args.batch_size:
        kwargs['batch_size'] = args.batch_size
    if args.batch_delay:
        kwargs['batch_delay'] = args.batch_delay
    if args.max_workers:
        kwargs['max_workers'] = args.max_workers
    if args.firmware:
        kwargs['firmware_path'] = args.firmware
    
    try:
        manager.run(args.operation, **kwargs)
    except KeyboardInterrupt:
        print('\nInterrupted by user')
        sys.exit(1)
    except Exception as e:
        print(f'\nError: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

