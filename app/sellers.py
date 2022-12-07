from .models.inventory import Inventory
from flask_login import current_user
from app import products
from .models.product import Product
from .models.inventory import Inventory
from .models.orderhistory import OrderHistory
import base64
from io import BytesIO
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from flask import render_template, request, redirect, url_for

from flask import Blueprint
bp = Blueprint('sellers', __name__)

@bp.route('/seller_inventory/', methods=['POST','GET'])
def seller_inventory():
    sid = request.args.get('sid')
    seller_inventory = Inventory.get_by_uid(sid)
    return render_template('inventory.html',
                           sid = sid,
                           seller_inventory = seller_inventory)

@bp.route('/full_seller_inventory/', methods=['POST', 'GET'])
def get_full_seller_inventory():
    sid = request.args.get('sid')
    seller_inventory = Inventory.get_full_details_by_uid(sid)
    return render_template('inventory.html',
                           sid = sid,
                           seller_inventory = seller_inventory)

@bp.route('/delete_inventory/<int:sid>/<int:pid>', methods=['POST','GET'])                 
def delete_inventory(sid, pid):
        Inventory.delete_product(sid, pid)
        return products.product(pid)

@bp.route('/seller_history/', methods=['POST','GET'])
def seller_history():
    sid = request.form['sid'] if request.method == "POST" else current_user.id
    seller_inventory = Inventory.get_seller_detailed_history(sid)
    return render_template('seller_history.html',
                           sid = sid,
                           seller_history = seller_inventory,
                           order_history = OrderHistory)

@bp.route('/seller_history/fulfill/<int:order_number>', methods=['POST','GET'])
def flip_fulfill(order_number):
    sid = request.form['sid'] if request.method == "POST" else current_user.id
    OrderHistory.flip_fulfilled(order_number,sid)
    seller_inventory = Inventory.get_seller_detailed_history(sid)
    return render_template('seller_history.html',
                           sid = sid,
                           seller_history = seller_inventory,
                           order_history = OrderHistory)

@bp.route('/sellers/add/<int:id>', methods=['GET', 'POST'])
def add_seller(id):
    if not current_user.is_authenticated:
        return redirect(url_for('index.index'))
    product = Product.get(id)
    form = products.ProductForm()
    form.category.choices = [(category, category) for category in Product.get_all_categories()][1:]
    if form.validate_on_submit():
        if Inventory.add_seller(current_user.id,id,form.stock.data,form.price.data):
            return redirect(url_for('products.product', id=id))
    form.name.data = product.name
    form.description.data = product.description
    form.img_url.data = product.img_url
    form.category.data = product.category
    form.price.data = product.price
    form.stock.data = 1
    return render_template('product_form.html', form=form, action="Edit Product")

@bp.route('/sellers/seller_analytics/<int:sid>', methods=['GET','POST'])
def seller_analytics(sid):
    sales = Inventory.get_seller_revenue(sid)
    item_sales = OrderHistory.get_seller_quantity_by_item(sid)


    values_map = {}
    volume_map = {}
    for row in sales:
        date = str(row[2].date())[:7]
        values_map[date] = row[1]*row[0]
        volume_map[date] = row[0]
        print(values_map[date], volume_map[date])
    
    product_map = {}
    for row in item_sales:
        product_name = row[1][:15]
        product_map[product_name] = row[0]

    courses = list(values_map.keys())
    values = list(values_map.values())

    fig = Figure()
    fig = plt.figure(figsize = (10, 5))

    plt.bar(courses, values, color ='maroon',
            width = 0.4)
    
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.title("Revenue by Month")
    plt.show()
    #save to temp buffer
    buf1= BytesIO()
    fig.savefig(buf1, format="png")

    fig = Figure()
    fig = plt.figure(figsize = (10, 5))
    # creating the bar plot
    plt.bar(volume_map.keys(), volume_map.values(), color ='maroon',
            width = 0.4)
    
    plt.xlabel("Month")
    plt.ylabel("Volume")
    plt.title("Quantity Sold by Month")
    plt.show()
    #save to temp buffer
    buf2= BytesIO()
    fig.savefig(buf2, format="png")

    fig = Figure()
    fig = plt.figure(figsize = (10, 5))
    # creating the bar plot
    plt.bar(product_map.keys(), product_map.values(), color ='maroon',
            width = 0.4)
    print(product_map.keys())
    print(product_map.values())

    plt.xlabel("Product Name")
    plt.ylabel("Volume")
    plt.title("Quantity Sold by Product")
    plt.show()
    #save to temp buffer
    buf3= BytesIO()
    fig.savefig(buf3, format="png")

    # Embed the result in the html output.
    monthly_revenue = base64.b64encode(buf1.getbuffer()).decode("ascii")
    monthly_volume = base64.b64encode(buf2.getbuffer()).decode("ascii")
    product_volume = base64.b64encode(buf3.getbuffer()).decode("ascii")
    return render_template("seller_analytics.html", monthly_revenue=f"data:image/png;base64,{monthly_revenue}",
    monthly_volume=f"data:image/png;base64,{monthly_volume}",product_volume=f"data:image/png;base64,{product_volume}")
    # return f"<img src='data:image/png;base64,{data}'/>"

