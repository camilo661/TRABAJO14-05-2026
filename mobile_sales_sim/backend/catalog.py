"""
catalog.py
Static catalog of mobile operators and their available plans.
All prices are in Colombian Pesos (COP).
"""

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

OPERATORS: dict[str, dict] = {
    "tigo": {
        "display_name": "Tigo",
        "color": "#00AEEF",
        "plans": [
            {
                "id": "tigo_1",
                "name": "Tigo Básico",
                "price": 2500,
                "minutes": 50,
                "data_mb": 500,
                "sms": 50,
                "validity_days": 30,
                "description": "Plan de entrada con minutos y datos esenciales",
                "tier": 1,
            },
            {
                "id": "tigo_2",
                "name": "Tigo Plus",
                "price": 4500,
                "minutes": 150,
                "data_mb": 2048,
                "sms": 100,
                "validity_days": 30,
                "description": "Más minutos y 2 GB para redes sociales",
                "tier": 2,
            },
            {
                "id": "tigo_3",
                "name": "Tigo Premium",
                "price": 11000,
                "minutes": 500,
                "data_mb": 8192,
                "sms": 300,
                "validity_days": 30,
                "description": "Plan ilimitado de alta velocidad para uso intensivo",
                "tier": 3,
            },
        ],
    },
    "claro": {
        "display_name": "Claro",
        "color": "#E8001C",
        "plans": [
            {
                "id": "claro_1",
                "name": "Claro Inicial",
                "price": 2000,
                "minutes": 30,
                "data_mb": 300,
                "sms": 30,
                "validity_days": 30,
                "description": "Plan económico para llamadas y navegación básica",
                "tier": 1,
            },
            {
                "id": "claro_2",
                "name": "Claro Intermedio",
                "price": 5000,
                "minutes": 200,
                "data_mb": 3072,
                "sms": 150,
                "validity_days": 30,
                "description": "3 GB y minutos para uso diario cómodo",
                "tier": 2,
            },
            {
                "id": "claro_3",
                "name": "Claro Max",
                "price": 12000,
                "minutes": 600,
                "data_mb": 10240,
                "sms": 500,
                "validity_days": 30,
                "description": "10 GB y 600 minutos para usuarios exigentes",
                "tier": 3,
            },
        ],
    },
    "movistar": {
        "display_name": "Movistar",
        "color": "#019DF4",
        "plans": [
            {
                "id": "movistar_1",
                "name": "Movistar Lite",
                "price": 3000,
                "minutes": 60,
                "data_mb": 750,
                "sms": 60,
                "validity_days": 30,
                "description": "Plan ligero con datos y minutos para comunicación diaria",
                "tier": 1,
            },
            {
                "id": "movistar_2",
                "name": "Movistar Smart",
                "price": 4000,
                "minutes": 120,
                "data_mb": 1536,
                "sms": 80,
                "validity_days": 30,
                "description": "1.5 GB con redes sociales incluidas",
                "tier": 2,
            },
            {
                "id": "movistar_3",
                "name": "Movistar Full",
                "price": 10000,
                "minutes": 400,
                "data_mb": 7168,
                "sms": 250,
                "validity_days": 30,
                "description": "7 GB y llamadas ilimitadas a Movistar",
                "tier": 3,
            },
        ],
    },
    "wom": {
        "display_name": "WOM",
        "color": "#8B00FF",
        "plans": [
            {
                "id": "wom_1",
                "name": "WOM Starter",
                "price": 2500,
                "minutes": 40,
                "data_mb": 600,
                "sms": 40,
                "validity_days": 30,
                "description": "Entrada al mundo WOM con datos y minutos básicos",
                "tier": 1,
            },
            {
                "id": "wom_2",
                "name": "WOM Connect",
                "price": 4500,
                "minutes": 180,
                "data_mb": 2560,
                "sms": 120,
                "validity_days": 30,
                "description": "2.5 GB y minutos extra para conectarte más",
                "tier": 2,
            },
            {
                "id": "wom_3",
                "name": "WOM Ultra",
                "price": 11500,
                "minutes": 450,
                "data_mb": 9216,
                "sms": 400,
                "validity_days": 30,
                "description": "9 GB de alta velocidad y minutos generosos",
                "tier": 3,
            },
        ],
    },
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_operator(operator_key: str) -> dict | None:
    """Return operator dict by key, or None if not found."""
    return OPERATORS.get(operator_key.lower())


def get_plan(operator_key: str, plan_id: str) -> dict | None:
    """Return a specific plan from an operator, or None if not found."""
    operator = get_operator(operator_key)
    if not operator:
        return None
    for plan in operator["plans"]:
        if plan["id"] == plan_id:
            return plan
    return None


def format_price(price: int) -> str:
    """Format an integer price in Colombian Pesos."""
    return f"${price:,}".replace(",", ".")


def format_data(mb: int) -> str:
    """Convert MB to a readable string (MB or GB)."""
    if mb >= 1024:
        gb = mb / 1024
        return f"{gb:.1f} GB"
    return f"{mb} MB"
