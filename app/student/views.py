from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import student
from .. import db
from ..models import User, Student
from ..email import send_email
from .forms import NewStudentForm, RegisterSessionForm

@student.route('/add?user=<user_id>', methods=['GET', 'POST'])
@login_required
def addstudent(user_id):
    form = NewStudentForm()
    if form.validate_on_submit():
        student = Student(last_name = form.lastname.data,
                    first_name = form.firstname.data,
                    middle_name = form.middlename.data,
                    chinese_name = form.chname.data,
                    birthday = form.birthday.data,
                    user = current_user._get_current_object())
        db.session.add(student)
        db.session.commit()
    return render_template("student/addstudent.html", form=form)



@student.route('/student?student=<student_id>', methods=['GET', 'POST'])
@login_required
def profile(student_id):
	student = Student.query.filter_by(id=student_id).first_or_404()
	return render_template('student/student.html', student=student)


@student.route('/register?student=<student_id>', methods=['GET', 'POST'])
@login_required
def register(student_id):
    student = Student.query.filter_by(id=student_id).first_or_404()
    pass



@student.route('/browse', methods=['GET', 'POST'])
def browse():
    students = Student.query.all()
    return render_template("student/student_browse.html", students=students)


@student.route('/edit?student=<student_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(student_id):
    student = Student.query.filter_by(id=student_id).first_or_404()
    form = EditProfileForm()
    if form.validate_on_submit():
        student.last_name = form.lastname.data
        student.first_name = form.firstname.data
        student.middle_name = form.middlename.data
        student.chinese_name = form.chinesename.data
        db.session.add(student)
        flash('The student profile has been updated.')
        return redirect(url_for('.profile', student_id=student.id))
    form.firstname.data = student.first_name
    form.lastname.data = student.last_name
    form.middlename.data = student.middle_name
    form.chinesename.data = student.chinese_name
    return render_template('student/edit_profile.html', form=form, student=student)