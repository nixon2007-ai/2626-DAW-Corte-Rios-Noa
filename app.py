from flask import Flask, render_template, redirect, url_for, abort, request
from flask_wtf.csrf import CSRFProtect

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

import sqlite3
import os

# Ruta absoluta a la base de datos, para que funcione sin importar desde dónde se ejecute
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'gastrobar.db')


def get_conexion():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acceder a columnas por nombre
    return conn


def crear_tabla_productos():
    conn = get_conexion()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            estado TEXT NOT NULL,
            descripcion TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

app = Flask(__name__)

# Clave secreta necesaria para el funcionamiento de Flask-WTF y la
# protección CSRF de los formularios.
app.config['SECRET_KEY'] = 'mar-y-selva-gastrobar-clave-secreta-2026'

# Habilita la función csrf_token() en las plantillas, usada por los
# formularios de eliminar (botones que no usan una clase FlaskForm completa).
csrf = CSRFProtect(app)


# ---------------------------------------------------------------------------
# "Bases de datos" temporales en memoria (listas de Python).
# El módulo de productos ya usa SQLite (ver funciones get_conexion /
# crear_tabla_productos). Los demás módulos se migrarán progresivamente.
# ---------------------------------------------------------------------------

lista_clientes = [
    {"nombre": "María Fernanda López", "correo": "mflopez@gmail.com",
     "telefono": "0991234567", "tipo": "Frecuente", "mesa_preferida": "Terraza", "reservas": 5},
    {"nombre": "Carlos Andrés Ramírez", "correo": "caramirez@gmail.com",
     "telefono": "0987654321", "tipo": "Nuevo", "mesa_preferida": "Salón Interior", "reservas": 1},
    {"nombre": "Daniela Castillo Pinta", "correo": "dcastillo@gmail.com",
     "telefono": "0965432198", "tipo": "Frecuente", "mesa_preferida": "Barra", "reservas": 8},
    {"nombre": "Jorge Luis Vera", "correo": "jlvera@gmail.com",
     "telefono": "0978965412", "tipo": "Nuevo", "mesa_preferida": "Terraza", "reservas": 2},
]

lista_proveedores = [
    {"empresa": "Pesquera del Pacífico S.A.", "insumo": "Mariscos y pescado fresco",
     "categoria": "Mar", "contacto": "0998765432", "frecuencia": "Semanal"},
    {"empresa": "AmazonFrut Cía. Ltda.", "insumo": "Frutas amazónicas (arazá, chontaduro, guayusa)",
     "categoria": "Amazonía", "contacto": "0987651234", "frecuencia": "Quincenal"},
    {"empresa": "Licores del Litoral", "insumo": "Aguardiente, ron y licores",
     "categoria": "Bebidas", "contacto": "0965478123", "frecuencia": "Mensual"},
    {"empresa": "Distribuidora El Oro", "insumo": "Abarrotes y bebidas gaseosas",
     "categoria": "Abarrotes", "contacto": "0976543210", "frecuencia": "Semanal"},
]

lista_facturas = [
    {"numero": "001-001-000000123", "cliente": "María Fernanda López", "mesa": 4,
     "productos": ["Selvático de Paiche y Camarón", "Cóctel Brisa del Oriente"],
     "subtotal": 17.50, "iva": 2.10, "total": 19.60,
     "metodo_pago": "Efectivo", "estado": "Pagada", "fecha": "10/08/2026"},
    {"numero": "001-001-000000124", "cliente": "Carlos Andrés Ramírez", "mesa": 2,
     "productos": ["Bolón de Yuca Relleno de Maito de Pescado"],
     "subtotal": 6.00, "iva": 0.72, "total": 6.72,
     "metodo_pago": "Tarjeta", "estado": "Pagada", "fecha": "11/08/2026"},
    {"numero": "001-001-000000125", "cliente": "Daniela Castillo Pinta", "mesa": 7,
     "productos": ["Verde con Cecina Ahumada y Langostinos", "Arroz Meloso del Manglar con Guayusa y Mariscos"],
     "subtotal": 25.00, "iva": 3.00, "total": 28.00,
     "metodo_pago": "Transferencia", "estado": "Pendiente", "fecha": "12/08/2026"},
]


# RUTA PRINCIPAL
@app.route('/')
def index():
    return render_template('index.html')


# INICIO DE SESION (acceso al sistema interno)
@app.route('/login')
def login():
    return render_template('login.html')


# PANEL DEL SISTEMA (rutas internas: Clientes, Facturación, Productos, Proveedores)
@app.route('/panel')
def panel():
    return render_template('panel.html')


# ---------------------------------------------------------------------------
# MODULO PRODUCTOS (Menú del gastrobar) - Persistencia con SQLite
# ---------------------------------------------------------------------------

@app.route('/productos')
def productos():
    conn = get_conexion()
    filas = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()

    categorias = sorted(set(fila['categoria'] for fila in filas))
    return render_template('productos.html', productos=filas, categorias=categorias)


@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = get_conexion()
        conn.execute(
            'INSERT INTO productos (nombre, categoria, precio, estado, descripcion) VALUES (?, ?, ?, ?, ?)',
            (form.nombre.data, form.categoria.data, form.precio.data, form.estado.data, form.descripcion.data)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('productos'))
    return render_template('formulario_productos.html', form=form, modo='nuevo')


@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    conn = get_conexion()
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    conn.close()

    if producto is None:
        abort(404)

    if request.method == 'GET':
        form = ProductoForm(data=dict(producto))
    else:
        form = ProductoForm()

    if form.validate_on_submit():
        conn = get_conexion()
        conn.execute(
            'UPDATE productos SET nombre = ?, categoria = ?, precio = ?, estado = ?, descripcion = ? WHERE id = ?',
            (form.nombre.data, form.categoria.data, form.precio.data, form.estado.data, form.descripcion.data, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('productos'))

    return render_template('formulario_productos.html', form=form, modo='editar', id=id)


@app.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    conn = get_conexion()
    conn.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('productos'))


# ---------------------------------------------------------------------------
# MODULO CLIENTES (Reservas y comensales)
# ---------------------------------------------------------------------------

@app.route('/clientes')
def clientes():
    return render_template('clientes.html', clientes=lista_clientes)


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        lista_clientes.append({
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "telefono": form.telefono.data,
            "tipo": form.tipo.data,
            "mesa_preferida": form.mesa_preferida.data,
            "reservas": form.reservas.data,
        })
        return redirect(url_for('clientes'))
    return render_template('formulario_cliente.html', form=form)


# ---------------------------------------------------------------------------
# MODULO PROVEEDORES (Insumos del gastrobar)
# ---------------------------------------------------------------------------

@app.route('/proveedores')
def proveedores():
    return render_template('proveedores.html', proveedores=lista_proveedores)


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        lista_proveedores.append({
            "empresa": form.empresa.data,
            "insumo": form.insumo.data,
            "categoria": form.categoria.data,
            "contacto": form.contacto.data,
            "frecuencia": form.frecuencia.data,
        })
        return redirect(url_for('proveedores'))
    return render_template('formulario_proveedor.html', form=form)


# ---------------------------------------------------------------------------
# MODULO FACTURACION (Cuenta por mesa)
# ---------------------------------------------------------------------------

@app.route('/facturacion')
def facturacion():
    return render_template('facturacion.html', facturas=lista_facturas)


@app.route('/facturacion/nueva', methods=['GET', 'POST'])
def nueva_facturacion():
    form = FacturacionForm()
    if form.validate_on_submit():
        subtotal = form.subtotal.data
        iva = round(subtotal * 0.12, 2)
        total = round(subtotal + iva, 2)
        productos_lista = [p.strip() for p in form.productos.data.split(',') if p.strip()]
        lista_facturas.append({
            "numero": form.numero.data,
            "cliente": form.cliente.data,
            "mesa": form.mesa.data,
            "productos": productos_lista,
            "subtotal": subtotal,
            "iva": iva,
            "total": total,
            "metodo_pago": form.metodo_pago.data,
            "estado": form.estado.data,
            "fecha": form.fecha.data,
        })
        return redirect(url_for('facturacion'))
    return render_template('formulario_facturacion.html', form=form)


crear_tabla_productos()

if __name__ == '__main__':
    app.run(debug=True)