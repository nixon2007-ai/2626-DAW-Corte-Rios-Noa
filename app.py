from flask import Flask, render_template, redirect, url_for, abort, request, session
from flask_wtf.csrf import CSRFProtect

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from conexion.conexion import get_conexion
from flask import flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from io import BytesIO
from werkzeug.utils import secure_filename
from xhtml2pdf import pisa
from flask import Response

from models import obtener_usuario_por_id, obtener_usuario_por_nombre
from forms.login_form import LoginForm
from forms.usuario_form import RegistroForm
import os
from datetime import datetime
from io import BytesIO
from werkzeug.utils import secure_filename
from xhtml2pdf import pisa
import random
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mar-y-selva-gastrobar-clave-secreta-2026'
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'img', 'productos')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@login_manager.user_loader
def load_user(user_id):
    return obtener_usuario_por_id(user_id)


def obtener_choices_proveedores():
    conn = get_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT id, empresa FROM proveedores ORDER BY empresa')
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    return [(f['id'], f['empresa']) for f in filas]


def obtener_choices_clientes():
    conn = get_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT id, nombre FROM clientes ORDER BY nombre')
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    return [(f['id'], f['nombre']) for f in filas]


@app.route('/')
def index():
    return render_template('index.html')


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

    if request.method == 'POST':
        if form.validate_on_submit():
            captcha_esperado = session.get('captcha_resultado')
            if captcha_esperado is None or form.captcha.data != captcha_esperado:
                flash('La verificación es incorrecta. Intenta de nuevo.', 'danger')
            else:
                usuario = obtener_usuario_por_nombre(form.usuario.data)
                if usuario and check_password_hash(usuario.password, form.password.data):
                    session.pop('captcha_resultado', None)
                    login_user(usuario)
                    return redirect(url_for('panel'))
                else:
                    flash('Usuario o contraseña incorrectos.', 'danger')

    # Genera una nueva operación de verificación cada vez que se muestra el formulario
    num_a = random.randint(1, 10)
    num_b = random.randint(1, 10)
    session['captcha_resultado'] = num_a + num_b

    return render_template('login.html', form=form, num_a=num_a, num_b=num_b)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('login'))


@app.route('/panel')
@login_required
def panel():
    return render_template('panel.html')

# ---------------------------------------------------------------------------
# MODULO PRODUCTOS
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
        nombre_archivo = None
        if form.imagen.data:
            nombre_archivo = secure_filename(form.imagen.data.filename)
            form.imagen.data.save(os.path.join(UPLOAD_FOLDER, nombre_archivo))

        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO productos (nombre, categoria, precio, estado, descripcion, '
            'produccion_diaria, imagen, proveedor_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (form.nombre.data, form.categoria.data, form.precio.data, form.estado.data,
             form.descripcion.data, form.produccion_diaria.data, nombre_archivo, form.proveedor_id.data)
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
        nombre_archivo = producto['imagen']
        if form.imagen.data:
            nombre_archivo = secure_filename(form.imagen.data.filename)
            form.imagen.data.save(os.path.join(UPLOAD_FOLDER, nombre_archivo))

        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE productos SET nombre=%s, categoria=%s, precio=%s, estado=%s, descripcion=%s, '
            'produccion_diaria=%s, imagen=%s, proveedor_id=%s WHERE id=%s',
            (form.nombre.data, form.categoria.data, form.precio.data, form.estado.data,
             form.descripcion.data, form.produccion_diaria.data, nombre_archivo,
             form.proveedor_id.data, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('productos'))

    return render_template('formulario_productos.html', form=form, modo='editar', id=id, producto=producto)


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
# MODULO CLIENTES
# ---------------------------------------------------------------------------


@app.route('/clientes')
@login_required
def clientes():
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes ORDER BY id')
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
            'INSERT INTO clientes (nombre, cedula, correo, telefono, tipo, mesa_preferida, reservas) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (form.nombre.data, form.cedula.data, form.correo.data, form.telefono.data,
             form.tipo.data, form.mesa_preferida.data, form.reservas.data)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('clientes'))
    return render_template('formulario_cliente.html', form=form)


@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    conn = get_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
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
            'UPDATE clientes SET nombre=%s, cedula=%s, correo=%s, telefono=%s, tipo=%s, '
            'mesa_preferida=%s, reservas=%s WHERE id=%s',
            (form.nombre.data, form.cedula.data, form.correo.data, form.telefono.data, form.tipo.data,
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
    try:
        cursor.execute('DELETE FROM clientes WHERE id = %s', (id,))
        conn.commit()
        flash('Cliente eliminado.', 'info')
    except Exception:
        conn.rollback()
        flash('No se puede eliminar: este cliente ya tiene facturas registradas.', 'danger')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('clientes'))


# ---------------------------------------------------------------------------
# MODULO PROVEEDORES
# ---------------------------------------------------------------------------

@app.route('/proveedores')
@login_required
def proveedores():
    conn = get_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM proveedores ORDER BY empresa')
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('proveedores.html', proveedores=filas)


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_proveedor():
    form = ProveedorForm()
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
    cursor = conn.cursor(cursor_factory=RealDictCursor)
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
    try:
        cursor.execute('DELETE FROM proveedores WHERE id = %s', (id,))
        conn.commit()
        flash('Proveedor eliminado.', 'info')
    except Exception:
        conn.rollback()
        flash('No se puede eliminar: este proveedor ya tiene productos asociados.', 'danger')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('proveedores'))

# ---------------------------------------------------------------------------
# MODULO FACTURACION
# ---------------------------------------------------------------------------

def obtener_productos_disponibles():
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio FROM productos WHERE estado = 'Disponible' ORDER BY nombre")
    filas = cursor.fetchall()
    cursor.close()
    conn.close()
    return filas


@app.route('/facturacion')
@login_required
def facturacion():
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT f.*, c.nombre AS cliente_nombre, c.cedula AS cliente_cedula
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

    if request.method == 'POST' and form.validate_on_submit():
        productos_ids = request.form.getlist('producto_id[]')
        cantidades = request.form.getlist('cantidad[]')

        lineas = []
        subtotal_total = 0.0
        stock_insuficiente = []
        for pid, cant in zip(productos_ids, cantidades):
            if not pid or not cant:
                continue
            pid = int(pid)
            cant = int(cant)
            if cant <= 0:
                continue
            conn = get_conexion()
            cursor = conn.cursor()
            cursor.execute('SELECT nombre, precio, produccion_diaria FROM productos WHERE id = %s', (pid,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            if not row:
                continue

            stock_disponible = row['produccion_diaria'] or 0
            if cant > stock_disponible:
                stock_insuficiente.append(
                    f"{row['nombre']} (pediste {cant}, quedan {stock_disponible})"
                )
                continue

            precio_unit = float(row['precio'])
            sub = precio_unit * cant
            subtotal_total += sub
            lineas.append((pid, cant, precio_unit, sub))

        if stock_insuficiente:
            flash('No hay suficiente stock para: ' + '; '.join(stock_insuficiente), 'danger')
            return render_template('formulario_facturacion.html', form=form,
                                    productos=obtener_productos_disponibles())

        if not lineas:
            flash('Debes seleccionar al menos un producto con cantidad válida.', 'danger')
            return render_template('formulario_facturacion.html', form=form,
                                    productos=obtener_productos_disponibles())

        iva_total = round(subtotal_total * 0.12, 2)
        total_general = round(subtotal_total + iva_total, 2)

        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO facturas (numero, cliente_id, mesa, subtotal, iva, total, metodo_pago, estado, fecha) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id',
            (form.numero.data, form.cliente_id.data, form.mesa.data, round(subtotal_total, 2),
             iva_total, total_general, form.metodo_pago.data, form.estado.data, form.fecha.data)
        )
        factura_id = cursor.fetchone()['id']

        for pid, cant, precio_unit, sub in lineas:
            cursor.execute(
                'INSERT INTO detalle_factura (factura_id, producto_id, cantidad, precio_unitario, subtotal) '
                'VALUES (%s, %s, %s, %s, %s)',
                (factura_id, pid, cant, precio_unit, sub)
            )
            # Descuenta la cantidad facturada del stock/producción diaria del producto
            cursor.execute(
                'UPDATE productos SET produccion_diaria = produccion_diaria - %s WHERE id = %s',
                (cant, pid)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('facturacion'))

    return render_template('formulario_facturacion.html', form=form,
                            productos=obtener_productos_disponibles())


@app.route('/facturacion/pdf/<int:id>')
@login_required
def factura_pdf(id):
    conn = get_conexion()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT f.*, c.nombre AS cliente_nombre, c.cedula AS cliente_cedula
        FROM facturas f LEFT JOIN clientes c ON f.cliente_id = c.id
        WHERE f.id = %s
    ''', (id,))
    factura = cursor.fetchone()

    cursor.execute('''
        SELECT d.*, p.nombre AS producto_nombre
        FROM detalle_factura d JOIN productos p ON d.producto_id = p.id
        WHERE d.factura_id = %s
    ''', (id,))
    detalle = cursor.fetchall()
    cursor.close()
    conn.close()

    if factura is None:
        abort(404)

    html = render_template('factura_pdf.html', factura=factura, detalle=detalle)
    resultado = BytesIO()
    pisa.CreatePDF(html, dest=resultado)
    resultado.seek(0)

    return Response(
        resultado.getvalue(),
        mimetype='application/pdf',
        headers={'Content-Disposition': f'attachment; filename=factura_{factura["numero"]}.pdf'}
    )

if __name__ == '__main__':
    app.run(debug=True)