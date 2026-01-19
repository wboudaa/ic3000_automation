# IC3000 Automation Toolkit

A comprehensive Python-based automation toolkit for managing Cisco IC3000 Industrial Compute devices at scale.

## Features

- **NTP Configuration**: Bulk configure NTP servers (single or multiple) across all devices
- **Firmware Upgrades**: Automated software upgrades with parallel processing
- **REST API Integration**: Direct integration with IC3000 hidden REST API
- **Batch Processing**: Process devices in configurable batches to avoid network overload
- **Parallel Execution**: Configure multiple devices simultaneously with thread pools
- **CSV-Based Management**: Simple CSV file for device inventory management
- **YAML Configuration**: Centralized configuration for all settings
- **Detailed Reporting**: CSV reports with timestamps for audit trails

## Quick Start

### Prerequisites

```bash
# Python 3.7 or higher
python3 --version

# Install dependencies
pip3 install -r requirements.txt
```

### Setup

1. **Configure devices CSV file**:

```bash
cp examples/ic3000_devices.csv.example ic3000_devices.csv
# Edit with your device information
```

2. **Configure settings**:

```bash
cp ic3000_config.yaml.example ic3000_config.yaml
# Adjust settings as needed
```

### Usage

#### NTP Configuration

```bash
# Test mode (first 2 devices only)
python3 ic3000_auto.py ntp --test

# Configure all devices
python3 ic3000_auto.py ntp

# Batch processing (5 devices at a time)
python3 ic3000_auto.py ntp --batch-size 5 --batch-delay 120

# Skip confirmation prompt
python3 ic3000_auto.py ntp --yes
```

#### Firmware Upgrade

```bash
# Test mode (first 2 devices only)
python3 ic3000_auto.py upgrade --test

# Upgrade all devices
python3 ic3000_auto.py upgrade

# Custom firmware file
python3 ic3000_auto.py upgrade --firmware /path/to/IC3000-K9-1.5.1.SPA
```

## Configuration

### CSV File Format

The `ic3000_devices.csv` file should contain:

```csv
DeviceName,IPAddress,Username,Password,NTPServer
IC3000-Site1,192.168.1.100,admin,password123,"10.0.0.1, 10.0.0.2"
IC3000-Site2,192.168.1.101,admin,password123,10.0.0.1
```

**Fields:**
- `DeviceName`: Friendly name for the device
- `IPAddress`: IP address of the IC3000 device
- `Username`: Admin username (typically "admin")
- `Password`: Admin password
- `NTPServer`: NTP server(s) - comma-separated for multiple servers

### Configuration File

The `ic3000_config.yaml` file controls:

```yaml
# Device inventory
devices_csv: "ic3000_devices.csv"

# Firmware settings
software:
  firmware_path: "IC3000-K9-1.5.1.SPA"

# NTP configuration
ntp:
  default_server: "pool.ntp.org"

# Parallel processing
parallel:
  batch_size: 5           # Process N devices at a time
  batch_delay: 60         # Wait N seconds between batches
  max_workers_ntp: 10     # Max parallel threads for NTP
  max_workers_upgrade: 3  # Max parallel threads for upgrades

# Timeouts (seconds)
timeouts:
  login: 15
  api_call: 30
  upload: 300
  install: 60

# Safety features
safety:
  require_confirmation: true
  prompt_between_batches: true
```

## Command-Line Options

### Common Options

```bash
--config FILE        Use custom config file (default: ic3000_config.yaml)
--csv FILE          Use custom CSV file (overrides config)
--batch-size N      Process N devices per batch
--batch-delay N     Wait N seconds between batches
--workers N         Number of parallel workers
--test              Test mode: process only first 2 devices
--limit N           Process only first N devices
--yes               Skip all confirmation prompts
```

### NTP-Specific Options

```bash
python3 ic3000_auto.py ntp [OPTIONS]

# Use custom NTP server for all devices
# (Note: per-device NTP servers from CSV take precedence)
```

### Upgrade-Specific Options

```bash
python3 ic3000_auto.py upgrade [OPTIONS]

--firmware FILE     Path to firmware file (overrides config)
```

## Multiple NTP Servers

You can configure multiple NTP servers for redundancy:

**In CSV:**
```csv
DeviceName,IPAddress,Username,Password,NTPServer
IC3000-Site1,192.168.1.100,admin,pass,"10.0.0.1, 10.0.0.2, 10.0.0.3"
```

**In config file:**
```yaml
ntp:
  default_server: "10.0.0.1, 10.0.0.2, 10.0.0.3"
```

All servers are configured simultaneously on each device.

## Output and Reporting

### Console Output

```
================================================================================
IC3000 NTP CONFIGURATION
================================================================================
Total Devices: 10
Success: 9
Failed: 1
Duration: 45.2s
Success Rate: 90.0%
================================================================================

DETAILED RESULTS:
--------------------------------------------------------------------------------
Device                    IP                 Status     Target
--------------------------------------------------------------------------------
IC3000-Site1              192.168.1.100      Success    10.0.0.1, 10.0.0.2
IC3000-Site2              192.168.1.101      Failed     10.0.0.1
```

### CSV Reports

Results are automatically saved to `results/` directory:
- `ic3000_ntp_YYYYMMDD_HHMMSS.csv` - NTP configuration results
- `ic3000_upgrade_YYYYMMDD_HHMMSS.csv` - Firmware upgrade results

CSV contains:
- DeviceName, IPAddress, Operation, Target, Status, Message, Timestamp

## Architecture

### Core Components

1. **ic3000_auto.py** - Main unified automation script
   - Command-line interface
   - Batch processing logic
   - Results aggregation and reporting

2. **ic3000_api_client.py** - REST API client for NTP operations
   - Authentication (token-based via port 8443)
   - NTP configuration (GET/PUT via port 8444)
   - Multi-server support

3. **ic3000_upgrade_api.py** - Firmware upgrade client
   - File upload handling
   - Installation triggering
   - Reboot management

### Authentication Flow

```
1. POST https://device:8443/login → Get session cookie
2. POST https://device:8443/iox/api/v2/hosting/tokenservice → Get X-IDA-AUTH-TOKEN
3. Use token for all API calls to port 8444
```

### API Endpoints

**Port 8444 (REST API):**
- `GET /ntp` - Get current NTP configuration
- `PUT /config/ntp` - Set NTP configuration
- `POST /file/upload` - Upload firmware file
- `POST /firmware/install` - Trigger firmware installation

## Troubleshooting

### Authentication Failures

**Error:** "Authentication failed - invalid credentials"

**Solution:** Verify username/password in CSV file. Default is typically `admin / sentryo69!`

### Connection Timeouts

**Error:** "Connection timeout"

**Solution:** 
- Verify device IP is reachable: `ping <device_ip>`
- Check if ports 8443 and 8444 are accessible
- Increase timeout values in `ic3000_config.yaml`

### Firmware Upload Failures

**Error:** "Upload failed"

**Solution:**
- Verify firmware file exists and path is correct
- Check available disk space on device
- Ensure firmware file is correct version for IC3000

### Certificate Warnings

**Note:** The toolkit disables SSL certificate verification (`verify=False`) as IC3000 devices typically use self-signed certificates. This is expected behavior for internal infrastructure.

## Best Practices

### Production Use

1. **Test First**: Always use `--test` flag on 2 devices before bulk operations
2. **Batch Processing**: Use `--batch-size 5` to avoid overwhelming your network
3. **Backup Configs**: Document current NTP settings before making changes
4. **Maintenance Windows**: Schedule upgrades during maintenance windows
5. **Monitor Progress**: Watch console output for failures and investigate immediately

### Security

1. **Protect Credentials**: 
   - Never commit CSV files with real passwords to Git
   - Use file permissions: `chmod 600 ic3000_devices.csv`
   - Consider using environment variables or secrets management

2. **Network Security**:
   - Run from secure management network
   - Use VPN if accessing devices remotely
   - Audit all operations via CSV reports

### Performance Tuning

- **NTP**: Can use 10+ parallel workers safely
- **Upgrades**: Limit to 3-5 workers due to large file transfers
- **Batch Size**: 5-10 devices per batch recommended
- **Batch Delay**: 60-120 seconds between batches

## Examples

See `examples/` directory for:
- Sample CSV files
- Configuration templates
- Common usage scenarios

## License

Internal tool for Cisco Cyber Vision IC3000 management.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review console output and CSV reports
3. Verify device connectivity and credentials
4. Check firmware file compatibility

## Version History

- **v1.0** - Initial release
  - NTP configuration automation
  - Firmware upgrade automation
  - Batch processing support
  - Multiple NTP servers support
  - CSV reporting



