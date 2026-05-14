"""
app_window.py
Main application window that composes all UI components together.
"""

import tkinter as tk
from tkinter import messagebox

from frontend.components import (
    COLORS,
    FONT_FAMILY,
    OperatorSelector,
    PlanSelector,
    CustomerForm,
)
from frontend.history_panel import HistoryPanel
from frontend.receipt_dialog import ReceiptDialog
from backend.processor import create_recharge_request, get_all_requests, ValidationError


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------

class AppWindow(tk.Tk):
    """Root application window."""

    APP_TITLE = "Simulador de Ventas - Planes Móviles"
    MIN_WIDTH = 1100
    MIN_HEIGHT = 720

    def __init__(self):
        super().__init__()
        self.title(self.APP_TITLE)
        self.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.configure(bg=COLORS["bg"])

        self._selected_operator: str | None = None
        self._selected_plan: dict | None = None

        self._build()
        self._load_history()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build(self):
        # ---- Top bar ----
        topbar = tk.Frame(self, bg=COLORS["surface2"], height=52)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        tk.Label(
            topbar,
            text="📱  Simulador de Ventas de Planes Móviles",
            bg=COLORS["surface2"],
            fg=COLORS["accent"],
            font=(FONT_FAMILY, 15, "bold"),
        ).pack(side="left", padx=20, pady=12)

        tk.Label(
            topbar,
            text="Colombia · COP",
            bg=COLORS["surface2"],
            fg=COLORS["text_muted"],
            font=(FONT_FAMILY, 9),
        ).pack(side="right", padx=20)

        # ---- Main layout: left panel + history ----
        main = tk.Frame(self, bg=COLORS["bg"])
        main.pack(fill="both", expand=True, padx=20, pady=16)

        # Left panel (operator + plan + form)
        left = tk.Frame(main, bg=COLORS["bg"])
        left.pack(side="left", fill="y", padx=(0, 20))
        left.pack_propagate(False)
        left.config(width=440)

        # Operator selector
        self._op_selector = OperatorSelector(left, on_select=self._on_operator_selected)
        self._op_selector.pack(fill="x", pady=(0, 16))

        # Divider
        tk.Frame(left, bg=COLORS["border"], height=1).pack(fill="x", pady=(0, 16))

        # Plan selector
        self._plan_selector = PlanSelector(left, on_select=self._on_plan_selected)
        self._plan_selector.pack(fill="x", pady=(0, 16))

        # Divider
        tk.Frame(left, bg=COLORS["border"], height=1).pack(fill="x", pady=(0, 16))

        # Customer form
        self._form = CustomerForm(left, on_submit=self._on_form_submit)
        self._form.pack(fill="x")

        # Right panel (history)
        right = tk.Frame(main, bg=COLORS["bg"])
        right.pack(side="left", fill="both", expand=True)

        self._history = HistoryPanel(right)
        self._history.pack(fill="both", expand=True)

        # ---- Status bar ----
        statusbar = tk.Frame(self, bg=COLORS["surface2"], height=26)
        statusbar.pack(fill="x", side="bottom")
        statusbar.pack_propagate(False)

        self._status_label = tk.Label(
            statusbar,
            text="Listo. Selecciona un operador para comenzar.",
            bg=COLORS["surface2"],
            fg=COLORS["text_muted"],
            font=(FONT_FAMILY, 8),
        )
        self._status_label.pack(side="left", padx=12, pady=4)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_operator_selected(self, operator_key: str):
        self._selected_operator = operator_key
        self._selected_plan = None
        self._plan_selector.load_operator(operator_key)
        from backend.catalog import OPERATORS
        op_name = OPERATORS[operator_key]["display_name"]
        self._set_status(f"Operador seleccionado: {op_name}. Elige un plan.")

    def _on_plan_selected(self, plan: dict):
        self._selected_plan = plan
        self._set_status(
            f"Plan seleccionado: {plan['name']} — ${plan['price']:,}. Completa los datos del cliente."
        )

    def _on_form_submit(self, form_data: dict):
        self._form.clear_error()

        if not self._selected_operator:
            self._form.show_error("Debes seleccionar un operador antes de continuar.")
            return

        if not self._selected_plan:
            self._form.show_error("Debes seleccionar un plan antes de continuar.")
            return

        try:
            request = create_recharge_request(
                operator_key=self._selected_operator,
                plan_id=self._selected_plan["id"],
                customer_name=form_data.get("nombre", ""),
                phone_number=form_data.get("telefono", ""),
                email=form_data.get("correo", ""),
            )
        except ValidationError as exc:
            self._form.show_error(str(exc))
            return

        # Update history table
        self._history.add_row(request)

        # Show receipt
        ReceiptDialog(self, request)

        # Reset form for next sale
        self._form.reset()
        self._set_status(
            f"Solicitud #{request['id']:03d} registrada con estado: {request['status'].upper()}"
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _load_history(self):
        """Load existing history on startup (in case of pre-seeded data)."""
        self._history.refresh(get_all_requests())

    def _set_status(self, message: str):
        self._status_label.config(text=message)
