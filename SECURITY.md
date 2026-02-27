# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public GitHub issue
2. Email the maintainer directly (see [README contact section](README.md#contact))
3. Include a description of the vulnerability, steps to reproduce, and potential impact

You should receive an acknowledgment within 48 hours. We will work with you to understand the scope and develop a fix before any public disclosure.

## Current Security Posture

This project is in **Phase 1 (prototype)** and is not yet suitable for production deployment. Known security gaps are documented in the [README Security Considerations section](README.md#security-considerations).

Key items to be aware of:

- **No authentication or authorization** — the API is open to anyone with network access
- **No HTTPS enforcement** — TLS must be handled at the deployment layer
- **No rate limiting** — endpoints are unprotected against abuse
- **Flat-file storage** — migration data is stored as plaintext JSON on disk
- **Open CORS** — all origins are currently allowed

These are tracked in the [roadmap](ROADMAP.md) for resolution in Phase 2.

## Dependencies

Backend dependencies are pinned in `requirements.txt`. Frontend dependencies are declared in `frontend/package.json`. We recommend running `pip audit` and `npm audit` regularly to check for known vulnerabilities.
