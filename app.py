from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
app.secret_key = 'miclavesecreta123'
CORS(app)

DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        nombre TEXT NOT NULL
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE NOT NULL,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL,
        categoria TEXT
    )''')

    cur.execute("SELECT id FROM usuarios WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO usuarios (username,password,nombre) VALUES (?,?,?)",
                    ('admin','admin123','Administrador'))
        cur.execute("INSERT INTO usuarios (username,password,nombre) VALUES (?,?,?)",
                    ('usuario1','pass123','Juan Perez'))

    productos = [
        ('P001','Laptop HP','Laptop Intel Core i5 8GB RAM 512GB SSD',2899.90,15,'Computadoras'),
        ('P002','Mouse Logitech','Mouse inalambrico USB 3 botones',49.90,80,'Perifericos'),
        ('P003','Teclado Redragon','Teclado mecanico RGB switches Blue',159.90,45,'Perifericos'),
        ('P004','Monitor LG 24','Monitor Full HD 1080p 75Hz HDMI',599.90,20,'Monitores'),
        ('P005','Auriculares Sony','Auriculares Bluetooth noise cancelling',799.90,12,'Audio'),
        ('P006','Webcam Logitech','Camara web Full HD microfono integrado',249.90,35,'Perifericos'),
        ('P007','Disco Duro 1TB','Disco externo Seagate USB 3.0',179.90,50,'Almacenamiento'),
        ('P008','Impresora HP','Impresora laser WiFi 23ppm',549.90,8,'Impresoras'),
    ]
    for p in productos:
        cur.execute("SELECT id FROM productos WHERE codigo=?", (p[0],))
        if not cur.fetchone():
            cur.execute("INSERT INTO productos (codigo,nombre,descripcion,precio,stock,categoria) VALUES (?,?,?,?,?,?)", p)

    conn.commit()
    conn.close()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, password))
        usuario = cur.fetchone()
        conn.close()
        if usuario:
            session['id'] = usuario['id']
            session['nombre'] = usuario['nombre']
            return redirect(url_for('principal'))
        else:
            error = 'Usuario o contrasena incorrectos'
    return render_template('login.html', error=error)

@app.route('/principal')
def principal():
    if 'id' not in session:
        return redirect(url_for('login'))
    return render_template('principal.html', nombre=session['nombre'])

@app.route('/buscador')
def buscador():
    if 'id' not in session:
        return redirect(url_for('login'))
    return render_template('buscador.html')

@app.route('/api/buscar_producto', methods=['POST'])
def buscar_producto():
    if 'id' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    data = request.get_json()
    codigo = data.get('codigo', '').strip().upper()
    if not codigo:
        return jsonify({'error': 'Ingresa un codigo'}), 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos WHERE codigo=?", (codigo,))
    p = cur.fetchone()
    conn.close()
    if p:
        return jsonify({
            'encontrado': True,
            'codigo': p['codigo'],
            'nombre': p['nombre'],
            'descripcion': p['descripcion'],
            'precio': p['precio'],
            'stock': p['stock'],
            'categoria': p['categoria']
        })
    else:
        return jsonify({'encontrado': False, 'mensaje': 'Producto no encontrado'}), 404

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

init_db()

if __name__ == '__main__':
    print("Servidor iniciado en http://localhost:5000")
    app.run(debug=True)
