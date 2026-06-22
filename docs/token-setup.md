# Token Setup

GitHub Manager needs a GitHub token to call the REST API.

## Where the token is read from

In order:

1. `GH_TOKEN` environment variable
2. `GITHUB_TOKEN` environment variable
3. `~/.config/tt-github/env` file

```bash
mkdir -p ~/.config/tt-github
cat > ~/.config/tt-github/env <<'ENV'
GH_TOKEN=your_token_here
GITHUB_USER=your-github-username
ENV
chmod 600 ~/.config/tt-github/env
```

The token is never printed by the script.

## Minimum PAT permissions

Use a fine-grained Personal Access Token where possible.

| Capability | Permission | When needed |
|------------|-----------|-------------|
| Metadata | Read-only | Always |
| Contents | Read and write | push / publish |
| Administration | Read and write | create-repo / delete-repo |
| Issues | Read and write | create-issue / list-issues |

Repository access: select specific repos when possible instead of "All repositories".

## Verify the token

```bash
python3 scripts/gh_manager.py whoami
```

Expected output includes your `login` and `public_repos`.

## Common token errors

| HTTP | Meaning | Fix |
|------|---------|-----|
| 401 | Token invalid/expired | Regenerate PAT, update env file |
| 403 | Missing permission or rate limited | Add required scope, or wait/respect rate limit |
| 404 | Repo not found or token lacks access | Check repo path; for private repos grant access to the PAT |
| 422 | Invalid input (repo exists, bad topics) | Adjust name/topics |

## Rate limits

- Authenticated REST API allows up to 5,000 requests/hour.
- `403` with a rate-limit message means you hit the cap.
- Check the `X-RateLimit-Reset` time and retry after it.
- Avoid tight loops; batch operations where possible.

## Rotating the token

1. Create a new fine-grained PAT.
2. Update `~/.config/tt-github/env`.
3. Confirm permissions remain `600`.
4. Revoke the old token in GitHub settings.
