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
# Utilidades para poblar los <select> de los formularios con datos reales
# de la base de datos (relaciones por clave foránea).
# ---------------------------------------------------------------------------

def obtener_choices_proveedores():
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT id, empresa FROM proveedores ORDER BY empresa')
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    return [(f['id'], f['empresa']) for f in filas]


def obtener_choices_clientes():
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre FROM clientes ORDER BY nombre')
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    return [(f['id'], f['nombre']) for f in filas]


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
# MODULO PRODUCTOS (Menú del gastrobar) - Persistencia con PostgreSQL
# ---------------------------------------------------------------------------

@app.route('/productos')
@login_required
def productos():
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, pr.empresa AS proveedor_nombre
        FROM productos p
        LEFT JOIN proveedores pr ON p.proveedor_id = pr.id
        ORDER BY p.categoria, p.nombre
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
        flash('Producto registrado correctamente.', 'success')
        return redirect(url_for('productos'))
    return render_template('formulario_productos.html', form=form, modo='nuevo')


@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    conn = get_conexion()
    cursor = conn.cursor()
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
        flash('Producto actualizado correctamente.', 'success')
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
    flash('Producto eliminado.', 'info')
    return redirect(url_for('productos'))


# ---------------------------------------------------------------------------
# MODULO CLIENTES (Reservas y comensales) - Persistencia con PostgreSQL
# ---------------------------------------------------------------------------

@app.route('/clientes')
@login_required
def clientes():
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes ORDER BY nombre')
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', clientes=filas)


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO clientes (nombre, correo, telefono, tipo, mesa_preferida, reservas) '
            'VALUES (%s, %s, %s, %s, %s, %s)',
            (form.nombre.data, form.correo.data, form.telefono.data,
             form.tipo.data, form.mesa_preferida.data, form.reservas.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Cliente registrado correctamente.', 'success')
        return redirect(url_for('clientes'))
    return render_template('formulario_cliente.html', form=form, modo='nuevo')


@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes WHERE id = %s', (id,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()

    if cliente is None:
        abort(404)

    form = ClienteForm(data=cliente) if request.method == 'GET' else ClienteForm()

    if form.validate_on_submit():
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE clientes SET nombre=%s, correo=%s, telefono=%s, tipo=%s, '
            'mesa_preferida=%s, reservas=%s WHERE id=%s',
            (form.nombre.data, form.correo.data, form.telefono.data, form.tipo.data,
             form.mesa_preferida.data, form.reservas.data, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Cliente actualizado correctamente.', 'success')
        return redirect(url_for('clientes'))

    return render_template('formulario_cliente.html', form=form, modo='editar', id=id)


@app.route('/clientes/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_cliente(id):
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Cliente eliminado.', 'info')
    return redirect(url_for('clientes'))


# ---------------------------------------------------------------------------
# MODULO PROVEEDORES (Insumos del gastrobar) - Persistencia con PostgreSQL
# ---------------------------------------------------------------------------

@app.route('/proveedores')
@login_required
def proveedores():
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM proveedores ORDER BY empresa')
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('proveedores.html', proveedores=filas)


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_proveedor():
    form = ProveedorForm()
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT 1')
    cursor.close()
    conn.close()
    if form.validate_on_submit():
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO proveedores (empresa, insumo, categoria, contacto, frecuencia) '
            'VALUES (%s, %s, %s, %s, %s)',
            (form.empresa.data, form.insumo.data, form.categoria.data,
             form.contacto.data, form.frecuencia.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Proveedor registrado correctamente.', 'success')
        return redirect(url_for('proveedores'))
    return render_template('formulario_proveedor.html', form=form, modo='nuevo')


@app.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_proveedor(id):
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM proveedores WHERE id = %s', (id,))
    proveedor = cursor.fetchone()
    cursor.close()
    conn.close()

    if proveedor is None:
        abort(404)

    form = ProveedorForm(data=proveedor) if request.method == 'GET' else ProveedorForm()

    if form.validate_on_submit():
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE proveedores SET empresa=%s, insumo=%s, categoria=%s, contacto=%s, '
            'frecuencia=%s WHERE id=%s',
            (form.empresa.data, form.insumo.data, form.categoria.data,
             form.contacto.data, form.frecuencia.data, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Proveedor actualizado correctamente.', 'success')
        return redirect(url_for('proveedores'))

    return render_template('formulario_proveedor.html', form=form, modo='editar', id=id)


@app.route('/proveedores/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_proveedor(id):
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM proveedores WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Proveedor eliminado.', 'info')
    return redirect(url_for('proveedores'))

# ---------------------------------------------------------------------------
# MODULO FACTURACION (Cuenta por mesa) - Persistencia con PostgreSQL
# Relacionada con clientes mediante cliente_id (FK) -> se usa JOIN al listar
# ---------------------------------------------------------------------------

@app.route('/facturacion')
@login_required
def facturacion():
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT f.*, c.nombre AS cliente_nombre
        FROM facturas f
        LEFT JOIN clientes c ON f.cliente_id = c.id
        ORDER BY f.id DESC
    ''')
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('facturacion.html', facturas=filas)


@app.route('/facturacion/nueva', methods=['GET', 'POST'])
@login_required
def nueva_facturacion():
    form = FacturacionForm()
    form.cliente_id.choices = obtener_choices_clientes()
    if form.validate_on_submit():
        subtotal = form.subtotal.data
        iva = round(subtotal * 0.12, 2)
        total = round(subtotal + iva, 2)

        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO facturas (numero, cliente_id, mesa, productos, subtotal, iva, total, '
            'metodo_pago, estado, fecha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (form.numero.data, form.cliente_id.data, form.mesa.data, form.productos.data,
             subtotal, iva, total, form.metodo_pago.data, form.estado.data, form.fecha.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Factura registrada correctamente.', 'success')
        return redirect(url_for('facturacion'))
    return render_template('formulario_facturacion.html', form=form, modo='nuevo')


@app.route('/facturacion/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_facturacion(id):
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM facturas WHERE id = %s', (id,))
    factura = cursor.fetchone()
    cursor.close()
    conn.close()

    if factura is None:
        abort(404)

    form = FacturacionForm(data=factura) if request.method == 'GET' else FacturacionForm()
    form.cliente_id.choices = obtener_choices_clientes()

    if form.validate_on_submit():
        subtotal = form.subtotal.data
        iva = round(subtotal * 0.12, 2)
        total = round(subtotal + iva, 2)

        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE facturas SET numero=%s, cliente_id=%s, mesa=%s, productos=%s, subtotal=%s, '
            'iva=%s, total=%s, metodo_pago=%s, estado=%s, fecha=%s WHERE id=%s',
            (form.numero.data, form.cliente_id.data, form.mesa.data, form.productos.data,
             subtotal, iva, total, form.metodo_pago.data, form.estado.data, form.fecha.data, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Factura actualizada correctamente.', 'success')
        return redirect(url_for('facturacion'))

    return render_template('formulario_facturacion.html', form=form, modo='editar', id=id)


@app.route('/facturacion/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_facturacion(id):
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM facturas WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Factura eliminada.', 'info')
    return redirect(url_for('facturacion'))


if __name__ == '__main__':
    app.run(debug=True)