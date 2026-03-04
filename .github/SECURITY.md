# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project (e.g., exposed API keys, insecure dependencies), please report it responsibly:

1. **Do not** open a public GitHub issue.
2. Email the maintainer directly or use GitHub's [private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability) feature.

## Scope

This is a personal intelligence platform. Security concerns primarily involve:

- API key or credential exposure (`.env` files, hardcoded secrets)
- Dependency vulnerabilities (Python packages, GitHub Actions)
- Data leakage in generated reports (PII, non-public source access credentials)
- Supply chain attacks via compromised dependencies

## Supported Versions

| Version          | Supported |
| ---------------- | --------- |
| Latest on `main` | ✅        |

## Security Practices

- Secrets are managed via `.env` files (never committed — see `.gitignore`)
- Pre-commit hooks include `detect-private-key` to prevent accidental key commits
- Dependabot monitors Python and GitHub Actions dependencies weekly
- All CI runs use pinned action versions (`@v4`, not `@main`)
