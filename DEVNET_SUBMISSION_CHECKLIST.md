# DevNet Code Exchange Submission Checklist

**Repository**: https://github.com/wboudaa/ic3000_automation  
**Date**: January 19, 2026  
**Previous OpenSSF Score**: 4.5/10  
**Target Score**: 8.0+/10

## ✅ Security Improvements Completed

### 1. Branch Protection (Score: 0 → 10) ⚠️ REQUIRES MANUAL SETUP

**Status**: Needs GitHub settings configuration

**Action Required**:
1. Go to: https://github.com/wboudaa/ic3000_automation/settings/branches
2. Click "Add branch protection rule"
3. Branch pattern: `main` (and `master` if you use it)
4. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require approvals: 1
   - ✅ Dismiss stale pull request approvals
   - ✅ Require status checks to pass
   - ✅ Require conversation resolution
5. Click "Create"

**Impact**: Critical for DevNet submission - shows professional development practices

---

### 2. Security Policy (Score: 0 → 10) ✅ COMPLETE

**Status**: ✅ Added `SECURITY.md`

**What we added**:
- Vulnerability reporting process
- Cisco PSIRT contact information
- Security best practices for users
- Responsible disclosure guidelines
- Known security considerations

**File**: https://github.com/wboudaa/ic3000_automation/blob/main/SECURITY.md

---

### 3. SAST Tools (Score: 0 → 10) ✅ COMPLETE

**Status**: ✅ Added CodeQL and Bandit scanning

**What we added**:
- `.github/workflows/codeql-analysis.yml` - GitHub CodeQL security scanning
- `.github/workflows/python-tests.yml` - Bandit, pylint, safety checks
- Automated security scans on every push and PR
- Weekly scheduled scans

**Impact**: Continuous security monitoring

---

### 4. CI Tests (Score: -1 → 10) ✅ COMPLETE

**Status**: ✅ Added Python CI pipeline

**What we added**:
- Python 3.7-3.11 compatibility testing
- Linting with pylint
- Security scanning with bandit
- Dependency vulnerability checks
- Syntax validation

**File**: `.github/workflows/python-tests.yml`

---

### 5. Dependency Updates (Score: 0 → 10) ✅ COMPLETE

**Status**: ✅ Added Dependabot

**What we added**:
- `.github/dependabot.yml`
- Automated weekly dependency updates
- Security update grouping
- Python pip and GitHub Actions updates

**Impact**: Automatic PRs for dependency updates and security patches

---

### 6. Code Review Process (Score: 0 → 8) ✅ COMPLETE

**Status**: ✅ Added PR and issue templates

**What we added**:
- `.github/PULL_REQUEST_TEMPLATE.md` - Structured PR submissions
- `.github/ISSUE_TEMPLATE/bug_report.md` - Bug report template
- `.github/ISSUE_TEMPLATE/feature_request.md` - Feature request template
- `.github/ISSUE_TEMPLATE/security_vulnerability.md` - Security template

**Impact**: Improves contribution quality and project management

---

### 7. Community Standards (Score: 0 → 10) ✅ COMPLETE

**Status**: ✅ Added community files

**What we added**:
- `CODE_OF_CONDUCT.md` - Contributor Covenant 2.0
- `CONTRIBUTING.md` - Comprehensive contribution guidelines
- Clear security guidelines
- Development setup instructions

**Impact**: Professional open-source project structure

---

## 📊 Expected OpenSSF Scorecard Improvements

### Before (4.5/10):
```
✅ Binary-Artifacts: 10
❌ Branch-Protection: 0
❌ CI-Tests: -1
❌ CII-Best-Practices: 0
❌ Code-Review: 0
❌ Contributors: 0
✅ Dangerous-Workflow: 10
❌ Dependency-Update-Tool: 0
❌ Fuzzing: 0
✅ License: 10
⚠️  Maintained: 1
❌ Packaging: -1
✅ Pinned-Dependencies: 10
❌ SAST: 0
❌ Security-Policy: 0
❌ Signed-Releases: -1
✅ Token-Permissions: 10
✅ Vulnerabilities: 10
```

### After Improvements (Est. 8.0+/10):
```
✅ Binary-Artifacts: 10 (unchanged)
✅ Branch-Protection: 10 (AFTER manual setup)
✅ CI-Tests: 10 (workflows added)
⚠️  CII-Best-Practices: 0 (optional)
✅ Code-Review: 8 (templates added)
⚠️  Contributors: 0 (will improve with community)
✅ Dangerous-Workflow: 10 (unchanged)
✅ Dependency-Update-Tool: 10 (Dependabot added)
❌ Fuzzing: 0 (not applicable)
✅ License: 10 (unchanged)
✅ Maintained: 8 (active development)
❌ Packaging: -1 (can add later)
✅ Pinned-Dependencies: 10 (unchanged)
✅ SAST: 10 (CodeQL + Bandit added)
✅ Security-Policy: 10 (SECURITY.md added)
❌ Signed-Releases: -1 (can add later)
✅ Token-Permissions: 10 (unchanged)
✅ Vulnerabilities: 10 (unchanged)
```

**Projected Score**: 8.0-8.5/10 ✅

---

## 🚀 Next Steps for DevNet Submission

### 1. Manual GitHub Setup (CRITICAL)

- [ ] Enable branch protection on `main` branch
- [ ] Enable GitHub Advanced Security (if available)
- [ ] Enable Dependabot security updates
- [ ] Enable Dependabot alerts

### 2. Repository Settings

- [ ] Make repository public (Settings → Danger Zone → Change visibility)
- [ ] Add repository description
- [ ] Add topics: `cybervision`, `ic3000`, `automation`, `industrial-iot`, `cisco`
- [ ] Set repository website to DevNet page (after approval)

### 3. Verify Workflows

```bash
# Check that workflows will run
# After pushing, visit:
https://github.com/wboudaa/ic3000_automation/actions

# Verify:
- CodeQL Analysis workflow exists
- Python CI workflow exists
- No workflow errors
```

### 4. Wait for First Scans

- [ ] Wait 24-48 hours for GitHub to run security scans
- [ ] Check Actions tab for successful runs
- [ ] Review any security alerts
- [ ] Check OpenSSF Scorecard: https://securityscorecards.dev/viewer/?uri=github.com/wboudaa/ic3000_automation
- [ ] DevNet Code Exchange report (security score): https://developer.cisco.com/codeexchange/github/repo/wboudaa/ic3000_automation/report/
- [ ] DevNet Code Exchange edit (metadata): https://developer.cisco.com/codeexchange/github/repo/wboudaa/ic3000_automation/edit/

### 5. Pre-Submission Review

Before submitting to DevNet, verify:

- [ ] README.md is clear and comprehensive
- [ ] All example files use placeholder data
- [ ] No credentials or sensitive data in repository
- [ ] LICENSE file is present (check it's appropriate)
- [ ] Repository is public
- [ ] Workflows are passing
- [ ] Branch protection is enabled

### 6. Submit to DevNet Code Exchange

1. **Create/Login to DevNet Account**:
   - Visit: https://developer.cisco.com/
   - Use Cisco email: wboudaa@cisco.com

2. **Submit Repository**:
   - Go to: https://developer.cisco.com/codeexchange/github/submit
   - Repository URL: `https://github.com/wboudaa/ic3000_automation`
   - Short description: "Automation toolkit for Cisco IC3000 (Cyber Vision) bulk configuration, NTP setup, and firmware upgrades"
   - Tags: `cybervision`, `ic3000`, `automation`, `industrial-iot`, `network-automation`
   - Category: Industrial IoT / Network Automation

3. **Wait for Review**:
   - DevNet team reviews submissions (1-2 weeks)
   - They may request changes
   - Respond to feedback promptly

---

## 📝 Files Added/Modified

### New Files:
```
.github/
├── dependabot.yml
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   ├── feature_request.md
│   └── security_vulnerability.md
├── PULL_REQUEST_TEMPLATE.md
└── workflows/
    ├── codeql-analysis.yml
    ├── python-tests.yml   # Bandit, safety, syntax (CI-Tests + SAST)
    ├── scorecard.yml      # OpenSSF Scorecard (publishes to Security tab)
    └── status-check.yml

CODE_OF_CONDUCT.md
CONTRIBUTING.md
SECURITY.md
DEVNET_SUBMISSION_CHECKLIST.md (this file)
requirements.txt
```

### Modified Files:
```
.gitignore (already secure)
```

---

## 🔒 Security Verification

Before going public, run these checks:

```bash
# 1. Check for credentials
cd /path/to/ic3000_automation
grep -r "password\|secret\|api_key\|token" . --exclude-dir=.git | grep -v ".md" | grep -v "example"

# 2. Check for IP addresses (optional)
grep -rE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' . --exclude-dir=.git | grep -v ".md" | grep -v "example"

# 3. Check for sensitive files
ls -la ic3000_devices.csv  # Should NOT exist
ls -la ic3000_config.yaml  # Should NOT exist

# 4. Verify examples are sanitized
cat examples/ic3000_devices.csv.example  # Should have placeholders
cat ic3000_config.yaml.example  # Should have placeholders
```

---

## 🎯 Success Criteria

Your repository is ready for DevNet submission when:

- ✅ OpenSSF Scorecard shows 8.0+/10
- ✅ Branch protection enabled
- ✅ All GitHub Actions workflows passing
- ✅ Repository is public
- ✅ No security alerts
- ✅ Documentation is clear and complete
- ✅ No sensitive data in repository
- ✅ Community files present (CODE_OF_CONDUCT, CONTRIBUTING, SECURITY)
- ✅ License is appropriate (Apache 2.0, MIT, or Cisco Sample Code)

---

## 🔐 If Security Score Is Still Low (DevNet)

Cisco Code Exchange uses **OpenSSF Scorecard** (and optionally **KubeClarity** for SBOM). To see why the score is low:

1. **View your report** (login with Cisco/DevNet):  
   [Code Exchange report](https://developer.cisco.com/codeexchange/github/repo/wboudaa/ic3000_automation/report/)
2. **Edit listing/metadata**:  
   [Code Exchange edit](https://developer.cisco.com/codeexchange/github/repo/wboudaa/ic3000_automation/edit/)
3. **OpenSSF Scorecard (public)**:  
   [securityscorecards.dev](https://securityscorecards.dev/viewer/?uri=github.com/wboudaa/ic3000_automation)

Common fixes:
- **Branch protection**: Enable on `main` (Settings → Branches).
- **CI / SAST**: Ensure `python-tests.yml` (Bandit, safety) and `codeql-analysis.yml` run and pass.
- **Scorecard workflow**: The `scorecard.yml` workflow runs weekly and publishes results; re-submit or wait for the next run so DevNet sees updated scores.
- **Dependencies**: Run `safety check -r requirements.txt` locally and fix any reported issues.

---

## 📞 Support

**Questions about this checklist**:
- Email: wboudaa@cisco.com

**DevNet Code Exchange**:
- DevNet Portal: https://developer.cisco.com/codeexchange
- DevNet Support: https://developer.cisco.com/site/support/

**OpenSSF Scorecard**:
- Documentation: https://github.com/ossf/scorecard
- Check your score: https://securityscorecards.dev/

---

**Last Updated**: January 19, 2026  
**Version**: 1.0  
**Status**: Ready for GitHub setup and DevNet submission
