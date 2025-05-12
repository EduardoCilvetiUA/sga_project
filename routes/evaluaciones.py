from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.evaluacion import Evaluacion
from models.seccion import Seccion

bp = Blueprint("evaluaciones", __name__, url_prefix="/evaluaciones")


@bp.route("/")
def index():
    topicos = Evaluacion.get_all_topics()
    return render_template("evaluaciones/index.html", topicos=topicos)


@bp.route("/create", methods=("GET", "POST"))
def create():
    secciones = Seccion.get_all()
    seccion_id = request.args.get("seccion_id", None)

    if request.method == "POST":
        return _handle_create_post(secciones, seccion_id)

    return render_template(
        "evaluaciones/create.html", secciones=secciones, seccion_id=seccion_id
    )


def _handle_create_post(secciones, seccion_id):
    form_data = _extract_topic_form_data()
    seccion_id = form_data["seccion_id"]

    error = _validate_topic_form_data(form_data)

    if error is None:
        error = _validate_section_percentage(seccion_id, form_data)

    if error is None:
        try:
            Evaluacion.create_topic(
                seccion_id,
                form_data["nombre"],
                form_data["valor"],
                form_data["usa_porcentaje"],
            )
            flash("Tópico de evaluación creado exitosamente!")
            return redirect(url_for("evaluaciones.index"))
        except Exception as e:
            error = f"Error al crear el tópico de evaluación: {e}"

    flash(error)
    return render_template(
        "evaluaciones/create.html", secciones=secciones, seccion_id=seccion_id
    )


def _extract_topic_form_data():
    return {
        "seccion_id": request.form["seccion_id"],
        "nombre": request.form["nombre"],
        "valor": request.form["valor"],
        "usa_porcentaje": "usa_porcentaje" in request.form,
    }


def _validate_topic_form_data(form_data):
    if not form_data["seccion_id"]:
        return "La sección es requerida."
    elif not form_data["nombre"]:
        return "El nombre del tópico es requerido."
    elif not form_data["valor"]:
        return "El valor es requerido."
    return None


def _validate_section_percentage(seccion_id, form_data):
    try:
        seccion = Seccion.get_by_id(seccion_id)
        seccion_usa_porcentaje = seccion["usa_porcentaje"]

        if seccion_usa_porcentaje:
            total_valor = Evaluacion.get_section_total_percentage(seccion_id)

            if total_valor is not None:
                total_valor_float = float(total_valor)
            else:
                total_valor_float = 0

            valor_float = float(form_data["valor"])

            if total_valor_float + valor_float > 100:
                return f"El porcentaje total excede el 100%. Actualmente: {total_valor_float}%"
        return None
    except Exception as e:
        return f"Error al verificar la configuración de la sección: {e}"


@bp.route("/topic/<int:id>/edit", methods=("GET", "POST"))
def edit_topic(id):
    topico = Evaluacion.get_topic_by_id(id)

    if request.method == "POST":
        return _handle_edit_topic_post(id, topico)

    return render_template("evaluaciones/edit_topic.html", topico=topico)


def _handle_edit_topic_post(id, topico):
    form_data = _extract_topic_form_data()

    error = _validate_edit_topic_form_data(form_data)

    if error is None:
        error = _validate_edit_topic_percentage(topico, form_data)

    if error is None:
        try:
            Evaluacion.update_topic(
                id, form_data["nombre"], form_data["valor"], form_data["usa_porcentaje"]
            )
            flash("Tópico de evaluación actualizado exitosamente!")
            return redirect(url_for("evaluaciones.view_topic", id=id))
        except Exception as e:
            error = f"Error al actualizar el tópico de evaluación: {e}"

    flash(error)
    return render_template("evaluaciones/edit_topic.html", topico=topico)


def _validate_edit_topic_form_data(form_data):
    if not form_data["nombre"]:
        return "El nombre del tópico es requerido."
    elif not form_data["valor"]:
        return "El valor es requerido."
    return None


def _validate_edit_topic_percentage(topico, form_data):
    seccion_id = topico["seccion_id"]
    seccion_usa_porcentaje = topico["seccion_usa_porcentaje"]

    if seccion_usa_porcentaje:
        total_valor = Evaluacion.get_section_total_percentage(seccion_id)

        if total_valor is not None:
            total_valor_float = float(total_valor) - float(topico["valor"])
        else:
            total_valor_float = 0

        valor_float = float(form_data["valor"])

        if total_valor_float + valor_float > 100:
            return (
                f"El porcentaje total excede el 100%. Actualmente: {total_valor_float}%"
            )
    return None


@bp.route("/topic/<int:id>/delete", methods=("POST",))
def delete_topic(id):
    try:
        Evaluacion.delete_topic(id)
        flash("Tópico de evaluación eliminado exitosamente!")
    except Exception as e:
        flash(f"Error al eliminar el tópico de evaluación: {e}")

    return redirect(url_for("evaluaciones.index"))


@bp.route("/topic/<int:id>/view")
def view_topic(id):
    topico = Evaluacion.get_topic_by_id(id)
    instancias = Evaluacion.get_instances(id)

    return render_template(
        "evaluaciones/view_topic.html", topico=topico, instancias=instancias
    )


@bp.route("/topic/<int:id>/add_instance", methods=("GET", "POST"))
def add_instance(id):
    topico = Evaluacion.get_topic_by_id(id)

    if request.method == "POST":
        return _handle_add_instance_post(id, topico)

    return render_template("evaluaciones/add_instance.html", topico=topico)


def _handle_add_instance_post(id, topico):
    form_data = _extract_instance_form_data()

    error = _validate_instance_form_data(form_data)

    if error is None:
        error = _validate_instance_percentage(id, topico, form_data)

    if error is None:
        try:
            Evaluacion.create_instance(
                id, form_data["nombre"], form_data["valor"], form_data["opcional"]
            )
            flash("Instancia de evaluación creada exitosamente!")
            return redirect(url_for("evaluaciones.view_topic", id=id))
        except Exception as e:
            error = f"Error al crear la instancia de evaluación: {e}"

    flash(error)
    return render_template("evaluaciones/add_instance.html", topico=topico)


def _extract_instance_form_data():
    return {
        "nombre": request.form["nombre"],
        "valor": request.form["valor"],
        "opcional": "opcional" in request.form,
    }


def _validate_instance_form_data(form_data):
    if not form_data["nombre"]:
        return "El nombre de la instancia es requerido."
    elif not form_data["valor"]:
        return "El valor es requerido."
    return None


def _validate_instance_percentage(id, topico, form_data):
    usa_porcentaje = topico["usa_porcentaje"]

    if usa_porcentaje:
        total_valor = Evaluacion.get_topic_total_percentage(id)

        if total_valor is not None:
            total_valor_float = float(total_valor)
        else:
            total_valor_float = 0

        valor_float = float(form_data["valor"])

        if total_valor_float + valor_float > 100:
            return (
                f"El porcentaje total excede el 100%. Actualmente: {total_valor_float}%"
            )
    return None


@bp.route("/instance/<int:id>/edit", methods=("GET", "POST"))
def edit_instance(id):
    instancia = Evaluacion.get_instance_by_id(id)

    if request.method == "POST":
        return _handle_edit_instance_post(id, instancia)

    return render_template("evaluaciones/edit_instance.html", instancia=instancia)


def _handle_edit_instance_post(id, instancia):
    form_data = _extract_instance_form_data()

    error = _validate_instance_form_data(form_data)

    if error is None:
        error = _validate_edit_instance_percentage(instancia, form_data)

    if error is None:
        try:
            Evaluacion.update_instance(
                id, form_data["nombre"], form_data["valor"], form_data["opcional"]
            )
            flash("Instancia de evaluación actualizada exitosamente!")
            return redirect(
                url_for("evaluaciones.view_topic", id=instancia["topico_id"])
            )
        except Exception as e:
            error = f"Error al actualizar la instancia de evaluación: {e}"

    flash(error)
    return render_template("evaluaciones/edit_instance.html", instancia=instancia)


def _validate_edit_instance_percentage(instancia, form_data):
    topico_id = instancia["topico_id"]
    usa_porcentaje = instancia["usa_porcentaje"]

    if usa_porcentaje:
        total_valor = Evaluacion.get_topic_total_percentage(topico_id)

        if total_valor is not None:
            total_valor_float = float(total_valor) - float(instancia["valor"])
        else:
            total_valor_float = 0

        valor_float = float(form_data["valor"])

        if total_valor_float + valor_float > 100:
            return (
                f"El porcentaje total excede el 100%. Actualmente: {total_valor_float}%"
            )
    return None


@bp.route("/instance/<int:id>/delete", methods=("POST",))
def delete_instance(id):
    instancia = Evaluacion.get_instance_by_id(id)
    topico_id = instancia["topico_id"]

    try:
        Evaluacion.delete_instance(id)
        flash("Instancia de evaluación eliminada exitosamente!")
    except Exception as e:
        flash(f"Error al eliminar la instancia de evaluación: {e}")

    return redirect(url_for("evaluaciones.view_topic", id=topico_id))
