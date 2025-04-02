-- Create database
CREATE DATABASE IF NOT EXISTS sga_db;
USE sga_db;

-- Courses table
CREATE TABLE IF NOT EXISTS cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(10) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    CONSTRAINT UC_curso UNIQUE (codigo)
);

-- Course prerequisites
CREATE TABLE IF NOT EXISTS prerequisitos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    curso_id INT NOT NULL,
    prerequisito_id INT NOT NULL,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE,
    FOREIGN KEY (prerequisito_id) REFERENCES cursos(id) ON DELETE CASCADE,
    CONSTRAINT UC_prerequisito UNIQUE (curso_id, prerequisito_id)
);

-- Professors table
CREATE TABLE IF NOT EXISTS profesores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    CONSTRAINT UC_profesor_correo UNIQUE (correo)
);

-- Students table
CREATE TABLE IF NOT EXISTS alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    fecha_ingreso DATE NOT NULL,
    CONSTRAINT UC_alumno_correo UNIQUE (correo)
);

-- Course instances
CREATE TABLE IF NOT EXISTS instancias_curso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    curso_id INT NOT NULL,
    anio INT NOT NULL,
    periodo VARCHAR(2) NOT NULL,
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE CASCADE,
    CONSTRAINT UC_instancia UNIQUE (curso_id, anio, periodo)
);

-- Sections with usa_porcentaje field
CREATE TABLE IF NOT EXISTS secciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    instancia_curso_id INT NOT NULL,
    numero INT NOT NULL,
    usa_porcentaje BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'True: evaluación por porcentaje, False: evaluación por peso',
    FOREIGN KEY (instancia_curso_id) REFERENCES instancias_curso(id) ON DELETE CASCADE,
    CONSTRAINT UC_seccion UNIQUE (instancia_curso_id, numero)
);

-- Professors assigned to sections
CREATE TABLE IF NOT EXISTS profesor_seccion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profesor_id INT NOT NULL,
    seccion_id INT NOT NULL,
    FOREIGN KEY (profesor_id) REFERENCES profesores(id) ON DELETE CASCADE,
    FOREIGN KEY (seccion_id) REFERENCES secciones(id) ON DELETE CASCADE,
    CONSTRAINT UC_profesor_seccion UNIQUE (profesor_id, seccion_id)
);

-- Students enrolled in sections
CREATE TABLE IF NOT EXISTS alumno_seccion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    seccion_id INT NOT NULL,
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE,
    FOREIGN KEY (seccion_id) REFERENCES secciones(id) ON DELETE CASCADE,
    CONSTRAINT UC_alumno_seccion UNIQUE (alumno_id, seccion_id)
);

-- Evaluation topics with valor field and usa_porcentaje field
CREATE TABLE IF NOT EXISTS topicos_evaluacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    seccion_id INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    valor DECIMAL(5,2) NOT NULL COMMENT 'Porcentaje o peso según configuración de la sección',
    usa_porcentaje BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'True: evaluación por porcentaje, False: evaluación por peso para las instancias',
    FOREIGN KEY (seccion_id) REFERENCES secciones(id) ON DELETE CASCADE,
    CONSTRAINT UC_topico UNIQUE (seccion_id, nombre)
);

-- Evaluation instances with valor field
CREATE TABLE IF NOT EXISTS instancias_evaluacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topico_id INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    valor DECIMAL(5,2) NOT NULL COMMENT 'Porcentaje o peso dentro del tópico según configuración del tópico',
    opcional BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (topico_id) REFERENCES topicos_evaluacion(id) ON DELETE CASCADE,
    CONSTRAINT UC_instancia_evaluacion UNIQUE (topico_id, nombre)
);

-- Grades
CREATE TABLE IF NOT EXISTS notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_seccion_id INT NOT NULL,
    instancia_evaluacion_id INT NOT NULL,
    nota DECIMAL(3,1) NOT NULL,
    FOREIGN KEY (alumno_seccion_id) REFERENCES alumno_seccion(id) ON DELETE CASCADE,
    FOREIGN KEY (instancia_evaluacion_id) REFERENCES instancias_evaluacion(id) ON DELETE CASCADE,
    CONSTRAINT UC_nota UNIQUE (alumno_seccion_id, instancia_evaluacion_id)
);

-- Completed courses tracking table
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

-- Add some sample data
INSERT INTO cursos (codigo, nombre) VALUES 
('ICC5130', 'Diseño de Software Verificable'),
('ICC5119', 'Ingeniería de Software'),
('ICC5124', 'Diseño Avanzado de Base de Datos');

INSERT INTO profesores (nombre, correo) VALUES 
('Juan Perez', 'juan.perez@universidad.cl'),
('Maria Rodriguez', 'maria.rodriguez@universidad.cl');

INSERT INTO alumnos (nombre, correo, fecha_ingreso) VALUES 
('Pedro Gomez', 'pedro.gomez@universidad.cl', '2022-03-01'),
('Ana Martinez', 'ana.martinez@universidad.cl', '2023-03-01');

-- Grant privileges
GRANT ALL PRIVILEGES ON sga_db.* TO 'sga_user'@'%';
FLUSH PRIVILEGES;