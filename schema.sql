-- Create database
CREATE DATABASE IF NOT EXISTS sga_db;
USE sga_db;

-- Drop tables if they exist (in order of dependencies)
DROP TABLE IF EXISTS cursos_aprobados;
DROP TABLE IF EXISTS notas;
DROP TABLE IF EXISTS instancias_evaluacion;
DROP TABLE IF EXISTS topicos_evaluacion;
DROP TABLE IF EXISTS alumno_seccion;
DROP TABLE IF EXISTS profesor_seccion;
DROP TABLE IF EXISTS secciones;
DROP TABLE IF EXISTS instancias_curso;
DROP TABLE IF EXISTS prerequisitos;
DROP TABLE IF EXISTS alumnos;
DROP TABLE IF EXISTS profesores;
DROP TABLE IF EXISTS cursos;

-- Create tables (from schema)
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

-- Populate the database with sample data

-- 1. Insertar cursos
INSERT INTO cursos (codigo, nombre) VALUES 
('ICC5130', 'Diseño de Software Verificable'),
('ICC5119', 'Ingeniería de Software'),
('ICC5124', 'Diseño Avanzado de Base de Datos'),
('ICC5100', 'Introducción a la Programación'),
('ICC5200', 'Estructuras de Datos'),
('ICC5300', 'Algoritmos Avanzados'),
('ICC5400', 'Programación Orientada a Objetos'),
('ICC5500', 'Arquitectura de Software'),
('ICC5600', 'Desarrollo Web'),
('ICC5700', 'Inteligencia Artificial');

-- 2. Establecer prerequisitos entre cursos
-- ICC5200 (Estructuras de Datos) requiere ICC5100 (Introducción a la Programación)
INSERT INTO prerequisitos (curso_id, prerequisito_id) VALUES 
((SELECT id FROM cursos WHERE codigo = 'ICC5200'), (SELECT id FROM cursos WHERE codigo = 'ICC5100'));

-- ICC5300 (Algoritmos Avanzados) requiere ICC5200 (Estructuras de Datos)
INSERT INTO prerequisitos (curso_id, prerequisito_id) VALUES 
((SELECT id FROM cursos WHERE codigo = 'ICC5300'), (SELECT id FROM cursos WHERE codigo = 'ICC5200'));

-- ICC5400 (Programación Orientada a Objetos) requiere ICC5100 (Introducción a la Programación)
INSERT INTO prerequisitos (curso_id, prerequisito_id) VALUES 
((SELECT id FROM cursos WHERE codigo = 'ICC5400'), (SELECT id FROM cursos WHERE codigo = 'ICC5100'));

-- ICC5500 (Arquitectura de Software) requiere ICC5400 (Programación Orientada a Objetos)
INSERT INTO prerequisitos (curso_id, prerequisito_id) VALUES 
((SELECT id FROM cursos WHERE codigo = 'ICC5500'), (SELECT id FROM cursos WHERE codigo = 'ICC5400'));

-- ICC5119 (Ingeniería de Software) requiere ICC5400 (Programación Orientada a Objetos)
INSERT INTO prerequisitos (curso_id, prerequisito_id) VALUES 
((SELECT id FROM cursos WHERE codigo = 'ICC5119'), (SELECT id FROM cursos WHERE codigo = 'ICC5400'));

-- ICC5130 (Diseño de Software Verificable) requiere ICC5119 (Ingeniería de Software)
INSERT INTO prerequisitos (curso_id, prerequisito_id) VALUES 
((SELECT id FROM cursos WHERE codigo = 'ICC5130'), (SELECT id FROM cursos WHERE codigo = 'ICC5119'));

-- ICC5124 (Diseño Avanzado de Base de Datos) requiere ICC5200 (Estructuras de Datos)
INSERT INTO prerequisitos (curso_id, prerequisito_id) VALUES 
((SELECT id FROM cursos WHERE codigo = 'ICC5124'), (SELECT id FROM cursos WHERE codigo = 'ICC5200'));

-- ICC5600 (Desarrollo Web) requiere ICC5500 (Arquitectura de Software)
INSERT INTO prerequisitos (curso_id, prerequisito_id) VALUES 
((SELECT id FROM cursos WHERE codigo = 'ICC5600'), (SELECT id FROM cursos WHERE codigo = 'ICC5500'));

-- ICC5700 (Inteligencia Artificial) requiere ICC5300 (Algoritmos Avanzados)
INSERT INTO prerequisitos (curso_id, prerequisito_id) VALUES 
((SELECT id FROM cursos WHERE codigo = 'ICC5700'), (SELECT id FROM cursos WHERE codigo = 'ICC5300'));

-- 3. Insertar profesores
INSERT INTO profesores (nombre, correo) VALUES 
('Juan Pérez', 'juan.perez@universidad.cl'),
('María Rodríguez', 'maria.rodriguez@universidad.cl'),
('Carlos López', 'carlos.lopez@universidad.cl'),
('Ana González', 'ana.gonzalez@universidad.cl'),
('Roberto Sánchez', 'roberto.sanchez@universidad.cl'),
('Laura Martínez', 'laura.martinez@universidad.cl'),
('Miguel Fernández', 'miguel.fernandez@universidad.cl'),
('Carmen Díaz', 'carmen.diaz@universidad.cl'),
('José Torres', 'jose.torres@universidad.cl'),
('Isabel Ramírez', 'isabel.ramirez@universidad.cl');

-- 4. Insertar alumnos
INSERT INTO alumnos (nombre, correo, fecha_ingreso) VALUES 
('Pedro Gómez', 'pedro.gomez@universidad.cl', '2022-03-01'),
('Ana Martínez', 'ana.martinez@universidad.cl', '2023-03-01'),
('Luis Morales', 'luis.morales@universidad.cl', '2022-03-01'),
('Carla Vargas', 'carla.vargas@universidad.cl', '2023-03-01'),
('Jorge Castro', 'jorge.castro@universidad.cl', '2021-03-01'),
('Daniela Rojas', 'daniela.rojas@universidad.cl', '2021-03-01'),
('Felipe Núñez', 'felipe.nunez@universidad.cl', '2023-08-01'),
('Valentina Muñoz', 'valentina.munoz@universidad.cl', '2023-08-01'),
('Sebastián Silva', 'sebastian.silva@universidad.cl', '2022-08-01'),
('Camila Herrera', 'camila.herrera@universidad.cl', '2022-08-01'),
('Matías Araya', 'matias.araya@universidad.cl', '2021-08-01'),
('Javiera Pizarro', 'javiera.pizarro@universidad.cl', '2021-08-01'),
('Diego Campos', 'diego.campos@universidad.cl', '2024-03-01'),
('Paula Vega', 'paula.vega@universidad.cl', '2024-03-01'),
('Gabriel Bravo', 'gabriel.bravo@universidad.cl', '2024-03-01');

-- 5. Crear instancias de curso (para 2023 y 2024, periodos: 1=primer semestre, 2=segundo semestre, V=verano)
-- Año 2023, Primer semestre
INSERT INTO instancias_curso (curso_id, anio, periodo) VALUES
((SELECT id FROM cursos WHERE codigo = 'ICC5100'), 2023, '1'),
((SELECT id FROM cursos WHERE codigo = 'ICC5200'), 2023, '1'),
((SELECT id FROM cursos WHERE codigo = 'ICC5300'), 2023, '1'),
((SELECT id FROM cursos WHERE codigo = 'ICC5400'), 2023, '1');

-- Año 2023, Segundo semestre
INSERT INTO instancias_curso (curso_id, anio, periodo) VALUES
((SELECT id FROM cursos WHERE codigo = 'ICC5100'), 2023, '2'),
((SELECT id FROM cursos WHERE codigo = 'ICC5200'), 2023, '2'),
((SELECT id FROM cursos WHERE codigo = 'ICC5500'), 2023, '2'),
((SELECT id FROM cursos WHERE codigo = 'ICC5119'), 2023, '2');

-- Año 2024, Primer semestre
INSERT INTO instancias_curso (curso_id, anio, periodo) VALUES
((SELECT id FROM cursos WHERE codigo = 'ICC5100'), 2024, '1'),
((SELECT id FROM cursos WHERE codigo = 'ICC5200'), 2024, '1'),
((SELECT id FROM cursos WHERE codigo = 'ICC5300'), 2024, '1'),
((SELECT id FROM cursos WHERE codigo = 'ICC5400'), 2024, '1'),
((SELECT id FROM cursos WHERE codigo = 'ICC5500'), 2024, '1'),
((SELECT id FROM cursos WHERE codigo = 'ICC5130'), 2024, '1'),
((SELECT id FROM cursos WHERE codigo = 'ICC5124'), 2024, '1'),
((SELECT id FROM cursos WHERE codigo = 'ICC5600'), 2024, '1'),
((SELECT id FROM cursos WHERE codigo = 'ICC5700'), 2024, '1');

-- 6. Crear secciones para cada instancia de curso (algunas con porcentaje, otras con peso)
-- Secciones para 2023, Primer semestre
INSERT INTO secciones (instancia_curso_id, numero, usa_porcentaje) VALUES
((SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1'), 1, TRUE),
((SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1'), 2, FALSE),
((SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5200') AND anio = 2023 AND periodo = '1'), 1, TRUE),
((SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5300') AND anio = 2023 AND periodo = '1'), 1, TRUE),
((SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5400') AND anio = 2023 AND periodo = '1'), 1, TRUE);

-- Secciones para 2023, Segundo semestre
INSERT INTO secciones (instancia_curso_id, numero, usa_porcentaje) VALUES
((SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '2'), 1, TRUE),
((SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5200') AND anio = 2023 AND periodo = '2'), 1, TRUE),
((SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5500') AND anio = 2023 AND periodo = '2'), 1, FALSE),
((SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5119') AND anio = 2023 AND periodo = '2'), 1, TRUE);

-- Secciones para 2024, Primer semestre (selección)
INSERT INTO secciones (instancia_curso_id, numero, usa_porcentaje) VALUES
((SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2024 AND periodo = '1'), 1, TRUE),
((SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2024 AND periodo = '1'), 2, FALSE),
((SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5200') AND anio = 2024 AND periodo = '1'), 1, TRUE),
((SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5300') AND anio = 2024 AND periodo = '1'), 1, TRUE),
((SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5400') AND anio = 2024 AND periodo = '1'), 1, TRUE),
((SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5130') AND anio = 2024 AND periodo = '1'), 1, TRUE),
((SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5124') AND anio = 2024 AND periodo = '1'), 1, FALSE);

-- 7. Asignar profesores a secciones
-- Asignaciones para 2023, Primer semestre
INSERT INTO profesor_seccion (profesor_id, seccion_id) VALUES
((SELECT id FROM profesores WHERE nombre = 'Juan Pérez'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1)),
((SELECT id FROM profesores WHERE nombre = 'María Rodríguez'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 2)),
((SELECT id FROM profesores WHERE nombre = 'Carlos López'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5200') AND anio = 2023 AND periodo = '1') AND numero = 1)),
((SELECT id FROM profesores WHERE nombre = 'Ana González'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5300') AND anio = 2023 AND periodo = '1') AND numero = 1)),
((SELECT id FROM profesores WHERE nombre = 'Roberto Sánchez'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5400') AND anio = 2023 AND periodo = '1') AND numero = 1));

-- Algunas asignaciones para 2024, Primer semestre
INSERT INTO profesor_seccion (profesor_id, seccion_id) VALUES
((SELECT id FROM profesores WHERE nombre = 'Laura Martínez'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2024 AND periodo = '1') AND numero = 1)),
((SELECT id FROM profesores WHERE nombre = 'Miguel Fernández'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2024 AND periodo = '1') AND numero = 2)),
((SELECT id FROM profesores WHERE nombre = 'Carmen Díaz'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5130') AND anio = 2024 AND periodo = '1') AND numero = 1)),
((SELECT id FROM profesores WHERE nombre = 'José Torres'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5124') AND anio = 2024 AND periodo = '1') AND numero = 1));

-- 8. Inscribir alumnos en secciones
-- Inscripciones para 2023, Primer semestre (alumnos de primer año)
INSERT INTO alumno_seccion (alumno_id, seccion_id) VALUES
-- Alumnos en ICC5100, sección 1
((SELECT id FROM alumnos WHERE nombre = 'Pedro Gómez'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1)),
((SELECT id FROM alumnos WHERE nombre = 'Ana Martínez'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1)),
((SELECT id FROM alumnos WHERE nombre = 'Luis Morales'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1)),
-- Alumnos en ICC5100, sección 2
((SELECT id FROM alumnos WHERE nombre = 'Carla Vargas'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 2)),
((SELECT id FROM alumnos WHERE nombre = 'Jorge Castro'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 2)),
-- Alumnos de segundo año en cursos de primer año
((SELECT id FROM alumnos WHERE nombre = 'Daniela Rojas'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5200') AND anio = 2023 AND periodo = '1') AND numero = 1)),
((SELECT id FROM alumnos WHERE nombre = 'Sebastián Silva'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5300') AND anio = 2023 AND periodo = '1') AND numero = 1)),
((SELECT id FROM alumnos WHERE nombre = 'Camila Herrera'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5400') AND anio = 2023 AND periodo = '1') AND numero = 1));

-- Inscripciones para 2024, Primer semestre (ejemplo: alumnos nuevos)
INSERT INTO alumno_seccion (alumno_id, seccion_id) VALUES
-- Alumnos nuevos en ICC5100, sección 1
((SELECT id FROM alumnos WHERE nombre = 'Diego Campos'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2024 AND periodo = '1') AND numero = 1)),
((SELECT id FROM alumnos WHERE nombre = 'Paula Vega'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2024 AND periodo = '1') AND numero = 1)),
-- Alumno en curso avanzado (ya aprobó prerequisitos)
((SELECT id FROM alumnos WHERE nombre = 'Pedro Gómez'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5200') AND anio = 2024 AND periodo = '1') AND numero = 1)),
((SELECT id FROM alumnos WHERE nombre = 'Ana Martínez'), 
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5200') AND anio = 2024 AND periodo = '1') AND numero = 1));

-- 9. Crear tópicos de evaluación para algunas secciones
-- Tópicos para ICC5100, 2023, periodo 1, sección 1 (con porcentaje)
INSERT INTO topicos_evaluacion (seccion_id, nombre, valor, usa_porcentaje) VALUES
((SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1), 
 'Controles', 30.00, TRUE),
((SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1), 
 'Tareas', 30.00, TRUE),
((SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1), 
 'Examen', 40.00, TRUE);

-- Tópicos para ICC5100, 2023, periodo 1, sección 2 (con peso)
INSERT INTO topicos_evaluacion (seccion_id, nombre, valor, usa_porcentaje) VALUES
((SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 2), 
 'Controles', 3.00, FALSE),
((SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 2), 
 'Tareas', 3.00, FALSE),
((SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 2), 
 'Examen', 4.00, FALSE);

-- Tópicos para ICC5200, 2023, periodo 1, sección 1
INSERT INTO topicos_evaluacion (seccion_id, nombre, valor, usa_porcentaje) VALUES
((SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5200') AND anio = 2023 AND periodo = '1') AND numero = 1), 
 'Controles', 20.00, TRUE),
((SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5200') AND anio = 2023 AND periodo = '1') AND numero = 1), 
 'Proyecto', 40.00, TRUE),
((SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5200') AND anio = 2023 AND periodo = '1') AND numero = 1), 
 'Examen', 40.00, TRUE);

-- 10. Crear instancias de evaluación para los tópicos
-- Instancias para el tópico 'Controles' de ICC5100, 2023, periodo 1, sección 1
INSERT INTO instancias_evaluacion (topico_id, nombre, valor, opcional) VALUES
((SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Controles'), 
 'Control 1', 30.00, FALSE),
((SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Controles'), 
 'Control 2', 30.00, FALSE),
((SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Controles'), 
 'Control 3', 40.00, FALSE);

-- Instancias para el tópico 'Tareas' de ICC5100, 2023, periodo 1, sección 1
INSERT INTO instancias_evaluacion (topico_id, nombre, valor, opcional) VALUES
((SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Tareas'), 
 'Tarea 1', 20.00, FALSE),
((SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Tareas'), 
 'Tarea 2', 30.00, FALSE),
((SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Tareas'), 
 'Tarea 3', 30.00, FALSE),
((SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Tareas'), 
 'Tarea 4', 20.00, TRUE);

-- Instancia para el tópico 'Examen' de ICC5100, 2023, periodo 1, sección 1
INSERT INTO instancias_evaluacion (topico_id, nombre, valor, opcional) VALUES
((SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Examen'), 
 'Examen Final', 100.00, FALSE);

-- Instancias para el tópico 'Controles' de ICC5100, 2023, periodo 1, sección 2 (con peso)
INSERT INTO instancias_evaluacion (topico_id, nombre, valor, opcional) VALUES
((SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 2) AND nombre = 'Controles'), 
 'Control 1', 1.00, FALSE),
((SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 2) AND nombre = 'Controles'), 
 'Control 2', 1.00, FALSE),
((SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 2) AND nombre = 'Controles'), 
 'Control 3', 1.00, FALSE);

-- Instancias para el tópico 'Controles' de ICC5200, 2023, periodo 1, sección 1
INSERT INTO instancias_evaluacion (topico_id, nombre, valor, opcional) VALUES
((SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5200') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Controles'), 
 'Control 1', 50.00, FALSE),
((SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5200') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Controles'), 
 'Control 2', 50.00, FALSE);

-- Instancias para el tópico 'Proyecto' de ICC5200, 2023, periodo 1, sección 1
INSERT INTO instancias_evaluacion (topico_id, nombre, valor, opcional) VALUES
((SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5200') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Proyecto'), 
 'Entrega 1', 30.00, FALSE),
((SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5200') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Proyecto'), 
 'Entrega 2', 30.00, FALSE),
((SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5200') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Proyecto'), 
 'Entrega Final', 40.00, FALSE);

-- 11. Registrar notas para algunos alumnos
-- Notas para Pedro Gómez en ICC5100, 2023, periodo 1, sección 1
-- Primero, obtener el alumno_seccion_id
SET @alumno_seccion_id_pedro = (
    SELECT id FROM alumno_seccion 
    WHERE alumno_id = (SELECT id FROM alumnos WHERE nombre = 'Pedro Gómez') 
    AND seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1)
);

-- Notas para Control 1, 2 y 3
INSERT INTO notas (alumno_seccion_id, instancia_evaluacion_id, nota) VALUES
(@alumno_seccion_id_pedro, 
 (SELECT id FROM instancias_evaluacion WHERE topico_id = (SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Controles') AND nombre = 'Control 1'), 
 5.5),
(@alumno_seccion_id_pedro, 
 (SELECT id FROM instancias_evaluacion WHERE topico_id = (SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Controles') AND nombre = 'Control 2'), 
 6.2),
(@alumno_seccion_id_pedro, 
 (SELECT id FROM instancias_evaluacion WHERE topico_id = (SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Controles') AND nombre = 'Control 3'), 
 6.8);

-- Notas para Tareas 1, 2 y 3
INSERT INTO notas (alumno_seccion_id, instancia_evaluacion_id, nota) VALUES
(@alumno_seccion_id_pedro, 
 (SELECT id FROM instancias_evaluacion WHERE topico_id = (SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Tareas') AND nombre = 'Tarea 1'), 
 7.0),
(@alumno_seccion_id_pedro, 
 (SELECT id FROM instancias_evaluacion WHERE topico_id = (SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Tareas') AND nombre = 'Tarea 2'), 
 6.5),
(@alumno_seccion_id_pedro, 
 (SELECT id FROM instancias_evaluacion WHERE topico_id = (SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Tareas') AND nombre = 'Tarea 3'), 
 6.0);

-- Nota para Examen Final
INSERT INTO notas (alumno_seccion_id, instancia_evaluacion_id, nota) VALUES
(@alumno_seccion_id_pedro, 
 (SELECT id FROM instancias_evaluacion WHERE topico_id = (SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Examen') AND nombre = 'Examen Final'), 
 5.8);

-- Notas para Ana Martínez en ICC5100, 2023, periodo 1, sección 1
SET @alumno_seccion_id_ana = (
    SELECT id FROM alumno_seccion 
    WHERE alumno_id = (SELECT id FROM alumnos WHERE nombre = 'Ana Martínez') 
    AND seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1)
);

-- Notas para Control 1, 2 y 3
INSERT INTO notas (alumno_seccion_id, instancia_evaluacion_id, nota) VALUES
(@alumno_seccion_id_ana, 
 (SELECT id FROM instancias_evaluacion WHERE topico_id = (SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Controles') AND nombre = 'Control 1'), 
 6.0),
(@alumno_seccion_id_ana, 
 (SELECT id FROM instancias_evaluacion WHERE topico_id = (SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Controles') AND nombre = 'Control 2'), 
 6.5),
(@alumno_seccion_id_ana, 
 (SELECT id FROM instancias_evaluacion WHERE topico_id = (SELECT id FROM topicos_evaluacion WHERE seccion_id = (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1) AND nombre = 'Controles') AND nombre = 'Control 3'), 
 7.0);

-- 12. Registrar cursos aprobados
-- Pedro Gómez aprueba ICC5100 (2023-1)
INSERT INTO cursos_aprobados (alumno_id, curso_id, seccion_id, nota_final, aprobado, fecha_aprobacion) VALUES
((SELECT id FROM alumnos WHERE nombre = 'Pedro Gómez'),
 (SELECT id FROM cursos WHERE codigo = 'ICC5100'),
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1),
 6.2, TRUE, '2023-07-15');

-- Ana Martínez aprueba ICC5100 (2023-1)
INSERT INTO cursos_aprobados (alumno_id, curso_id, seccion_id, nota_final, aprobado, fecha_aprobacion) VALUES
((SELECT id FROM alumnos WHERE nombre = 'Ana Martínez'),
 (SELECT id FROM cursos WHERE codigo = 'ICC5100'),
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1),
 6.5, TRUE, '2023-07-15');

-- Luis Morales aprueba ICC5100 (2023-1)
INSERT INTO cursos_aprobados (alumno_id, curso_id, seccion_id, nota_final, aprobado, fecha_aprobacion) VALUES
((SELECT id FROM alumnos WHERE nombre = 'Luis Morales'),
 (SELECT id FROM cursos WHERE codigo = 'ICC5100'),
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 1),
 5.8, TRUE, '2023-07-15');

-- Carla Vargas aprueba ICC5100 (2023-1)
INSERT INTO cursos_aprobados (alumno_id, curso_id, seccion_id, nota_final, aprobado, fecha_aprobacion) VALUES
((SELECT id FROM alumnos WHERE nombre = 'Carla Vargas'),
 (SELECT id FROM cursos WHERE codigo = 'ICC5100'),
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5100') AND anio = 2023 AND periodo = '1') AND numero = 2),
 5.9, TRUE, '2023-07-15');

-- Daniela Rojas aprueba ICC5200 (2023-1)
INSERT INTO cursos_aprobados (alumno_id, curso_id, seccion_id, nota_final, aprobado, fecha_aprobacion) VALUES
((SELECT id FROM alumnos WHERE nombre = 'Daniela Rojas'),
 (SELECT id FROM cursos WHERE codigo = 'ICC5200'),
 (SELECT id FROM secciones WHERE instancia_curso_id = (SELECT id FROM instancias_curso WHERE curso_id = (SELECT id FROM cursos WHERE codigo = 'ICC5200') AND anio = 2023 AND periodo = '1') AND numero = 1),
 6.3, TRUE, '2023-07-15');

-- Grant privileges
GRANT ALL PRIVILEGES ON sga_db.* TO 'sga_user'@'%';
FLUSH PRIVILEGES;