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
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            raise ValueError(f"Error al cargar el archivo JSON: {str(e)}")

    @staticmethod
    def validate_percentage_distribution(valores, normalizar=False):
        total = sum(valores)
        if abs(total - 100) < 0.01:
            return valores

        if not normalizar:
            raise ValueError(f"Los porcentajes deben sumar 100%. Suma actual: {total}%")

        factor = 100 / total
        return [round(valor * factor, 2) for valor in valores]

    @staticmethod
    def _normalize_percentages(valores, umbral=0.1):
        total = sum(valores)
        if abs(total - 100) <= umbral:
            return valores
        
        factor = 100 / total
        return [round(valor * factor, 2) for valor in valores]

    @staticmethod
    def _create_result_template(count):
        return {
            "total": count,
            "exitosos": 0,
            "fallidos": 0,
            "errores": [],
        }

    @staticmethod
    def _check_required_fields(entity, required_fields, entity_type):
        entity_id = entity.get('id', 'desconocido')
        if not all(k in entity for k in required_fields):
            raise ValueError(f"{entity_type.capitalize()} con ID {entity_id} no tiene todos los campos requeridos")
        return entity_id

    @staticmethod
    def _process_entity(data, entity_key, check_query, update_query, insert_query, required_fields, format_insert_data, format_update_data=None):
        if entity_key not in data:
            raise ValueError(f"El archivo JSON no contiene la estructura esperada para {entity_key}")
        
        entities = data[entity_key]
        result = JsonLoader._create_result_template(len(entities))
        
        if format_update_data is None:
            format_update_data = format_insert_data
        
        for entity in entities:
            try:
                entity_id = JsonLoader._check_required_fields(entity, required_fields, entity_key[:-1])
                
                existing = execute_query(check_query, (entity_id,), fetch=True)
                
                if existing:
                    update_data = format_update_data(entity)
                    execute_query(update_query, update_data + (entity_id,))
                else:
                    insert_data = format_insert_data(entity)
                    execute_query(insert_query, (entity_id,) + insert_data)
                
                result["exitosos"] += 1
            except Exception as e:
                result["fallidos"] += 1
                result["errores"].append({f"{entity_key[:-1]}_id": entity_id, "error": str(e)})
        
        return result

    @staticmethod
    def _process_instancias_evaluacion(topico_id, topico_config):
        valores_instancias = topico_config["valores"]
        obligatorias = topico_config["obligatorias"]
        cantidad = topico_config["cantidad"]
        
        if len(valores_instancias) != cantidad or len(obligatorias) != cantidad:
            raise ValueError(f"La cantidad de instancias no coincide con los valores proporcionados para el tópico {topico_id}")
        
        if topico_config["tipo"] == "porcentaje":
            valores_instancias = JsonLoader._normalize_percentages(valores_instancias)
        
        execute_query(delete_instancias_evaluacion, (topico_id,))
        
        for i in range(cantidad):
            nombre_instancia = f"Instancia {i+1}"
            valor_instancia = valores_instancias[i]
            opcional = not obligatorias[i]
            
            execute_query(
                insert_instancia_evaluacion,
                (topico_id, nombre_instancia, valor_instancia, opcional)
            )

    @staticmethod
    def _process_topicos_evaluacion(seccion, usa_porcentaje, result):
        if "combinacion_topicos" not in seccion["evaluacion"]:
            return
            
        topicos = seccion["evaluacion"]["combinacion_topicos"]
        
        if usa_porcentaje:
            valores = [topico["valor"] for topico in topicos]
            topicos_normalizados = JsonLoader._normalize_percentages(valores)
            for i, valor in enumerate(topicos_normalizados):
                topicos[i]["valor"] = valor
        
        for topico in topicos:
            topico_id = topico["id"]
            topico_nombre = topico["nombre"]
            topico_valor = topico["valor"]
            
            topico_config = seccion["evaluacion"]["topicos"].get(str(topico_id))
            if not topico_config:
                raise ValueError(f"No se encontró la configuración para el tópico {topico_id}")
            
            existing_topico = execute_query(check_topico_exists, (topico_id,), fetch=True)
            
            topico_usa_porcentaje = topico_config["tipo"] == "porcentaje"
            
            if existing_topico:
                execute_query(
                    update_topico,
                    (seccion["id"], topico_nombre, topico_valor, topico_usa_porcentaje, topico_id)
                )
            else:
                execute_query(
                    insert_topico,
                    (topico_id, seccion["id"], topico_nombre, topico_valor, topico_usa_porcentaje)
                )
            
            JsonLoader._process_instancias_evaluacion(topico_id, topico_config)

    @staticmethod
    def load_alumnos(file_path):
        data = JsonLoader.load_file(file_path)
        
        def format_data(alumno):
            return (alumno["nombre"], alumno["correo"], f"{alumno['anio_ingreso']}-01-01")
        
        return JsonLoader._process_entity(
            data, "alumnos", check_alumno_exists, update_alumno, insert_alumno,
            ["id", "nombre", "correo", "anio_ingreso"], format_data
        )

    @staticmethod
    def load_profesores(file_path):
        data = JsonLoader.load_file(file_path)
        
        def format_data(profesor):
            return (profesor["nombre"], profesor["correo"])
        
        return JsonLoader._process_entity(
            data, "profesores", check_profesor_exists, update_profesor, insert_profesor,
            ["id", "nombre", "correo"], format_data
        )

    @staticmethod
    def load_salas(file_path):
        data = JsonLoader.load_file(file_path)
        
        def format_data(sala):
            return (sala["nombre"], sala["capacidad"])
        
        return JsonLoader._process_entity(
            data, "salas", check_sala_exists, update_sala, insert_sala,
            ["id", "nombre", "capacidad"], format_data
        )

    @staticmethod
    def _process_requisitos(cursos, curso_codigos, result):
        for curso in cursos:
            if "requisitos" in curso and isinstance(curso["requisitos"], list):
                try:
                    curso_id = curso["id"]
                    execute_query(delete_prerequisitos, (curso_id,))
                    
                    for req_codigo in curso["requisitos"]:
                        if req_codigo in curso_codigos:
                            req_id = curso_codigos[req_codigo]
                            execute_query(insert_prerequisito, (curso_id, req_id))
                        else:
                            raise ValueError(f"No se encontró el curso con código {req_codigo}")
                except Exception as e:
                    result["errores"].append({
                        "curso_id": curso.get("id", "desconocido"),
                        "error": f"Error al establecer prerrequisitos: {str(e)}"
                    })

    @staticmethod
    def load_cursos(file_path):
        data = JsonLoader.load_file(file_path)
        
        if "cursos" not in data:
            raise ValueError("El archivo JSON no contiene la estructura esperada para cursos")
        
        result = JsonLoader._create_result_template(len(data["cursos"]))
        
        curso_codigos = {}
        for curso in data["cursos"]:
            try:
                entity_id = JsonLoader._check_required_fields(curso, ["id", "codigo", "descripcion"], "curso")
                
                creditos = curso.get("creditos", 2)
                curso_codigos[curso["codigo"]] = curso["id"]
                
                existing = execute_query(check_curso_exists, (entity_id,), fetch=True)
                
                if existing:
                    execute_query(
                        update_curso,
                        (curso["codigo"], curso["descripcion"], creditos, entity_id)
                    )
                else:
                    execute_query(
                        insert_curso,
                        (entity_id, curso["codigo"], curso["descripcion"], creditos, False)
                    )
                
                result["exitosos"] += 1
            except Exception as e:
                result["fallidos"] += 1
                result["errores"].append({"curso_id": entity_id, "error": str(e)})
        
        JsonLoader._process_requisitos(data["cursos"], curso_codigos, result)
        return result

    @staticmethod
    def load_instancias_cursos(file_path):
        data = JsonLoader.load_file(file_path)
        
        if not all(k in data for k in ["año", "semestre", "instancias"]):
            raise ValueError("El archivo JSON no tiene la estructura esperada para instancias de cursos")
        
        result = JsonLoader._create_result_template(len(data["instancias"]))
        año = data["año"]
        semestre = data["semestre"]
        
        for instancia in data["instancias"]:
            try:
                entity_id = JsonLoader._check_required_fields(instancia, ["id", "curso_id"], "instancia")
                
                curso_exists = execute_query(check_curso_exists_by_id, (instancia["curso_id"],), fetch=True)
                
                if not curso_exists:
                    raise ValueError(f"No existe un curso con ID {instancia['curso_id']}")
                
                existing = execute_query(check_instancia_exists, (entity_id,), fetch=True)
                
                if existing:
                    execute_query(
                        update_instancia,
                        (instancia["curso_id"], año, str(semestre), entity_id)
                    )
                else:
                    execute_query(
                        insert_instancia,
                        (entity_id, instancia["curso_id"], año, str(semestre))
                    )
                
                result["exitosos"] += 1
            except Exception as e:
                result["fallidos"] += 1
                result["errores"].append({"instancia_id": entity_id, "error": str(e)})
        
        return result

    @staticmethod
    def load_secciones(file_path):
        data = JsonLoader.load_file(file_path)
        
        if "secciones" not in data:
            raise ValueError("El archivo JSON no tiene la estructura esperada para secciones")
        
        result = JsonLoader._create_result_template(len(data["secciones"]))
        
        for seccion in data["secciones"]:
            try:
                entity_id = JsonLoader._check_required_fields(
                    seccion, ["id", "instancia_curso", "profesor_id", "evaluacion"], "sección"
                )
                
                # Verificar dependencias
                if not execute_query(check_instancia_exists, (seccion["instancia_curso"],), fetch=True):
                    raise ValueError(f"No existe una instancia de curso con ID {seccion['instancia_curso']}")
                
                if not execute_query(check_profesor_exists, (seccion["profesor_id"],), fetch=True):
                    raise ValueError(f"No existe un profesor con ID {seccion['profesor_id']}")
                
                tipo_evaluacion = seccion["evaluacion"]["tipo"]
                usa_porcentaje = tipo_evaluacion == "porcentaje"
                
                # Procesar sección
                existing = execute_query(check_seccion_exists, (entity_id,), fetch=True)
                max_numero = execute_query(get_max_section_number, (seccion["instancia_curso"],), fetch=True)
                siguiente_numero = (max_numero[0]["max_num"] or 0) + 1
                
                if existing:
                    execute_query(
                        update_seccion,
                        (seccion["instancia_curso"], siguiente_numero, usa_porcentaje, entity_id)
                    )
                else:
                    execute_query(
                        insert_seccion,
                        (entity_id, seccion["instancia_curso"], siguiente_numero, usa_porcentaje)
                    )
                
                # Asignar profesor
                profesor_seccion_exists = execute_query(
                    check_profesor_seccion_exists,
                    (seccion["profesor_id"], entity_id),
                    fetch=True
                )
                
                if not profesor_seccion_exists:
                    execute_query(insert_profesor_seccion, (seccion["profesor_id"], entity_id))
                
                # Procesar tópicos
                JsonLoader._process_topicos_evaluacion(seccion, usa_porcentaje, result)
                
                result["exitosos"] += 1
            except Exception as e:
                result["fallidos"] += 1
                result["errores"].append({"seccion_id": entity_id, "error": str(e)})
        
        return result

    @staticmethod
    def load_alumnos_seccion(file_path):
        data = JsonLoader.load_file(file_path)
        
        if "alumnos_seccion" not in data:
            raise ValueError("El archivo JSON no tiene la estructura esperada para alumnos por sección")
        
        result = JsonLoader._create_result_template(len(data["alumnos_seccion"]))
        
        for asignacion in data["alumnos_seccion"]:
            try:
                alumno_id = asignacion.get("alumno_id", "desconocido")
                seccion_id = asignacion.get("seccion_id", "desconocido")
                
                if not all(k in asignacion for k in ["seccion_id", "alumno_id"]):
                    raise ValueError("La asignación no tiene todos los campos requeridos")
                
                # Verificar dependencias
                if not execute_query(check_seccion_exists_by_id, (seccion_id,), fetch=True):
                    raise ValueError(f"No existe una sección con ID {seccion_id}")
                
                if not execute_query(check_alumno_exists_by_id, (alumno_id,), fetch=True):
                    raise ValueError(f"No existe un alumno con ID {alumno_id}")
                
                # Inscribir alumno si no existe
                existing = execute_query(
                    check_alumno_seccion_exists,
                    (alumno_id, seccion_id),
                    fetch=True
                )
                
                if not existing:
                    execute_query(insert_alumno_seccion, (alumno_id, seccion_id))
                
                result["exitosos"] += 1
            except Exception as e:
                result["fallidos"] += 1
                result["errores"].append({
                    "alumno_id": alumno_id,
                    "seccion_id": seccion_id,
                    "error": str(e)
                })
        
        return result

    @staticmethod
    def load_notas(file_path):
        data = JsonLoader.load_file(file_path)
        
        if "notas" not in data:
            raise ValueError("El archivo JSON no tiene la estructura esperada para notas")
        
        result = JsonLoader._create_result_template(len(data["notas"]))
        
        for nota_data in data["notas"]:
            try:
                alumno_id = nota_data.get("alumno_id", "desconocido")
                topico_id = nota_data.get("topico_id", "desconocido")
                instancia_num = nota_data.get("instancia", "desconocido")
                
                if not all(k in nota_data for k in ["alumno_id", "topico_id", "instancia", "nota"]):
                    raise ValueError("La nota no tiene todos los campos requeridos")
                
                # Verificar dependencias
                if not execute_query(check_alumno_exists_by_id, (alumno_id,), fetch=True):
                    raise ValueError(f"No existe un alumno con ID {alumno_id}")
                
                if not execute_query(check_topico_exists_by_id, (topico_id,), fetch=True):
                    raise ValueError(f"No existe un tópico con ID {topico_id}")
                
                # Obtener sección del tópico
                seccion_result = execute_query(get_seccion_id_from_topico, (topico_id,), fetch=True)
                if not seccion_result:
                    raise ValueError(f"No se pudo obtener la sección del tópico {topico_id}")
                
                seccion_id = seccion_result[0]["seccion_id"]
                
                # Verificar que alumno está en la sección
                alumno_seccion = execute_query(
                    check_alumno_seccion_by_seccion,
                    (alumno_id, seccion_id),
                    fetch=True
                )
                
                if not alumno_seccion:
                    raise ValueError(f"El alumno con ID {alumno_id} no está inscrito en la sección del tópico {topico_id}")
                
                alumno_seccion_id = alumno_seccion[0]["id"]
                
                # Obtener la instancia de evaluación
                instancia_evaluacion = execute_query(
                    get_instancia_evaluacion_by_offset,
                    (topico_id, instancia_num - 1),
                    fetch=True
                )
                
                if not instancia_evaluacion:
                    raise ValueError(f"No existe la instancia {instancia_num} para el tópico {topico_id}")
                
                instancia_id = instancia_evaluacion[0]["id"]
                
                # Validar nota
                nota_valor = float(nota_data["nota"])
                if nota_valor < 1.0 or nota_valor > 7.0:
                    raise ValueError(f"La nota debe estar entre 1.0 y 7.0. Valor: {nota_valor}")
                
                # Insertar o actualizar nota
                existing = execute_query(check_nota_exists, (alumno_seccion_id, instancia_id), fetch=True)
                
                if existing:
                    execute_query(update_nota, (nota_valor, existing[0]["id"]))
                else:
                    execute_query(insert_nota, (alumno_seccion_id, instancia_id, nota_valor))
                
                result["exitosos"] += 1
            except Exception as e:
                result["fallidos"] += 1
                result["errores"].append({
                    "alumno_id": alumno_id,
                    "topico_id": topico_id,
                    "instancia": instancia_num,
                    "error": str(e)
                })
        
        return result