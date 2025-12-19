# Quick Start Guide

Get up and running with the IC3000 Automation Toolkit in 5 minutes!

## Step 1: Install Dependencies

```bash
# Make sure you have Python 3.7+
python3 --version

# Install required packages
pip3 install -r requirements.txt
```

## Step 2: Create Your Device List

```bash
# Copy the example CSV
cp examples/ic3000_devices.csv.example ic3000_devices.csv

# Edit with your devices
nano ic3000_devices.csv
```

**Example content:**
```csv
DeviceName,IPAddress,Username,Password,NTPServer
IC3000-Building1,192.168.1.100,admin,your_password,"10.0.0.1, 10.0.0.2"
IC3000-Building2,192.168.1.101,admin,your_password,10.0.0.1
```

**Security Note:** Protect this file!
```bash
chmod 600 ic3000_devices.csv  # Only you can read/write
```

## Step 3: Create Configuration File

```bash
# Copy the example config
cp ic3000_config.yaml.example ic3000_config.yaml

# Edit if needed (optional - defaults work fine)
nano ic3000_config.yaml
```

## Step 4: Test with 2 Devices

```bash
# Test NTP configuration (safe - only first 2 devices)
python3 ic3000_auto.py ntp --test
```

You should see:
```
✓ IC3000-Building1 (192.168.1.100) → 10.0.0.1, 10.0.0.2
✓ IC3000-Building2 (192.168.1.101) → 10.0.0.1

Success Rate: 100.0%
```

## Step 5: Run on All Devices

```bash
# Configure NTP on all devices
python3 ic3000_auto.py ntp

# Or use batch processing (5 at a time)
python3 ic3000_auto.py ntp --batch-size 5
```

## Firmware Upgrade

```bash
# Place firmware file in the directory
# Edit ic3000_config.yaml to set firmware_path

# Test upgrade on 2 devices
python3 ic3000_auto.py upgrade --test

# Upgrade all devices (in small batches)
python3 ic3000_auto.py upgrade --batch-size 3 --batch-delay 120
```

## Common Commands

```bash
# NTP: Test mode (2 devices only)
python3 ic3000_auto.py ntp --test

# NTP: All devices, batch processing
python3 ic3000_auto.py ntp --batch-size 5 --batch-delay 60

# NTP: Skip confirmations (for automation)
python3 ic3000_auto.py ntp --yes

# Upgrade: Test mode
python3 ic3000_auto.py upgrade --test

# Upgrade: Custom firmware file
python3 ic3000_auto.py upgrade --firmware /path/to/file.SPA

# Upgrade: Process first 10 devices only
python3 ic3000_auto.py upgrade --limit 10
```

## Viewing Results

Results are saved to `results/` directory:

```bash
# View latest NTP results
ls -lt results/ic3000_ntp_*.csv | head -1 | xargs cat

# View latest upgrade results
ls -lt results/ic3000_upgrade_*.csv | head -1 | xargs cat
```

## Troubleshooting

### "Authentication failed"
- Check username/password in CSV
- Verify device is reachable: `ping <ip_address>`

### "Connection timeout"
- Check network connectivity
- Verify ports 8443 and 8444 are open
- Try increasing timeouts in `ic3000_config.yaml`

### "Module not found"
- Run: `pip3 install -r requirements.txt`

## Need Help?

1. Check `README.md` for detailed documentation
2. Review example files in `examples/` directory
3. Check console output for specific error messages
4. Review CSV reports in `results/` directory

## Best Practices

1. ✅ **Always test first**: Use `--test` flag
2. ✅ **Use batch processing**: Don't overwhelm your network
3. ✅ **Protect credentials**: `chmod 600 ic3000_devices.csv`
4. ✅ **Review results**: Check CSV reports after each run
5. ✅ **Backup configs**: Document current settings before changes

