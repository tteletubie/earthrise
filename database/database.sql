PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS categoria (
  id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre VARCHAR(60) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS grado (
  id_grado INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre VARCHAR(20) NOT NULL UNIQUE
);

INSERT OR IGNORE INTO grado (id_grado, nombre) VALUES
  (1, '1°'),
  (2, '2°'),
  (3, '3°'),
  (4, '4°'),
  (5, '5°'),
  (6, '6°');

CREATE TABLE IF NOT EXISTS usuario (
  id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre VARCHAR(80) NOT NULL,
  apellido_paterno VARCHAR(100) NOT NULL,
  id_grado INTEGER NOT NULL,
  fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_grado) REFERENCES grado (id_grado)
);

CREATE TABLE IF NOT EXISTS grupo (
  id_grupo INTEGER PRIMARY KEY AUTOINCREMENT,
  id_grado INTEGER NOT NULL,
  nombre VARCHAR(10) NOT NULL,
  ciclo_escolar VARCHAR(9) NOT NULL,
  FOREIGN KEY (id_grado) REFERENCES grado (id_grado)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_grupo_unico
ON grupo (id_grado, nombre, ciclo_escolar);

CREATE TABLE IF NOT EXISTS maestro_grupo (
  id_maestro_grupo INTEGER PRIMARY KEY AUTOINCREMENT,
  id_usuario INTEGER NOT NULL,
  id_grupo INTEGER NOT NULL,
  FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
  FOREIGN KEY (id_grupo) REFERENCES grupo (id_grupo)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_maestro_grupo_unico
ON maestro_grupo (id_usuario, id_grupo);

CREATE TABLE IF NOT EXISTS libro (
  id_libro INTEGER PRIMARY KEY AUTOINCREMENT,
  id_categoria INTEGER,
  titulo VARCHAR(150) NOT NULL,
  autor VARCHAR(120),
  descripcion TEXT,
  portada_url VARCHAR(255),
  archivo_url VARCHAR(255) NOT NULL,
  id_usuario INTEGER NOT NULL,
  fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_eliminacion DATETIME,
  FOREIGN KEY (id_categoria) REFERENCES categoria (id_categoria),
  FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
);

CREATE TABLE IF NOT EXISTS libro_grado (
  id_libro_grado INTEGER PRIMARY KEY AUTOINCREMENT,
  id_libro INTEGER NOT NULL,
  id_grado INTEGER NOT NULL,
  FOREIGN KEY (id_libro) REFERENCES libro (id_libro),
  FOREIGN KEY (id_grado) REFERENCES grado (id_grado)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_libro_grado_unico
ON libro_grado (id_libro, id_grado);

CREATE TABLE IF NOT EXISTS actividad (
  id_actividad INTEGER PRIMARY KEY AUTOINCREMENT,
  id_libro INTEGER NOT NULL,
  titulo VARCHAR(150) NOT NULL,
  instrucciones TEXT NOT NULL,
  id_usuario_creador INTEGER NOT NULL,
  fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_eliminacion DATETIME,
  FOREIGN KEY (id_libro) REFERENCES libro (id_libro),
  FOREIGN KEY (id_usuario_creador) REFERENCES usuario (id_usuario)
);

CREATE TABLE IF NOT EXISTS pregunta (
  id_pregunta INTEGER PRIMARY KEY AUTOINCREMENT,
  id_actividad INTEGER NOT NULL,
  enunciado TEXT NOT NULL,
  tipo VARCHAR(20) NOT NULL,
  orden SMALLINT NOT NULL,
  FOREIGN KEY (id_actividad) REFERENCES actividad (id_actividad) ON DELETE CASCADE
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_pregunta_orden
ON pregunta (id_actividad, orden);

CREATE TABLE IF NOT EXISTS opcion (
  id_opcion INTEGER PRIMARY KEY AUTOINCREMENT,
  id_pregunta INTEGER NOT NULL,
  texto VARCHAR(255) NOT NULL,
  es_correcta BOOLEAN NOT NULL DEFAULT 0,
  orden SMALLINT NOT NULL,
  FOREIGN KEY (id_pregunta) REFERENCES pregunta (id_pregunta) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS bitacora (
  id_bitacora INTEGER PRIMARY KEY AUTOINCREMENT,
  id_usuario INTEGER NOT NULL,
  accion VARCHAR(20) NOT NULL,
  entidad VARCHAR(30) NOT NULL,
  id_entidad INTEGER NOT NULL,
  detalle TEXT,
  fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
);

CREATE TABLE IF NOT EXISTS sesion_lectura (
  id_sesion INTEGER PRIMARY KEY AUTOINCREMENT,
  id_usuario INTEGER NOT NULL,
  id_libro INTEGER NOT NULL,
  id_grupo INTEGER NOT NULL,
  fecha_inicio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_fin DATETIME,
  observaciones TEXT,
  FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
  FOREIGN KEY (id_libro) REFERENCES libro (id_libro),
  FOREIGN KEY (id_grupo) REFERENCES grupo (id_grupo)
);

CREATE INDEX IF NOT EXISTS idx_sesion_usuario_fecha
ON sesion_lectura (id_usuario, fecha_inicio);

CREATE INDEX IF NOT EXISTS idx_sesion_libro
ON sesion_lectura (id_libro);

CREATE TABLE IF NOT EXISTS aplicacion_actividad (
  id_aplicacion INTEGER PRIMARY KEY AUTOINCREMENT,
  id_sesion INTEGER NOT NULL,
  id_actividad INTEGER NOT NULL,
  fecha_mostrada DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_fin DATETIME,
  FOREIGN KEY (id_sesion) REFERENCES sesion_lectura (id_sesion),
  FOREIGN KEY (id_actividad) REFERENCES actividad (id_actividad)
);
