"""
history_panel.py
Tkinter component that displays the recharge request history as a table.
"""

import tkinter as tk
from tkinter import ttk
from frontend.components import COLORS, FONT_FAMILY


# ---------------------------------------------------------------------------
# Status badge colors
# ---------------------------------------------------------------------------
STATUS_COLORS = {
    "hecho": COLORS["success"],
    "pendiente": COLORS["warning"],
    "rechazado": COLORS["danger"],
}

STATUS_ICONS = {
    "hecho": "✅",
    "pendiente": "⏳",
    "rechazado": "❌",
}


# ---------------------------------------------------------------------------
# History Panel
# ---------------------------------------------------------------------------

class HistoryPanel(tk.Frame):
    """
    Scrollable table that lists all recharge requests with their statuses.
    """

    COLUMNS = ("ID", "Fecha/Hora", "Operador", "Plan", "Precio", "Cliente", "Teléfono", "Estado")
    COL_WIDTHS = (45, 140, 80, 130, 80, 160, 110, 90)

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS["bg"], **kwargs)
        self._build()

    def _build(self):
        header = tk.Frame(self, bg=COLORS["bg"])
        header.pack(fill="x", pady=(0, 6))

        tk.Label(
            header,
            text="📋  Historial de Solicitudes",
            bg=COLORS["bg"],
            fg=COLORS["accent"],
            font=(FONT_FAMILY, 13, "bold"),
        ).pack(side="left")

        self._count_label = tk.Label(
            header,
            text="0 solicitudes",
            bg=COLORS["bg"],
            fg=COLORS["text_muted"],
            font=(FONT_FAMILY, 9),
        )
        self._count_label.pack(side="right")

        # --- Treeview style ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "History.Treeview",
            background=COLORS["surface"],
            foreground=COLORS["text"],
            rowheight=28,
            fieldbackground=COLORS["surface"],
            borderwidth=0,
            font=(FONT_FAMILY, 9),
        )
        style.configure(
            "History.Treeview.Heading",
            background=COLORS["surface2"],
            foreground=COLORS["accent"],
            font=(FONT_FAMILY, 9, "bold"),
            borderwidth=0,
            relief="flat",
        )
        style.map("History.Treeview", background=[("selected", COLORS["surface2"])])

        # --- Scrollbars ---
        container = tk.Frame(self, bg=COLORS["bg"])
        container.pack(fill="both", expand=True)

        v_scroll = ttk.Scrollbar(container, orient="vertical")
        v_scroll.pack(side="right", fill="y")

        h_scroll = ttk.Scrollbar(container, orient="horizontal")
        h_scroll.pack(side="bottom", fill="x")

        self._tree = ttk.Treeview(
            container,
            columns=self.COLUMNS,
            show="headings",
            style="History.Treeview",
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set,
            selectmode="browse",
        )

        for col, width in zip(self.COLUMNS, self.COL_WIDTHS):
            self._tree.heading(col, text=col)
            self._tree.column(col, width=width, minwidth=width, anchor="center")

        v_scroll.config(command=self._tree.yview)
        h_scroll.config(command=self._tree.xview)

        self._tree.pack(fill="both", expand=True)

        # Row tags for status colour
        self._tree.tag_configure("hecho", foreground=COLORS["success"])
        self._tree.tag_configure("pendiente", foreground=COLORS["warning"])
        self._tree.tag_configure("rechazado", foreground=COLORS["danger"])
        self._tree.tag_configure("even", background=COLORS["surface"])
        self._tree.tag_configure("odd", background="#253044")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def refresh(self, requests: list):
        """Clear and repopulate the table from the provided request list."""
        for item in self._tree.get_children():
            self._tree.delete(item)

        for idx, req in enumerate(requests):
            status = req["status"]
            icon = STATUS_ICONS.get(status, "")
            row_tag = "even" if idx % 2 == 0 else "odd"

            self._tree.insert(
                "",
                "end",
                values=(
                    f"#{req['id']:03d}",
                    req["timestamp"],
                    req["operator_name"],
                    req["plan_name"],
                    f"${req['plan_price']:,}".replace(",", "."),
                    req["customer_name"],
                    req["phone_number"],
                    f"{icon} {status.capitalize()}",
                ),
                tags=(status, row_tag),
            )

        count = len(requests)
        self._count_label.config(text=f"{count} solicitud{'es' if count != 1 else ''}")

    def add_row(self, req: dict):
        """Append a single new row without full refresh."""
        status = req["status"]
        icon = STATUS_ICONS.get(status, "")
        idx = len(self._tree.get_children())
        row_tag = "even" if idx % 2 == 0 else "odd"

        self._tree.insert(
            "",
            "end",
            values=(
                f"#{req['id']:03d}",
                req["timestamp"],
                req["operator_name"],
                req["plan_name"],
                f"${req['plan_price']:,}".replace(",", "."),
                req["customer_name"],
                req["phone_number"],
                f"{icon} {status.capitalize()}",
            ),
            tags=(status, row_tag),
        )

        # Scroll to the new entry
        children = self._tree.get_children()
        if children:
            self._tree.see(children[-1])

        count = len(children)
        self._count_label.config(text=f"{count} solicitud{'es' if count != 1 else ''}")
