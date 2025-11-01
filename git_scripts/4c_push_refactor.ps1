# ========================================
# SCRIPT 4: COMMIT VÀ PUSH - REFACTOR-GAME-LOGIC
# ========================================

Write-Host "`n⚙️ Xử lý nhánh: refactor-game-logic" -ForegroundColor Yellow

# Checkout nhánh
git checkout refactor-game-logic

# Add files
Write-Host "→ Đang add files..." -ForegroundColor Gray
git add core/ logic/ server/game_logic.py

# Commit
Write-Host "→ Đang commit..." -ForegroundColor Gray
git commit -m "refactor: improve game logic architecture and code organization" -m "Breaking changes:
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

# Push
Write-Host "→ Đang push..." -ForegroundColor Gray
git push -u origin refactor-game-logic

Write-Host "`n✅ Hoàn thành! Nhánh refactor-game-logic đã được push." -ForegroundColor Green

# Hiển thị status
git log --oneline -3
