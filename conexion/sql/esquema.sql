-- =============================================================================
-- Esquema PostgreSQL - Mar & Selva Gastrobar
-- VERSION CORREGIDA - alineada 100% con app.py, models.py y forms/*.py
--
-- Corrige las fallas detectadas por el docente:
--   1) La factura ya NO guarda el nombre del producto como texto libre.
--      Ahora existe la tabla "detalle_factura" que relaciona
--      factura <-> producto mediante llaves foraneas (FK), con su cantidad
--      y precio, tal como se explico en la revision.
--   2) Se agrega la columna "cedula" a clientes (la usa el formulario y
--      se muestra en la factura en PDF).
--   3) Se agregan "produccion_diaria" e "imagen" a productos (las pide el
--      formulario de productos).
--   4) Las llaves foraneas que protegen contra borrado (proveedor con
--      productos, cliente con facturas, producto con detalle_factura) usan
--      el comportamiento por defecto (RESTRICT), para que el mensaje de
--      "no se puede eliminar" que ya maneja app.py funcione correctamente.
--
-- Ejecutar este script UNA SOLA VEZ contra tu base local "gastrobar_db".
-- Si ya tenias tablas viejas, primero corre limpiar_bd.sql (o borra y
-- vuelve a crear la base) para evitar choques con el diseno anterior.
-- =============================================================================

-- --- 1. Usuarios del sistema (login del panel) --------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- --- 2. Proveedores ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS proveedores (
    id SERIAL PRIMARY KEY,
    empresa VARCHAR(100) NOT NULL,
    insumo VARCHAR(150) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    contacto VARCHAR(15) NOT NULL,
    frecuencia VARCHAR(20) NOT NULL
);

-- --- 3. Productos (menu del gastrobar) ------------------------------------------
CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    precio NUMERIC(10,2) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    descripcion VARCHAR(300) NOT NULL,
    produccion_diaria INTEGER NOT NULL DEFAULT 0,
    imagen VARCHAR(255),
    proveedor_id INTEGER REFERENCES proveedores(id)
);

-- --- 4. Clientes -----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cedula VARCHAR(10) NOT NULL UNIQUE,
    correo VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    mesa_preferida VARCHAR(50) NOT NULL,
    reservas INTEGER NOT NULL DEFAULT 0
);

-- --- 5. Facturas (cabecera) -------------------------------------------------------
-- OJO: ya NO tiene columna "productos" de texto libre. Los productos de
-- cada factura viven en la tabla detalle_factura (punto 6).
CREATE TABLE IF NOT EXISTS facturas (
    id SERIAL PRIMARY KEY,
    numero VARCHAR(30) NOT NULL UNIQUE,
    cliente_id INTEGER REFERENCES clientes(id),
    mesa VARCHAR(20) NOT NULL,
    subtotal NUMERIC(10,2) NOT NULL,
    iva NUMERIC(10,2) NOT NULL,
    total NUMERIC(10,2) NOT NULL,
    metodo_pago VARCHAR(30) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    fecha VARCHAR(30) NOT NULL
);

-- --- 6. Detalle de factura (relacion factura <-> producto) ------------------------
-- Esta es la tabla que el docente pidio agregar: aqui se guarda el ID del
-- producto vendido (no su nombre escrito a mano), la cantidad y el precio
-- que tenia en ese momento.
CREATE TABLE IF NOT EXISTS detalle_factura (
    id SERIAL PRIMARY KEY,
    factura_id INTEGER NOT NULL REFERENCES facturas(id) ON DELETE CASCADE,
    producto_id INTEGER NOT NULL REFERENCES productos(id),
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(10,2) NOT NULL,
    subtotal NUMERIC(10,2) NOT NULL
);

-- =============================================================================
-- Datos de ejemplo (opcional, puedes borrar este bloque si no los quieres)
-- =============================================================================

INSERT INTO proveedores (empresa, insumo, categoria, contacto, frecuencia) VALUES
('Pesquera del Pacifico S.A.', 'Mariscos y pescado fresco', 'Mar', '0998765432', 'Semanal'),
('AmazonFrut Cia. Ltda.', 'Frutas amazonicas', 'Amazonia', '0987651234', 'Quincenal'),
('Licores del Litoral', 'Aguardiente, ron y licores', 'Bebidas', '0965478123', 'Mensual');

INSERT INTO clientes (nombre, cedula, correo, telefono, tipo, mesa_preferida, reservas) VALUES
('Maria Fernanda Lopez', '1712345678', 'mflopez@gmail.com', '0991234567', 'Frecuente', 'Terraza', 5),
('Carlos Andres Ramirez', '1723456789', 'caramirez@gmail.com', '0987654321', 'Nuevo', 'Salon Interior', 1),
('Daniela Castillo Pinta', '1734567890', 'dcastillo@gmail.com', '0965432198', 'Frecuente', 'Barra', 8);

INSERT INTO productos (nombre, categoria, precio, estado, descripcion, produccion_diaria, imagen, proveedor_id) VALUES
('Ceviche Manaba', 'Entrada', 8.50, 'Disponible', 'Ceviche de camaron estilo manaba, servido con chifles y canguil.', 25, NULL, 1),
('Tilapia Frita', 'Plato Fuerte', 12.00, 'Disponible', 'Filete de tilapia frito acompanado de arroz y patacones.', 20, NULL, 1),
('Jugo de Naranjilla', 'Bebida', 3.00, 'Disponible', 'Jugo natural de naranjilla amazonica.', 40, NULL, 2);