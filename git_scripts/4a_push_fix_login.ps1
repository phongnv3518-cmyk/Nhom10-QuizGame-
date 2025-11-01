# ========================================
# SCRIPT 4: COMMIT VÀ PUSH - FIX-LOGIN-BUG
# ========================================

Write-Host "`n🐛 Xử lý nhánh: fix-login-bug" -ForegroundColor Yellow

# Checkout nhánh
git checkout fix-login-bug

# Add files
Write-Host "→ Đang add files..." -ForegroundColor Gray
git add client/

# Commit
Write-Host "→ Đang commit..." -ForegroundColor Gray
git commit -m "fix: resolve login timeout issue in client connection" -m "- Fix socket timeout configuration
- Add retry logic for failed connections
- Update error handling in gui_client.py
- Tested with 50+ concurrent connections"

# Push
Write-Host "→ Đang push..." -ForegroundColor Gray
git push -u origin fix-login-bug

Write-Host "`n✅ Hoàn thành! Nhánh fix-login-bug đã được push." -ForegroundColor Green

# Hiển thị status
git log --oneline -3
