-- Parcial II - Programacion Computacional III - Codigo: usss096224
-- Importar en phpMyAdmin (XAMPP / MariaDB)
CREATE DATABASE IF NOT EXISTS `db_academica_parcial-2` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `db_academica_parcial-2`;

CREATE TABLE IF NOT EXISTS `usuarios_usss096224` (
  `idUsuario` int(10) NOT NULL AUTO_INCREMENT,
  `usuario` char(35) NOT NULL,
  `clave` char(35) NOT NULL,
  `nombre` char(85) NOT NULL,
  `direccion` char(100) NOT NULL,
  `telefono` char(9) NOT NULL,
  PRIMARY KEY (`idUsuario`),
  UNIQUE KEY `uq_usuario` (`usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Usuario inicial para entrar al sistema: admin / admin123  (clave guardada en MD5, cabe en char(35))
INSERT INTO `usuarios_usss096224` (`usuario`,`clave`,`nombre`,`direccion`,`telefono`) VALUES
('admin', MD5('admin123'), 'Administrador', 'Usulutan', '7000-0000');
