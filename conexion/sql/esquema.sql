CREATE DATABASE IF NOT EXISTS gastrobar_db;
USE gastrobar_db;

CREATE TABLE IF NOT EXISTS proveedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa VARCHAR(100) NOT NULL,
    insumo VARCHAR(150) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    contacto VARCHAR(15) NOT NULL,
    frecuencia VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    descripcion VARCHAR(300) NOT NULL,
    proveedor_id INT,
    FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
);

CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    mesa_preferida VARCHAR(50) NOT NULL,
    reservas INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS facturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(30) NOT NULL,
    cliente_id INT,
    mesa INT NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    iva DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    metodo_pago VARCHAR(30) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

INSERT INTO proveedores (empresa, insumo, categoria, contacto, frecuencia) VALUES
('Pesquera del Pacífico S.A.', 'Mariscos y pescado fresco', 'Mar', '0998765432', 'Semanal'),
('AmazonFrut Cía. Ltda.', 'Frutas amazónicas', 'Amazonía', '0987651234', 'Quincenal'),
('Licores del Litoral', 'Aguardiente, ron y licores', 'Bebidas', '0965478123', 'Mensual');