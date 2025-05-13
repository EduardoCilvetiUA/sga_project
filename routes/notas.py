from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.nota import Nota
from models.seccion import Seccion
from models.alumno import Alumno
from models.evaluacion import Evaluacion

bp = Blueprint("notas", __name__, url_prefix="/notas")


@bp.route("/")
def index():
    notas = Nota.get_all()
    return render_template("notas/index.html", notas=notas)


@bp.route("/create", methods=("GET", "POST"))
def create():
    secciones = Seccion.get_all()
    seccion_id = request.args.get("seccion_id", None)
    alumno_id = request.args.get("alumno_id", None)

    alumnos, instancias = _load_grade_creation_data(seccion_id, alumno_id)

    if request.method == "POST":
        if "seccion_id" in request.form and "alumno_id" not in request.form:
            return _handle_section_selection(request)

        elif _is_student_selection_stage(request.form):
            return _handle_student_selection(request)

        elif _is_grade_submission_stage(request.form):
            return _handle_grade_submission(request)

    return render_template(
        "notas/create.html",
        secciones=secciones,
        alumnos=alumnos,
        instancias=instancias,
        seccion_id=seccion_id,
        alumno_id=alumno_id,
    )


def _load_grade_creation_data(seccion_id, alumno_id):
    alumnos = []
    instancias = []

    if seccion_id:
        alumnos = Seccion.get_students(seccion_id)
        if alumno_id:
            instancias = Nota.get_pending_evaluations(alumno_id, seccion_id)

    return alumnos, instancias


def _is_student_selection_stage(form_data):
    return (
        "seccion_id" in form_data
        and "alumno_id" in form_data
        and "instancia_id" not in form_data
    )


def _is_grade_submission_stage(form_data):
    return (
        "seccion_id" in form_data
        and "alumno_id" in form_data
        and "instancia_id" in form_data
        and "nota" in form_data
    )


def _handle_section_selection(request):
    seccion_id = request.form["seccion_id"]
    return redirect(url_for("notas.create", seccion_id=seccion_id))


def _handle_student_selection(request):
    seccion_id = request.form["seccion_id"]
    alumno_id = request.form["alumno_id"]
    return redirect(url_for("notas.create", seccion_id=seccion_id, alumno_id=alumno_id))


def _handle_grade_submission(request):
    form_data = {
        "seccion_id": request.form["seccion_id"],
        "alumno_id": request.form["alumno_id"],
        "instancia_id": request.form["instancia_id"],
        "nota_valor": request.form["nota"],
    }

    error = _validate_grade_form_data(form_data)

    if error is None:
        try:
            alumno_seccion_id = Nota.get_alumno_seccion_by_id(
                form_data["alumno_id"], form_data["seccion_id"]
            )

            if not alumno_seccion_id:
                error = "El alumno no está inscrito en esta sección."
            else:
                Nota.create(
                    alumno_seccion_id,
                    form_data["instancia_id"],
                    form_data["nota_valor"],
                )
                flash("Nota registrada exitosamente!")
                return redirect(url_for("notas.index"))
        except Exception as e:
            error = f"Error al registrar la nota: {e}"

    flash(error)
    return redirect(
        url_for(
            "notas.create",
            seccion_id=form_data["seccion_id"],
            alumno_id=form_data["alumno_id"],
        )
    )


def _validate_grade_form_data(form_data):
    if not form_data["seccion_id"]:
        return "La sección es requerida."
    elif not form_data["alumno_id"]:
        return "El alumno es requerido."
    elif not form_data["instancia_id"]:
        return "La instancia de evaluación es requerida."
    elif not form_data["nota_valor"]:
        return "La nota es requerida."
    return None


@bp.route("/<int:id>/edit", methods=("GET", "POST"))
def edit(id):
    nota = Nota.get_by_id(id)

    if request.method == "POST":
        nota_valor = request.form["nota"]

        error = None

        if not nota_valor:
            error = "La nota es requerida."

        if error is None:
            try:
                Nota.update(id, nota_valor)
                flash("Nota actualizada exitosamente!")
                return redirect(url_for("notas.index"))
            except Exception as e:
                error = f"Error al actualizar la nota: {e}"

        flash(error)

    return render_template("notas/edit.html", nota=nota)


@bp.route("/<int:id>/delete", methods=("POST",))
def delete(id):
    try:
        Nota.delete(id)
        flash("Nota eliminada exitosamente!")
    except Exception as e:
        flash(f"Error al eliminar la nota: {e}")

    return redirect(url_for("notas.index"))


@bp.route("/student/<int:alumno_id>/section/<int:seccion_id>")
def student_grades(alumno_id, seccion_id):
    alumno = Alumno.get_by_id(alumno_id)
    seccion = Seccion.get_by_id(seccion_id)
    notas = Nota.get_grades_by_student_section(alumno_id, seccion_id)
    nota_final = Nota.calculate_final_grade(alumno_id, seccion_id)

    return render_template(
        "notas/student_grades.html",
        alumno=alumno,
        seccion=seccion,
        notas=notas,
        nota_final=nota_final,
    )


@bp.route("/section/<int:seccion_id>")
def section_grades(seccion_id):
    seccion = Seccion.get_by_id(seccion_id)
    alumnos = Seccion.get_students(seccion_id)
    topicos = Evaluacion.get_topics_by_section(seccion_id)

    notas_finales = {}
    for alumno in alumnos:
        nota_final = Nota.calculate_final_grade(alumno["id"], seccion_id)
        notas_finales[alumno["id"]] = nota_final

    return render_template(
        "notas/section_grades.html",
        seccion=seccion,
        alumnos=alumnos,
        topicos=topicos,
        notas_finales=notas_finales,
    )
