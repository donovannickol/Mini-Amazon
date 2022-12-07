from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange

from .models.user import User
from .models.purchase import Purchase
from .models.cart import Cart
from .models.pRatingNAMES import pRatingNAMES
from .models.inventory import Inventory
from datetime import datetime


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
    get_all_purchases = Purchase.get_all_by_uid(uid)
    firstname = current_user.firstname
    return render_template('get_all_purchases.html',
                            get_all_purchases = get_all_purchases, 
                            firstname = firstname)

@bp.route('/purchases_less_than_max/', methods = ['GET', 'POST'])
def get_all_purchases_less_than_max():
    uid = current_user.id
    maxi = request.form['max']
    if maxi == "" or float(maxi) < 0:
        get_all_purchases = Purchase.get_all_by_uid(uid)
    else:
        get_all_purchases = Purchase.get_all_by_uid_max_price(current_user.id, maxi)
    firstname = current_user.firstname
    return render_template('get_all_purchases.html',
                            get_all_purchases = get_all_purchases, 
                            firstname = firstname)

@bp.route('/purchases_less_than_items/', methods = ['GET', 'POST'])
def get_all_purchases_less_than_items():
    uid = current_user.id
    items = request.form['max']
    if items == "" or int(items) < 0:
        get_all_purchases = Purchase.get_all_by_uid(uid)
    else:
        get_all_purchases = Purchase.get_all_by_uid_max_items(current_user.id, items)
    firstname = current_user.firstname
    return render_template('get_all_purchases.html',
                            get_all_purchases = get_all_purchases, 
                            firstname = firstname)

@bp.route('/user_reviews', methods = ['GET', 'POST'])
def user_reviews():
    uid = current_user.id
    firstname = current_user.firstname
    get_reviews = pRatingNAMES.get(uid)
    return render_template('user_reviews.html', 
    firstname = firstname, get_reviews = get_reviews)


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

def validate_withdrawal(form, field):
        if (field.data > current_user.balance):
            raise ValidationError("Must be less than or equal to balance")

class UpdateBalanceForm(FlaskForm):
    withdraw = DecimalField('Withdraw', 
                            validators = [NumberRange(min = 0, 
                            message = "Must be greater than 0"), validate_withdrawal])
    
    top = DecimalField('Add to Balance',
                       validators = [NumberRange(min = 0,
                       message = "Must be greater than 0")])
    
    submit = SubmitField('Update Balance')

@bp.route('/account', methods = ['GET','POST'])
def publicView():
    id_number = current_user.id
    name = f'{current_user.firstname} {current_user.lastname}'
    email = current_user.email
    get_reviews = pRatingNAMES.get(id_number)
    get_inventory = Inventory.get_by_uid(id_number)
    error = ''
    if request.args.get('error'):
        error = request.args.get('error')    
    location = current_user.city + ", " + current_user.state
    balance = "$" + str(current_user.balance)
    return render_template('user_public_view.html', 
    id = id_number, name = name, email = email, location = location, balance = balance,
    error = error, get_reviews = get_reviews, get_inventory = get_inventory)

@bp.route('/user_search', methods = ['GET', 'POST'])
def userSearch():
    search_term = request.form['search_term']
    public = request.args.get('public', "", type = str)
    if search_term == "":
        return redirect(url_for('users.publicView', error = "Please enter an ID"))
    if (int(search_term) < 0):
        return redirect(url_for('users.publicView', error = "Please enter an number greater than 0"))
    return redirect(url_for('users.getPublicView', search_term = search_term))

@bp.route('/public_view', methods = ['GET','POST'])
def getPublicView():
    id_number = request.args.get('search_term', "", type=str)
    the_user = User.get(id_number)
    if the_user == None:
        return redirect(url_for('users.publicView', error = "User does not exist"))
    name = f'{the_user.firstname} {the_user.lastname}'
    firstname = the_user.firstname
    email = the_user.email
    address = the_user.address + ", " + the_user.city + ", " + the_user.state
    balance = "$" + str(the_user.balance)
    get_reviews = pRatingNAMES.get(id_number)
    get_inventory = Inventory.get_by_uid(id_number)
    return render_template('user_actual_public_view.html', 
    id  = id_number, name = name, email = email, balance = balance, get_reviews = get_reviews,
    get_inventory = get_inventory, address = address, firstname = firstname)

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

@bp.route('/balance', methods = ['GET', 'POST'])
def update_balance():
    form = UpdateBalanceForm()
    if form.validate_on_submit():
        User.update_balance(current_user.balance,
                            form.withdraw.data,
                            form.top.data,
                            current_user.id)          
        return redirect(url_for('users.publicView'))
    form.withdraw.data = 0.00
    form.top.data = 0.00
    return render_template('update_balance.html',
    form = form, balance = current_user.balance)
    

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
