from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.seccion import Seccion
from models.instancia import Instancia

bp = Blueprint('secciones', __name__, url_prefix='/secciones')

@bp.route('/')
def index():
    secciones = Seccion.get_all()
    return render_template('secciones/index.html', secciones=secciones)

@bp.route('/create', methods=('GET', 'POST'))
def create():
    instancias = Instancia.get_all()
    instancia_id = request.args.get('instancia_id', None)
    
    if request.method == 'POST':
        instancia_curso_id = request.form['instancia_curso_id']
        numero = request.form['numero']
        
        error = None
        
        if not instancia_curso_id:
            error = 'La instancia de curso es requerida.'
        elif not numero:
            error = 'El número de sección es requerido.'
        
        if error is None:
            try:
                Seccion.create(instancia_curso_id, numero)
                flash('Sección creada exitosamente!')
                return redirect(url_for('secciones.index'))
            except Exception as e:
                error = f'Error al crear la sección: {e}'
        
        flash(error)
    
    return render_template('secciones/create.html', instancias=instancias, instancia_id=instancia_id)

@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    seccion = Seccion.get_by_id(id)
    instancias = Instancia.get_all()
    
    if request.method == 'POST':
        instancia_curso_id = request.form['instancia_curso_id']
        numero = request.form['numero']
        
        error = None
        
        if not instancia_curso_id:
            error = 'La instancia de curso es requerida.'
        elif not numero:
            error = 'El número de sección es requerido.'
        
        if error is None:
            try:
                Seccion.update(id, instancia_curso_id, numero)
                flash('Sección actualizada exitosamente!')
                return redirect(url_for('secciones.index'))
            except Exception as e:
                error = f'Error al actualizar la sección: {e}'
        
        flash(error)
    
    return render_template('secciones/edit.html', seccion=seccion, instancias=instancias)

@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    try:
        Seccion.delete(id)
        flash('Sección eliminada exitosamente!')
    except Exception as e:
        flash(f'Error al eliminar la sección: {e}')
    
    return redirect(url_for('secciones.index'))

@bp.route('/<int:id>/view')
def view(id):
    seccion = Seccion.get_by_id(id)
    profesores = Seccion.get_professors(id)
    alumnos = Seccion.get_students(id)
    
    return render_template('secciones/view.html', 
                         seccion=seccion, 
                         profesores=profesores, 
                         alumnos=alumnos)

@bp.route('/<int:id>/assign_professor', methods=('GET', 'POST'))
def assign_professor(id):
    seccion = Seccion.get_by_id(id)
    profesores_asignados = Seccion.get_professors(id)
    profesores_disponibles = Seccion.get_available_professors(id)
    
    if request.method == 'POST':
        profesor_id = request.form['profesor_id']
        
        if not profesor_id:
            flash('Por favor seleccione un profesor.')
        else:
            try:
                Seccion.assign_professor(id, profesor_id)
                flash('Profesor asignado exitosamente!')
                return redirect(url_for('secciones.view', id=id))
            except Exception as e:
                flash(f'Error al asignar el profesor: {e}')
    
    return render_template('secciones/assign_professor.html', 
                         seccion=seccion, 
                         profesores_asignados=profesores_asignados,
                         profesores_disponibles=profesores_disponibles)

@bp.route('/<int:id>/remove_professor/<int:profesor_id>', methods=('POST',))
def remove_professor(id, profesor_id):
    try:
        Seccion.remove_professor(id, profesor_id)
        flash('Profesor removido exitosamente!')
    except Exception as e:
        flash(f'Error al remover el profesor: {e}')
    
    return redirect(url_for('secciones.view', id=id))

@bp.route('/<int:id>/enroll_student', methods=('GET', 'POST'))
def enroll_student(id):
    seccion = Seccion.get_by_id(id)
    alumnos_inscritos = Seccion.get_students(id)
    alumnos_disponibles = Seccion.get_available_students(id)
    
    if request.method == 'POST':
        alumno_id = request.form['alumno_id']
        
        if not alumno_id:
            flash('Por favor seleccione un alumno.')
        else:
            try:
                Seccion.enroll_student(id, alumno_id)
                flash('Alumno inscrito exitosamente!')
                return redirect(url_for('secciones.view', id=id))
            except Exception as e:
                flash(f'Error al inscribir al alumno: {e}')
    
    return render_template('secciones/enroll_student.html', 
                         seccion=seccion, 
                         alumnos_inscritos=alumnos_inscritos,
                         alumnos_disponibles=alumnos_disponibles)

@bp.route('/<int:id>/unenroll_student/<int:alumno_id>', methods=('POST',))
def unenroll_student(id, alumno_id):
    try:
        Seccion.unenroll_student(id, alumno_id)
        flash('Alumno removido exitosamente!')
    except Exception as e:
        flash(f'Error al remover al alumno: {e}')
    
    return redirect(url_for('secciones.view', id=id))