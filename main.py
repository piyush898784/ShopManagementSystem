"""
Smart Shop Management System
Main Entry Point
Tech Stack: Python, Tkinter, MySQL
"""

import sys
import os

# Add root directory to sys.path to enable direct execution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow
from database.db_config import DatabaseConfig
from database.db_helper import DBHelper


def main():
    # Attempt automatic database & schema initialization on startup if MySQL is available
    try:
        success, msg = DBHelper.initialize_database()
        if success:
            print("[INFO] MySQL connection established and database verified.")
    except Exception as e:
        print(f"[WARN] MySQL not yet initialized or connected: {e}")
        print("[INFO] You can configure database credentials from the Settings tab in the application.")

    # Start Tkinter Application
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
