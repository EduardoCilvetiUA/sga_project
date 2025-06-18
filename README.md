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
- **Gestión completa de salas de clases (CRUD)**
- **Sistema de horarios con validaciones**
- **Carga masiva de datos en formato JSON**
- **Generación automática de horarios**
- **Visualización de horarios en calendario**
- **Exportación de horarios a Excel**
- **Control de capacidad de salas**
- **Créditos y estado de los cursos**

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
   docker exec -it sga_project-web-1 pytest -v
   ```
   
   Para ejecutar pruebas con cobertura:
   ```
   docker exec -it sga_project-web-1 pytest --cov=. tests/
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
- **`utils/`**: Contiene utilidades del sistema
  - **Generador de horarios**: Archivo para la generación automática de horarios
  - **Cargador de JSON**: Archivo para procesar las cargas masivas de datos en formato JSON

## Estructuras clave

### Cursos
Los cursos tienen código, nombre y pueden tener requisitos (otros cursos). **Nuevos atributos**:
- **`creditos`**: Número de créditos académicos (por defecto: 2)
- **`cerrado`**: Indica si el curso está cerrado para inscripción (por defecto: false)

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

### **Nuevas estructuras**

### Salas de Clases
- **`id`**: Identificador único
- **`nombre`**: Nombre de la sala (único)
- **`capacidad`**: Número máximo de estudiantes (debe ser mayor a 0)

### Horarios
- **`id`**: Identificador único  
- **`seccion_id`**: Referencia a la sección
- **`sala_id`**: Referencia a la sala asignada
- **`dia`**: Día de la semana (Lunes-Viernes)
- **`hora_inicio`**: Hora de inicio de la clase
- **`hora_fin`**: Hora de término de la clase

#### Validaciones de horarios:
- El horario debe estar entre 09:00 y 18:00
- La hora de inicio debe ser anterior a la hora de fin
- Se prohíben clases que crucen el horario de almuerzo (13:00-14:00)
- Cada sala puede tener solo un horario por día y hora específica

## Formatos de datos para carga masiva

### Formato JSON para Alumnos
```json
{
  "alumnos": [
    {
      "id": 1,
      "nombre": "Juan Pérez",
      "correo": "juan.perez@ejemplo.com",
      "anio_ingreso": 2023
    }
  ]
}
```

### Formato JSON para Profesores
```json
{
  "profesores": [
    {
      "id": 1,
      "nombre": "María González",
      "correo": "maria.gonzalez@ejemplo.com"
    }
  ]
}
```

### Formato JSON para Cursos
```json
{
  "cursos": [
    {
      "id": 20,
      "codigo": "ICC1001",
      "descripcion": "Introducción a la Programación",
      "requisitos": [],
      "creditos": 2
    },
    {
      "id": 19,
      "codigo": "ICC1002",
      "descripcion": "Estructuras de Datos",
      "requisitos": [
        "ICC1001"
      ],
      "creditos": 1
    }
  ]
}
```

### Formato JSON para Salas
```json
{
  "salas": [
    {
      "id": 1,
      "nombre": "Reloj 102",
      "capacidad": 17
    },
    {
      "id": 2,
      "nombre": "Ciencias 506",
      "capacidad": 45
    }
  ]
}
```

### Formato JSON para Instancias de Curso
```json
{
  "año": 2025,
  "semestre": 1,
  "instancias": [
    {
      "id": 1,
      "curso_id": 20
    },
    {
      "id": 2,
      "curso_id": 19
    }
  ]
}
```

### Formato JSON para Secciones con Evaluación
```json
{
  "secciones": [
    {
      "id": 1,
      "instancia_curso": 1,
      "profesor_id": 5,
      "evaluacion": {
        "tipo": "porcentaje",
        "combinacion_topicos": [
          {
            "id": 1,
            "nombre": "Pruebas",
            "valor": 30.0
          },
          {
            "id": 2,
            "nombre": "Proyecto",
            "valor": 70.0
          }
        ],
        "topicos": {
          "1": {
            "id": 1,
            "cantidad": 2,
            "tipo": "porcentaje",
            "valores": [50.0, 50.0],
            "obligatorias": [true, true]
          },
          "2": {
            "id": 2,
            "cantidad": 3,
            "tipo": "peso",
            "valores": [1, 2, 2],
            "obligatorias": [true, false, true]
          }
        }
      }
    }
  ]
}
```

### Formato JSON para Alumnos por Sección
```json
{
  "alumnos_seccion": [
    {
      "seccion_id": 1,
      "alumno_id": 1
    },
    {
      "seccion_id": 1,
      "alumno_id": 2
    }
  ]
}
```

### Formato JSON para Notas
```json
{
  "notas": [
    {
      "alumno_id": 1,
      "topico_id": 1,
      "instancia": 1,
      "nota": 6.3
    },
    {
      "alumno_id": 1,
      "topico_id": 2,
      "instancia": 1,
      "nota": 4.9
    }
  ]
}
```

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
  - **Especifique el número de créditos (por defecto: 2)**
  - **Marque si el curso está cerrado para inscripción**
- **Requisitos**: En la vista detallada de un curso específico, puede agregar los requisitos previos para ese curso.

### Gestión de Profesores y Alumnos
- **Acceder**: Seleccione el tópico correspondiente en el navbar o en la página de inicio.
- **Operaciones**: Se pueden realizar todas las acciones CRUD.
- **Crear**: Complete todos los datos requeridos y el usuario será creado.

### **Carga Masiva de Datos**
- **Acceder**: Desde el navbar o la página de inicio, sección "Carga Masiva de Datos".
- **Funcionalidades disponibles**:
  - Carga de alumnos en masa
  - Carga de profesores en masa
  - Carga de cursos y prerrequisitos en masa
  - Carga de salas en masa
  - Carga de instancias de curso en masa
  - Carga de secciones en masa
  - Carga de inscripciones de alumnos en secciones
  - Carga de notas en masa
- **Importante**: Cada tipo de carga requiere un formato JSON específico. Si el formato no es correcto, el sistema mostrará un error indicando la estructura esperada.

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

### **Gestión de Salas** (CRUD completo)
- **Acceder**: Desde el navbar o la página de inicio.
- **Operaciones**: Se pueden realizar todas las acciones CRUD.
- **Crear**:
  - Asigne un nombre único a la sala
  - Especifique la capacidad máxima (debe ser mayor a 0)
- **Gestión**: Las salas se pueden asociar a horarios específicos de las secciones.

### **Sistema de Gestión de Horarios**
- **Acceder**: Desde el navbar, sección "Gestión de Horarios".
- **Funcionalidades principales**:

#### Generar Horarios (Automático)
- **Función**: Asignar automáticamente horarios a todas las secciones sin conflictos
- **Operación**: 
  - Seleccione el año y período académico
  - Haga clic en "Generar Horarios"
  - El sistema asignará automáticamente horarios a todas las secciones
- **Algoritmo de generación**:
  - Considera la disponibilidad de salas según su capacidad
  - Evita conflictos de profesores y alumnos
  - Respeta el número de créditos de cada curso (máximo 4 horas consecutivas)
  - Horarios permitidos: Lunes a Viernes, 9:00 a 18:00 (excepto 13:00-14:00)
  - Las secciones con más de 4 créditos no se programarán
  - Las secciones sin profesores asignados no se programarán

#### Ver Horarios
- **Función**: Visualizar horarios existentes en formato calendario
- **Operación**: Seleccione el año y período para ver todos los horarios en una vista de calendario
- **Filtros disponibles**:
  - Por día de la semana
  - Por sala específica
  - Por curso específico
  - Por profesor específico

#### Exportar a Excel
- **Función**: Descargar horarios en formato Excel
- **Operación**: Seleccione el año y período, el sistema generará automáticamente un archivo Excel con todos los horarios
- **Contenido del archivo**: 
  - Hoja "Horarios": Todos los horarios generales
  - Hoja "Salas": Horarios organizados por sala
  - Hoja "Cursos": Horarios organizados por curso y sección
  - Hoja "Profesores": Horarios organizados por profesor

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

Claro, aquí tienes un texto en formato README, redactado en tercera persona, que explica las funcionalidades implementadas en la tercera parte del proyecto, tomando en cuenta las aclaraciones proporcionadas:

## Nuevas Funcionalidades - Entrega 3

### Cierre de Instancias de Curso

#### **Funcionalidad de Cierre**
- **Acceder**: Desde la vista detallada de una instancia de curso específica.
- **Operación**: Utilice el botón "Cerrar Instancia" para finalizar el período académico.
- **Proceso automático**:
  - Al cerrar una instancia, el sistema calcula automáticamente las notas finales de todos los alumnos inscritos en las secciones correspondientes
  - Las notas finales se generan basándose en la configuración de evaluación de cada sección (porcentaje o peso)
  - Se considera el estado de todas las instancias de evaluación (obligatorias y opcionales)

#### **Restricciones para Instancias Cerradas**
Una vez que una instancia de curso está cerrada:
- **No es posible editar** la información de la instancia
- **No es posible modificar** las secciones asociadas a la instancia
- **No se pueden agregar** nuevos tópicos de evaluación
- **No se pueden modificar** las notas existentes
- **No se pueden inscribir** nuevos alumnos
- Estas restricciones garantizan la integridad de las notas finales calculadas

### Sistema de Reportes

#### **Reporte de Notas por Instancia de Tópico**
- **Función**: Generar reporte de notas de una evaluación específica
- **Ejemplo**: Notas de la "Entrega 2 del Proyecto" de la sección 1 del curso ICC5130 202501
- **Acceso**: Desde la vista detallada de la instancia de evaluación correspondiente
- **Contenido**: Lista de todos los alumnos con sus notas en esa evaluación específica

#### **Reporte de Notas Finales por Sección**
- **Función**: Generar reporte de notas finales de una sección completa
- **Ejemplo**: Notas finales de la sección 1 de ICC5130 202501
- **Restricción**: Solo disponible para cursos con instancias cerradas
- **Acceso**: Desde la vista detallada de la sección
- **Contenido**: Lista completa de alumnos con sus notas finales calculadas y estado de aprobación

#### **Certificado de Notas del Alumno**
- **Función**: Generar certificado académico completo de un estudiante
- **Acceso**: Desde el perfil del alumno o sección de reportes
- **Contenido incluido**:
  - Todas las notas de cursos cerrados tomados por el alumno
  - Nota final obtenida en cada curso
  - Información del curso (código y nombre)
  - Instancia específica (año/semestre)
  - Sección cursada
  - Fecha de cursado
  - Estado de aprobación
- **Formato**: Reporte ordenado cronológicamente para facilitar la revisión del historial académico

### Manejo Robusto de Errores y Validaciones

#### **Validación en Carga Masiva**
El sistema cuenta con validación exhaustiva para la carga masiva de datos (implementado desde entregas anteriores):
- **Validación de formato JSON**: Detecta automáticamente si el archivo no tiene el formato JSON correcto
- **Validación de estructura**: Verifica que la estructura del JSON coincida con el formato esperado para cada tipo de carga
- **Validación de datos**: Comprueba que los datos cumplan con las restricciones de la base de datos (valores únicos, tipos de datos, etc.)
- **Mensajes de error específicos**: El sistema proporciona mensajes detallados indicando exactamente qué está mal en el archivo cargado
- **Prevención de errores**: No hay problemas al equivocarse en subir un JSON incorrecto o con parámetros mal definidos, ya que el sistema identifica y reporta el error

#### **Robustez General del Sistema**
- **Validación de formularios**: Todos los formularios incluyen validación tanto en frontend como backend
- **Manejo de excepciones**: El sistema captura y maneja apropiadamente todas las excepciones que puedan ocurrir
- **Mensajes informativos**: Los usuarios reciben mensajes claros sobre cualquier error o problema encontrado
- **Prevención de estados inconsistentes**: El sistema previene operaciones que podrían dejar la base de datos en un estado inconsistente
- **Validación de integridad**: Se verifican todas las relaciones entre entidades antes de realizar operaciones
- **Transacciones seguras**: Las operaciones críticas se realizan dentro de transacciones para garantizar consistencia