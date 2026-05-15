"""
history_manager.py
Extended history operations: filtering, cancellation, and CSV/Excel export.
All functions operate on AppState — no modifications to existing modules.
"""

import csv
import io
import datetime
from backend.singleton import AppState
from backend.processor import STATUS_PENDING, STATUS_DONE, STATUS_REJECTED

STATUS_CANCELLED = "cancelado"


def filter_requests(
    status: str | None = None,
    operator: str | None = None,
    date_from: str | None = None,  # "YYYY-MM-DD"
    date_to: str | None = None,
    search: str | None = None,     # partial name or phone
) -> list[dict]:
    """Return requests matching all provided filters."""
    results = AppState().get_history()

    if status and status != "todos":
        results = [r for r in results if r["status"] == status]

    if operator and operator != "todos":
        results = [r for r in results if r["operator_key"] == operator]

    if date_from:
        results = [r for r in results if r["timestamp"][:10] >= date_from]

    if date_to:
        results = [r for r in results if r["timestamp"][:10] <= date_to]

    if search:
        q = search.lower()
        results = [
            r for r in results
            if q in r["customer_name"].lower() or q in r["phone_number"]
        ]

    return sorted(results, key=lambda r: r["id"])


def cancel_request(request_id: int) -> bool:
    """
    Cancel a PENDING request.
    Returns True if cancelled, False if not found or already processed.
    """
    state = AppState()
    for req in state.get_history():
        if req["id"] == request_id and req["status"] == STATUS_PENDING:
            return state.update_status(request_id, STATUS_CANCELLED)
    return False


def export_to_csv(requests: list[dict]) -> str:
    """Return a CSV string for the given requests list."""
    output = io.StringIO()
    fieldnames = [
        "id", "timestamp", "operator_name", "plan_name",
        "plan_price", "plan_minutes", "plan_data_mb",
        "customer_name", "phone_number", "email", "status",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for req in requests:
        writer.writerow(req)
    return output.getvalue()


def export_to_excel_bytes(requests: list[dict]) -> bytes:
    """
    Return xlsx bytes for the given requests list.
    Uses openpyxl (stdlib-independent, always available with Tkinter installs).
    """
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment
    except ImportError:
        raise RuntimeError("openpyxl no está instalado. Instala con: pip install openpyxl")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Historial"

    headers = [
        "ID", "Fecha/Hora", "Operador", "Plan", "Precio (COP)",
        "Minutos", "Datos (MB)", "Cliente", "Teléfono", "Correo", "Estado",
    ]
    keys = [
        "id", "timestamp", "operator_name", "plan_name", "plan_price",
        "plan_minutes", "plan_data_mb", "customer_name", "phone_number", "email", "status",
    ]

    header_fill = PatternFill("solid", fgColor="334155")
    header_font = Font(bold=True, color="38BDF8")

    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    status_colors = {
        "hecho": "4ADE80",
        "pendiente": "FACC15",
        "rechazado": "F87171",
        "cancelado": "94A3B8",
    }

    for row_idx, req in enumerate(requests, 2):
        for col, key in enumerate(keys, 1):
            ws.cell(row=row_idx, column=col, value=req.get(key, ""))

        status = req.get("status", "")
        color = status_colors.get(status, "FFFFFF")
        ws.cell(row=row_idx, column=len(keys)).fill = PatternFill("solid", fgColor=color)

    # Auto-width
    for col_cells in ws.columns:
        max_len = max((len(str(c.value or "")) for c in col_cells), default=10)
        ws.column_dimensions[col_cells[0].column_letter].width = min(max_len + 4, 40)

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()
