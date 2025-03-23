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

4. Ejecute la aplicación:
   ```
   python app.py
   ```

5. Acceda a la aplicación en su navegador:
   ```
   http://localhost:5000
   ```

## Ejecución con Docker

Para ejecutar la aplicación utilizando Docker, siga los siguientes pasos:

1. Asegúrese de tener Docker y Docker Compose instalados en su sistema.

2. Construya los contenedores (primera vez o cuando se realicen cambios):
   ```
   docker-compose build --no-cache
   ```

3. Inicie los servicios:
   ```
   docker-compose up
   ```
   
   Para ejecutar en segundo plano, use:
   ```
   docker-compose up -d
   ```

4. Acceda a la aplicación en su navegador:
   ```
   http://localhost:5000
   ```

5. Para detener los contenedores:
   ```
   docker-compose down
   ```

   Para detener y eliminar volúmenes (esto eliminará los datos persistentes):
   ```
   docker-compose down -v
   ```

6. Para ejecutar pruebas dentro del contenedor:
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
- `routes/`: Contiene las rutas de la aplicación
- `templates/`: Contiene las plantillas HTML
- `static/`: Contiene los recursos estáticos (CSS, JS, etc.)

## Estructuras clave

### Cursos
Los cursos tienen código, nombre y pueden tener requisitos (otros cursos).

### Instancias de Cursos
Representan un curso dictado en un periodo específico (año y semestre).

### Secciones
Divisiones de una instancia de curso, cada una puede tener diferentes profesores y alumnos.

### Evaluaciones
Cada sección tiene tópicos de evaluación (controles, tareas, etc.) con un porcentaje. Cada tópico puede tener múltiples instancias de evaluación (p.ej. "Control 1", "Control 2").

### Notas
Registro de las calificaciones de los alumnos en cada instancia de evaluación.

## Aclaraciones sobre el sistema de evaluación

- Cada tópico de evaluación tiene un porcentaje del total de la nota final
- Cada instancia de evaluación tiene un peso dentro de su tópico
- Las instancias pueden ser opcionales, en cuyo caso no afectan al promedio si no existen
- Si una instancia no es opcional (obligatoria) y no tiene nota, se considera como un 1.0