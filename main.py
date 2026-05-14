"""
main.py
Entry point for the Mobile Plan Sales Simulator.

Usage:
    python main.py
"""

from frontend.app_window import AppWindow


def main():
    app = AppWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
