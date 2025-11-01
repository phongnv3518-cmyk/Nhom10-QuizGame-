# 🚀 Hướng Dẫn Git Workflow Tự Động

**Repository:** https://github.com/phongnv3518-cmyk/Nhom10-QuizGame-  
**Ngày tạo:** November 18, 2025

---

## 📋 MỤC LỤC

1. [Kết nối Repository với Remote](#1-kết-nối-repository-với-remote)
2. [Đồng bộ nhánh main với Remote](#2-đồng-bộ-nhánh-main-với-remote)
3. [Tạo và Quản lý Nhánh Mới](#3-tạo-và-quản-lý-nhánh-mới)
4. [Commit và Push Thay Đổi](#4-commit-và-push-thay-đổi)
5. [Kiểm tra Trạng Thái](#5-kiểm-tra-trạng-thái)

---

## 1. Kết nối Repository với Remote

### Bước 1.1: Kiểm tra trạng thái Git hiện tại

```powershell
# Kiểm tra xem đã có repository Git chưa
git status

# Nếu chưa có, khởi tạo Git repository
git init
```

### Bước 1.2: Kiểm tra remote hiện tại

```powershell
# Xem danh sách remote hiện có
git remote -v
```

### Bước 1.3: Thêm hoặc cập nhật remote origin

```powershell
# Nếu chưa có remote, thêm mới
git remote add origin https://github.com/phongnv3518-cmyk/Nhom10-QuizGame-

# Nếu đã có remote nhưng sai URL, cập nhật lại
git remote set-url origin https://github.com/phongnv3518-cmyk/Nhom10-QuizGame-

# Xác nhận remote đã đúng
git remote -v
```

**Kết quả mong đợi:**
```
origin  https://github.com/phongnv3518-cmyk/Nhom10-QuizGame- (fetch)
origin  https://github.com/phongnv3518-cmyk/Nhom10-QuizGame- (push)
```

---

## 2. Đồng bộ nhánh main với Remote

### Bước 2.1: Đảm bảo đang ở nhánh main

```powershell
# Chuyển về nhánh main
git checkout main

# Nếu chưa có nhánh main, tạo mới
git checkout -b main
```

### Bước 2.2: Fetch thông tin từ remote

```powershell
# Lấy thông tin mới nhất từ remote mà không merge
git fetch origin

# Xem các nhánh remote
git branch -r
```

### Bước 2.3: Pull và merge với remote main

```powershell
# Pull thay đổi từ remote main và merge
git pull origin main --rebase

# Nếu có conflict, giải quyết conflict rồi tiếp tục:
# 1. Sửa các file conflict
# 2. git add <file-đã-sửa>
# 3. git rebase --continue
```

### Bước 2.4: Thiết lập tracking branch

```powershell
# Thiết lập main tracking origin/main
git branch --set-upstream-to=origin/main main

# Hoặc ngắn gọn hơn
git branch -u origin/main main
```

**Lưu ý:** Nếu remote chưa có nhánh main, bạn cần push lần đầu:

```powershell
# Push main lần đầu và thiết lập tracking
git push -u origin main
```

---

## 3. Tạo và Quản lý Nhánh Mới

### Bước 3.1: Tạo 3 nhánh mới từ main

```powershell
# Đảm bảo đang ở main và đã cập nhật
git checkout main
git pull origin main

# Tạo nhánh 1: Fix login bug
git checkout -b fix-login-bug

# Quay về main
git checkout main

# Tạo nhánh 2: Update UI tests
git checkout -b update-ui-tests

# Quay về main
git checkout main

# Tạo nhánh 3: Refactor game logic
git checkout -b refactor-game-logic
```

### Bước 3.2: Xem tất cả nhánh đã tạo

```powershell
# Xem tất cả nhánh local
git branch

# Xem tất cả nhánh (local + remote)
git branch -a
```

**Kết quả mong đợi:**
```
  main
  fix-login-bug
  update-ui-tests
* refactor-game-logic
```

---

## 4. Commit và Push Thay Đổi

### 📁 Kịch bản 1: Nhánh fix-login-bug

```powershell
# Chuyển sang nhánh fix-login-bug
git checkout fix-login-bug

# Thêm các file thay đổi (ví dụ: fix bug trong client/)
git add client/

# Hoặc thêm các file cụ thể
git add client/client.py client/gui_client.py

# Commit với message rõ ràng
git commit -m "fix: resolve login timeout issue in client connection

- Fix socket timeout configuration
- Add retry logic for failed connections
- Update error handling in gui_client.py
- Tested with 50+ concurrent connections"

# Push nhánh lên remote và thiết lập tracking
git push -u origin fix-login-bug
```

### 🎨 Kịch bản 2: Nhánh update-ui-tests

```powershell
# Chuyển sang nhánh update-ui-tests
git checkout update-ui-tests

# Thêm thư mục tests/
git add tests/

# Hoặc thêm file specific
git add tests/test_ui_client.py tests/test_server_dashboard.py

# Commit với message chi tiết
git commit -m "test: add comprehensive UI tests for client and server

- Add unit tests for client GUI components
- Add integration tests for server dashboard
- Implement mock server for isolated client testing
- Add pytest fixtures for common test scenarios
- Coverage increased to 85%"

# Push và track
git push -u origin update-ui-tests
```

### ⚙️ Kịch bản 3: Nhánh refactor-game-logic

```powershell
# Chuyển sang nhánh refactor-game-logic
git checkout refactor-game-logic

# Thêm các file logic đã refactor
git add core/ logic/ server/game_logic.py

# Commit với message structured
git commit -m "refactor: improve game logic architecture and code organization

Breaking changes:
- Restructure core/shared_logic.py into modular components
- Extract quiz session management into separate class
- Refactor state machine in server/game_logic.py

Improvements:
- Better separation of concerns
- Reduced cyclomatic complexity
- Improved testability
- Added comprehensive docstrings

Migration guide:
- No API changes, fully backward compatible
- Internal implementation only"

# Push và track
git push -u origin refactor-game-logic
```

### 🔄 Kịch bản 4: Commit tất cả thay đổi

```powershell
# Nếu muốn commit tất cả file đã thay đổi
git add .

# Xem những gì sẽ được commit
git status

# Commit
git commit -m "chore: update project structure and documentation

- Update README.md with new features
- Add requirements.txt dependencies
- Generate bug fix reports
- Update Git workflow documentation"

# Push
git push -u origin <tên-nhánh-hiện-tại>
```

---

## 5. Kiểm tra Trạng Thái

### Bước 5.1: Xem nhánh hiện tại

```powershell
# Xem nhánh đang làm việc
git branch --show-current

# Hoặc xem chi tiết hơn
git status
```

### Bước 5.2: Xem lịch sử commit

```powershell
# Xem commit log đẹp
git log --oneline --graph --all --decorate -10

# Xem chi tiết commit gần nhất
git log -1 --stat

# Xem commits của tất cả nhánh
git log --oneline --all --graph
```

### Bước 5.3: Xem tracking branch status

```powershell
# Xem trạng thái tracking của tất cả nhánh
git branch -vv

# Xem có thay đổi nào chưa push không
git status
```

**Kết quả mong đợi:**
```
  main              a1b2c3d [origin/main] Latest commit message
  fix-login-bug     d4e5f6g [origin/fix-login-bug] fix: resolve login timeout issue
  update-ui-tests   h7i8j9k [origin/update-ui-tests] test: add comprehensive UI tests
* refactor-game-logic l0m1n2o [origin/refactor-game-logic: ahead 1] refactor: improve game logic
```

### Bước 5.4: Xem tất cả remote branches

```powershell
# Xem tất cả nhánh trên remote
git ls-remote --heads origin

# Hoặc
git branch -r
```

---

## 📚 WORKFLOW TỰ ĐỘNG HOÀN CHỈNH

### Script PowerShell tự động (Tất cả trong một)

```powershell
# ========================================
# GIT WORKFLOW TỰ ĐỘNG
# ========================================

Write-Host "🚀 Bắt đầu Git Workflow..." -ForegroundColor Cyan

# 1. Kiểm tra và kết nối remote
Write-Host "`n📡 BƯỚC 1: Kết nối Remote..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin https://github.com/phongnv3518-cmyk/Nhom10-QuizGame-
git remote -v

# 2. Đồng bộ main
Write-Host "`n🔄 BƯỚC 2: Đồng bộ nhánh main..." -ForegroundColor Yellow
git checkout main
git fetch origin
git pull origin main --rebase
git branch -u origin/main main

# 3. Tạo 3 nhánh mới
Write-Host "`n🌿 BƯỚC 3: Tạo 3 nhánh mới..." -ForegroundColor Yellow

git checkout main
git checkout -b fix-login-bug
Write-Host "✅ Đã tạo nhánh: fix-login-bug" -ForegroundColor Green

git checkout main
git checkout -b update-ui-tests
Write-Host "✅ Đã tạo nhánh: update-ui-tests" -ForegroundColor Green

git checkout main
git checkout -b refactor-game-logic
Write-Host "✅ Đã tạo nhánh: refactor-game-logic" -ForegroundColor Green

# 4. Commit và push từng nhánh
Write-Host "`n💾 BƯỚC 4: Commit và Push..." -ForegroundColor Yellow

# Nhánh 1: fix-login-bug
git checkout fix-login-bug
git add client/
git commit -m "fix: resolve login timeout issue in client connection" -m "- Fix socket timeout configuration`n- Add retry logic for failed connections`n- Update error handling in gui_client.py"
git push -u origin fix-login-bug
Write-Host "✅ Pushed: fix-login-bug" -ForegroundColor Green

# Nhánh 2: update-ui-tests
git checkout update-ui-tests
git add tests/
git commit -m "test: add comprehensive UI tests for client and server" -m "- Add unit tests for client GUI components`n- Add integration tests for server dashboard`n- Coverage increased to 85%"
git push -u origin update-ui-tests
Write-Host "✅ Pushed: update-ui-tests" -ForegroundColor Green

# Nhánh 3: refactor-game-logic
git checkout refactor-game-logic
git add core/ logic/ server/game_logic.py
git commit -m "refactor: improve game logic architecture" -m "- Restructure core/shared_logic.py`n- Extract quiz session management`n- Better separation of concerns"
git push -u origin refactor-game-logic
Write-Host "✅ Pushed: refactor-game-logic" -ForegroundColor Green

# 5. Hiển thị trạng thái
Write-Host "`n📊 BƯỚC 5: Trạng thái sau khi push..." -ForegroundColor Yellow

Write-Host "`n🌿 Tất cả nhánh local:" -ForegroundColor Cyan
git branch

Write-Host "`n📍 Nhánh hiện tại:" -ForegroundColor Cyan
git branch --show-current

Write-Host "`n🔍 Tracking status:" -ForegroundColor Cyan
git branch -vv

Write-Host "`n📝 Commit history (10 commits gần nhất):" -ForegroundColor Cyan
git log --oneline --graph --all --decorate -10

Write-Host "`n✅ HOÀN THÀNH WORKFLOW!" -ForegroundColor Green
```

### Lưu script trên thành file

```powershell
# Tạo file script
New-Item -Path "git_auto_workflow.ps1" -ItemType File -Force

# Copy nội dung script vào file (hoặc dùng editor)
# Sau đó chạy:
.\git_auto_workflow.ps1
```

---

## 🛠️ CÁC LỆNH HỮU ÍCH

### Quản lý Nhánh

```powershell
# Xem nhánh hiện tại
git branch --show-current

# Xem tất cả nhánh
git branch -a

# Xóa nhánh local
git branch -d <tên-nhánh>

# Xóa nhánh remote
git push origin --delete <tên-nhánh>

# Đổi tên nhánh hiện tại
git branch -m <tên-mới>

# Merge nhánh vào main
git checkout main
git merge <tên-nhánh>
```

### Undo Changes

```powershell
# Undo commit gần nhất (giữ thay đổi)
git reset --soft HEAD~1

# Undo commit gần nhất (xóa thay đổi)
git reset --hard HEAD~1

# Undo changes chưa commit
git restore <file>

# Undo tất cả changes chưa commit
git restore .
```

### Stash Changes

```powershell
# Lưu tạm thay đổi
git stash

# Xem danh sách stash
git stash list

# Apply stash gần nhất
git stash apply

# Apply và xóa stash
git stash pop
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

### 1. Trước khi commit

- ✅ Kiểm tra file đang ở đúng nhánh: `git branch --show-current`
- ✅ Xem file nào sẽ được commit: `git status`
- ✅ Xem chi tiết thay đổi: `git diff`

### 2. Commit Messages Best Practices

Dùng **Conventional Commits** format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: Feature mới
- `fix`: Sửa bug
- `docs`: Thay đổi documentation
- `style`: Code formatting (không ảnh hưởng logic)
- `refactor`: Code refactoring
- `test`: Thêm/sửa tests
- `chore`: Maintenance tasks

**Ví dụ:**

```
feat(client): add auto-reconnect feature

- Implement exponential backoff algorithm
- Add connection status indicator
- Update UI to show reconnection attempts

Closes #123
```

### 3. Nhánh main luôn stable

- ❌ Không commit trực tiếp vào main
- ✅ Luôn tạo nhánh mới cho mỗi feature/fix
- ✅ Merge vào main qua Pull Request (trên GitHub)

### 4. Trước khi push

```powershell
# Kiểm tra kỹ những gì sẽ push
git log origin/<branch>..HEAD --oneline

# Đảm bảo không push thông tin nhạy cảm
git diff origin/<branch> HEAD
```

### 5. Xử lý Conflicts

Nếu gặp conflict khi pull/merge:

```powershell
# 1. Xem file conflict
git status

# 2. Mở file và sửa conflict (tìm <<<<<<, ======, >>>>>>)

# 3. Sau khi sửa xong
git add <file-đã-sửa>

# 4. Tiếp tục merge/rebase
git rebase --continue
# hoặc
git merge --continue

# 5. Nếu muốn hủy
git rebase --abort
# hoặc
git merge --abort
```

---

## 📖 WORKFLOW CHO TỪNG VAI TRÒ

### Developer đang fix bug

```powershell
# 1. Tạo nhánh từ main
git checkout main
git pull origin main
git checkout -b fix-socket-timeout

# 2. Code và test

# 3. Commit
git add client/client.py
git commit -m "fix: resolve socket timeout in client connection"

# 4. Push
git push -u origin fix-socket-timeout

# 5. Tạo Pull Request trên GitHub
```

### Developer thêm feature mới

```powershell
# 1. Tạo nhánh feature
git checkout main
git pull origin main
git checkout -b feat-auto-save

# 2. Develop feature

# 3. Commit từng phần nhỏ
git add server/auto_save.py
git commit -m "feat: add auto-save functionality"

git add tests/test_auto_save.py
git commit -m "test: add auto-save tests"

# 4. Push
git push -u origin feat-auto-save

# 5. PR on GitHub
```

### Tester thêm tests

```powershell
# 1. Nhánh test
git checkout main
git pull origin main
git checkout -b test-game-logic

# 2. Viết tests

# 3. Commit
git add tests/
git commit -m "test: add integration tests for game logic"

# 4. Push
git push -u origin test-game-logic
```

---

## 🎯 CHECKLIST HOÀN CHỈNH

### Trước khi bắt đầu:

- [ ] Có Git đã cài đặt: `git --version`
- [ ] Repository đã init: `git status`
- [ ] Remote URL đúng: `git remote -v`
- [ ] Nhánh main đã đồng bộ: `git pull origin main`

### Khi tạo nhánh mới:

- [ ] Checkout main trước: `git checkout main`
- [ ] Pull latest changes: `git pull origin main`
- [ ] Tạo nhánh với tên có ý nghĩa: `git checkout -b <tên-rõ-ràng>`

### Khi commit:

- [ ] Đang ở đúng nhánh: `git branch --show-current`
- [ ] Xem file thay đổi: `git status`
- [ ] Add đúng files: `git add <files>`
- [ ] Message rõ ràng: `git commit -m "type: subject"`

### Khi push:

- [ ] Review commit: `git log -1`
- [ ] Push với tracking: `git push -u origin <branch>`
- [ ] Verify trên GitHub: Mở GitHub và xem nhánh

### Sau khi push:

- [ ] Check tracking status: `git branch -vv`
- [ ] Tạo Pull Request trên GitHub (nếu cần)
- [ ] Request review từ team

---

## 🔗 TÀI LIỆU THAM KHẢO

- [Git Official Documentation](https://git-scm.com/doc)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [Git Branching Model](https://nvie.com/posts/a-successful-git-branching-model/)

---

**END OF GUIDE**

*Được tạo cho project: Nhom10-QuizGame*  
*Repository: https://github.com/phongnv3518-cmyk/Nhom10-QuizGame-*
