from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from utils.horario_generator import HorarioGenerator
import os
from querys.horario_queries import raw_schedule_query
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
            
            generator = HorarioGenerator()
            resultados = generator.generar_horarios(anio, periodo)
            
            if resultados['estado'] in ['no_secciones', 'no_salas', 'error']:
                flash(resultados['mensaje'])
                return redirect(request.url)
                
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
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"horarios_{anio}_{periodo}_{timestamp}.xlsx"
        file_path = os.path.join('/tmp', filename)
        
        generator = HorarioGenerator()
        resultados = generator.exportar_horarios_excel(anio, periodo, file_path)
        
        if resultados['estado'] != 'exito':
            flash(resultados['mensaje'])
            return redirect(url_for('horarios.index'))
            
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
        
        horarios_raw = execute_query(raw_schedule_query,(anio, periodo),fetch=True)
        
        horarios = []
        for h in horarios_raw:
            horario = dict(h)
            if hasattr(horario['hora_inicio'], 'strftime'):
                horario['hora_inicio'] = horario['hora_inicio'].strftime('%H:%M')
            elif isinstance(horario['hora_inicio'], str):
                pass
            else:
                total_seconds = int(horario['hora_inicio'].total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                horario['hora_inicio'] = f"{hours:02d}:{minutes:02d}"
                
            if hasattr(horario['hora_fin'], 'strftime'):
                horario['hora_fin'] = horario['hora_fin'].strftime('%H:%M')
            elif isinstance(horario['hora_fin'], str):
                pass
            else:
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