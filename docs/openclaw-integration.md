# OpenClaw Integration

GitHub Manager is an OpenClaw skill that lets an agent manage GitHub from chat.

## Install

Place the skill folder under your OpenClaw skills directory:

```bash
git clone https://github.com/NachaFromMars/github-manager.git \
  ~/.openclaw/workspace/skills/github-manager

openclaw skills check
```

Confirm it appears as eligible and visible to the model.

## Configure token

See [`token-setup.md`](token-setup.md). At minimum:

```bash
mkdir -p ~/.config/tt-github
printf 'GH_TOKEN=YOUR_TOKEN\nGITHUB_USER=your-user\n' > ~/.config/tt-github/env
chmod 600 ~/.config/tt-github/env
```

## Triggers

The skill is intended for requests like:

- "push this skill to GitHub"
- "create a repo for this project"
- "publish this folder as a polished repo"
- "set repo description / topics"
- "open a GitHub issue"
- "cut a release"
- "show my repos" / "what repos have I uploaded"

## Agent publish workflow

The recommended flow for shipping a folder as a presentable repo:

1. Verify token: `whoami`
2. Publish in one shot:

```bash
python3 scripts/gh_manager.py publish \
  --path <folder> \
  --repo OWNER/NAME \
  --create \
  --desc "Short public pitch" \
  --topics openclaw,ai-agent,automation \
  --tag v0.1.0 \
  --notes "Initial release"
```

3. Optionally ask the user before generating banner/logo/screenshot assets.
4. Record the repo in My Repo Library (automatic on publish).

## Safety expectations for agents

- Prefer `publish` or `push --method api`.
- Treat `delete-repo` as destructive; confirm with the human.
- Never echo the token into chat or logs.
- `--note` stays local; do not present it as a GitHub-public field.

## Verifying a run

```bash
python3 scripts/gh_manager.py repo-info --repo OWNER/NAME
python3 scripts/gh_manager.py library-list --query NAME
```
