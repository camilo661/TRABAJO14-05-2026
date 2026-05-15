"""
main.py
Entry point for the Mobile Plan Sales Simulator.

Usage:
    python main.py
"""

from frontend.main_window import MainWindow


def main():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
