from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import classbp
from .. import db
from ..models import User, Student, Class, Permission
from ..email import send_email
from .forms import NewClassForm, EditProfileForm
from ..decorators import permission_required


#CL1
@classbp.route('/class?class=<class_id>', methods=['GET', 'POST'])
@login_required
def profile(class_id):
    tclass = Class.query.filter_by(id=class_id).first_or_404()
    return render_template("class/profile.html", tclass=tclass)


#CL2
@classbp.route('/edit?class=<class_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(class_id):
    tclass = Class.query.filter_by(id=class_id).first_or_404()
    form = EditProfileForm()
    if form.validate_on_submit():
        tclass.name = form.name.data
        tclass.description = form.description.data
        tclass.class_type = form.classtype.data
        db.session.add(tclass)
        flash('The class profile has been updated.')
        return redirect(url_for('.profile', class_id=tclass.id))
    form.name.data = tclass.name
    form.description.data = tclass.description
    form.classtype.data = tclass.class_type
    return render_template('class/edit_profile.html', form=form, tclass=tclass)


#CL3
@classbp.route('/add', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.bit5)
def addclass():
    form = NewClassForm()
    if form.validate_on_submit():
        newclass =  Class(name = form.name.data,
                    description = form.description.data,
                    class_type = form.classtype.data)
        db.session.add(newclass)
        db.session.commit()
        return redirect(url_for('.profile', class_id=newclass.id))
    return render_template("class/addclass.html", form=form)


#CL4
@classbp.route('/browse', methods=['GET', 'POST'])
@login_required
def browse():
	classes = Class.query.all()
	return render_template("class/class_browse.html", classes=classes)


