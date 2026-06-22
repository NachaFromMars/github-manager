# Repo Metadata

Use `update-repo` to keep GitHub-facing metadata clean and searchable.

```bash
python3 scripts/gh_manager.py update-repo \
  --repo OWNER/NAME \
  --desc "Short public repo pitch" \
  --topics openclaw,ai-agent,automation \
  --homepage https://github.com/OWNER/NAME \
  --note "local-only internal note"
```

## Public fields

These are sent to GitHub and visible on the repo page:

- `--desc`
- `--topics`
- `--homepage`
- `--private true|false` when used

## Local-only field

`--note` is **local-only**.

It is saved in:

```text
~/.config/tt-github/repos.json
```

It is never sent to GitHub. Use it for operator reminders, publishing context, or agent-only notes.

## Recommended topics

For OpenClaw/agent tools:

```text
openclaw, ai-agent, github-api, automation, developer-tools, python
```
