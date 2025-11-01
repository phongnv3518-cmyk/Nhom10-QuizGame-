# 📁 Git Scripts - Hướng Dẫn Sử Dụng

Thư mục này chứa các script PowerShell để tự động hóa Git workflow.

## 📂 Cấu trúc

```
git_scripts/
├── 1_connect_remote.ps1      # Kết nối với remote repository
├── 2_sync_main.ps1            # Đồng bộ nhánh main
├── 3_create_branches.ps1      # Tạo 3 nhánh mới
├── 4a_push_fix_login.ps1      # Push nhánh fix-login-bug
├── 4b_push_ui_tests.ps1       # Push nhánh update-ui-tests
├── 4c_push_refactor.ps1       # Push nhánh refactor-game-logic
└── 5_show_status.ps1          # Hiển thị trạng thái
```

## 🚀 Cách Sử Dụng

### Option 1: Chạy từng script riêng lẻ

```powershell
# Bước 1: Kết nối remote
cd git_scripts
.\1_connect_remote.ps1

# Bước 2: Đồng bộ main
.\2_sync_main.ps1

# Bước 3: Tạo 3 nhánh
.\3_create_branches.ps1

# Bước 4: Push từng nhánh
.\4a_push_fix_login.ps1
.\4b_push_ui_tests.ps1
.\4c_push_refactor.ps1

# Bước 5: Xem trạng thái
.\5_show_status.ps1
```

### Option 2: Chạy tất cả cùng lúc

```powershell
# Chạy script tự động hoàn chỉnh (ở thư mục gốc)
.\git_auto_workflow.ps1
```

### Option 3: Chạy từng bước thủ công

Xem file `git_workflow_guide.md` để biết các lệnh Git chi tiết.

## ⚠️ Lưu Ý Trước Khi Chạy

1. **Kiểm tra Git đã cài đặt:**
   ```powershell
   git --version
   ```

2. **Đảm bảo đang ở thư mục project:**
   ```powershell
   cd "c:\Users\quang\OneDrive\Máy tính\phong"
   ```

3. **Có quyền truy cập repository:**
   - Repository: https://github.com/phongnv3518-cmyk/Nhom10-QuizGame-
   - Cần có quyền push

4. **Execution Policy:**
   ```powershell
   # Nếu gặp lỗi execution policy, chạy:
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
   ```

## 📋 Chi Tiết Từng Script

### 1. connect_remote.ps1
- Xóa remote origin cũ (nếu có)
- Thêm remote mới: https://github.com/phongnv3518-cmyk/Nhom10-QuizGame-
- Xác nhận kết nối thành công

### 2. sync_main.ps1
- Checkout nhánh main
- Fetch thông tin từ remote
- Pull và rebase với origin/main
- Thiết lập tracking branch

### 3. create_branches.ps1
- Tạo nhánh: `fix-login-bug`
- Tạo nhánh: `update-ui-tests`
- Tạo nhánh: `refactor-game-logic`
- Hiển thị danh sách nhánh

### 4a. push_fix_login.ps1
- Checkout `fix-login-bug`
- Add files trong `client/`
- Commit với message rõ ràng
- Push lên origin/fix-login-bug

### 4b. push_ui_tests.ps1
- Checkout `update-ui-tests`
- Add files trong `tests/`
- Commit với message chi tiết
- Push lên origin/update-ui-tests

### 4c. push_refactor.ps1
- Checkout `refactor-game-logic`
- Add files: `core/`, `logic/`, `server/game_logic.py`
- Commit với message structured
- Push lên origin/refactor-game-logic

### 5. show_status.ps1
- Hiển thị tất cả nhánh local
- Hiển thị nhánh remote
- Hiển thị tracking status
- Hiển thị commit history
- Hiển thị remote URLs

## 🎯 Workflow Khuyến Nghị

### Lần Đầu Setup Repository

```powershell
# Chạy script tự động
.\git_auto_workflow.ps1
```

### Khi Làm Việc Hàng Ngày

```powershell
# 1. Cập nhật main
.\git_scripts\2_sync_main.ps1

# 2. Checkout nhánh cần làm
git checkout fix-login-bug

# 3. Code và test
# ...

# 4. Commit thay đổi
git add <files>
git commit -m "fix: your message"

# 5. Push
git push origin fix-login-bug

# 6. Xem status
.\git_scripts\5_show_status.ps1
```

## 🔧 Troubleshooting

### Lỗi: "git is not recognized"
```powershell
# Git chưa cài đặt hoặc chưa có trong PATH
# Download Git: https://git-scm.com/download/win
```

### Lỗi: "permission denied"
```powershell
# Không có quyền push lên repository
# Kiểm tra:
# 1. Đã thêm SSH key hoặc Personal Access Token chưa?
# 2. Có quyền write trong repository không?
```

### Lỗi: "conflict"
```powershell
# Có conflict khi merge/rebase
# Giải quyết:
# 1. Xem file conflict: git status
# 2. Sửa conflict trong editor
# 3. git add <file-đã-sửa>
# 4. git rebase --continue
```

### Lỗi: "remote already exists"
```powershell
# Remote origin đã tồn tại
# Cập nhật URL thay vì add:
git remote set-url origin https://github.com/phongnv3518-cmyk/Nhom10-QuizGame-
```

## 📚 Tài Liệu Tham Khảo

- `git_workflow_guide.md` - Hướng dẫn chi tiết Git workflow
- `git_auto_workflow.ps1` - Script tự động hoàn chỉnh
- [Git Documentation](https://git-scm.com/doc)

## 💡 Tips

1. **Luôn pull trước khi push:**
   ```powershell
   git pull origin <branch> --rebase
   git push origin <branch>
   ```

2. **Kiểm tra trước khi commit:**
   ```powershell
   git status
   git diff
   ```

3. **Commit message rõ ràng:**
   ```
   type(scope): subject
   
   body
   ```

4. **Backup trước khi làm thao tác nguy hiểm:**
   ```powershell
   git branch backup-$(Get-Date -Format "yyyyMMdd-HHmmss")
   ```

---

**Repository:** https://github.com/phongnv3518-cmyk/Nhom10-QuizGame-  
**Project:** Nhom10-QuizGame  
**Created:** November 18, 2025
