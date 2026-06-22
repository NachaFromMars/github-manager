# Branch & PR Workflow

v0.4.0 adds a safe collaboration layer so the agent can propose changes through pull requests instead of pushing straight to the default branch.

## Principle: no direct main pushes for collaborative changes

For shared/important repos, the agent should:

1. Create a feature branch.
2. Push changes to that branch.
3. Open a pull request.
4. Let a human review/merge (or merge only with explicit confirmation).

Direct pushes to `main` are still possible for solo/quick work, but the PR flow is the recommended path when review matters.

## Commands

### create-branch

```bash
python3 scripts/gh_manager.py create-branch --repo OWNER/NAME --name feature/my-change [--base main]
```

Creates `feature/my-change` from `--base` (defaults to the repo's default branch).

### Push changes to the branch

Use the Contents API push, targeting the branch:

```bash
python3 scripts/gh_manager.py push --path ./dir --repo OWNER/NAME --branch feature/my-change --method api
```

### open-pr

```bash
python3 scripts/gh_manager.py open-pr \
  --repo OWNER/NAME \
  --head feature/my-change \
  --base main \
  --title "Add my change" \
  --body "What and why" \
  [--draft]
```

### list-prs

```bash
python3 scripts/gh_manager.py list-prs --repo OWNER/NAME --state open
```

### comment-issue

Works for both issues and pull requests (a PR is an issue in the GitHub API):

```bash
python3 scripts/gh_manager.py comment-issue --repo OWNER/NAME --number 12 --body "LGTM after CI passes"
```

### merge-pr (guarded)

Merging is destructive to branch state, so it requires an exact confirmation token `REPO#NUMBER`:

```bash
python3 scripts/gh_manager.py merge-pr \
  --repo OWNER/NAME \
  --number 12 \
  --method squash \
  --confirm OWNER/NAME#12
```

Merge methods: `merge` (default), `squash`, `rebase`.

## Safety notes

- `merge-pr` requires `--confirm OWNER/NAME#NUMBER` to match exactly; a mismatch is rejected.
- Prefer human review before merging into `main`.
- Use `--draft` for work-in-progress PRs.
- The agent should not auto-merge without explicit human confirmation.
