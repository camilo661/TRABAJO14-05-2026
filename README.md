# 📱 Simulador de Ventas de Planes Móviles

Sistema de simulación de ventas para recargas de planes móviles en Colombia.
Desarrollado en Python puro con Tkinter.

---

## 🗂 Estructura del Proyecto

```
mobile_sales_sim/
├── main.py                    ← Punto de entrada
├── README.md
├── backend/
│   ├── __init__.py
│   ├── singleton.py           ← Patrón Singleton (AppState)
│   ├── catalog.py             ← Catálogo de operadores y planes
│   └── processor.py           ← Lógica de negocio y procesamiento
└── frontend/
    ├── __init__.py
    ├── app_window.py          ← Ventana principal
    ├── components.py          ← Componentes reutilizables (selector, form)
    ├── history_panel.py       ← Panel de historial
    └── receipt_dialog.py      ← Diálogo de comprobante
```

---

## 🚀 Cómo ejecutar

### Requisitos
- Python 3.10 o superior
- Tkinter (incluido por defecto en Python estándar)

### Ejecución
```bash
# Desde la carpeta raíz del proyecto
python main.py
```

> **Nota:** Tkinter viene incluido en la instalación estándar de Python en
> Windows y macOS. En Linux (Ubuntu/Debian) puede instalarse con:
> ```bash
> sudo apt-get install python3-tk
> ```

---

## 📦 Operadores y Planes

| Operador  | Plan 1 (Básico)     | Plan 2 (Estándar)    | Plan 3 (Premium)    |
|-----------|---------------------|----------------------|---------------------|
| **Tigo**  | $2.500 · 50min · 500MB  | $4.500 · 150min · 2GB  | $11.000 · 500min · 8GB  |
| **Claro** | $2.000 · 30min · 300MB  | $5.000 · 200min · 3GB  | $12.000 · 600min · 10GB |
| **Movistar** | $3.000 · 60min · 750MB | $4.000 · 120min · 1.5GB | $10.000 · 400min · 7GB |
| **WOM**   | $2.500 · 40min · 600MB  | $4.500 · 180min · 2.5GB | $11.500 · 450min · 9GB |

---

## 🔄 Flujo del Sistema

1. **Seleccionar Operador** → Tigo, Claro, Movistar o WOM
2. **Seleccionar Plan** → Se muestran 3 planes con precios, minutos y megas
3. **Ingresar Datos** → Nombre, teléfono y correo electrónico
4. **Procesar Pago** → El sistema simula el procesamiento
5. **Comprobante** → Diálogo con estado: ✅ Hecho / ⏳ Pendiente / ❌ Rechazado
6. **Historial** → Todas las solicitudes numeradas consecutivamente

---

## 🏗 Arquitectura

### Patrón Singleton (`backend/singleton.py`)
`AppState` usa metaclase `SingletonMeta` para garantizar una única instancia
en toda la aplicación. Gestiona el historial y el contador de IDs.

### Backend (`backend/`)
- **catalog.py** → Datos estáticos de operadores/planes
- **processor.py** → Validación, creación de solicitudes y lógica de negocio

### Frontend (`frontend/`)
- Separado del backend; sólo importa lo que necesita del backend
- Componentes reutilizables e independientes

---

## ℹ️ Notas
- Los estados se generan de forma aleatoria para simular una pasarela de pago
- Los IDs son consecutivos y no se reinician durante la sesión
- El correo se usa únicamente para la factura digital (simulada)
