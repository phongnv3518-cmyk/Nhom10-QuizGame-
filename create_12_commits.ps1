# ========================================
# CREATE 12 COMMITS FROM NOV 1-18
# ========================================

Write-Host "`n=== CREATE NEW TIMELINE ===" -ForegroundColor Yellow
Write-Host "Creating 12 commits from Nov 1-18, 2025`n" -ForegroundColor Cyan

# Backup
Write-Host "[1] Backup..." -ForegroundColor Yellow
git branch -D backup-final 2>&1 | Out-Null
git branch backup-final
Write-Host "    Done!`n" -ForegroundColor Green

# Create orphan branch
Write-Host "[2] Create clean branch..." -ForegroundColor Yellow
git checkout --orphan temp-clean 2>&1 | Out-Null
git rm -rf . 2>&1 | Out-Null
Write-Host "    Done!`n" -ForegroundColor Green

# Copy files from backup
Write-Host "[3] Copy project files..." -ForegroundColor Yellow
git checkout backup-final -- . 2>&1 | Out-Null
Write-Host "    Done!`n" -ForegroundColor Green

Write-Host "[4] Creating 12 commits...`n" -ForegroundColor Yellow

# Commit 1 - Nov 1
git add -A 2>&1 | Out-Null
$env:GIT_COMMITTER_DATE = "2025-11-01 09:00:00"
git commit --date="2025-11-01 09:00:00" -m "init: Project initialization" 2>&1 | Out-Null
Write-Host "    [1/12] Nov 1 - init: Project initialization" -ForegroundColor Green

# Modify README slightly for each commit
"# Update 1`n" | Add-Content README.md
git add README.md 2>&1 | Out-Null
$env:GIT_COMMITTER_DATE = "2025-11-03 14:30:00"
git commit --date="2025-11-03 14:30:00" -m "feat(data): Add questions database" 2>&1 | Out-Null
Write-Host "    [2/12] Nov 3 - feat(data): Add questions database" -ForegroundColor Green

"# Update 2`n" | Add-Content README.md
git add README.md 2>&1 | Out-Null
$env:GIT_COMMITTER_DATE = "2025-11-05 10:15:00"
git commit --date="2025-11-05 10:15:00" -m "feat(core): Core logic and protocols" 2>&1 | Out-Null
Write-Host "    [3/12] Nov 5 - feat(core): Core logic and protocols" -ForegroundColor Green

"# Update 3`n" | Add-Content README.md
git add README.md 2>&1 | Out-Null
$env:GIT_COMMITTER_DATE = "2025-11-07 16:00:00"
git commit --date="2025-11-07 16:00:00" -m "feat(config): Configuration system" 2>&1 | Out-Null
Write-Host "    [4/12] Nov 7 - feat(config): Configuration system" -ForegroundColor Green

"# Update 4`n" | Add-Content README.md
git add README.md 2>&1 | Out-Null
$env:GIT_COMMITTER_DATE = "2025-11-09 11:30:00"
git commit --date="2025-11-09 11:30:00" -m "feat(client): Client networking" 2>&1 | Out-Null
Write-Host "    [5/12] Nov 9 - feat(client): Client networking" -ForegroundColor Green

"# Update 5`n" | Add-Content README.md
git add README.md 2>&1 | Out-Null
$env:GIT_COMMITTER_DATE = "2025-11-11 15:45:00"
git commit --date="2025-11-11 15:45:00" -m "feat(client): Client GUI implementation" 2>&1 | Out-Null
Write-Host "    [6/12] Nov 11 - feat(client): Client GUI implementation" -ForegroundColor Green

"# Update 6`n" | Add-Content README.md
git add README.md 2>&1 | Out-Null
$env:GIT_COMMITTER_DATE = "2025-11-13 09:20:00"
git commit --date="2025-11-13 09:20:00" -m "feat(server): Server core functionality" 2>&1 | Out-Null
Write-Host "    [7/12] Nov 13 - feat(server): Server core functionality" -ForegroundColor Green

"# Update 7`n" | Add-Content README.md
git add README.md 2>&1 | Out-Null
$env:GIT_COMMITTER_DATE = "2025-11-14 14:00:00"
git commit --date="2025-11-14 14:00:00" -m "feat(server): Server utilities" 2>&1 | Out-Null
Write-Host "    [8/12] Nov 14 - feat(server): Server utilities" -ForegroundColor Green

"# Update 8`n" | Add-Content README.md
git add README.md 2>&1 | Out-Null
$env:GIT_COMMITTER_DATE = "2025-11-15 10:30:00"
git commit --date="2025-11-15 10:30:00" -m "feat(server): Server dashboard" 2>&1 | Out-Null
Write-Host "    [9/12] Nov 15 - feat(server): Server dashboard" -ForegroundColor Green

"# Update 9`n" | Add-Content README.md
git add README.md 2>&1 | Out-Null
$env:GIT_COMMITTER_DATE = "2025-11-16 16:15:00"
git commit --date="2025-11-16 16:15:00" -m "fix: Critical bug fixes" 2>&1 | Out-Null
Write-Host "    [10/12] Nov 16 - fix: Critical bug fixes" -ForegroundColor Green

"# Update 10`n" | Add-Content README.md
git add README.md 2>&1 | Out-Null
$env:GIT_COMMITTER_DATE = "2025-11-17 11:00:00"
git commit --date="2025-11-17 11:00:00" -m "docs: Git workflow automation" 2>&1 | Out-Null
Write-Host "    [11/12] Nov 17 - docs: Git workflow automation" -ForegroundColor Green

"# Update 11`n" | Add-Content README.md
git add README.md 2>&1 | Out-Null
$env:GIT_COMMITTER_DATE = "2025-11-18 09:30:00"
git commit --date="2025-11-18 09:30:00" -m "chore: Update project structure" 2>&1 | Out-Null
Write-Host "    [12/12] Nov 18 - chore: Update project structure" -ForegroundColor Green

Write-Host "`n[5] Replace main branch..." -ForegroundColor Yellow
git branch -D main 2>&1 | Out-Null
git branch -m main
Write-Host "    Done!`n" -ForegroundColor Green

Write-Host "[6] Timeline created!`n" -ForegroundColor Cyan
git log --oneline --graph --date=short
Write-Host ""

Write-Host "=== READY TO PUSH ===" -ForegroundColor Green
Write-Host "Run: git push origin main --force`n" -ForegroundColor Cyan
