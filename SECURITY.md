# Security Policy

GitHub Manager handles GitHub credentials on behalf of an automated agent. Treat its token like a production secret.

## Token handling

- Tokens are read from `GH_TOKEN`, `GITHUB_TOKEN`, or `~/.config/tt-github/env`.
- Tokens are never printed in normal command output.
- The recommended publishing paths (`publish`, `push --method api`) use the GitHub Contents API and never place the token in a git remote.
- The legacy `push --method git` path temporarily embeds the token in the remote URL and scrubs it after push. Prefer the API paths.

## Recommended token scope

Use a fine-grained Personal Access Token (PAT) with the minimum required scope:

- **Metadata:** Read-only (always required)
- **Contents:** Read and write (push/publish)
- **Administration:** Read and write (only if creating/deleting repos)
- **Issues:** Read and write (only if using issue commands)

Avoid classic tokens with broad `repo` scope when a fine-grained PAT works.

## If a token leaks

1. Revoke the token immediately in GitHub → Settings → Developer settings → Personal access tokens.
2. Generate a new fine-grained PAT with minimum scope.
3. Update `~/.config/tt-github/env` and confirm file permissions are `600`.
4. Rotate any downstream automation that cached the old token.
5. Review repo audit log for unexpected pushes, releases, or deletions.

## Reporting a vulnerability

- Do not open public issues containing tokens, secrets, private repo names, or logs with credentials.
- Report sensitive issues privately to the repository owner.
- Include reproduction steps and impact, but redact all secrets.

## Safe usage rules

- Never paste a token into an issue, pull request, chat, or log.
- Keep `~/.config/tt-github/env` permissioned `600` and out of version control.
- `--note` values are local-only and must not be assumed private if the local machine is shared.
- Destructive operations (`delete-repo`) require an exact `--confirm OWNER/NAME` match and should be confirmed with a human.
