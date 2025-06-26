from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.seccion import Seccion
from models.instancia import Instancia

bp = Blueprint("secciones", __name__, url_prefix="/secciones")


@bp.route("/")
def index():
    secciones = Seccion.get_all()
    return render_template("secciones/index.html", secciones=secciones)


@bp.route("/create", methods=("GET", "POST"))
def create():
    instancias = Instancia.get_all()
    instancia_id = request.args.get("instancia_id", None)
    
    if instancia_id:
        if not _validate_instancia_not_cerrada(instancia_id, "creación de sección"):
            return redirect(url_for("instancias.view", id=instancia_id))

    if request.method == "POST":
        return _handle_create_seccion_post(instancias, instancia_id)
    
    return render_template("secciones/create.html", instancias=instancias, instancia_id=instancia_id)


def _validate_instancia_not_cerrada(instancia_id, action):
    try:
        Instancia.validate_not_cerrada(int(instancia_id), action)
        return True
    except ValueError as e:
        flash(str(e))
        return False


def _handle_create_seccion_post(instancias, instancia_id):
    instancia_curso_id = request.form["instancia_curso_id"]
    numero = request.form["numero"]
    usa_porcentaje = "usa_porcentaje" in request.form
    
    error = _validate_seccion_data(instancia_curso_id, numero)
    
    if error is None:
        try:
            Seccion.create(instancia_curso_id, numero, usa_porcentaje)
            flash("Sección creada exitosamente!")
            return redirect(url_for("secciones.index"))
        except Exception as e:
            error = f"Error al crear la sección: {e}"
    
    flash(error)
    return render_template("secciones/create.html", instancias=instancias, instancia_id=instancia_id)


def _validate_seccion_data(instancia_curso_id, numero):
    if not instancia_curso_id:
        return "La instancia de curso es requerida."
    if not numero:
        return "El número de sección es requerido."
    try:
        Instancia.validate_not_cerrada(int(instancia_curso_id), "creación de sección")
    except ValueError as e:
        return str(e)
    return None


@bp.route("/<int:id>/edit", methods=("GET", "POST"))
def edit(id):
    try:
        Seccion.validate_not_cerrada(id, "edición")
        
        seccion = Seccion.get_by_id(id)
        instancias = Instancia.get_all()

        if request.method == "POST":
            instancia_curso_id = request.form["instancia_curso_id"]
            numero = request.form["numero"]
            usa_porcentaje = "usa_porcentaje" in request.form

            error = None

            if not instancia_curso_id:
                error = "La instancia de curso es requerida."
            elif not numero:
                error = "El número de sección es requerido."
            else:
                try:
                    Instancia.validate_not_cerrada(int(instancia_curso_id), "asignación a instancia")
                except ValueError as e:
                    error = str(e)

            if error is None:
                try:
                    Seccion.update(id, instancia_curso_id, numero, usa_porcentaje)
                    flash("Sección actualizada exitosamente!")
                    return redirect(url_for("secciones.index"))
                except Exception as e:
                    error = f"Error al actualizar la sección: {e}"

            flash(error)

        return render_template(
            "secciones/edit.html", seccion=seccion, instancias=instancias
        )
        
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("secciones.view", id=id))


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    try:
        Seccion.validate_not_cerrada(id, "eliminación")
        
        Seccion.delete(id)
        flash("Sección eliminada exitosamente!")
        
    except ValueError as e:
        flash(str(e))
    except Exception as e:
        flash(f"Error al eliminar la sección: {e}")

    return redirect(url_for("secciones.index"))


@bp.route("/<int:id>/view")
def view(id):
    seccion = Seccion.get_by_id(id)
    profesores = Seccion.get_profesores(id)
    alumnos = Seccion.get_alumnos(id)

    return render_template(
        "secciones/view.html", seccion=seccion, profesores=profesores, alumnos=alumnos
    )


@bp.route("/<int:id>/assign_professor", methods=("GET", "POST"))
def assign_profesor(id):
    try:
        Seccion.validate_not_cerrada(id, "asignación de profesor")
        
        seccion = Seccion.get_by_id(id)
        profesores_asignados = Seccion.get_profesores(id)
        profesores_disponibles = Seccion.get_available_profesores(id)

        if request.method == "POST":
            profesor_id = request.form["profesor_id"]

            if not profesor_id:
                flash("Por favor seleccione un profesor.")
            else:
                try:
                    Seccion.assign_profesor(id, profesor_id)
                    flash("Profesor asignado exitosamente!")
                    return redirect(url_for("secciones.view", id=id))
                except Exception as e:
                    flash(f"Error al asignar el profesor: {e}")

        return render_template(
            "secciones/assign_professor.html",
            seccion=seccion,
            profesores_asignados=profesores_asignados,
            profesores_disponibles=profesores_disponibles,
        )
        
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("secciones.view", id=id))


@bp.route("/<int:id>/remove_professor/<int:profesor_id>", methods=("POST",))
def remove_profesor(id, profesor_id):
    try:
        Seccion.validate_not_cerrada(id, "remoción de profesor")
        
        Seccion.remove_profesor(id, profesor_id)
        flash("Profesor removido exitosamente!")
        
    except ValueError as e:
        flash(str(e))
    except Exception as e:
        flash(f"Error al remover el profesor: {e}")

    return redirect(url_for("secciones.view", id=id))


@bp.route("/<int:id>/enroll_alumno", methods=("GET", "POST"))
def enroll_alumno(id):
    try:
        Seccion.validate_not_cerrada(id, "inscripción de alumno")
        
        seccion = Seccion.get_by_id(id)
        alumnos_inscritos = Seccion.get_alumnos(id)
        alumnos_disponibles = Seccion.get_available_alumnos(id)

        if request.method == "POST":
            alumno_id = request.form["alumno_id"]

            if not alumno_id:
                flash("Por favor seleccione un alumno.")
            else:
                try:
                    Seccion.enroll_alumno(id, alumno_id)
                    flash("Alumno inscrito exitosamente!")
                    return redirect(url_for("secciones.view", id=id))
                except Exception as e:
                    flash(f"Error al inscribir al alumno: {e}")

        return render_template(
            "secciones/enroll_alumno.html",
            seccion=seccion,
            alumnos_inscritos=alumnos_inscritos,
            alumnos_disponibles=alumnos_disponibles,
        )
        
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("secciones.view", id=id))


@bp.route("/<int:id>/unenroll_alumno/<int:alumno_id>", methods=("POST",))
def unenroll_alumno(id, alumno_id):
    try:
        Seccion.validate_not_cerrada(id, "remoción de alumno")
        
        Seccion.unenroll_alumno(id, alumno_id)
        flash("Alumno removido exitosamente!")
        
    except ValueError as e:
        flash(str(e))
    except Exception as e:
        flash(f"Error al remover al alumno: {e}")

    return redirect(url_for("secciones.view", id=id))