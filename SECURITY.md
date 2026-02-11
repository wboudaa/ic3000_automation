# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please follow these steps:

### For Cisco Employees

1. **Internal Reporting**: Report security issues through Cisco's internal PSIRT process
2. **Email**: Contact the maintainer at wboudaa@cisco.com
3. **Cisco PSIRT**: https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html

### For External Contributors

1. **DO NOT** open a public GitHub issue for security vulnerabilities
2. **Email**: Send details to wboudaa@cisco.com with subject "SECURITY: IC3000 Automation"
3. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

### What to Expect

- **Response Time**: You will receive an acknowledgment within 48 hours
- **Status Updates**: We will keep you informed of our progress
- **Disclosure**: We follow coordinated disclosure practices
- **Credit**: Security researchers will be credited (unless they prefer to remain anonymous)

## Security Best Practices for Users

When using this tool:

1. **Never commit credentials**: Use example files (`.example` suffix) for configuration templates
2. **Protect your CSV files**: Ensure `ic3000_devices.csv` contains no production passwords
3. **Use SSH keys**: Prefer SSH authentication over password-based authentication
4. **Network isolation**: Run automation tools from secure, isolated networks
5. **Review logs**: Check output logs for sensitive information before sharing
6. **Update regularly**: Keep dependencies up to date using `pip install --upgrade`

## Known Security Considerations

### Authentication & Credentials
- This tool requires IC3000 device credentials to function
- Credentials should be stored securely outside the repository
- Use environment variables or secure credential managers for production use

### Network Security
- Tool communicates with IC3000 devices over HTTPS (ports 8443, 8444)
- IC3000 devices typically use self-signed certificates; the client disables TLS verification by default (`verify=False`). Use only in trusted, isolated networks. To enable certificate verification when devices use proper PKI, set environment variable `IC3000_VERIFY_SSL=true` (support can be added in a future release).
- Ensure network path between automation host and IC3000 devices is secure

### Data Handling
- Device configurations may contain sensitive network information
- Results are stored locally in the `results/` directory
- Clean up result files after use in production environments

## Dependency Security

We use:
- `requests` library for HTTPS communication
- `urllib3` for SSL/TLS handling
- Python 3.7+ with security updates

Run security audits:
```bash
pip install safety
safety check -r requirements.txt
```

## Secure Development

Contributors should:
- Follow secure coding practices
- Never commit secrets or credentials
- Run security linters before submitting PRs
- Keep dependencies updated and patched

## Compliance

This tool is designed for use with Cisco IC3000 (Cyber Vision) products and follows:
- Cisco Secure Development Lifecycle (CSDL)
- OWASP secure coding guidelines
- Python security best practices

## Contact

For security concerns, contact:
- **Maintainer**: Walid Boudaa (wboudaa@cisco.com)
- **Cisco PSIRT**: https://tools.cisco.com/security/center/

---

**Last Updated**: January 2026
