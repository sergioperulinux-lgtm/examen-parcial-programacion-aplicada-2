# StockPro — Sistema Web Flask (MVC + SQLite)

## ──────────────────────────────────────────────
## 1. ESTRUCTURA DEL PROYECTO
## ──────────────────────────────────────────────
```
flask_proyecto/
  ├── app.py                  ← Controlador principal (Flask)
  ├── database.db             ← Base de datos SQLite (auto-generada)
  ├── requirements.txt        ← Dependencias Python
  ├── README.md               ← Este archivo
  └── templates/
        ├── login.html        ← Vista: pantalla de acceso
        ├── principal.html    ← Vista: panel principal
        └── buscador.html     ← Vista: buscador de productos
```

## ──────────────────────────────────────────────
## 2. INSTALACIÓN Y EJECUCIÓN LOCAL
## ──────────────────────────────────────────────

### Paso 1 — Crear entorno virtual (recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Paso 2 — Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 3 — Ejecutar el servidor
```bash
python app.py
```

### Paso 4 — Abrir en el navegador
```
http://localhost:5000
```

## ──────────────────────────────────────────────
## 3. CREDENCIALES DE PRUEBA
## ──────────────────────────────────────────────
| Usuario   | Contraseña | Nombre completo            |
|-----------|------------|----------------------------|
| admin     | admin123   | Administrador del Sistema  |
| usuario1  | pass123    | Juan Pérez                 |

## ──────────────────────────────────────────────
## 4. CÓDIGOS DE PRODUCTOS DE PRUEBA
## ──────────────────────────────────────────────
| Código | Producto                        | Precio   |
|--------|---------------------------------|----------|
| P001   | Laptop HP Pavilion              | S/ 2899.90 |
| P002   | Mouse Inalámbrico Logitech      | S/ 49.90   |
| P003   | Teclado Mecánico Redragon       | S/ 159.90  |
| P004   | Monitor LG 24"                  | S/ 599.90  |
| P005   | Auriculares Sony WH-1000XM4     | S/ 799.90  |
| P006   | Webcam Logitech C920            | S/ 249.90  |
| P007   | Disco Duro Externo 1TB          | S/ 179.90  |
| P008   | Impresora HP LaserJet           | S/ 549.90  |

## ──────────────────────────────────────────────
## 5. RUTAS DISPONIBLES
## ──────────────────────────────────────────────
| Método    | Ruta                    | Descripción                          |
|-----------|-------------------------|--------------------------------------|
| GET       | /                       | Redirige al login                    |
| GET/POST  | /login                  | Formulario de acceso                 |
| GET       | /principal              | Panel principal (requiere sesión)    |
| GET       | /buscador               | Buscador de productos (requiere sesión)|
| POST      | /api/buscar_producto    | API JSON: busca producto por código  |
| GET       | /logout                 | Cierra sesión y redirige al login    |

## ──────────────────────────────────────────────
## 6. DESPLIEGUE EN RENDER (Backend)
## ──────────────────────────────────────────────

### Paso 1 — Subir el proyecto a GitHub
```bash
git init
git add .
git commit -m "first commit"
git remote add origin https://github.com/TU_USUARIO/flask-stockpro.git
git push -u origin main
```

### Paso 2 — Crear Web Service en Render
1. Ir a https://render.com → New → Web Service
2. Conectar el repositorio de GitHub
3. Configurar:
   - **Name:** flask-stockpro
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Agregar variable de entorno:
   - `SECRET_KEY` = (cualquier cadena aleatoria larga)
5. Click en **Create Web Service**

### Paso 3 — Modificar app.py para Render
```python
# Línea final del app.py — ya incluida:
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
```
Gunicorn usará `app:app` directamente. Asegúrate de llamar `init_db()` al importar:
Agrega esto justo antes del bloque `if __name__ == '__main__':`:
```python
init_db()   # se ejecuta al iniciar con gunicorn también
```

## ──────────────────────────────────────────────
## 7. DESPLIEGUE EN VERCEL (Frontend estático)
## ──────────────────────────────────────────────
> ⚠️ Vercel es para sitios estáticos. Flask (Python) no corre en Vercel de forma nativa.
> Para un deploy completo usa solo **Render** con Flask sirviendo los templates Jinja2.
> Si quisieras separar front/back, los templates deberían convertirse a HTML estático
> y apuntar al backend de Render mediante fetch().

### vercel.json (referencia si usas HTML estático)
```json
{
  "version": 2,
  "builds": [{ "src": "templates/**", "use": "@vercel/static" }],
  "env": {
    "BACKEND_URL": "https://tu-app.onrender.com"
  }
}
```

## ──────────────────────────────────────────────
## 8. DEPENDENCIAS (requirements.txt)
## ──────────────────────────────────────────────
```
flask==3.0.3
flask-cors==4.0.1
gunicorn==22.0.0
```
Instalar manualmente (sin entorno virtual):
```bash
pip install flask flask-cors gunicorn
```
