"""
processor.py
Business logic for processing recharge requests.
Handles validation, status simulation, and request creation.
"""

import random
import datetime
from backend.singleton import AppState
from backend.catalog import get_operator, get_plan

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------
STATUS_PENDING = "pendiente"
STATUS_DONE = "hecho"
STATUS_REJECTED = "rechazado"

# Simulated probability weights for each outcome
_STATUS_WEIGHTS = [STATUS_DONE, STATUS_DONE, STATUS_DONE, STATUS_PENDING, STATUS_REJECTED]


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class ValidationError(Exception):
    """Raised when input data fails validation."""
    pass


def _validate_phone(phone: str) -> str:
    """Validate and normalise a Colombian mobile phone number."""
    digits = phone.strip().replace(" ", "").replace("-", "")
    if not digits.isdigit():
        raise ValidationError("El número de teléfono solo debe contener dígitos.")
    if len(digits) not in (10, 12):
        raise ValidationError("El número de teléfono debe tener 10 dígitos (ej: 3001234567).")
    return digits


def _validate_email(email: str) -> str:
    """Basic e-mail validation."""
    email = email.strip()
    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValidationError("El correo electrónico no es válido.")
    return email


def _validate_name(name: str) -> str:
    """Ensure the name is not empty."""
    name = name.strip()
    if len(name) < 2:
        raise ValidationError("El nombre debe tener al menos 2 caracteres.")
    return name


# ---------------------------------------------------------------------------
# Request creation
# ---------------------------------------------------------------------------

def create_recharge_request(
    operator_key: str,
    plan_id: str,
    customer_name: str,
    phone_number: str,
    email: str,
) -> dict:
    """
    Validate inputs, simulate payment processing, persist the request,
    and return the resulting request record.

    Raises ValidationError if any field is invalid.
    """
    # --- Validate inputs ---
    name = _validate_name(customer_name)
    phone = _validate_phone(phone_number)
    mail = _validate_email(email)

    # --- Verify operator and plan exist ---
    operator = get_operator(operator_key)
    if not operator:
        raise ValidationError(f"Operador '{operator_key}' no encontrado.")

    plan = get_plan(operator_key, plan_id)
    if not plan:
        raise ValidationError(f"Plan '{plan_id}' no encontrado para {operator['display_name']}.")

    # --- Build request record ---
    state = AppState()
    request_id = state.get_next_id()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Simulate payment gateway result
    simulated_status = random.choice(_STATUS_WEIGHTS)

    request = {
        "id": request_id,
        "timestamp": timestamp,
        "operator_key": operator_key,
        "operator_name": operator["display_name"],
        "plan_id": plan_id,
        "plan_name": plan["name"],
        "plan_price": plan["price"],
        "plan_minutes": plan["minutes"],
        "plan_data_mb": plan["data_mb"],
        "customer_name": name,
        "phone_number": phone,
        "email": mail,
        "status": simulated_status,
    }

    state.add_request(request)
    return request


# ---------------------------------------------------------------------------
# History retrieval
# ---------------------------------------------------------------------------

def get_all_requests() -> list:
    """Return the full request history ordered by ID (ascending)."""
    state = AppState()
    return sorted(state.get_history(), key=lambda r: r["id"])


def get_request_by_id(request_id: int) -> dict | None:
    """Find a single request by its ID."""
    for req in AppState().get_history():
        if req["id"] == request_id:
            return req
    return None
