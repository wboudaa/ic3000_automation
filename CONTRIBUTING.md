# Contributing to IC3000 Automation Toolkit

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🤝 How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Create a new issue** with:
   - Clear, descriptive title
   - Steps to reproduce the bug
   - Expected vs actual behavior
   - Your environment (OS, Python version, IC3000 version)
   - Relevant logs (remove sensitive information!)

### Suggesting Enhancements

1. **Open an issue** describing:
   - The problem you're trying to solve
   - Your proposed solution
   - Any alternatives you've considered
   - Examples of how it would work

### Pull Requests

We welcome pull requests! Here's the process:

#### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/ic3000_automation.git
cd ic3000_automation
git remote add upstream https://github.com/wboudaa/ic3000_automation.git
```

#### 2. Create a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

#### 3. Make Your Changes

Follow these guidelines:

**Code Style:**
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and under 50 lines when possible

**Security:**
- Never commit credentials or sensitive data
- Use `.example` suffix for configuration templates
- Follow the security guidelines in SECURITY.md
- Run security checks before committing

**Testing:**
- Test your changes with actual IC3000 devices (if possible)
- Add error handling for edge cases
- Verify backward compatibility

**Documentation:**
- Update README.md if adding new features
- Add inline comments for complex logic
- Update CHANGELOG.md

#### 4. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a clear message
git commit -m "Add feature: brief description

Longer explanation of what changed and why.
Fixes #123 (if applicable)"
```

**Commit Message Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: Add support for bulk firmware upgrades

Implemented batch processing for upgrading multiple IC3000 
devices simultaneously with progress tracking and error recovery.

Closes #45
```

```
fix: Handle timeout errors during authentication

Added retry logic and better error messages when device 
authentication fails due to network timeouts.

Fixes #78
```

#### 5. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Then create a Pull Request on GitHub
```

**PR Description Should Include:**
- What changes you made
- Why you made them
- How to test them
- Screenshots/logs (if applicable)
- Related issues

## 🔍 Code Review Process

1. **Automated Checks**: Your PR will automatically run:
   - CodeQL security analysis
   - Python linting (pylint)
   - Security scanning (bandit)
   - Dependency checks (safety)

2. **Manual Review**: A maintainer will review your code for:
   - Code quality and readability
   - Security considerations
   - Test coverage
   - Documentation completeness

3. **Feedback**: Address review comments by:
   - Making requested changes
   - Explaining your reasoning if you disagree
   - Pushing updates to your branch

4. **Merge**: Once approved, a maintainer will merge your PR

## 🛡️ Security Guidelines

### Before Committing

Always check for sensitive data:

```bash
# Check for potential secrets
grep -r "password\|secret\|api_key\|token" . --exclude-dir=.git

# Run security scanner
pip install bandit
bandit -r .
```

### Handling Credentials

- Use environment variables for credentials
- Never commit `ic3000_devices.csv` with real data
- Use `ic3000_devices.csv.example` for templates
- Document credential requirements in README

### Reporting Security Issues

**DO NOT** open public issues for security vulnerabilities.  
See [SECURITY.md](SECURITY.md) for reporting instructions.

## 📋 Development Setup

### Prerequisites

- Python 3.7 or higher
- pip package manager
- Git
- Access to IC3000 devices for testing (optional)

### Local Development

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/ic3000_automation.git
cd ic3000_automation

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install pylint bandit safety black isort

# Create example config files
cp examples/ic3000_devices.csv.example ic3000_devices.csv
# Edit ic3000_devices.csv with your test devices

# Run the tool
python3 ic3000_auto.py
```

### Code Quality Tools

```bash
# Format code with black
black *.py

# Sort imports
isort *.py

# Lint code
pylint *.py

# Security scan
bandit -r .

# Check dependencies
safety check
```

## 📝 Documentation

### README Updates

When adding features, update:
- Feature list
- Usage examples
- Command-line arguments
- Troubleshooting section

### Code Comments

Add comments for:
- Complex algorithms
- API endpoints and their quirks
- Workarounds for IC3000 issues
- Security considerations

### Examples

Add real-world examples in:
- README.md usage section
- Inline code comments
- `examples/` directory

## 🧪 Testing

### Manual Testing

Test your changes with:
- Various IC3000 firmware versions
- Different network configurations
- Edge cases (timeouts, invalid data, etc.)

### Test Checklist

Before submitting a PR:
- [ ] Code runs without errors
- [ ] Tested with actual IC3000 devices (if possible)
- [ ] Error handling works correctly
- [ ] No hardcoded credentials
- [ ] Documentation updated
- [ ] Security checks pass
- [ ] Code is formatted and linted

## 🏆 Recognition

Contributors will be:
- Listed in README.md acknowledgments
- Credited in release notes
- Mentioned in commit messages

## 📧 Questions?

- **Issues**: Open a GitHub issue
- **Email**: wboudaa@cisco.com
- **Cisco DevNet**: Join discussions on DevNet forums

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as this project (see LICENSE file).

## 🙏 Thank You!

Every contribution, no matter how small, helps improve this tool for the entire community. We appreciate your time and effort!

---

**Last Updated**: January 2026
