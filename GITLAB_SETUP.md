# GitLab Repository Setup Guide

Follow these steps to push this IC3000 toolkit to your GitLab repository.

## Prerequisites

- GitLab account with repository access
- Git installed on your system
- SSH key configured with GitLab (or use HTTPS with credentials)

## Step 1: Initialize Git Repository

```bash
cd /Users/wboudaa/Documents/Cursor/ic3000-toolkit

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: IC3000 Automation Toolkit v1.0

- NTP configuration automation with multiple server support
- Firmware upgrade automation with batch processing
- REST API client with token-based authentication
- CSV-based device management
- YAML configuration file
- Comprehensive documentation and examples"
```

## Step 2: Create GitLab Repository

### Option A: Via GitLab Web UI

1. Go to your GitLab instance (e.g., `https://gitlab.company.com`)
2. Click **"New project"**
3. Select **"Create blank project"**
4. Fill in:
   - **Project name**: `ic3000-automation-toolkit`
   - **Visibility**: Private (recommended)
   - **Initialize repository**: NO (you already have code)
5. Click **"Create project"**

### Option B: Via GitLab CLI (if available)

```bash
# Create new project
gitlab project create --name ic3000-automation-toolkit \
  --description "Automation toolkit for Cisco IC3000 devices" \
  --visibility private
```

## Step 3: Add GitLab Remote

After creating the project, you'll see a repository URL. Use it:

```bash
# For SSH (recommended):
git remote add origin git@gitlab.company.com:your-username/ic3000-automation-toolkit.git

# For HTTPS:
git remote add origin https://gitlab.company.com/your-username/ic3000-automation-toolkit.git

# Verify remote was added
git remote -v
```

## Step 4: Push to GitLab

```bash
# Push to main branch
git push -u origin main

# Or if your default branch is 'master':
git branch -M main
git push -u origin main
```

## Step 5: Verify Upload

1. Go to your GitLab repository URL
2. You should see:
   - ✅ `README.md` with full documentation
   - ✅ Python scripts (`ic3000_auto.py`, etc.)
   - ✅ Example files (`examples/`)
   - ✅ Configuration template (`ic3000_config.yaml.example`)
   - ❌ NO `ic3000_devices.csv` (sensitive data excluded by .gitignore)
   - ❌ NO `ic3000_config.yaml` (sensitive data excluded)

## Step 6: Protect Sensitive Data

**IMPORTANT:** Verify the following files are NOT in your repository:

```bash
# Check what files are tracked
git ls-files

# You should NOT see:
# - ic3000_devices.csv (contains passwords)
# - ic3000_config.yaml (may contain real config)
# - results/*.csv (may contain sensitive data)
# - *.SPA or *.bin (firmware files are too large)
```

If sensitive files were committed:

```bash
# Remove from git (keeps local copy)
git rm --cached ic3000_devices.csv
git rm --cached ic3000_config.yaml

# Commit the removal
git commit -m "Remove sensitive data from repository"

# Force push (WARNING: rewrites history)
git push -f origin main
```

## Step 7: Set Up Repository Settings (Optional)

### Add Repository Description

1. Go to **Settings** → **General**
2. Update description: "Automation toolkit for bulk NTP configuration and firmware upgrades of Cisco IC3000 Industrial Compute devices"

### Add Topics/Tags

Add tags like:
- `cisco`
- `ic3000`
- `automation`
- `python`
- `devops`
- `network-automation`

### Enable CI/CD (Optional)

Create `.gitlab-ci.yml` for automated testing:

```yaml
image: python:3.9

stages:
  - test
  - lint

test:
  stage: test
  script:
    - pip install -r requirements.txt
    - python3 -m py_compile ic3000_auto.py
    - python3 -m py_compile ic3000_api_client.py
    - python3 -m py_compile ic3000_upgrade_api.py
  only:
    - main
    - merge_requests

lint:
  stage: lint
  script:
    - pip install pylint
    - pylint --disable=all --enable=E ic3000_*.py || true
  only:
    - main
    - merge_requests
```

### Protect Main Branch

1. Go to **Settings** → **Repository** → **Protected branches**
2. Protect `main` branch:
   - ✅ Allowed to merge: Maintainers
   - ✅ Allowed to push: No one
   - ✅ Require approval: Yes (optional)

## Step 8: Clone on Other Systems

Other team members can now clone the repository:

```bash
# Clone via SSH
git clone git@gitlab.company.com:your-username/ic3000-automation-toolkit.git

# Clone via HTTPS
git clone https://gitlab.company.com/your-username/ic3000-automation-toolkit.git

# Enter directory
cd ic3000-automation-toolkit

# Set up their own config files
cp examples/ic3000_devices.csv.example ic3000_devices.csv
cp ic3000_config.yaml.example ic3000_config.yaml

# Edit with their credentials
nano ic3000_devices.csv

# Install dependencies
pip3 install -r requirements.txt

# Ready to use!
python3 ic3000_auto.py ntp --test
```

## Updating the Repository

When you make changes:

```bash
# Check what changed
git status

# Add changes
git add ic3000_auto.py
git add README.md

# Or add all changes
git add .

# Commit with descriptive message
git commit -m "Add support for multiple NTP servers"

# Push to GitLab
git push origin main
```

## Creating Releases/Tags

Tag stable versions:

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release v1.0.0: Initial stable release

Features:
- NTP configuration automation
- Firmware upgrade automation
- Batch processing support
- Multiple NTP servers
- CSV reporting"

# Push tag to GitLab
git push origin v1.0.0

# Push all tags
git push origin --tags
```

In GitLab UI, go to **Repository** → **Tags** to see your releases.

## Sharing with Team

Share the repository URL with your team:

```
https://gitlab.company.com/your-username/ic3000-automation-toolkit
```

They can:
1. Clone the repository
2. Follow the `QUICKSTART.md` guide
3. Create their own `ic3000_devices.csv` with their devices
4. Start automating!

## Security Best Practices

1. ✅ **Never commit passwords**: Use `.gitignore`
2. ✅ **Use SSH keys**: More secure than HTTPS passwords
3. ✅ **Set repository to Private**: Sensitive internal tool
4. ✅ **Enable branch protection**: Prevent accidental overwrites
5. ✅ **Regular updates**: Pull latest changes before working
6. ✅ **Code review**: Use merge requests for changes

## Troubleshooting

### "Permission denied (publickey)"

Your SSH key isn't configured:

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@company.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitLab: Profile → SSH Keys
```

### "Repository not found"

Check the remote URL:

```bash
git remote -v

# Update if wrong
git remote set-url origin git@gitlab.company.com:correct-path/repo.git
```

### "Failed to push"

Branch might be protected:

```bash
# Create a branch and merge request instead
git checkout -b feature/my-changes
git push origin feature/my-changes

# Then create merge request in GitLab UI
```

## Next Steps

- [ ] Set up CI/CD for automated testing
- [ ] Add team members as collaborators
- [ ] Create wiki pages for advanced usage
- [ ] Set up issue templates for bug reports
- [ ] Consider adding changelog (CHANGELOG.md)
- [ ] Add contribution guidelines (CONTRIBUTING.md)

