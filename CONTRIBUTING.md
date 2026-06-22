# Contributing to GitHub Manager

Thanks for improving GitHub Manager. This tool gives an agent real GitHub write access, so contributions must preserve its safety guarantees.

## Ground rules

- Never weaken the token-safety model. Tokens must stay out of logs, chat, and committed files.
- Keep the recommended publishing paths (`publish`, `push --method api`) as the safe default.
- Do not turn `push --method git` (legacy) into a default again.
- `--note` is local-only. Do not make it sync to GitHub.
- Destructive commands must keep their confirmation guards.

## Development setup

```bash
git clone https://github.com/NachaFromMars/github-manager.git
cd github-manager

# Configure a test token (use a throwaway repo where possible)
mkdir -p ~/.config/tt-github
printf 'GH_TOKEN=YOUR_TOKEN\nGITHUB_USER=your-user\n' > ~/.config/tt-github/env
chmod 600 ~/.config/tt-github/env
```

## Branch and commit workflow

1. Fork the repo (or branch if you have write access).
2. Create a topic branch: `git checkout -b feature/short-name`.
3. Make focused changes; keep unrelated edits in separate commits.
4. Use clear commit messages, e.g.:
   - `feat: add create-branch command`
   - `fix: scrub token on legacy push failure`
   - `docs: expand troubleshooting for 403`
5. Open a pull request describing the change and its safety impact.

## Testing before a PR

Minimum checks:

```bash
# 1) Syntax check
python3 -m py_compile scripts/gh_manager.py

# 2) Token + account works
python3 scripts/gh_manager.py whoami

# 3) Safe read path
python3 scripts/gh_manager.py repo-info --repo OWNER/test-repo

# 4) If touching publish/push, test against a throwaway repo only
```

Do not run destructive commands against real repos during testing.

## Commit message convention

- `feat:` new capability
- `fix:` bug fix
- `docs:` documentation only
- `refactor:` internal change, no behavior change
- `chore:` tooling/maintenance

## What will be rejected

- Changes that print or persist tokens insecurely.
- Defaults that bypass safety guards.
- New destructive commands without confirmation guards.
- Features that make `--note` or local library data public.
