# Command Reference

All commands run as:

```bash
python3 scripts/gh_manager.py <command> [options]
```

Output is JSON. Tokens are never printed.

---

## whoami

Verify token and account.

```bash
python3 scripts/gh_manager.py whoami
```

---

## list-repos

List recently updated repositories.

| Option | Description | Default |
|--------|-------------|---------|
| `--limit N` | Max repos to list | 30 |

```bash
python3 scripts/gh_manager.py list-repos --limit 50
```

---

## create-repo

Create a new repository. Auto-saves to My Repo Library.

| Option | Description | Required |
|--------|-------------|----------|
| `--name` | Repo name | yes |
| `--desc` | Description | no |
| `--private` | Make repo private | no |

```bash
python3 scripts/gh_manager.py create-repo --name my-skill --desc "Agent tool" --private
```

---

## repo-info

Inspect a repository. Successful lookups sync to the library.

| Option | Description | Required |
|--------|-------------|----------|
| `--repo` | `OWNER/NAME` | yes |

```bash
python3 scripts/gh_manager.py repo-info --repo OWNER/NAME
```

---

## push

Push a local folder. Defaults to the safe Contents API method.

| Option | Description | Default |
|--------|-------------|---------|
| `--path` | Local folder | required |
| `--repo` | `OWNER/NAME` | required |
| `--branch` | Target branch | main |
| `--message` | Commit message | update |
| `--create` | Create repo first | off |
| `--desc` | Description on create | empty |
| `--private` | Private on create | off |
| `--method` | `api` or `git` | api |

```bash
python3 scripts/gh_manager.py push --path ./dir --repo OWNER/NAME --create --method api
```

`--method git` is legacy/riskier (temporarily embeds the token in the remote URL).

---

## publish

Recommended one-shot path: ensure repo → push (Contents API) → set description → topics → optional release. Auto-saves to library.

| Option | Description | Default |
|--------|-------------|---------|
| `--path` | Local folder | required |
| `--repo` | `OWNER/NAME` | required |
| `--branch` | Target branch | main |
| `--message` | Commit message | publish |
| `--create` | Create repo first | off |
| `--private` | Private on create | off |
| `--desc` | Description | empty |
| `--homepage` | Homepage URL | empty |
| `--topics` | Comma-separated topics | default set |
| `--tag` | Release tag (optional) | none |
| `--release-name` | Release title | tag value |
| `--notes` | Release notes | empty |

```bash
python3 scripts/gh_manager.py publish \
  --path ./my-skill --repo OWNER/my-skill --create \
  --desc "Short pitch" --topics openclaw,ai-agent,automation \
  --tag v0.1.0 --notes "Initial release"
```

---

## update-repo

Update GitHub-facing metadata. Auto-saves to library.

| Option | Description | Public on GitHub |
|--------|-------------|------------------|
| `--repo` | `OWNER/NAME` (required) | — |
| `--desc` | Description | yes |
| `--topics` | Comma-separated topics | yes |
| `--homepage` | Homepage URL | yes |
| `--private` | `true`/`false` | yes |
| `--note` | Internal note | **no, local-only** |

```bash
python3 scripts/gh_manager.py update-repo --repo OWNER/NAME \
  --desc "Pitch" --topics openclaw,automation --note "local reminder"
```

---

## library-list / library-add / library-remove

Manage the local My Repo Library (`~/.config/tt-github/repos.json`).

```bash
python3 scripts/gh_manager.py library-list
python3 scripts/gh_manager.py library-list --query github
python3 scripts/gh_manager.py library-add --repo OWNER/NAME --desc "..." --topics a,b --note "local"
python3 scripts/gh_manager.py library-remove --repo OWNER/NAME
```

---

## create-issue / list-issues

```bash
python3 scripts/gh_manager.py create-issue --repo OWNER/NAME --title "Bug" --body "Details"
python3 scripts/gh_manager.py list-issues --repo OWNER/NAME --state open
```

---

## create-release

```bash
python3 scripts/gh_manager.py create-release --repo OWNER/NAME --tag v1.0.0 --name "v1.0.0" --notes "..."
```

---

## set-topics / set-meta

Lower-level helpers used by `publish`/`update-repo`.

```bash
python3 scripts/gh_manager.py set-topics --repo OWNER/NAME --topics openclaw,automation
python3 scripts/gh_manager.py set-meta --repo OWNER/NAME --desc "..." --homepage "https://..."
```

---

## delete-repo

Guarded destructive command. `--confirm` must equal `--repo` exactly.

```bash
python3 scripts/gh_manager.py delete-repo --repo OWNER/NAME --confirm OWNER/NAME
```
