-- Esquema completo para Hágala Corta
-- Filosofía: limpieza, privacidad, posibilidad de extensión
-- Se incluye la tabla principal 'urls' y una tabla opcional 'visitas' para analítica anónima

-- Tabla principal de URLs acortadas
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL CHECK(LENGTH(codigo) <= 12),
    url_original TEXT NOT NULL CHECK(LENGTH(url_original) <= 2048),
    fecha_creacion TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
    contador_clics INTEGER DEFAULT 0
);

-- Tabla opcional para visitas, si se desea agregar analítica (IP hash opcional)
CREATE TABLE IF NOT EXISTS visitas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url_id INTEGER NOT NULL,
    fecha TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
    ip_hash TEXT CHECK(LENGTH(ip_hash) = 64), -- SHA-256
    user_agent TEXT CHECK(LENGTH(user_agent) <= 512),
    FOREIGN KEY (url_id) REFERENCES urls(id) ON DELETE CASCADE
);

-- Índices para mejorar rendimiento si se usa la tabla visitas
CREATE INDEX IF NOT EXISTS idx_visitas_url_id ON visitas(url_id);
CREATE INDEX IF NOT EXISTS idx_visitas_fecha ON visitas(fecha);

-- Comentario: Si no deseas usar la tabla 'visitas', simplemente ignora su inserción desde el backend.
