import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
import sys

filepath = "/home/vcm/mini-amazon/db/data/gen/complete/"
sep = "^"
  
# conn_string = 'postgres://user:password@host/data1'

# db = create_engine(conn_string)
# conn = db.connect()

  
# Create DataFrame
conn_string = "postgresql+psycopg2:///amazon"


db = create_engine(conn_string, poolclass=QueuePool)
# conn = db.connect()
# conn = psycopg2.DB(host="vcm-28570.vm.duke.edu", user="vcm", passwd="pErfryr5vy", dbname="amazon")
conn = psycopg2.connect(host="vcm-28570.vm.duke.edu", user="vcm", password="pErfryr5vy", dbname="amazon")

def load(df, table_name):
    global conn
    df.to_sql(table_name, con=conn, if_exists='replace',
            index=False, method='multi')
    # conn = psycopg2.connect(conn_string
    #                         )
    conn = psycopg2.connect(host="vcm-28570.vm.duke.edu", user="vcm", passwd="pErfryr5vy", dbname="amazon")
    conn.autocommit = True
    cursor = conn.cursor()

def load_all():
    global conn
    users = pd.read_csv(filepath+"users.csv",sep=sep)
    load(users, "Users")

    categories = pd.read_csv(filepath+"categories.csv",sep=sep)
    load(categories, "Categories")

    products = pd.read_csv(filepath+"products.csv",sep=sep)
    load(products, "Products")

    purchases = pd.read_csv(filepath+"purchases.csv", sep=sep)
    load(purchases, "Purchases")

    inventory = pd.read_csv(filepath+"inventory.csv", sep=sep)
    load(inventory, "Inventory")

    cart = pd.read_csv("Cart.csv",sep=",")
    load(cart, "Cart")

    orderhistory = pd.read_csv(filepath+"orderhistory.csv",sep=sep)
    load(orderhistory, "OrderHistory")

    productrating = pd.read_csv(filepath+"reviews.csv",sep=sep)
    load(productrating, "productRating")

    sellerrating = pd.read_csv(filepath+"reviews.csv",sep=sep)
    load(sellerrating, "SellerRating")

load_all()