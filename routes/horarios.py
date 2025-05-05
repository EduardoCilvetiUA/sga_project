from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from utils.horario_generator import HorarioGenerator
import os
from db import execute_query
from datetime import datetime

bp = Blueprint("horarios", __name__, url_prefix="/horarios")

@bp.route("/")
def index():
    return render_template("horarios/index.html")

@bp.route("/generar", methods=["GET", "POST"])
def generar():
    if request.method == "POST":
        anio = request.form.get('anio')
        periodo = request.form.get('periodo')
        
        if not anio or not periodo:
            flash('Debe ingresar año y período')
            return redirect(request.url)
            
        try:
            anio = int(anio)
            periodo = str(periodo)
            
            # Generar horarios
            generator = HorarioGenerator()
            resultados = generator.generar_horarios(anio, periodo)
            
            if resultados['estado'] in ['no_secciones', 'no_salas', 'error']:
                flash(resultados['mensaje'])
                return redirect(request.url)
                
            # Si fue exitoso, redirigir a la página de resultados
            return render_template(
                "horarios/resultados.html", 
                resultados=resultados, 
                anio=anio, 
                periodo=periodo
            )
        except Exception as e:
            flash(f"Error al generar horarios: {str(e)}")
            return redirect(request.url)
            
    return render_template("horarios/generar.html")

@bp.route("/exportar", methods=["POST"])
def exportar():
    anio = request.form.get('anio')
    periodo = request.form.get('periodo')
    
    if not anio or not periodo:
        flash('Debe ingresar año y período')
        return redirect(url_for('horarios.index'))
        
    try:
        anio = int(anio)
        periodo = str(periodo)
        
        # Generar nombre de archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"horarios_{anio}_{periodo}_{timestamp}.xlsx"
        file_path = os.path.join('/tmp', filename)
        
        # Exportar horarios a Excel
        generator = HorarioGenerator()
        resultados = generator.exportar_horarios_excel(anio, periodo, file_path)
        
        if resultados['estado'] != 'exito':
            flash(resultados['mensaje'])
            return redirect(url_for('horarios.index'))
            
        # Enviar archivo al usuario
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        flash(f"Error al exportar horarios: {str(e)}")
        return redirect(url_for('horarios.index'))

@bp.route("/view", methods=["GET"])
def view():
    anio = request.args.get('anio')
    periodo = request.args.get('periodo')
    
    if not anio or not periodo:
        flash('Debe ingresar año y período')
        return redirect(url_for('horarios.index'))
        
    try:
        anio = int(anio)
        periodo = str(periodo)
        
        # Obtener horarios
        horarios_raw = execute_query(
            """
            SELECT h.id, h.dia, h.hora_inicio, h.hora_fin, 
                   s.nombre as sala_nombre, s.capacidad as sala_capacidad,
                   c.codigo as curso_codigo, c.nombre as curso_nombre,
                   sec.numero as seccion_numero, p.nombre as profesor_nombre
            FROM horarios h
            JOIN salas s ON h.sala_id = s.id
            JOIN secciones sec ON h.seccion_id = sec.id
            JOIN instancias_curso ic ON sec.instancia_curso_id = ic.id
            JOIN cursos c ON ic.curso_id = c.id
            LEFT JOIN profesor_seccion ps ON sec.id = ps.seccion_id
            LEFT JOIN profesores p ON ps.profesor_id = p.id
            WHERE ic.anio = %s AND ic.periodo = %s
            ORDER BY h.dia, h.hora_inicio, s.nombre
            """,
            (anio, periodo),
            fetch=True
        )
        
        # Formatear los horarios para manejar correctamente los objetos de tiempo
        horarios = []
        for h in horarios_raw:
            horario = dict(h)
            # Convertir objetos time o timedelta a cadenas con formato
            if hasattr(horario['hora_inicio'], 'strftime'):
                horario['hora_inicio'] = horario['hora_inicio'].strftime('%H:%M')
            elif isinstance(horario['hora_inicio'], str):
                # Ya es una cadena, no hacer nada
                pass
            else:
                # Es un timedelta, convertir a cadena con formato
                total_seconds = int(horario['hora_inicio'].total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                horario['hora_inicio'] = f"{hours:02d}:{minutes:02d}"
                
            if hasattr(horario['hora_fin'], 'strftime'):
                horario['hora_fin'] = horario['hora_fin'].strftime('%H:%M')
            elif isinstance(horario['hora_fin'], str):
                # Ya es una cadena, no hacer nada
                pass
            else:
                # Es un timedelta, convertir a cadena con formato
                total_seconds = int(horario['hora_fin'].total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                horario['hora_fin'] = f"{hours:02d}:{minutes:02d}"
                
            horarios.append(horario)
        
        return render_template(
            "horarios/view.html", 
            horarios=horarios, 
            anio=anio, 
            periodo=periodo
        )
    except Exception as e:
        flash(f"Error al obtener horarios: {str(e)}")
        return redirect(url_for('horarios.index'))