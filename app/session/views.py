from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import session
from .. import db
from ..models import User, Session
from ..email import send_email
from .forms import NewSessionForm, EditProfileForm	

@session.route('/add', methods=['GET', 'POST'])
@login_required
def addsession():
    form = NewSessionForm()
    if form.validate_on_submit():
        newsession = Session(school_year = form.year.data,
                    time = form.time.data,
                    room = form.room.data)
        db.session.add(newsession)
        db.session.commit()
    return render_template("session/addsession.html", form=form)


@session.route('/session?session=<session_id>', methods=['GET', 'POST'])
@login_required
def profile(session_id):
    session = Session.query.filter_by(id=session_id).first_or_404()
    return render_template("session/profile.html", session=session)



@session.route('/browse', methods=['GET', 'POST'])
def browse():
	sessions = Session.query.all()
	return render_template("session/session_browse.html", sessions=sessions)



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