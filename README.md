# Sistema de Gestión Académica (SGA)

Este proyecto implementa un sistema de gestión académica centrado en el registro de cursos, profesores, alumnos y evaluaciones.

## Características principales

- Gestión de cursos y sus requisitos
- Gestión de profesores 
- Gestión de alumnos
- Gestión de instancias de cursos por período académico
- Gestión de secciones
- Sistema de evaluación flexible (tópicos e instancias)
- Registro y cálculo de notas

## Requisitos técnicos

- Python 3.9 o superior
- Flask
- MySQL

## Instrucciones de instalación

1. Clone el repositorio:
   ```
   git clone <url-del-repositorio>
   cd sga
   ```

2. Cree un entorno virtual e instale las dependencias:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure la base de datos:
   - Asegúrese de tener MySQL instalado y en ejecución
   - Cree una base de datos llamada `sga_db` o modifique el nombre en `config.py`
   - Actualice las credenciales de la base de datos en `config.py` si es necesario

4. Configure las variables de entorno:
   - Cree un archivo `.env` en la raíz del proyecto con las siguientes variables:
   ```
   # Variables para Flask
   FLASK_APP=
   FLASK_ENV=
   FLASK_PORT=

   # Variables para la base de datos
   MYSQL_HOST=
   MYSQL_USER=
   MYSQL_PASSWORD=
   MYSQL_DB=
   MYSQL_ROOT_PASSWORD=
   MYSQL_PORT=
   SECRET_KEY=
   ```
   - Complete cada variable con el valor correspondiente según su entorno local

5. Ejecute la aplicación:
   ```
   python app.py
   ```

6. Acceda a la aplicación en su navegador:
   ```
   http://localhost:5000
   ```

## Ejecución con Docker

Para ejecutar la aplicación utilizando Docker, siga los siguientes pasos:

1. Asegúrese de tener Docker y Docker Compose instalados en su sistema.

2. Verifique que el archivo `.env` esté configurado correctamente, con `MYSQL_HOST=db` para el entorno Docker.

3. Construya los contenedores (primera vez o cuando se realicen cambios):
   ```
   docker-compose build --no-cache
   ```

4. Inicie los servicios:
   ```
   docker-compose up
   ```
   
   Para ejecutar en segundo plano, use:
   ```
   docker-compose up -d
   ```

5. Acceda a la aplicación en su navegador:
   ```
   http://localhost:5000
   ```

6. Para detener los contenedores:
   ```
   docker-compose down
   ```

   Para detener y eliminar volúmenes (esto eliminará los datos persistentes):
   ```
   docker-compose down -v
   ```

7. Para ejecutar pruebas dentro del contenedor:
   ```
   docker exec -it sga2-web-1 pytest -v
   ```
   
   Para ejecutar pruebas con cobertura:
   ```
   docker exec -it sga2-web-1 pytest --cov=. tests/
   ```

## Estructura del proyecto

- `app.py`: Punto de entrada de la aplicación
- `config.py`: Configuración de la aplicación
- `db.py`: Conexión a la base de datos
- `schema.sql`: Scripts de creación de tablas
- `models/`: Contiene los modelos de datos
- `querys/`: Creamos queries para cada modulo
- `routes/`: Contiene las rutas de la aplicación
- `templates/`: Contiene las plantillas HTML
- `static/`: Contiene los recursos estáticos (CSS, JS, etc.)

## Estructuras clave

### Cursos
Los cursos tienen código, nombre y pueden tener requisitos (otros cursos).

### Instancias de Cursos
Representan un curso dictado en un periodo específico (año y semestre).

### Secciones
Divisiones de una instancia de curso, cada una puede tener diferentes profesores y alumnos. Cada sección puede configurarse para usar evaluación por porcentaje o por peso mediante el campo `usa_porcentaje`.

### Profesores por Sección
La relación muchos a muchos entre profesores y secciones permite asignar múltiples profesores a cada sección y que un profesor pueda estar asociado a varias secciones.

### Alumno-Sección
La relación entre alumnos y secciones permite a un alumno inscribirse en múltiples secciones y a una sección tener múltiples alumnos.

### Evaluaciones
Cada sección tiene tópicos de evaluación (controles, tareas, etc.) con un porcentaje o peso. Cada tópico puede configurarse para usar evaluación por porcentaje o por peso para sus instancias mediante el campo `usa_porcentaje`. Cada tópico puede tener múltiples instancias de evaluación (p.ej. "Control 1", "Control 2").

### Notas
Registro de las calificaciones de los alumnos en cada instancia de evaluación.

### Cursos Aprobados
Registro de los cursos que los alumnos han completado, incluyendo la nota final, si fue aprobado o no, y la fecha de aprobación. Esta estructura es fundamental para el seguimiento del historial académico de los estudiantes.

## Aclaraciones sobre el sistema de evaluación

- Cada tópico de evaluación tiene un porcentaje o peso del total de la nota final, según la configuración de la sección
- Cada instancia de evaluación tiene un porcentaje o peso dentro de su tópico, según la configuración del tópico
- Las instancias pueden ser opcionales, en cuyo caso no afectan al promedio si no existen
- Si una instancia no es opcional (obligatoria) y no tiene nota, se considera como un 1.0

## Guía de uso de la aplicación web

**Nota importante**: Todos los módulos del sistema disponen de operaciones CRUD completas (Crear, Leer, Actualizar y Eliminar).

### Gestión de Cursos
- **Acceder**: Se puede acceder desde la página de inicio o desde el navbar.
- **Operaciones**: Se pueden realizar todas las acciones CRUD (Crear, Leer, Actualizar, Eliminar).
- **Crear un curso**: 
  - Introduzca un código único (Ejemplo: ICC5130)
  - Añada el nombre del curso
- **Requisitos**: En la vista detallada de un curso específico, puede agregar los requisitos previos para ese curso.

### Gestión de Profesores y Alumnos
- **Acceder**: Seleccione el tópico correspondiente en el navbar o en la página de inicio.
- **Operaciones**: Se pueden realizar todas las acciones CRUD.
- **Crear**: Complete todos los datos requeridos y el usuario será creado.

### Gestión de Instancias de Curso
- **Acceder**: Vaya desde el navbar o la página de inicio.
- **Operaciones**: Se pueden realizar todas las acciones CRUD.
- **Crear**: Seleccione un curso existente, el año y el periodo académico (verano, primer semestre o invierno).

### Gestión de Secciones
- **Acceder**: Desde el navbar, la página de inicio o a través de la opción "Ver" en la instancia de curso.
- **Operaciones**: Se pueden realizar todas las acciones CRUD.
- **Crear**:
  - Seleccione una instancia de curso ya creada
  - Asigne un número de sección (debe ser único)
  - Elija si los tópicos de evaluación se calcularán por porcentaje o peso
- **Gestionar participantes**:
  - Dentro de una sección creada, puede agregar profesores y alumnos existentes
  - Los alumnos solo pueden inscribirse si han aprobado los cursos requisito o si el curso no tiene requisitos
- **Detalles**: En la vista detallada de la sección puede editar, eliminar, agregar tópicos de evaluación y ver las notas específicas.

### Gestión de Tópicos de Evaluación
- **Acceder**: Dentro de la vista de sección, use el botón "Añadir Tópico de Evaluación".
- **Operaciones**: Se pueden realizar todas las acciones CRUD.
- **Crear**:
  - Seleccione la sección en el menú desplegable
  - Asigne un nombre al tópico
  - Especifique el porcentaje (o peso, según la configuración de la sección)
  - Determine si las instancias de este tópico se calcularán por porcentaje o peso
- **Listar**: Para ver todos los tópicos, acceda a la sección "Evaluación" en el navbar.

### Gestión de Instancias de Evaluación
- **Acceder**: Desde la vista detallada de un tópico de evaluación específico.
- **Operaciones**: Se pueden realizar todas las acciones CRUD.
- **Crear**:
  - Visualice el resumen del tópico de evaluación
  - Asigne un nombre a la instancia
  - Especifique el porcentaje o peso (según la configuración del tópico)
  - Marque la opción "Opcional" si desea que no se compare con el resto de instancias del tópico

### Gestión de Notas
- **Acceder**: Desde la sección "Notas" o en la página de inicio.
- **Operaciones**: Se pueden realizar todas las acciones CRUD.
- **Crear**:
  - Seleccione la sección
  - Elija el alumno (solo aparecerán los alumnos inscritos en esa sección)
  - Seleccione la instancia de evaluación
  - Asigne la nota
- **Visualizar**: Las notas específicas de una sección se pueden ver en los detalles de dicha sección.