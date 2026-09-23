-- ---------------------------------------------------------------------------
-- Esquema PostgreSQL - Mar & Selva Gastrobar
-- Ejecutar este script una vez contra la base "gastrobar_db"
-- (en Render, contra la base PostgreSQL que te asigne el servicio)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS proveedores (
    id SERIAL PRIMARY KEY,
    empresa VARCHAR(100) NOT NULL,
    insumo VARCHAR(150) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    contacto VARCHAR(15) NOT NULL,
    frecuencia VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    precio NUMERIC(10,2) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    descripcion VARCHAR(300) NOT NULL,
    proveedor_id INTEGER,
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    mesa_preferida VARCHAR(50) NOT NULL,
    reservas INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS facturas (
    id SERIAL PRIMARY KEY,
    numero VARCHAR(30) NOT NULL,
    cliente_id INTEGER,
    mesa INTEGER NOT NULL,
    productos VARCHAR(300) NOT NULL,
    subtotal NUMERIC(10,2) NOT NULL,
    iva NUMERIC(10,2) NOT NULL,
    total NUMERIC(10,2) NOT NULL,
    metodo_pago VARCHAR(30) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    fecha VARCHAR(10) NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE SET NULL
);

-- ---------------------------------------------------------------------------
-- Datos de ejemplo
-- ---------------------------------------------------------------------------

INSERT INTO proveedores (empresa, insumo, categoria, contacto, frecuencia) VALUES
('Pesquera del Pacifico S.A.', 'Mariscos y pescado fresco', 'Mar', '0998765432', 'Semanal'),
('AmazonFrut Cia. Ltda.', 'Frutas amazonicas', 'Amazonia', '0987651234', 'Quincenal'),
('Licores del Litoral', 'Aguardiente, ron y licores', 'Bebidas', '0965478123', 'Mensual');

INSERT INTO clientes (nombre, correo, telefono, tipo, mesa_preferida, reservas) VALUES
('Maria Fernanda Lopez', 'mflopez@gmail.com', '0991234567', 'Frecuente', 'Terraza', 5),
('Carlos Andres Ramirez', 'caramirez@gmail.com', '0987654321', 'Nuevo', 'Salon Interior', 1),
('Daniela Castillo Pinta', 'dcastillo@gmail.com', '0965432198', 'Frecuente', 'Barra', 8);