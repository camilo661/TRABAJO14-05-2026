"""
singleton.py
Singleton pattern implementation for the application state manager.
"""


class SingletonMeta(type):
    """Metaclass that implements the Singleton pattern."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class AppState(metaclass=SingletonMeta):
    """
    Central application state.
    Holds the request history and next request ID.
    Guaranteed to be a single instance across the entire application.
    """

    def __init__(self):
        self._history: list = []
        self._next_id: int = 1

    # ------------------------------------------------------------------
    # History management
    # ------------------------------------------------------------------
    def add_request(self, request: dict) -> None:
        """Append a new recharge request to the history."""
        self._history.append(request)

    def get_history(self) -> list:
        """Return a shallow copy of the full request history."""
        return list(self._history)

    def update_status(self, request_id: int, new_status: str) -> bool:
        """
        Update the status of an existing request by its ID.
        Returns True if the request was found and updated, False otherwise.
        """
        for req in self._history:
            if req["id"] == request_id:
                req["status"] = new_status
                return True
        return False

    # ------------------------------------------------------------------
    # ID counter
    # ------------------------------------------------------------------
    def get_next_id(self) -> int:
        """Return the next available sequential request ID."""
        current = self._next_id
        self._next_id += 1
        return current

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------
    def clear_history(self) -> None:
        """Reset the history and ID counter (useful for testing)."""
        self._history.clear()
        self._next_id = 1
