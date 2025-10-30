"""Module entry to start the GUI client: python -m client.gui_client
It delegates to gui_client_pkg.main_window.run().
"""
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui_client_pkg.main_window import run  # ✅ Đường dẫn đúng tới GUI code

if __name__ == "__main__":
    run()
