# My Repo Library

GitHub Manager keeps a local catalog of repos that the agent has published or curated.

```text
~/.config/tt-github/repos.json
```

This file is local-only. It is not pushed to GitHub by any library command.

## Why it exists

The library lets the agent answer questions like:

- Which repos have I already uploaded?
- What description/topics did I set?
- Which repos are public/private?
- What internal note did I leave for this repo?

## Commands

```bash
python3 scripts/gh_manager.py library-list
python3 scripts/gh_manager.py library-list --query github
python3 scripts/gh_manager.py library-add --repo OWNER/NAME --desc "Important repo" --topics openclaw,automation --note "local reminder"
python3 scripts/gh_manager.py library-remove --repo OWNER/NAME
```

## Auto-sync behavior

The following commands write/update library entries automatically:

- `create-repo`
- `push`
- `publish`
- `update-repo`
- `repo-info` when the repo lookup succeeds

## Local-only notes

`--note` is for private agent/operator context. It is stored only in `~/.config/tt-github/repos.json`.

It is **not** sent to GitHub, not stored as repo description, not added to topics, and not included in release notes.
