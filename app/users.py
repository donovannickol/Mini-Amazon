from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User
from .models.purchase import Purchase


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/all_purchases/', methods = ['GET','POST'])
def get_all_purchases():
    uid = current_user.id
    get_all_purchases = Purchase.get_all_by_uid(uid - 50)
    firstname = current_user.firstname
    return render_template('get_all_purchases.html',
                            get_all_purchases = get_all_purchases, 
                            firstname = firstname)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

class UpdateForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update User')

@bp.route('/account', methods = ['GET','POST'])
def publicView():
    id_number = current_user.id
    name = f'{current_user.firstname} {current_user.lastname}'
    email = current_user.email
    location = current_user.city + ", " + current_user.state
    balance = "$" + str(current_user.balance)
    return render_template('user_public_view.html', 
    id = id_number, name = name, email = email, location = location, balance = balance)

@bp.route('/update_info', methods = ['GET', 'POST'])
def update_info():
    form = UpdateForm()
    if form.validate_on_submit():
        if User.update_user(form.firstname.data,
                            form.lastname.data,
                            form.email.data,
                            form.address.data,
                            form.city.data,
                            form.state.data,
                            form.password.data,
                            current_user.id):
          return redirect(url_for('users.publicView'))
    form.firstname.data = current_user.firstname
    form.lastname.data = current_user.lastname
    form.email.data = current_user.email
    form.address.data = current_user.address
    form.city.data = current_user.city
    form.state.data = current_user.state
    return render_template('update_info.html',
    old_user = current_user, form = form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.address.data,
                         form.city.data,
                         form.state.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))
