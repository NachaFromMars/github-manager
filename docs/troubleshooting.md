# Troubleshooting

All commands return JSON. When something fails, check the `status` and `error` fields first.

## 401 — Bad credentials

Cause: token missing, invalid, or expired.

Fix:
- Confirm `~/.config/tt-github/env` has a valid `GH_TOKEN`.
- Run `python3 scripts/gh_manager.py whoami`.
- Regenerate the PAT if it expired.

## 403 — Forbidden or rate limited

Two common causes:

1. **Missing permission** — the PAT lacks the required scope (e.g. Administration for create/delete, Contents for push).
   - Fix: add the scope, or use a token that has it.
2. **Rate limit** — too many requests in the hour.
   - Fix: wait until `X-RateLimit-Reset`; avoid tight loops.

## 404 — Not found

Cause: repo path is wrong, or the token cannot access a private repo.

Fix:
- Double-check `OWNER/NAME`.
- For private repos, grant the fine-grained PAT access to that repository.

## 422 — Unprocessable entity

Common cases:

- Repo already exists when creating.
- Invalid topics (topics must be lowercase, alphanumeric with hyphens).
- Invalid field values.

Fix:
- Use `update-repo` instead of `create-repo` for an existing repo.
- Normalize topics (lowercase, no spaces).

## Push fails with "could not read Username"

Cause: a git-based push without embedded credentials (often after a rebase using the plain `git push`).

Fix:
- Use the skill's API path: `push --method api` or `publish`.
- These do not depend on git credential prompts.

## Non-fast-forward / rejected push

Cause: remote changed since your last fetch.

Fix:
- For API publishing, just re-run `publish` (it updates files via the Contents API).
- For git-based work, `git pull --rebase origin main`, resolve conflicts, then push via the API path.

## Library not updating

Cause: the command path does not auto-sync, or the write failed.

Fix:
- Auto-sync happens on `create-repo`, `push`, `publish`, `update-repo`, and successful `repo-info`.
- Manually add with `library-add`.
- Confirm `~/.config/tt-github/repos.json` is writable and permissioned `600`.

## Token appears in output

This should never happen. If you see it:
- Stop and revoke the token immediately.
- Report it as a security issue (see `SECURITY.md`).
