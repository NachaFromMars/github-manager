# Setup PAT (fine-grained) cho GitHub Manager

## Tạo token
GitHub → Settings → Developer settings → Personal access tokens → **Fine-grained tokens** → Generate new token.

## Cấu hình đúng (để agent quản lý repo)
- **Token name:** vd `tt-github-manager`
- **Expiration:** chọn hạn hợp lý (vd 90 ngày / 1 năm)
- **Repository access:** `All repositories` (hoặc chọn repo cụ thể nếu muốn giới hạn)
- **Permissions → Repository** (đổi từ Read-only sang **Read and write**):
  | Quyền | Mức | Để làm gì |
  |---|---|---|
  | Administration | Read and write | tạo/xoá/cấu hình repo |
  | Contents | Read and write | push code, tạo branch, release files |
  | Workflows | Read and write | dùng GitHub Actions |
  | Issues | Read and write | mở/đóng issue |
  | Pull requests | Read and write | tạo/merge PR |
  | Metadata | Read-only (Required, mặc định) | bắt buộc |

> ⚠️ Mặc định mỗi quyền là "Read-only". PHẢI bấm dropdown "Access" → chọn "Read and write" cho Administration + Contents thì mới tạo/push repo được. Nếu để Read-only sẽ bị lỗi 403 "Resource not accessible by personal access token".

## Lưu token an toàn (không lộ ra chat)
```bash
mkdir -p ~/.config/tt-github && chmod 700 ~/.config/tt-github
cat > ~/.config/tt-github/env <<EOF
GITHUB_USER=<your_login>
GH_TOKEN=<github_pat_...>
EOF
chmod 600 ~/.config/tt-github/env
```

## Kiểm tra
```bash
python3 <skill-dir>/scripts/gh_manager.py whoami
```
Trả về `login` đúng = token sống.

## Xoay token (khi lộ)
Nếu token lỡ bị lộ (paste nhầm vào chat/group): Settings → token → **Revoke**, tạo token mới, cập nhật lại file env. Gửi token qua DM/kênh riêng, không qua group.
