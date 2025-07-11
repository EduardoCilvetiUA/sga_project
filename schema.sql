CREATE DATABASE IF NOT EXISTS sga_db;
USE sga_db;

CREATE TABLE IF NOT EXISTS cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(10) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    creditos INT NOT NULL DEFAULT 2,
    CONSTRAINT UC_curso UNIQUE (codigo)
);

CREATE TABLE IF NOT EXISTS prerequisitos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    curso_id INT NOT NULL,
    prerequisito_id INT NOT NULL,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE,
    FOREIGN KEY (prerequisito_id) REFERENCES cursos(id) ON DELETE CASCADE,
    CONSTRAINT UC_prerequisito UNIQUE (curso_id, prerequisito_id)
);

CREATE TABLE IF NOT EXISTS profesores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    CONSTRAINT UC_profesor_correo UNIQUE (correo)
);

CREATE TABLE IF NOT EXISTS alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    fecha_ingreso DATE NOT NULL,
    CONSTRAINT UC_alumno_correo UNIQUE (correo)
);

CREATE TABLE IF NOT EXISTS instancias_curso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    curso_id INT NOT NULL,
    anio INT NOT NULL,
    periodo VARCHAR(2) NOT NULL,
    cerrado BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Indica si esta instancia específica está cerrada',
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE,
    CONSTRAINT UC_instancia UNIQUE (curso_id, anio, periodo)
);

CREATE TABLE IF NOT EXISTS secciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    instancia_curso_id INT NOT NULL,
    numero INT NOT NULL,
    usa_porcentaje BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'True: evaluación por porcentaje, False: evaluación por peso',
    FOREIGN KEY (instancia_curso_id) REFERENCES instancias_curso(id) ON DELETE CASCADE,
    CONSTRAINT UC_seccion UNIQUE (instancia_curso_id, numero)
);

CREATE TABLE IF NOT EXISTS profesor_seccion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profesor_id INT NOT NULL,
    seccion_id INT NOT NULL,
    FOREIGN KEY (profesor_id) REFERENCES profesores(id) ON DELETE CASCADE,
    FOREIGN KEY (seccion_id) REFERENCES secciones(id) ON DELETE CASCADE,
    CONSTRAINT UC_profesor_seccion UNIQUE (profesor_id, seccion_id)
);

CREATE TABLE IF NOT EXISTS alumno_seccion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    seccion_id INT NOT NULL,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE,
    FOREIGN KEY (seccion_id) REFERENCES secciones(id) ON DELETE CASCADE,
    CONSTRAINT UC_alumno_seccion UNIQUE (alumno_id, seccion_id)
);

CREATE TABLE IF NOT EXISTS topicos_evaluacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    seccion_id INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    valor DECIMAL(5,2) NOT NULL COMMENT 'Porcentaje o peso según configuración de la sección',
    usa_porcentaje BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'True: evaluación por porcentaje, False: evaluación por peso para las instancias',
    FOREIGN KEY (seccion_id) REFERENCES secciones(id) ON DELETE CASCADE,
    CONSTRAINT UC_topico UNIQUE (seccion_id, nombre)
);

CREATE TABLE IF NOT EXISTS instancias_evaluacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topico_id INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    valor DECIMAL(5,2) NOT NULL COMMENT 'Porcentaje o peso dentro del tópico según configuración del tópico',
    opcional BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (topico_id) REFERENCES topicos_evaluacion(id) ON DELETE CASCADE,
    CONSTRAINT UC_instancia_evaluacion UNIQUE (topico_id, nombre)
);

CREATE TABLE IF NOT EXISTS notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_seccion_id INT NOT NULL,
    instancia_evaluacion_id INT NOT NULL,
    nota DECIMAL(3,1) NOT NULL,
    FOREIGN KEY (alumno_seccion_id) REFERENCES alumno_seccion(id) ON DELETE CASCADE,
    FOREIGN KEY (instancia_evaluacion_id) REFERENCES instancias_evaluacion(id) ON DELETE CASCADE,
    CONSTRAINT UC_nota UNIQUE (alumno_seccion_id, instancia_evaluacion_id)
);

CREATE TABLE IF NOT EXISTS cursos_aprobados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    curso_id INT NOT NULL,
    seccion_id INT NOT NULL,
    nota_final DECIMAL(3,1) NOT NULL,
    aprobado BOOLEAN NOT NULL,
    fecha_aprobacion DATE NOT NULL,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE,
    FOREIGN KEY (seccion_id) REFERENCES secciones(id) ON DELETE CASCADE,
    CONSTRAINT UC_curso_aprobado UNIQUE (alumno_id, curso_id)
);

-- Crear tabla para salas de clases
CREATE TABLE IF NOT EXISTS salas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    capacidad INT NOT NULL CHECK (capacidad > 0),
    CONSTRAINT UC_sala_nombre UNIQUE (nombre)
);

-- Crear tabla para horarios
CREATE TABLE IF NOT EXISTS horarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    seccion_id INT NOT NULL,
    sala_id INT NOT NULL,
    dia ENUM('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes') NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    FOREIGN KEY (seccion_id) REFERENCES secciones(id) ON DELETE CASCADE,
    FOREIGN KEY (sala_id) REFERENCES salas(id) ON DELETE RESTRICT,
    CONSTRAINT CK_horario_horas CHECK (
        hora_inicio >= '09:00:00' AND 
        hora_fin <= '18:00:00' AND 
        hora_inicio < hora_fin AND
        NOT (hora_inicio < '14:00:00' AND hora_fin > '13:00:00')
    ),
    CONSTRAINT UC_horario UNIQUE (sala_id, dia, hora_inicio)
);

CREATE INDEX idx_horario_seccion ON horarios(seccion_id);
CREATE INDEX idx_horario_sala ON horarios(sala_id);
CREATE INDEX idx_horario_tiempo ON horarios(dia, hora_inicio, hora_fin);
CREATE INDEX idx_instancias_curso_cerrado ON instancias_curso(cerrado);

GRANT ALL PRIVILEGES ON sga_db.* TO 'sga_user'@'%';
FLUSH PRIVILEGES;