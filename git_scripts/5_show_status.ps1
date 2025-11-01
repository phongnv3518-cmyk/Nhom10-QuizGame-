# ========================================
# SCRIPT 5: HIỂN THỊ TRẠNG THÁI
# ========================================

Write-Host "`n📊 Trạng thái Repository..." -ForegroundColor Yellow

# Quay về main
git checkout main

Write-Host "`n🌿 Nhánh local:" -ForegroundColor Cyan
git branch

Write-Host "`n🌐 Nhánh remote:" -ForegroundColor Cyan
git branch -r

Write-Host "`n📍 Nhánh hiện tại:" -ForegroundColor Cyan
git branch --show-current

Write-Host "`n🔍 Tracking status:" -ForegroundColor Cyan
git branch -vv

Write-Host "`n📝 Commit history (10 commits):" -ForegroundColor Cyan
git log --oneline --graph --all --decorate -10

Write-Host "`n🔗 Remote URLs:" -ForegroundColor Cyan
git remote -v

Write-Host "`n✅ Hoàn thành!" -ForegroundColor Green
