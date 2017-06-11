from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import student
from .. import db
from ..models import User, Student, Session, Permission
from ..email import send_email
from .forms import NewStudentForm, RegisterSessionForm, EditProfileForm
from ..decorators import authority_required


#ST1
@student.route('/student?student=<student_id>', methods=['GET', 'POST'])
@login_required
def profile(student_id):
    student = Student.query.filter_by(id=student_id).first_or_404()
    if not current_user.has_student(student) and not current_user.is_admin() \
    and not current_user.is_teacing(student):
        abort(403)
    return render_template('student/student.html', student=student)


#ST2
@student.route('/add?user=<user_id>', methods=['GET', 'POST'])
@login_required
@authority_required(Permission.ADMIN)
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
        return redirect(url_for('user.account',user_id=user_id))
    return render_template("student/addstudent.html", form=form)


#ST3
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
    return render_template('student/edit_student.html', form=form, student=student)



@student.route('/sessionlist??student=<student_id>', methods=['GET', 'POST'])
@login_required
def sessionlist(student_id):
    student = Student.query.filter_by(id=student_id).first_or_404()
    sessions = Session.query.all()
    return render_template('student/sessionlist.html', sessions=sessions, student=student)





@student.route('/register?student=<student_id>&session=<session_id>', methods=['GET', 'POST'])
@login_required
def register(student_id,session_id):
    student = Student.query.filter_by(id=student_id).first_or_404()
    session = Session.query.filter_by(id=session_id).first_or_404()
    student.register(session)
    flash('You are noe enrolled.')
    return redirect(url_for('.profile',student_id=student.id))



@student.route('/browse', methods=['GET', 'POST'])
def browse():
    students = Student.query.all()
    return render_template("student/student_browse.html", students=students)

