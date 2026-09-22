from flask import Flask, render_template, redirect, url_for, abort, request
from flask_wtf.csrf import CSRFProtect

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from conexion.conexion import get_conexion
from flask import flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import obtener_usuario_por_id, obtener_usuario_por_nombre
from forms.login_form import LoginForm
from forms.usuario_form import RegistroForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mar-y-selva-gastrobar-clave-secreta-2026'
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return obtener_usuario_por_id(user_id)


# ---------------------------------------------------------------------------
# "Bases de datos" temporales en memoria (listas de Python).
# Clientes, Proveedores y Facturación se migrarán progresivamente.
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


def obtener_choices_proveedores():
    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, empresa FROM proveedores')
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    return [(f['id'], f['empresa']) for f in filas]


# RUTA PRINCIPAL
@app.route('/')
def index():
    return render_template('index.html')


# INICIO DE SESION
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        if obtener_usuario_por_nombre(form.usuario.data):
            flash('Ese nombre de usuario ya existe, elige otro.', 'danger')
        else:
            password_hash = generate_password_hash(form.password.data)
            conn = get_conexion()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO usuarios (usuario, password) VALUES (%s, %s)',
                (form.usuario.data, password_hash)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash('Usuario registrado correctamente. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
    return render_template('registro.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = obtener_usuario_por_nombre(form.usuario.data)
        if usuario and check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            return redirect(url_for('panel'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('login'))


# PANEL DEL SISTEMA
@app.route('/panel')
@login_required
def panel():
    return render_template('panel.html')

# ---------------------------------------------------------------------------
# MODULO PRODUCTOS (Menú del gastrobar) - Persistencia con MySQL
# ---------------------------------------------------------------------------

@app.route('/productos')
@login_required
def productos():
    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT p.*, pr.empresa AS proveedor_nombre
        FROM productos p
        LEFT JOIN proveedores pr ON p.proveedor_id = pr.id
    ''')
    filas = cursor.fetchall()
    cursor.close()
    conn.close()

    categorias = sorted(set(fila['categoria'] for fila in filas))
    return render_template('productos.html', productos=filas, categorias=categorias)


@app.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    form = ProductoForm()
    form.proveedor_id.choices = obtener_choices_proveedores()
    if form.validate_on_submit():
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO productos (nombre, categoria, precio, estado, descripcion, proveedor_id) '
            'VALUES (%s, %s, %s, %s, %s, %s)',
            (form.nombre.data, form.categoria.data, form.precio.data,
             form.estado.data, form.descripcion.data, form.proveedor_id.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('productos'))
    return render_template('formulario_productos.html', form=form, modo='nuevo')


@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    conn = get_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM productos WHERE id = %s', (id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()

    if producto is None:
        abort(404)

    form = ProductoForm(data=producto) if request.method == 'GET' else ProductoForm()
    form.proveedor_id.choices = obtener_choices_proveedores()

    if form.validate_on_submit():
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE productos SET nombre=%s, categoria=%s, precio=%s, estado=%s, '
            'descripcion=%s, proveedor_id=%s WHERE id=%s',
            (form.nombre.data, form.categoria.data, form.precio.data, form.estado.data,
             form.descripcion.data, form.proveedor_id.data, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('productos'))

    return render_template('formulario_productos.html', form=form, modo='editar', id=id)


@app.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('productos'))


# ---------------------------------------------------------------------------
# MODULO CLIENTES (Reservas y comensales)
# ---------------------------------------------------------------------------

@app.route('/clientes')
@login_required
def clientes():
    return render_template('clientes.html', clientes=lista_clientes)


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
@login_required
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
@login_required
def proveedores():
    return render_template('proveedores.html', proveedores=lista_proveedores)


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
@login_required
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
@login_required
def facturacion():
    return render_template('facturacion.html', facturas=lista_facturas)


@app.route('/facturacion/nueva', methods=['GET', 'POST'])
@login_required
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


if __name__ == '__main__':
    app.run(debug=True)