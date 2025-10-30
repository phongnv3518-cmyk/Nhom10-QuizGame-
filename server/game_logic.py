"""Thin game_logic wrapper in server package.

This module re-exports the shared load_questions implementation so callers
can import from server.game_logic if desired.
"""
from core.shared_logic import load_questions

__all__ = ["load_questions"]
