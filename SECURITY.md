# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by opening a private security advisory:

1. Go to the [Security tab](https://github.com/Sumaida-ab/Arabic-context-MCP/security)
2. Click "Report a vulnerability"
3. Provide details about the vulnerability

**Please do not open public issues for security vulnerabilities.**

We will respond within 48 hours and work with you to understand and address the issue.

## Security Measures

This project implements the following security measures:

- **Input sanitization**: All user inputs are sanitized to prevent path traversal attacks
- **Whitelist validation**: Only known accent IDs can be accessed
- **Locked dependencies**: All dependency versions are pinned to prevent supply chain attacks
- **No eval/exec**: No dynamic code execution
- **Read-only operations**: The MCP server only reads pre-built data files
