# ========================================
# SCRIPT 1: KẾT NỐI REMOTE
# ========================================

Write-Host "`n📡 Kết nối với Remote Repository..." -ForegroundColor Yellow

# Xóa remote cũ
git remote remove origin 2>$null

# Thêm remote mới
git remote add origin https://github.com/phongnv3518-cmyk/Nhom10-QuizGame-

# Kiểm tra
Write-Host "`n✓ Remote đã kết nối:" -ForegroundColor Green
git remote -v

Write-Host "`n✅ Hoàn thành!" -ForegroundColor Green
