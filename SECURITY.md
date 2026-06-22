# Security Policy

## Token handling

`github-manager` reads GitHub tokens from environment variables or `~/.config/tt-github/env`.
It is designed not to print tokens in normal command output.

Recommended token scope:

- Fine-grained PAT
- Contents: read/write
- Administration: read/write only if repo create/delete is needed
- Issues: read/write only if issue commands are needed

## Reporting issues

Do not open public issues containing secrets, tokens, private repository names, or logs with credentials.
Revoke exposed tokens immediately from GitHub settings.
