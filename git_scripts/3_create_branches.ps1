# ========================================
# SCRIPT 3: TẠO 3 NHÁNH MỚI
# ========================================

Write-Host "`n🌿 Tạo 3 nhánh mới từ main..." -ForegroundColor Yellow

# Đảm bảo ở main
git checkout main

# Nhánh 1: Fix login bug
Write-Host "`n🐛 Tạo nhánh: fix-login-bug" -ForegroundColor Cyan
git checkout -b fix-login-bug
git checkout main

# Nhánh 2: Update UI tests
Write-Host "🧪 Tạo nhánh: update-ui-tests" -ForegroundColor Cyan
git checkout -b update-ui-tests
git checkout main

# Nhánh 3: Refactor game logic
Write-Host "⚙️ Tạo nhánh: refactor-game-logic" -ForegroundColor Cyan
git checkout -b refactor-game-logic
git checkout main

# Hiển thị tất cả nhánh
Write-Host "`n✓ Danh sách nhánh đã tạo:" -ForegroundColor Green
git branch

Write-Host "`n✅ Hoàn thành!" -ForegroundColor Green
