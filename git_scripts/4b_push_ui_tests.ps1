# ========================================
# SCRIPT 4: COMMIT VÀ PUSH - UPDATE-UI-TESTS
# ========================================

Write-Host "`n🧪 Xử lý nhánh: update-ui-tests" -ForegroundColor Yellow

# Checkout nhánh
git checkout update-ui-tests

# Add files
Write-Host "→ Đang add files..." -ForegroundColor Gray
git add tests/

# Commit
Write-Host "→ Đang commit..." -ForegroundColor Gray
git commit -m "test: add comprehensive UI tests for client and server" -m "- Add unit tests for client GUI components
- Add integration tests for server dashboard
- Implement mock server for isolated client testing
- Add pytest fixtures for common test scenarios
- Coverage increased to 85%"

# Push
Write-Host "→ Đang push..." -ForegroundColor Gray
git push -u origin update-ui-tests

Write-Host "`n✅ Hoàn thành! Nhánh update-ui-tests đã được push." -ForegroundColor Green

# Hiển thị status
git log --oneline -3
