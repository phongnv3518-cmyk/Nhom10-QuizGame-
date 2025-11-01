# ========================================
# SCRIPT 2: ĐỒNG BỘ MAIN
# ========================================

Write-Host "`n🔄 Đồng bộ nhánh main..." -ForegroundColor Yellow

# Chuyển về main
git checkout main

# Fetch từ remote
git fetch origin

# Pull và rebase
git pull origin main --rebase

# Thiết lập tracking
git branch -u origin/main main

# Hiển thị status
Write-Host "`n✓ Main branch status:" -ForegroundColor Green
git status
git log --oneline -5

Write-Host "`n✅ Hoàn thành!" -ForegroundColor Green
