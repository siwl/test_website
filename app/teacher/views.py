from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import teacher
from .. import db
from ..models import User, Teacher, Permission
from ..email import send_email
from .forms import NewTeacherForm, EditProfileForm
from ..decorators import permission_required


#TE3
@teacher.route('/add', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.bit5)
def addteacher():
    form = NewTeacherForm()
    if form.validate_on_submit():
        newteacher = Teacher(last_name = form.lastname.data,
                    first_name = form.firstname.data,
                    middle_name = form.middlename.data,
                    chinese_name = form.chinesename.data,
                    user_id = form.user.data)
        db.session.add(newteacher)
        db.session.commit()
        return redirect(url_for('.profile', teacher_id=newteacher.id))
    return render_template("teacher/addteacher.html", form=form)



@teacher.route('/teacher?teacher=<teacher_id>', methods=['GET', 'POST'])
@login_required
def profile(teacher_id):
    teacher = Teacher.query.filter_by(id=teacher_id).first_or_404()
    return render_template("teacher/profile.html", teacher=teacher)



@teacher.route('/browse', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.bit4)
def browse():
	teachers = Teacher.query.all()
	return render_template("teacher/teacher_browse.html", teachers=teachers)



@teacher.route('/edit?teacher=<teacher_id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.bit4)
def edit_profile(teacher_id):
    teacher = Teacher.query.filter_by(id=teacher_id).first_or_404()
    form = EditProfileForm()
    if form.validate_on_submit():
        teacher.last_name = form.lastname.data
        teacher.first_name = form.firstname.data
        teacher.middle_name = form.middlename.data
        db.session.add(teacher)
        flash('The teacher profile has been updated.')
        return redirect(url_for('.profile', teacher_id=teacher.id))
    form.firstname.data = teacher.first_name
    form.lastname.data = teacher.last_name
    form.middlename.data = teacher.middle_name
    form.chinesename.data = teacher.chinese_name
    return render_template('teacher/edit_profile.html', form=form, teacher=teacher)

#TE6
@teacher.route('/delete?teacher=<teacher_id>')
@login_required
@permission_required(Permission.bit4)
def delete_teacher(teacher_id):
    teacher = Teacher.query.filter_by(id=teacher_id).first_or_404()
    if teacher is None:
        flash('Invalid Teacher!')
        return redirect(url_for('.browse'))
    db.session.delete(teacher)
    db.session.commit()
    return redirect(url_for('.browse'))