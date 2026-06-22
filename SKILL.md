---
name: github-manager
description: "Quản lý GitHub tự động cho agent: tạo repo, push code, mở/đọc issue, tạo release, xem thông tin repo, quản lý nhiều repo. Dùng khi user muốn đẩy code/skill lên GitHub, tạo repo mới, mở issue, ra release, kiểm tra repo, hoặc thao tác GitHub không cần mở web. Token đọc từ env GH_TOKEN hoặc ~/.config/tt-github/env, KHÔNG bao giờ in token ra chat. Triggers: push github, tạo repo, github repo, mở issue, tạo release, quản lý github, up lên github, list repo, github manager."
---

# GitHub Manager

Quản lý GitHub qua REST API bằng Python thuần (không cần cài `gh` CLI). Dành cho agent thao tác nhiều repo an toàn.

## Token (BẮT BUỘC, không lộ)

Thứ tự tìm token:
1. Biến môi trường `GH_TOKEN` / `GITHUB_TOKEN`
2. File `~/.config/tt-github/env` (dòng `GH_TOKEN=...`, `GITHUB_USER=...`)

Quy tắc:
- KHÔNG in token ra chat/log.
- Token nên là fine-grained PAT với quyền: Administration (tạo repo), Contents (push), Workflows (Actions), Issues/Pull requests (tùy chọn). Repository access: All repositories hoặc chọn repo cụ thể.
- Ưu tiên `publish` hoặc `push --method api` vì dùng GitHub Contents API. `push --method git` là legacy/riskier: tạm nhúng token vào remote URL rồi scrub sau push.

## Lệnh chính

```bash
S=<skill-dir>/scripts/gh_manager.py

python3 $S whoami                                   # kiểm tra token + login
python3 $S list-repos --limit 30
python3 $S create-repo --name my-skill --desc "..." [--private]
python3 $S repo-info --repo OWNER/NAME
python3 $S push --path /path/to/dir --repo OWNER/NAME --create --message "init" [--desc ..] [--private]
python3 $S create-issue --repo OWNER/NAME --title "Bug" --body "..."
python3 $S list-issues --repo OWNER/NAME --state open
python3 $S create-release --repo OWNER/NAME --tag v1.0 --name "v1.0" --notes "..."
python3 $S delete-repo --repo OWNER/NAME --confirm OWNER/NAME   # guarded: confirm phải khớp repo
```

## Quy trình đẩy skill/repo lên GitHub

1. `whoami` → xác nhận token còn sống + đúng account.
2. `push --path <dir> --repo <user>/<name> --create` → tạo repo (nếu chưa có) + commit + push.
3. `repo-info` → verify url + default_branch.
4. (tùy chọn) `create-release` đánh version.

## An toàn

- `delete-repo` có cơ chế guard: phải truyền `--confirm` đúng y `OWNER/NAME`.
- Thao tác phá hủy (delete repo/branch) → xác nhận với user trước.
- Lỗi 403 "Resource not accessible" = token thiếu quyền → hướng dẫn user thêm Administration/Contents = Read and write.
- Lỗi 401 = token sai/hết hạn → xin token mới qua kênh an toàn (DM/env), không qua chat công khai.

## Multi-repo

Để quản lý nhiều repo cùng lúc, lặp lệnh trên từng `OWNER/NAME`, hoặc kết hợp công cụ ngoài như `nosarthur/gita` / `alajmo/mani` cho thao tác git hàng loạt ở local.

## Files
- `scripts/gh_manager.py` — CLI REST API (whoami/list/create/push/issue/release/delete)
- `references/setup-pat.md` — hướng dẫn tạo + cấp quyền PAT đúng

## Auto polish (publish)
```bash
python3 <skill-dir>/scripts/gh_manager.py publish --path <dir> --repo OWNER/NAME --create --desc "..." --topics "openclaw,ai-agent,automation" --tag vX.Y.Z --notes "..."
```
Một lệnh: tạo repo (nếu cần) -> push file qua Contents API -> set description -> set topics -> tạo release. Token không in ra chat.

## Recommended path: publish first

For normal repo shipping, prefer `publish` over legacy git push:

```bash
python3 $S publish --path <dir> --repo OWNER/NAME --create --desc "..." --topics "openclaw,ai-agent,automation" --tag vX.Y.Z --notes "..."
```

`publish` uses the GitHub Contents API, then sets description/topics/homepage and optional release metadata.

## Push modes

```bash
python3 $S push --path <dir> --repo OWNER/NAME --create --method api   # default, recommended
python3 $S push --path <dir> --repo OWNER/NAME --method git            # legacy/riskier fallback
```

`--method git` temporarily embeds the token in the git remote URL before scrubbing it. Use only when API publishing is insufficient.

## Repo metadata

```bash
python3 $S update-repo --repo OWNER/NAME --desc "..." --topics "openclaw,ai-agent,automation" --homepage "https://github.com/OWNER/NAME" --note "local reminder"
```

Public on GitHub: `--desc`, `--topics`, `--homepage`, `--private`.

Local-only: `--note` is stored only in `~/.config/tt-github/repos.json`; it is not sent to GitHub and does not appear publicly.

## My Repo Library

```bash
python3 $S library-list
python3 $S library-list --query github
python3 $S library-add --repo OWNER/NAME --desc "..." --topics "openclaw,automation" --note "local reminder"
python3 $S library-remove --repo OWNER/NAME
```

Library path: `~/.config/tt-github/repos.json`.

Auto-sync commands: `create-repo`, `push`, `publish`, `update-repo`, successful `repo-info`.
