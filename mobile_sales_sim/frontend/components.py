"""
components.py
Reusable Tkinter UI components for the mobile sales simulator.
All user-facing labels and text are in Spanish.
"""

import tkinter as tk
from tkinter import ttk, font
from backend.catalog import OPERATORS, format_price, format_data


# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
COLORS = {
    "bg": "#0F172A",
    "surface": "#1E293B",
    "surface2": "#334155",
    "accent": "#38BDF8",
    "accent_dark": "#0284C7",
    "success": "#4ADE80",
    "warning": "#FACC15",
    "danger": "#F87171",
    "text": "#F1F5F9",
    "text_muted": "#94A3B8",
    "border": "#475569",
    "white": "#FFFFFF",
}

FONT_FAMILY = "Helvetica"


# ---------------------------------------------------------------------------
# Helper: rounded-look label-frame
# ---------------------------------------------------------------------------

def make_card(parent, **kwargs) -> tk.Frame:
    """Return a styled card frame."""
    defaults = dict(bg=COLORS["surface"], relief="flat", bd=0)
    defaults.update(kwargs)
    return tk.Frame(parent, **defaults)


def make_separator(parent) -> ttk.Separator:
    sep = ttk.Separator(parent, orient="horizontal")
    return sep


# ---------------------------------------------------------------------------
# Operator selector component
# ---------------------------------------------------------------------------

class OperatorSelector(tk.Frame):
    """
    Displays operator buttons in a grid.
    Calls `on_select(operator_key)` when one is clicked.
    """

    def __init__(self, parent, on_select, **kwargs):
        super().__init__(parent, bg=COLORS["bg"], **kwargs)
        self._on_select = on_select
        self._buttons: dict[str, tk.Button] = {}
        self._selected: str | None = None
        self._build()

    def _build(self):
        title = tk.Label(
            self,
            text="① Selecciona el Operador",
            bg=COLORS["bg"],
            fg=COLORS["accent"],
            font=(FONT_FAMILY, 13, "bold"),
        )
        title.pack(anchor="w", pady=(0, 8))

        grid = tk.Frame(self, bg=COLORS["bg"])
        grid.pack(fill="x")

        for col, (key, op) in enumerate(OPERATORS.items()):
            btn = tk.Button(
                grid,
                text=op["display_name"],
                bg=COLORS["surface2"],
                fg=COLORS["text"],
                activebackground=op["color"],
                activeforeground=COLORS["white"],
                font=(FONT_FAMILY, 11, "bold"),
                relief="flat",
                bd=0,
                padx=18,
                pady=10,
                cursor="hand2",
                command=lambda k=key: self._select(k),
            )
            btn.grid(row=0, column=col, padx=6, pady=4, sticky="ew")
            grid.columnconfigure(col, weight=1)
            self._buttons[key] = btn

    def _select(self, key: str):
        for k, btn in self._buttons.items():
            op_color = OPERATORS[k]["color"]
            if k == key:
                btn.config(bg=op_color, fg=COLORS["white"])
            else:
                btn.config(bg=COLORS["surface2"], fg=COLORS["text"])
        self._selected = key
        self._on_select(key)

    def get_selected(self) -> str | None:
        return self._selected

    def reset(self):
        for k, btn in self._buttons.items():
            btn.config(bg=COLORS["surface2"], fg=COLORS["text"])
        self._selected = None


# ---------------------------------------------------------------------------
# Plan card component
# ---------------------------------------------------------------------------

class PlanCard(tk.Frame):
    """Displays a single plan as a selectable card."""

    def __init__(self, parent, plan: dict, operator_color: str, on_select, **kwargs):
        super().__init__(parent, bg=COLORS["surface"], relief="flat", bd=2, **kwargs)
        self._plan = plan
        self._on_select = on_select
        self._color = operator_color
        self._build()
        self.bind("<Button-1>", self._click)

    def _build(self):
        # Tier badge
        tier_colors = {1: COLORS["text_muted"], 2: COLORS["warning"], 3: COLORS["success"]}
        tier_labels = {1: "Básico", 2: "Estándar", 3: "Premium"}
        tier = self._plan["tier"]

        header = tk.Frame(self, bg=self._color)
        header.pack(fill="x")
        tk.Label(
            header,
            text=self._plan["name"],
            bg=self._color,
            fg=COLORS["white"],
            font=(FONT_FAMILY, 11, "bold"),
            padx=10,
            pady=6,
        ).pack(side="left")
        tk.Label(
            header,
            text=tier_labels[tier],
            bg=self._color,
            fg=COLORS["white"],
            font=(FONT_FAMILY, 8),
            padx=8,
            pady=6,
        ).pack(side="right")

        body = tk.Frame(self, bg=COLORS["surface"], padx=10, pady=8)
        body.pack(fill="x")

        # Price
        tk.Label(
            body,
            text=format_price(self._plan["price"]),
            bg=COLORS["surface"],
            fg=COLORS["accent"],
            font=(FONT_FAMILY, 18, "bold"),
        ).pack(anchor="w")
        tk.Label(
            body,
            text="/ mes",
            bg=COLORS["surface"],
            fg=COLORS["text_muted"],
            font=(FONT_FAMILY, 9),
        ).pack(anchor="w")

        # Features
        features = [
            ("📞", f"{self._plan['minutes']} Minutos"),
            ("📶", format_data(self._plan["data_mb"])),
            ("💬", f"{self._plan['sms']} SMS"),
            ("📅", f"{self._plan['validity_days']} días vigencia"),
        ]
        for icon, text in features:
            row = tk.Frame(body, bg=COLORS["surface"])
            row.pack(anchor="w", pady=1)
            tk.Label(row, text=icon, bg=COLORS["surface"], font=(FONT_FAMILY, 9)).pack(side="left")
            tk.Label(
                row,
                text=text,
                bg=COLORS["surface"],
                fg=COLORS["text"],
                font=(FONT_FAMILY, 9),
            ).pack(side="left", padx=4)

        # Description
        tk.Label(
            body,
            text=self._plan["description"],
            bg=COLORS["surface"],
            fg=COLORS["text_muted"],
            font=(FONT_FAMILY, 8, "italic"),
            wraplength=200,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))

        # Select button
        tk.Button(
            body,
            text="Seleccionar Plan",
            bg=self._color,
            fg=COLORS["white"],
            font=(FONT_FAMILY, 9, "bold"),
            relief="flat",
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2",
            command=self._click,
        ).pack(fill="x", pady=(8, 0))

    def _click(self, event=None):
        self._on_select(self._plan)

    def highlight(self, active: bool):
        border_color = self._color if active else COLORS["surface"]
        self.config(highlightbackground=border_color, highlightthickness=2 if active else 0)


# ---------------------------------------------------------------------------
# Plan selector (container of PlanCards)
# ---------------------------------------------------------------------------

class PlanSelector(tk.Frame):
    """Shows three plan cards for the selected operator."""

    def __init__(self, parent, on_select, **kwargs):
        super().__init__(parent, bg=COLORS["bg"], **kwargs)
        self._on_select = on_select
        self._cards: list[PlanCard] = []
        self._selected_plan: dict | None = None

        self._title = tk.Label(
            self,
            text="② Selecciona el Plan",
            bg=COLORS["bg"],
            fg=COLORS["accent"],
            font=(FONT_FAMILY, 13, "bold"),
        )
        self._title.pack(anchor="w", pady=(0, 8))

        self._placeholder = tk.Label(
            self,
            text="← Primero selecciona un operador",
            bg=COLORS["bg"],
            fg=COLORS["text_muted"],
            font=(FONT_FAMILY, 10, "italic"),
        )
        self._placeholder.pack(anchor="w")

        self._grid = tk.Frame(self, bg=COLORS["bg"])
        self._grid.pack(fill="x")

    def load_operator(self, operator_key: str):
        """Re-render plan cards for the given operator."""
        self._selected_plan = None
        for card in self._cards:
            card.destroy()
        self._cards.clear()
        self._placeholder.pack_forget()

        op = OPERATORS[operator_key]
        for col, plan in enumerate(op["plans"]):
            card = PlanCard(
                self._grid,
                plan=plan,
                operator_color=op["color"],
                on_select=self._plan_selected,
            )
            card.grid(row=0, column=col, padx=8, sticky="nsew")
            self._grid.columnconfigure(col, weight=1)
            self._cards.append(card)

    def _plan_selected(self, plan: dict):
        self._selected_plan = plan
        for card in self._cards:
            card.highlight(card._plan["id"] == plan["id"])
        self._on_select(plan)

    def get_selected(self) -> dict | None:
        return self._selected_plan

    def reset(self):
        for card in self._cards:
            card.destroy()
        self._cards.clear()
        self._selected_plan = None
        self._placeholder.pack(anchor="w")


# ---------------------------------------------------------------------------
# Customer form component
# ---------------------------------------------------------------------------

class CustomerForm(tk.Frame):
    """Input form for customer name, phone number, and e-mail."""

    def __init__(self, parent, on_submit, **kwargs):
        super().__init__(parent, bg=COLORS["bg"], **kwargs)
        self._on_submit = on_submit
        self._vars: dict[str, tk.StringVar] = {}
        self._error_label: tk.Label | None = None
        self._build()

    def _build(self):
        tk.Label(
            self,
            text="③ Datos del Cliente",
            bg=COLORS["bg"],
            fg=COLORS["accent"],
            font=(FONT_FAMILY, 13, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        fields = [
            ("nombre", "Nombre completo", False),
            ("telefono", "Número de teléfono (10 dígitos)", False),
            ("correo", "Correo electrónico (para factura digital)", False),
        ]

        for key, label, secret in fields:
            var = tk.StringVar()
            self._vars[key] = var

            lbl = tk.Label(
                self,
                text=label,
                bg=COLORS["bg"],
                fg=COLORS["text_muted"],
                font=(FONT_FAMILY, 9),
            )
            lbl.pack(anchor="w")

            entry = tk.Entry(
                self,
                textvariable=var,
                bg=COLORS["surface"],
                fg=COLORS["text"],
                insertbackground=COLORS["text"],
                relief="flat",
                font=(FONT_FAMILY, 11),
                show="*" if secret else "",
            )
            entry.pack(fill="x", ipady=6, pady=(2, 8))

        # Error message
        self._error_label = tk.Label(
            self,
            text="",
            bg=COLORS["bg"],
            fg=COLORS["danger"],
            font=(FONT_FAMILY, 9),
            wraplength=400,
            justify="left",
        )
        self._error_label.pack(anchor="w")

        # Submit button
        tk.Button(
            self,
            text="💳  Procesar Pago",
            bg=COLORS["accent_dark"],
            fg=COLORS["white"],
            activebackground=COLORS["accent"],
            activeforeground=COLORS["white"],
            font=(FONT_FAMILY, 12, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self._submit,
        ).pack(fill="x", pady=(4, 0))

    def _submit(self):
        self._error_label.config(text="")
        data = {k: v.get() for k, v in self._vars.items()}
        self._on_submit(data)

    def show_error(self, message: str):
        self._error_label.config(text=f"⚠  {message}")

    def clear_error(self):
        self._error_label.config(text="")

    def get_values(self) -> dict:
        return {k: v.get() for k, v in self._vars.items()}

    def reset(self):
        for var in self._vars.values():
            var.set("")
        self.clear_error()
