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
from .models.orderhistory import OrderHistory
from .models.sellerRating import SellerRating
from .models.productRating import ProductRating

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

# Procedure to get the purchase page for the user
@bp.route('/all_purchases/', methods = ['GET','POST'])
def get_all_purchases():
    uid = current_user.id
    # Obtain all purchases for a user by given ID
    get_all_purchases = Purchase.get_all_by_uid(uid)
    firstname = current_user.firstname
    # Obtain order history for a given pid
    whatIOrdered = OrderHistory.productsUserOrd(uid) 
    return render_template('get_all_purchases.html',
                            get_all_purchases = get_all_purchases, 
                            firstname = firstname, whatIOrdered=whatIOrdered)

# Procedure to get the purchase page for a user, with total prices less than specified amount
@bp.route('/purchases_less_than_max/', methods = ['GET', 'POST'])
def get_all_purchases_less_than_max():
    uid = current_user.id
    maxi = request.form['max']
    if maxi == "" or float(maxi) < 0:
        # If no amount is listed or if the amount listed is negative, redirects to regular purchase page
        get_all_purchases = Purchase.get_all_by_uid(uid)
    else:
        # Obtains all purchases with a total price less than specified amount
        get_all_purchases = Purchase.get_all_by_uid_max_price(current_user.id, maxi)
    firstname = current_user.firstname
    return render_template('get_all_purchases.html',
                            get_all_purchases = get_all_purchases, 
                            firstname = firstname)

# Procedure to get the purchase page for a user, with number of items less than specified amount
@bp.route('/purchases_less_than_items/', methods = ['GET', 'POST'])
def get_all_purchases_less_than_items():
    uid = current_user.id
    items = request.form['max']
    if items == "" or int(items) < 0:
        # If no amount is listed or if the amount listed is negative, redirects to regular purchase page
        get_all_purchases = Purchase.get_all_by_uid(uid)
    else:
        # Obtains all purchases with a number of items less than specified amount
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

# Ensures that an email entered by a user does not already exist
def validate_email(form, field):
    if (User.email_exists(field.data)):
        raise ValidationError("Please enter a different email.")

# Form for a user to register
class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), validate_email])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

# Form for a user to update their information
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

# Ensures that amount to be withdrawn is less than user's balance
def validate_withdrawal(form, field):
        if (field.data > current_user.balance):
            raise ValidationError("Must be less than or equal to balance")

# Form for a user to update their balance
class UpdateBalanceForm(FlaskForm):
    # Field to withdraw - must be greater than 0 and less than balance
    withdraw = DecimalField('Withdraw', 
                            validators = [NumberRange(min = 0, 
                            message = "Must be greater than 0"), validate_withdrawal])
    
    # Field to add to balance - must be greater than 0
    top = DecimalField('Add to Balance',
                       validators = [NumberRange(min = 0,
                       message = "Must be greater than 0")])
    
    # Updates balance accordingly
    submit = SubmitField('Update Balance')

# Procedure for retrieving the account page for an authenticated user
@bp.route('/account', methods = ['GET','POST'])
def publicView():
    # Lines 142-160: Obtains relevant user information (e.g., account ID, balance)
    id_number = current_user.id
    name = f'{current_user.firstname} {current_user.lastname}'
    email = current_user.email
    get_reviews = pRatingNAMES.get(id_number)
    get_sreviews = SellerRating.get_personal(current_user.id)
    get_inventory = Inventory.get_by_uid(id_number)
    average_review =SellerRating.get_average_rating(current_user.id)
    number_of_reviews = SellerRating.get_numbers_of_rating(current_user.id)

    pRated = ProductRating.get_by_user_id_tot(id_number)
    whatIOrdered = OrderHistory.productsUserOrd(id_number)
    sRated = SellerRating.get_personal(id_number)
    seller_names = SellerRating.get_pot_sellers()

    error = ''
    if request.args.get('error'):
        error = request.args.get('error')    
    location = current_user.city + ", " + current_user.state
    balance = "$" + str(current_user.balance)
    # Renders account page with given information
    return render_template('user_public_view.html', 
    id = id_number, name = name, email = email, location = location, balance = balance,
    error = error, get_reviews = get_reviews, get_inventory = get_inventory, get_sreviews=get_sreviews, whatIOrdered=whatIOrdered, pRated=pRated, sRated=sRated, seller_names=seller_names,
    number_of_reviews = number_of_reviews, rating=average_review)

@bp.route('/review_page', methods = ['GET', 'POST'])
def reviewPage():
    id_number = current_user.id
    name = f'{current_user.firstname} {current_user.lastname}'
    email = current_user.email
    get_reviews = pRatingNAMES.get(id_number)
    get_sreviews = SellerRating.get_personal(current_user.id)
    get_inventory = Inventory.get_by_uid(id_number)
    average_review =SellerRating.get_average_rating(current_user.id)
    number_of_reviews = SellerRating.get_numbers_of_rating(current_user.id)

    pRated = ProductRating.get_by_user_id_tot(id_number)
    whatIOrdered = OrderHistory.productsUserOrd(id_number)
    sRated = SellerRating.get_personal(id_number)
    seller_names = SellerRating.get_pot_sellers()
    error = ''
    if request.args.get('error'):
        error = request.args.get('error')    
    location = current_user.city + ", " + current_user.state
    balance = "$" + str(current_user.balance)
    return render_template('review.html', 
    id = id_number, name = name, email = email, location = location, balance = balance,
    error = error, get_reviews = get_reviews, get_inventory = get_inventory, get_sreviews=get_sreviews, whatIOrdered=whatIOrdered, pRated=pRated, sRated=sRated, seller_names=seller_names,
    number_of_reviews = number_of_reviews, rating=average_review)

@bp.route('/user_search', methods = ['GET', 'POST'])
def userSearch():
    search_term = request.form['search_term']
    public = request.args.get('public', "", type = str)
    # If the user enters a blank entry, prompts them to enter an ID
    if search_term == "":
        # Redirects them to their account page with appropriate error message displayed
        return redirect(url_for('users.publicView', error = "Please enter an ID"))
    # If the user enters a negative number, prompts them to enter a positive number
    if (int(search_term) < 0):
        # Redirects them to their account page with appropriate error message displayed
        return redirect(url_for('users.publicView', error = "Please enter a number greater than 0"))
    # If the user's search passes the checks, redirects them to public view of the user with corresponding ID
    return redirect(url_for('users.getPublicView', search_term = search_term))

# Proecedure for retrieving the public view of another user
@bp.route('/public_view', methods = ['GET','POST'])
def getPublicView():
    id_number = request.args.get('search_term', "", type=str)
    # Obtains the user that corresponds to the ID given in userSearch()
    the_user = User.get(id_number)
    # If corresponding user does not exist, informs the user as much
    if the_user == None:
        # Redirects user to their account page with approriate error message
        return redirect(url_for('users.publicView', error = "User does not exist"))
    # Lines 191-199: Obtains relevant user information (e.g., name, email, address, inventory (if any))
    average_review =SellerRating.get_average_rating(id_number)
    number_of_reviews = SellerRating.get_numbers_of_rating(id_number)
    name = f'{the_user.firstname} {the_user.lastname}'
    firstname = the_user.firstname
    email = the_user.email
    address = the_user.address + ", " + the_user.city + ", " + the_user.state
    balance = "$" + str(the_user.balance)
    get_reviews = pRatingNAMES.get(id_number)
    get_inventory = Inventory.get_by_uid(id_number)
    # Renders public view page for the user with corresponding ID number
    return render_template('user_actual_public_view.html', 
    id  = id_number, name = name, email = email, balance = balance, get_reviews = get_reviews,
    get_inventory = get_inventory, address = address, firstname = firstname, number_of_reviews = number_of_reviews, rating=average_review)

# Procedure for enabling the user to update their information
@bp.route('/update_info', methods = ['GET', 'POST'])
def update_info():
    # Establishes the content of the form to be displayed
    form = UpdateForm()
    # If the form validates, updates user with given information
    if form.validate_on_submit():
        if User.update_user(form.firstname.data,
                            form.lastname.data,
                            form.email.data,
                            form.address.data,
                            form.city.data,
                            form.state.data,
                            form.password.data,
                            current_user.id):
          # Redirects user to their account page, which should display updated information  
          return redirect(url_for('users.publicView'))
    # Pre-sets all fields (except password) to current user information
    form.firstname.data = current_user.firstname
    form.lastname.data = current_user.lastname
    form.email.data = current_user.email
    form.address.data = current_user.address
    form.city.data = current_user.city
    form.state.data = current_user.state
    # Renders template for update information page
    return render_template('update_info.html',
    old_user = current_user, form = form)

# Proceudre to enable the user to update their balance
@bp.route('/balance', methods = ['GET', 'POST'])
def update_balance():
    # Establishes the content of the form to be displayed
    form = UpdateBalanceForm()
    # If the form validates, updates balance with given information
    if form.validate_on_submit():
        User.update_balance(current_user.balance,
                            form.withdraw.data,
                            form.top.data,
                            current_user.id)          
        return redirect(url_for('users.publicView'))
    # Pre-sets the amount to be withdrawn/added to $0.00
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
