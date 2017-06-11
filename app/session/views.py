from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import session
from .. import db
from ..models import User, Session, Permission
from ..email import send_email
from .forms import NewSessionForm, EditProfileForm	
from ..decorators import permission_required


#SE1
@session.route('/session?session=<session_id>', methods=['GET', 'POST'])
@login_required
def profile(session_id):
    session = Session.query.filter_by(id=session_id).first_or_404()
    return render_template("session/profile.html", session=session)


#SE2
@session.route('/edit?session=<session_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(session_id):
    session = Session.query.filter_by(id=session_id).first_or_404()
    form = EditProfileForm()
    if form.validate_on_submit():
        session.school_year = form.schoolyear.data
        session.room = form.room.data
        session.time = form.time.data
        session.duration = form.duration.data
        db.session.add(session)
        flash('This session has been updated.')
        return redirect(url_for('.profile', session_id=session.id))
    form.schoolyear.data = session.school_year
    form.room.data = session.room
    form.time.data = session.time
    form.duration.data = session.duration
    return render_template('session/edit_profile.html', form=form, session=session) 


#SE3
@session.route('/add?class=<class_id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.bit5)
def addsession(class_id):
    form = NewSessionForm()
    if form.validate_on_submit():
        newsession = Session(school_year = form.year.data,
                    time = form.time.data,
                    room = form.room.data,
                    class_id = class_id)
        db.session.add(newsession)
        db.session.commit()
        return redirect(url_for('classbp.profile', class_id=class_id))
    return render_template("session/addtoclass.html", form=form)


#SE4
@session.route('/assignteacher?session=<session_id>', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.bit5)
def assignteacher(session_id):
    form = AssignTeacherForm()
    session = Session.query.filter_by(id=session_id).first_or_404()
    if form.validate_on_submit():
        newteachersession = TeacherSession(status = Assign,
                            session_id = session_id,
                            teacher_id = form.teacher)
    return render_template("session/assignteacher.html", form=form)



#SE5
@session.route('/browse', methods=['GET', 'POST'])
def browse():
	sessions = Session.query.all()
	return render_template("session/session_browse.html", sessions=sessions)

#SE6
@session.route('/delete?session=<session_id>')
@login_required
@permission_required(Permission.bit5)
def delete_session(session_id):
    session = Session.query.filter_by(id=session_id).first_or_404()
    if session is None:
        flash('Invalid Session!')
        return redirect(url_for('.browse'))
    db.session.delete(session)
    db.session.commit()
    return redirect(url_for('.browse'))