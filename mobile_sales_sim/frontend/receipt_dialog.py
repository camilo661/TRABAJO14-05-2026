"""
receipt_dialog.py
Modal dialog that displays the payment confirmation receipt.
"""

import tkinter as tk
from frontend.components import COLORS, FONT_FAMILY
from backend.catalog import format_price, format_data

STATUS_COLORS = {
    "hecho": COLORS["success"],
    "pendiente": COLORS["warning"],
    "rechazado": COLORS["danger"],
}

STATUS_MESSAGES = {
    "hecho": "¡Pago exitoso! La recarga fue procesada correctamente.",
    "pendiente": "Tu solicitud está siendo procesada. Recibirás confirmación pronto.",
    "rechazado": "El pago fue rechazado. Verifica los datos o intenta con otro método.",
}


class ReceiptDialog(tk.Toplevel):
    """
    Modal window showing the result of a recharge request.
    """

    def __init__(self, parent, request: dict):
        super().__init__(parent)
        self.title("Comprobante de Solicitud")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg"])
        self.grab_set()  # Make modal

        self._request = request
        self._build()
        self._center(parent)

    def _build(self):
        status = self._request["status"]
        color = STATUS_COLORS.get(status, COLORS["text"])

        # ---- Header ----
        header = tk.Frame(self, bg=color, padx=20, pady=16)
        header.pack(fill="x")

        icons = {"hecho": "✅", "pendiente": "⏳", "rechazado": "❌"}
        tk.Label(
            header,
            text=f"{icons.get(status, '')}  Estado: {status.upper()}",
            bg=color,
            fg=COLORS["white"],
            font=(FONT_FAMILY, 14, "bold"),
        ).pack()

        tk.Label(
            header,
            text=STATUS_MESSAGES.get(status, ""),
            bg=color,
            fg=COLORS["white"],
            font=(FONT_FAMILY, 9),
        ).pack(pady=(4, 0))

        # ---- Body ----
        body = tk.Frame(self, bg=COLORS["surface"], padx=24, pady=16)
        body.pack(fill="both", padx=16, pady=16)

        rows = [
            ("Nº Solicitud", f"#{self._request['id']:03d}"),
            ("Fecha / Hora", self._request["timestamp"]),
            ("Operador", self._request["operator_name"]),
            ("Plan", self._request["plan_name"]),
            ("Minutos", f"{self._request['plan_minutes']} min"),
            ("Datos", format_data(self._request["plan_data_mb"])),
            ("Precio", format_price(self._request["plan_price"])),
            ("Cliente", self._request["customer_name"]),
            ("Teléfono", self._request["phone_number"]),
            ("Correo", self._request["email"]),
        ]

        for label, value in rows:
            row_frame = tk.Frame(body, bg=COLORS["surface"])
            row_frame.pack(fill="x", pady=2)

            tk.Label(
                row_frame,
                text=f"{label}:",
                bg=COLORS["surface"],
                fg=COLORS["text_muted"],
                font=(FONT_FAMILY, 9),
                width=14,
                anchor="w",
            ).pack(side="left")

            tk.Label(
                row_frame,
                text=value,
                bg=COLORS["surface"],
                fg=COLORS["text"],
                font=(FONT_FAMILY, 9, "bold"),
                anchor="w",
            ).pack(side="left")

        # ---- Footer ----
        tk.Label(
            self,
            text="Una factura digital será enviada al correo registrado.",
            bg=COLORS["bg"],
            fg=COLORS["text_muted"],
            font=(FONT_FAMILY, 8, "italic"),
        ).pack(pady=(0, 4))

        tk.Button(
            self,
            text="Cerrar",
            bg=COLORS["surface2"],
            fg=COLORS["text"],
            activebackground=COLORS["border"],
            font=(FONT_FAMILY, 10, "bold"),
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.destroy,
        ).pack(pady=(0, 16))

    def _center(self, parent):
        self.update_idletasks()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_x()
        py = parent.winfo_y()
        w = self.winfo_width()
        h = self.winfo_height()
        x = px + (pw - w) // 2
        y = py + (ph - h) // 2
        self.geometry(f"+{x}+{y}")
