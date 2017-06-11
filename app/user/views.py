from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import user
from .. import db
from ..models import User, Student, Permission
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    PasswordResetRequestForm, PasswordResetForm, EditProfileForm
from ..decorators import authority_required, admin_required

#US1
@user.route('/user?user=<user_id>')
@login_required
@authority_required(Permission.bit4)
def profile(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('user.html', user=user)


#US2
@user.route('/edit?user=<user_id>', methods=['GET', 'POST'])
@login_required
@authority_required(Permission.ADMIN)
def edit_profile(user_id):
    form = EditProfileForm()
    print 'vali'
    if form.validate_on_submit():
        print 'validating'
        current_user.phone = form.phone1.data
        current_user.first_name1 = form.first_name1.data
        current_user.last_name1 = form.last_name1.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.profile', user_id = user_id))
    form.first_name1.data = current_user.first_name1
    form.last_name1.data = current_user.last_name1
    form.phone1.data = current_user.phone1
    return render_template('edit_profile.html', form=form)

#US3
@user.route('/password?user=<user_id>', methods=['GET', 'POST'])
@login_required
@authority_required(Permission.ADMIN)
def change_password(user_id):
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('.profile', user_id = user_id))
        else:
            flash('Invalid password.')
    return render_template("user/auth/change_password.html", form=form)

#US4
@user.route('/account?user=<user_id>')
@login_required
@authority_required(Permission.ADMIN)
def account(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    students = user.students.order_by(Student.added_time.desc()).all()
    return render_template('user/account.html', user = user, students = students)

#US5
@user.route('/browse', methods=['GET', 'POST'])
@login_required
@admin_required
def browse():
    users = User.query.all()
    return render_template('user/user_browse.html', users = users)




@user.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'user.' \
                and request.endpoint != 'static':
            return redirect(url_for('user.unconfirmed'))


@user.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('user/auth/unconfirmed.html')


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('user/auth/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    password = form.password.data,
                    address = form.address.data,
                    nickname = form.nickname.data,
                    last_name1 = form.lastname1.data,
                    first_name1 = form.firstname1.data,
                    middle_name1 = form.middlename1.data,
                    chinese_name1 = form.chname1.data,
                    phone1 = form.phone1.data,
                    last_name2 = form.lastname2.data,
                    first_name2 = form.firstname2.data,
                    chinese_name2 = form.chname2.data,
                    middle_name2 = form.middlename2.data,
                    phone2 = form.phone2.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'user/auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('user.login'))
    return render_template('user/auth/register.html', form=form)


@user.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@user.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'user/auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))



@user.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'user/auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('user.login'))
    return render_template('user/auth/reset_password.html', form=form)


@user.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('user.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('user/auth/reset_password.html', form=form)


