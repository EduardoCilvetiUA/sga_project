import json
import os
from db import execute_query
from querys.json_loader_queries import (
    check_alumno_exists,
    update_alumno,
    insert_alumno,
    check_profesor_exists,
    update_profesor,
    insert_profesor,
    check_curso_exists,
    update_curso,
    insert_curso,
    delete_prerequisitos,
    insert_prerequisito,
    check_sala_exists,
    update_sala,
    insert_sala,
    check_instancia_exists,
    update_instancia,
    insert_instancia,
    check_curso_exists_by_id,
    check_seccion_exists,
    update_seccion,
    insert_seccion,
    check_profesor_seccion_exists,
    insert_profesor_seccion,
    check_topico_exists,
    update_topico,
    insert_topico,
    delete_instancias_evaluacion,
    insert_instancia_evaluacion,
    check_seccion_exists_by_id,
    check_alumno_exists_by_id,
    check_alumno_seccion_exists,
    insert_alumno_seccion,
    check_topico_exists_by_id,
    get_seccion_id_from_topico,
    check_alumno_seccion_by_seccion,
    get_instancia_evaluacion_by_offset,
    check_nota_exists,
    update_nota,
    insert_nota,
    get_max_section_number,
)


class JsonLoader:
    @staticmethod
    def load_file(file_path):
        """Carga un archivo JSON y retorna su contenido"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            raise ValueError(f"Error al cargar el archivo JSON: {str(e)}")

    @staticmethod
    def validate_percentage_distribution(valores, normalizar=False):
        """
        Valida que los valores porcentuales sumen 100%.
        Si normalizar=True, ajusta los valores para que sumen 100%.
        """
        total = sum(valores)
        if abs(total - 100) < 0.01:  # Tolerancia para errores de punto flotante
            return valores  # Ya suman 100%

        if not normalizar:
            raise ValueError(f"Los porcentajes deben sumar 100%. Suma actual: {total}%")

        # Normalizar los valores para que sumen 100%
        factor = 100 / total
        return [round(valor * factor, 2) for valor in valores]

    @staticmethod
    def load_alumnos(file_path):
        """Carga alumnos desde un archivo JSON"""
        data = JsonLoader.load_file(file_path)

        if "alumnos" not in data:
            raise ValueError(
                "El archivo JSON no contiene la estructura esperada para alumnos"
            )

        result = {
            "total": len(data["alumnos"]),
            "exitosos": 0,
            "fallidos": 0,
            "errores": [],
        }

        for alumno in data["alumnos"]:
            try:
                # Validar campos requeridos
                if not all(
                    k in alumno for k in ["id", "nombre", "correo", "anio_ingreso"]
                ):
                    raise ValueError(
                        f"Alumno con ID {alumno.get('id', 'desconocido')} no tiene todos los campos requeridos"
                    )

                # Verificar si el alumno ya existe
                existing = execute_query(
                    check_alumno_exists, (alumno["id"],), fetch=True
                )

                if existing:
                    # Actualizar alumno existente
                    execute_query(
                        update_alumno,
                        (
                            alumno["nombre"],
                            alumno["correo"],
                            f"{alumno['anio_ingreso']}-01-01",
                            alumno["id"],
                        ),
                    )
                else:
                    # Insertar nuevo alumno con ID específico
                    execute_query(
                        insert_alumno,
                        (
                            alumno["id"],
                            alumno["nombre"],
                            alumno["correo"],
                            f"{alumno['anio_ingreso']}-01-01",
                        ),
                    )

                result["exitosos"] += 1
            except Exception as e:
                result["fallidos"] += 1
                result["errores"].append(
                    {"alumno_id": alumno.get("id", "desconocido"), "error": str(e)}
                )

        return result

    @staticmethod
    def load_profesores(file_path):
        """Carga profesores desde un archivo JSON"""
        data = JsonLoader.load_file(file_path)

        if "profesores" not in data:
            raise ValueError(
                "El archivo JSON no contiene la estructura esperada para profesores"
            )

        result = {
            "total": len(data["profesores"]),
            "exitosos": 0,
            "fallidos": 0,
            "errores": [],
        }

        for profesor in data["profesores"]:
            try:
                # Validar campos requeridos
                if not all(k in profesor for k in ["id", "nombre", "correo"]):
                    raise ValueError(
                        f"Profesor con ID {profesor.get('id', 'desconocido')} no tiene todos los campos requeridos"
                    )

                # Verificar si el profesor ya existe
                existing = execute_query(
                    check_profesor_exists, (profesor["id"],), fetch=True
                )

                if existing:
                    # Actualizar profesor existente
                    execute_query(
                        update_profesor,
                        (profesor["nombre"], profesor["correo"], profesor["id"]),
                    )
                else:
                    # Insertar nuevo profesor con ID específico
                    execute_query(
                        insert_profesor,
                        (profesor["id"], profesor["nombre"], profesor["correo"]),
                    )

                result["exitosos"] += 1
            except Exception as e:
                result["fallidos"] += 1
                result["errores"].append(
                    {"profesor_id": profesor.get("id", "desconocido"), "error": str(e)}
                )

        return result

    @staticmethod
    def load_cursos(file_path):
        """Carga cursos desde un archivo JSON"""
        data = JsonLoader.load_file(file_path)

        if "cursos" not in data:
            raise ValueError(
                "El archivo JSON no contiene la estructura esperada para cursos"
            )

        result = {
            "total": len(data["cursos"]),
            "exitosos": 0,
            "fallidos": 0,
            "errores": [],
        }

        # Primero insertamos/actualizamos los cursos
        for curso in data["cursos"]:
            try:
                # Validar campos requeridos
                if not all(k in curso for k in ["id", "codigo", "descripcion"]):
                    raise ValueError(
                        f"Curso con ID {curso.get('id', 'desconocido')} no tiene todos los campos requeridos"
                    )

                # El campo creditos es opcional, usar valor por defecto si no existe
                creditos = curso.get("creditos", 2)

                # Verificar si el curso ya existe
                existing = execute_query(check_curso_exists, (curso["id"],), fetch=True)

                if existing:
                    # Actualizar curso existente
                    execute_query(
                        update_curso,
                        (curso["codigo"], curso["descripcion"], creditos, curso["id"]),
                    )
                else:
                    # Insertar nuevo curso con ID específico
                    execute_query(
                        insert_curso,
                        (
                            curso["id"],
                            curso["codigo"],
                            curso["descripcion"],
                            creditos,
                            False,
                        ),
                    )

                result["exitosos"] += 1
            except Exception as e:
                result["fallidos"] += 1
                result["errores"].append(
                    {"curso_id": curso.get("id", "desconocido"), "error": str(e)}
                )

        # Ahora procesamos los prerrequisitos
        curso_codigos = {}
        # Primero creamos un mapeo de códigos a IDs
        for curso in data["cursos"]:
            curso_codigos[curso["codigo"]] = curso["id"]

        for curso in data["cursos"]:
            if "requisitos" in curso and isinstance(curso["requisitos"], list):
                try:
                    curso_id = curso["id"]

                    # Eliminar prerrequisitos existentes
                    execute_query(delete_prerequisitos, (curso_id,))

                    # Añadir los nuevos prerrequisitos
                    for req_codigo in curso["requisitos"]:
                        if req_codigo in curso_codigos:
                            req_id = curso_codigos[req_codigo]
                            execute_query(insert_prerequisito, (curso_id, req_id))
                        else:
                            raise ValueError(
                                f"No se encontró el curso con código {req_codigo}"
                            )
                except Exception as e:
                    # No contamos como error de inserción principal
                    result["errores"].append(
                        {
                            "curso_id": curso.get("id", "desconocido"),
                            "error": f"Error al establecer prerrequisitos: {str(e)}",
                        }
                    )

        return result

    @staticmethod
    def load_salas(file_path):
        """Carga salas desde un archivo JSON"""
        data = JsonLoader.load_file(file_path)

        if "salas" not in data:
            raise ValueError(
                "El archivo JSON no contiene la estructura esperada para salas"
            )

        result = {
            "total": len(data["salas"]),
            "exitosos": 0,
            "fallidos": 0,
            "errores": [],
        }

        for sala in data["salas"]:
            try:
                # Validar campos requeridos
                if not all(k in sala for k in ["id", "nombre", "capacidad"]):
                    raise ValueError(
                        f"Sala con ID {sala.get('id', 'desconocido')} no tiene todos los campos requeridos"
                    )

                # Verificar si la sala ya existe
                existing = execute_query(check_sala_exists, (sala["id"],), fetch=True)

                if existing:
                    # Actualizar sala existente
                    execute_query(
                        update_sala, (sala["nombre"], sala["capacidad"], sala["id"])
                    )
                else:
                    # Insertar nueva sala con ID específico
                    execute_query(
                        insert_sala, (sala["id"], sala["nombre"], sala["capacidad"])
                    )

                result["exitosos"] += 1
            except Exception as e:
                result["fallidos"] += 1
                result["errores"].append(
                    {"sala_id": sala.get("id", "desconocido"), "error": str(e)}
                )

        return result

    @staticmethod
    def load_instancias_cursos(file_path):
        """Carga instancias de cursos desde un archivo JSON"""
        data = JsonLoader.load_file(file_path)

        if not all(k in data for k in ["año", "semestre", "instancias"]):
            raise ValueError(
                "El archivo JSON no tiene la estructura esperada para instancias de cursos"
            )

        result = {
            "total": len(data["instancias"]),
            "exitosos": 0,
            "fallidos": 0,
            "errores": [],
        }

        año = data["año"]
        semestre = data["semestre"]

        for instancia in data["instancias"]:
            try:
                # Validar campos requeridos
                if not all(k in instancia for k in ["id", "curso_id"]):
                    raise ValueError(
                        f"Instancia con ID {instancia.get('id', 'desconocido')} no tiene todos los campos requeridos"
                    )

                # Verificar que el curso exista
                curso_exists = execute_query(
                    check_curso_exists_by_id, (instancia["curso_id"],), fetch=True
                )

                if not curso_exists:
                    raise ValueError(
                        f"No existe un curso con ID {instancia['curso_id']}"
                    )

                # Verificar si la instancia ya existe
                existing = execute_query(
                    check_instancia_exists, (instancia["id"],), fetch=True
                )

                if existing:
                    # Actualizar instancia existente
                    execute_query(
                        update_instancia,
                        (instancia["curso_id"], año, str(semestre), instancia["id"]),
                    )
                else:
                    # Insertar nueva instancia con ID específico
                    execute_query(
                        insert_instancia,
                        (instancia["id"], instancia["curso_id"], año, str(semestre)),
                    )

                result["exitosos"] += 1
            except Exception as e:
                result["fallidos"] += 1
                result["errores"].append(
                    {
                        "instancia_id": instancia.get("id", "desconocido"),
                        "error": str(e),
                    }
                )

        return result

    @staticmethod
    def load_secciones(file_path):
        """Carga secciones y evaluaciones desde un archivo JSON"""
        data = JsonLoader.load_file(file_path)

        if "secciones" not in data:
            raise ValueError(
                "El archivo JSON no tiene la estructura esperada para secciones"
            )

        result = {
            "total": len(data["secciones"]),
            "exitosos": 0,
            "fallidos": 0,
            "errores": [],
        }

        for seccion in data["secciones"]:
            try:
                # Validar campos requeridos
                if not all(
                    k in seccion
                    for k in ["id", "instancia_curso", "profesor_id", "evaluacion"]
                ):
                    raise ValueError(
                        f"Sección con ID {seccion.get('id', 'desconocido')} no tiene todos los campos requeridos"
                    )

                # Verificar que la instancia de curso exista
                instancia_exists = execute_query(
                    check_instancia_exists, (seccion["instancia_curso"],), fetch=True
                )

                if not instancia_exists:
                    raise ValueError(
                        f"No existe una instancia de curso con ID {seccion['instancia_curso']}"
                    )

                # Verificar que el profesor exista
                profesor_exists = execute_query(
                    check_profesor_exists, (seccion["profesor_id"],), fetch=True
                )

                if not profesor_exists:
                    raise ValueError(
                        f"No existe un profesor con ID {seccion['profesor_id']}"
                    )

                # Procesar configuración de evaluación
                tipo_evaluacion = seccion["evaluacion"]["tipo"]
                usa_porcentaje = tipo_evaluacion == "porcentaje"

                # Verificar si la sección ya existe
                existing = execute_query(
                    check_seccion_exists, (seccion["id"],), fetch=True
                )
                max_numero = execute_query(
                    get_max_section_number, (seccion["instancia_curso"],), fetch=True
                )
                siguiente_numero = (max_numero[0]["max_num"] or 0) + 1

                if existing:
                    # Actualizar sección existente
                    execute_query(
                        update_seccion,
                        (
                            seccion["instancia_curso"],
                            siguiente_numero,
                            usa_porcentaje,
                            seccion["id"],
                        ),
                    )
                else:
                    # Insertar nueva sección con ID específico
                    execute_query(
                        insert_seccion,
                        (
                            seccion["id"],
                            seccion["instancia_curso"],
                            siguiente_numero,
                            usa_porcentaje,
                        ),
                    )

                # Asignar profesor a la sección
                profesor_seccion_exists = execute_query(
                    check_profesor_seccion_exists,
                    (seccion["profesor_id"], seccion["id"]),
                    fetch=True,
                )

                if not profesor_seccion_exists:
                    execute_query(
                        insert_profesor_seccion, (seccion["profesor_id"], seccion["id"])
                    )

                # Procesar tópicos de evaluación
                if "combinacion_topicos" in seccion["evaluacion"]:
                    topicos = seccion["evaluacion"]["combinacion_topicos"]

                    # Validar que los porcentajes sumen 100% si usa porcentaje
                    if usa_porcentaje:
                        valores = [topico["valor"] for topico in topicos]
                        total = sum(valores)

                        if abs(total - 100) > 0.1:  # Permitir pequeño margen de error
                            # Normalizar los porcentajes
                            factor = 100 / total
                            for i in range(len(valores)):
                                topicos[i]["valor"] = round(
                                    topicos[i]["valor"] * factor, 2
                                )

                    # Crear o actualizar tópicos
                    for topico in topicos:
                        topico_id = topico["id"]
                        topico_nombre = topico["nombre"]
                        topico_valor = topico["valor"]

                        # Verificar si el tópico existe en el JSON
                        topico_config = seccion["evaluacion"]["topicos"].get(
                            str(topico_id)
                        )
                        if not topico_config:
                            raise ValueError(
                                f"No se encontró la configuración para el tópico {topico_id}"
                            )

                        # Verificar si el tópico ya existe en la base de datos
                        existing_topico = execute_query(
                            check_topico_exists, (topico_id,), fetch=True
                        )

                        topico_usa_porcentaje = topico_config["tipo"] == "porcentaje"

                        if existing_topico:
                            # Actualizar tópico existente
                            execute_query(
                                update_topico,
                                (
                                    seccion["id"],
                                    topico_nombre,
                                    topico_valor,
                                    topico_usa_porcentaje,
                                    topico_id,
                                ),
                            )
                        else:
                            # Insertar nuevo tópico con ID específico
                            execute_query(
                                insert_topico,
                                (
                                    topico_id,
                                    seccion["id"],
                                    topico_nombre,
                                    topico_valor,
                                    topico_usa_porcentaje,
                                ),
                            )

                        # Procesar instancias de evaluación para este tópico
                        valores_instancias = topico_config["valores"]
                        obligatorias = topico_config["obligatorias"]
                        cantidad = topico_config["cantidad"]

                        # Validar que la cantidad coincida con los arrays
                        if (
                            len(valores_instancias) != cantidad
                            or len(obligatorias) != cantidad
                        ):
                            raise ValueError(
                                f"La cantidad de instancias no coincide con los valores proporcionados para el tópico {topico_id}"
                            )

                        # Validar que los porcentajes sumen 100% si usa porcentaje
                        if topico_usa_porcentaje:
                            total_instancias = sum(valores_instancias)
                            if (
                                abs(total_instancias - 100) > 0.1
                            ):  # Permitir pequeño margen de error
                                # Normalizar los porcentajes
                                factor = 100 / total_instancias
                                for i in range(len(valores_instancias)):
                                    valores_instancias[i] = round(
                                        valores_instancias[i] * factor, 2
                                    )

                        # Eliminar instancias existentes para este tópico
                        execute_query(delete_instancias_evaluacion, (topico_id,))

                        # Crear instancias de evaluación
                        for i in range(cantidad):
                            nombre_instancia = f"Instancia {i+1}"
                            valor_instancia = valores_instancias[i]
                            opcional = not obligatorias[i]

                            execute_query(
                                insert_instancia_evaluacion,
                                (
                                    topico_id,
                                    nombre_instancia,
                                    valor_instancia,
                                    opcional,
                                ),
                            )

                result["exitosos"] += 1
            except Exception as e:
                result["fallidos"] += 1
                result["errores"].append(
                    {"seccion_id": seccion.get("id", "desconocido"), "error": str(e)}
                )

        return result

    @staticmethod
    def load_alumnos_seccion(file_path):
        """Carga la asignación de alumnos a secciones desde un archivo JSON"""
        data = JsonLoader.load_file(file_path)

        if "alumnos_seccion" not in data:
            raise ValueError(
                "El archivo JSON no tiene la estructura esperada para alumnos por sección"
            )

        result = {
            "total": len(data["alumnos_seccion"]),
            "exitosos": 0,
            "fallidos": 0,
            "errores": [],
        }

        for asignacion in data["alumnos_seccion"]:
            try:
                # Validar campos requeridos
                if not all(k in asignacion for k in ["seccion_id", "alumno_id"]):
                    raise ValueError(
                        "La asignación no tiene todos los campos requeridos"
                    )

                # Verificar que la sección exista
                seccion_exists = execute_query(
                    check_seccion_exists_by_id, (asignacion["seccion_id"],), fetch=True
                )

                if not seccion_exists:
                    raise ValueError(
                        f"No existe una sección con ID {asignacion['seccion_id']}"
                    )

                # Verificar que el alumno exista
                alumno_exists = execute_query(
                    check_alumno_exists_by_id, (asignacion["alumno_id"],), fetch=True
                )

                if not alumno_exists:
                    raise ValueError(
                        f"No existe un alumno con ID {asignacion['alumno_id']}"
                    )

                # Verificar si ya existe la asignación
                existing = execute_query(
                    check_alumno_seccion_exists,
                    (asignacion["alumno_id"], asignacion["seccion_id"]),
                    fetch=True,
                )

                if not existing:
                    # Inscribir alumno en la sección
                    execute_query(
                        insert_alumno_seccion,
                        (asignacion["alumno_id"], asignacion["seccion_id"]),
                    )

                result["exitosos"] += 1
            except Exception as e:
                result["fallidos"] += 1
                result["errores"].append(
                    {
                        "alumno_id": asignacion.get("alumno_id", "desconocido"),
                        "seccion_id": asignacion.get("seccion_id", "desconocido"),
                        "error": str(e),
                    }
                )

        return result

    @staticmethod
    def load_notas(file_path):
        """Carga notas de alumnos desde un archivo JSON"""
        data = JsonLoader.load_file(file_path)

        if "notas" not in data:
            raise ValueError(
                "El archivo JSON no tiene la estructura esperada para notas"
            )

        result = {
            "total": len(data["notas"]),
            "exitosos": 0,
            "fallidos": 0,
            "errores": [],
        }

        for nota_data in data["notas"]:
            try:
                # Validar campos requeridos
                if not all(
                    k in nota_data
                    for k in ["alumno_id", "topico_id", "instancia", "nota"]
                ):
                    raise ValueError("La nota no tiene todos los campos requeridos")

                # Verificar que el alumno exista
                alumno_exists = execute_query(
                    check_alumno_exists_by_id, (nota_data["alumno_id"],), fetch=True
                )

                if not alumno_exists:
                    raise ValueError(
                        f"No existe un alumno con ID {nota_data['alumno_id']}"
                    )

                # Verificar que el tópico exista
                topico_exists = execute_query(
                    check_topico_exists_by_id, (nota_data["topico_id"],), fetch=True
                )

                if not topico_exists:
                    raise ValueError(
                        f"No existe un tópico con ID {nota_data['topico_id']}"
                    )

                seccion_id = execute_query(
                    get_seccion_id_from_topico, (nota_data["topico_id"],), fetch=True
                )

                if not seccion_id:
                    raise ValueError(
                        f"No se pudo obtener la sección del tópico {nota_data['topico_id']}"
                    )

                seccion_id = seccion_id[0]["seccion_id"]

                # Verificar que el alumno esté inscrito en la sección
                alumno_seccion = execute_query(
                    check_alumno_seccion_by_seccion,
                    (nota_data["alumno_id"], seccion_id),
                    fetch=True,
                )

                if not alumno_seccion:
                    raise ValueError(
                        f"El alumno con ID {nota_data['alumno_id']} no está inscrito en la sección del tópico {nota_data['topico_id']}"
                    )

                alumno_seccion_id = alumno_seccion[0]["id"]

                # Obtener la instancia de evaluación
                instancia_evaluacion = execute_query(
                    get_instancia_evaluacion_by_offset,
                    (nota_data["topico_id"], nota_data["instancia"] - 1),
                    fetch=True,
                )

                if not instancia_evaluacion:
                    raise ValueError(
                        f"No existe la instancia {nota_data['instancia']} para el tópico {nota_data['topico_id']}"
                    )

                instancia_id = instancia_evaluacion[0]["id"]

                # Validar la nota
                nota_valor = float(nota_data["nota"])
                if nota_valor < 1.0 or nota_valor > 7.0:
                    raise ValueError(
                        f"La nota debe estar entre 1.0 y 7.0. Valor: {nota_valor}"
                    )

                # Verificar si ya existe la nota
                existing = execute_query(
                    check_nota_exists, (alumno_seccion_id, instancia_id), fetch=True
                )

                if existing:
                    # Actualizar nota existente
                    execute_query(update_nota, (nota_valor, existing[0]["id"]))
                else:
                    # Insertar nueva nota
                    execute_query(
                        insert_nota, (alumno_seccion_id, instancia_id, nota_valor)
                    )

                result["exitosos"] += 1
            except Exception as e:
                result["fallidos"] += 1
                result["errores"].append(
                    {
                        "alumno_id": nota_data.get("alumno_id", "desconocido"),
                        "topico_id": nota_data.get("topico_id", "desconocido"),
                        "instancia": nota_data.get("instancia", "desconocido"),
                        "error": str(e),
                    }
                )

        return result
