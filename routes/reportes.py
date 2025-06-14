from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.reporte import Reporte

bp = Blueprint("reportes", __name__, url_prefix="/reportes")


@bp.route("/")
def index():
    return render_template("reportes/index.html")


@bp.route("/notas_instancia_topico", methods=["GET", "POST"])
def notas_instancia_topico():
    instancias = Reporte.get_instancias_evaluacion_disponibles()
    reporte_data = None
    
    if request.method == "POST":
        try:
            instancia_evaluacion_id = request.form.get("instancia_evaluacion_id")
            
            Reporte.validate_reporte_inputs(
                'instancia_topico', 
                instancia_evaluacion_id=instancia_evaluacion_id
            )
            
            reporte_data = Reporte.get_notas_instancia_topico(instancia_evaluacion_id)
            
            if not reporte_data:
                flash("No se encontraron notas para la instancia seleccionada", "warning")
                return redirect(request.url)
            
        except ValueError as e:
            flash(str(e), "error")
            return redirect(request.url)
        except Exception as e:
            flash(f"Error al generar el reporte: {str(e)}", "error")
            return redirect(request.url)
    
    return render_template(
        "reportes/notas_instancia_topico.html", 
        instancias=instancias,
        reporte=reporte_data
    )


@bp.route("/notas_finales_seccion", methods=["GET", "POST"])
def notas_finales_seccion():
    secciones = Reporte.get_secciones_cursos_cerrados()
    reporte_data = None
    
    if request.method == "POST":
        try:
            seccion_id = request.form.get("seccion_id")
            
            Reporte.validate_reporte_inputs(
                'notas_finales', 
                seccion_id=seccion_id
            )
            
            reporte_data = Reporte.get_notas_finales_seccion(seccion_id)
            
            if not reporte_data:
                flash("No se encontraron notas finales para la sección seleccionada", "warning")
                return redirect(request.url)
            
        except ValueError as e:
            flash(str(e), "error")
            return redirect(request.url)
        except Exception as e:
            flash(f"Error al generar el reporte: {str(e)}", "error")
            return redirect(request.url)
    
    return render_template(
        "reportes/notas_finales_seccion.html", 
        secciones=secciones,
        reporte=reporte_data
    )


@bp.route("/certificado_notas", methods=["GET", "POST"])
def certificado_notas():
    alumnos = Reporte.get_alumnos_disponibles()
    reporte_data = None
    
    if request.method == "POST":
        try:
            alumno_id = request.form.get("alumno_id")
            
            Reporte.validate_reporte_inputs(
                'certificado', 
                alumno_id=alumno_id
            )
            
            reporte_data = Reporte.get_certificado_notas_alumno(alumno_id)
            
            if not reporte_data:
                flash("No se encontraron cursos cerrados para el alumno seleccionado", "warning")
                return redirect(request.url)
            
        except ValueError as e:
            flash(str(e), "error")
            return redirect(request.url)
        except Exception as e:
            flash(f"Error al generar el reporte: {str(e)}", "error")
            return redirect(request.url)
    
    return render_template(
        "reportes/certificado_notas.html", 
        alumnos=alumnos,
        reporte=reporte_data
    )


@bp.route("/validate_instancia/<int:instancia_id>")
def validate_instancia(instancia_id):
    try:
        reporte = Reporte.get_notas_instancia_topico(instancia_id)
        return {"valid": True, "count": len(reporte['notas']) if reporte else 0}
    except Exception:
        return {"valid": False, "count": 0}


@bp.route("/validate_seccion/<int:seccion_id>")
def validate_seccion(seccion_id):
    try:
        reporte = Reporte.get_notas_finales_seccion(seccion_id)
        return {"valid": True, "count": len(reporte['notas']) if reporte else 0}
    except Exception:
        return {"valid": False, "count": 0}


@bp.route("/validate_alumno/<int:alumno_id>")
def validate_alumno(alumno_id):
    try:
        reporte = Reporte.get_certificado_notas_alumno(alumno_id)
        return {"valid": True, "count": len(reporte['cursos']) if reporte else 0}
    except Exception:
        return {"valid": False, "count": 0}