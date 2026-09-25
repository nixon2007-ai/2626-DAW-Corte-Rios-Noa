-- Ejecuta esto SOLO si ya habias creado las tablas viejas (con el diseno
-- que el docente marco como incorrecto) y quieres empezar de cero en tu
-- base de datos local antes de correr el nuevo esquema.sql.
--
-- ADVERTENCIA: esto borra TODOS los datos existentes en estas tablas.
DROP TABLE IF EXISTS detalle_factura CASCADE;
DROP TABLE IF EXISTS facturas CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS proveedores CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;