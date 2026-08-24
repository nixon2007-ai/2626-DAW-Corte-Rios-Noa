from flask import Flask, render_template

app = Flask(__name__)


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


# MODULO PRODUCTOS (Menú del gastrobar)
@app.route('/productos')
def productos():
    lista_productos = [
        {"nombre": "Ceviche Amazónico de Chontacoco", "categoria": "Plato Fuerte",
         "precio": 8.00, "estado": "Agotado",
         "descripcion": "Pescado fresco marinado en leche de tigre con toque de chontaduro y coco amazónico."},
        {"nombre": "Selvático de Paiche y Camarón", "categoria": "Plato Fuerte",
         "precio": 10.50, "estado": "Disponible",
         "descripcion": "Paiche amazónico y camarones en salsa de coco manabita, arroz perfumado y plátano maduro."},
        {"nombre": "Verde con Cecina Ahumada y Langostinos", "categoria": "Plato Fuerte",
         "precio": 15.00, "estado": "Disponible",
         "descripcion": "Clásico costeño reinventado con cecina amazónica ahumada y langostinos salteados."},
        {"nombre": "Bolón de Yuca Relleno de Maito de Pescado", "categoria": "Plato Fuerte",
         "precio": 6.00, "estado": "Disponible",
         "descripcion": "Bolón de yuca amazónica relleno de pescado envuelto en hoja de bijao."},
        {"nombre": "Arroz Meloso del Manglar con Guayusa y Mariscos", "categoria": "Plato Fuerte",
         "precio": 10.00, "estado": "Disponible",
         "descripcion": "Arroz cremoso infusionado con guayusa, mezclado con mariscos frescos."},
        {"nombre": "Costillas Glaseadas con Salsa de Arazá y Maracuyá", "categoria": "Plato Fuerte",
         "precio": 9.00, "estado": "Disponible",
         "descripcion": "Costillas de cerdo bañadas en reducción de frutas amazónicas y costeñas."},
        {"nombre": "Cóctel Selva Dorada", "categoria": "Cóctel",
         "precio": 9.00, "estado": "Agotado",
         "descripcion": "Cóctel tropical a base de aguardiente, maracuyá y arazá con espuma de guayusa."},
        {"nombre": "Cóctel Brisa del Oriente", "categoria": "Cóctel",
         "precio": 7.00, "estado": "Disponible",
         "descripcion": "Mezcla de ron, jugo de coco, guanábana y esencia de hierba luisa."},
    ]
    categorias = sorted(set(p["categoria"] for p in lista_productos))
    return render_template('productos.html', productos=lista_productos, categorias=categorias)


# MODULO CLIENTES (Reservas y comensales)
@app.route('/clientes')
def clientes():
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
    return render_template('clientes.html', clientes=lista_clientes)


# MODULO PROVEEDORES (Insumos del gastrobar)
@app.route('/proveedores')
def proveedores():
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
    return render_template('proveedores.html', proveedores=lista_proveedores)


# MODULO FACTURACION (Cuenta por mesa)
@app.route('/facturacion')
def facturacion():
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
    return render_template('facturacion.html', facturas=lista_facturas)


if __name__ == '__main__':
    app.run(debug=True)
