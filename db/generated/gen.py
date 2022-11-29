from werkzeug.security import generate_password_hash
import csv
import random
from faker import Faker
import pandas as pd

num_users = 100
num_products = 2000
num_purchases = 2500
categories = ['Books', 'Movies', 'Music']

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def isolate_category(long_category):
    if type(long_category) != float:
         return long_category.split(" in ")[-1].split("\n")[0] 
    else:
        return "Miscellaneous"

def get_users():
    users_df = pd.read_csv("/home/vcm/mini-amazon/db/generated/data_faker/ai_generated/user_data.csv", sep="^")
    relevant_columns = ["id","email","password","firstname","lastname","user_address","user_city","user_state","balance"]
    users_df = users_df[relevant_columns].drop_duplicates()
    users_df = users_df.drop_duplicates(subset="email")
    users_df = users_df.drop_duplicates(subset="id")
    if('Unnamed: 0' in users_df.columns.values):
        users_df = users_df.drop(columns=['Unnamed: 0'])
    users_df.to_csv("Users.csv", index=False, sep="^", quoting=1, quotechar='"', line_terminator="\n",header=False)

def get_categories():
    categories_df = pd.read_csv("/home/vcm/mini-amazon/db/generated/data_faker/ai_generated/products.csv", sep="^")
    categories_df = categories_df.dropna(subset=["Product_Category"])
    categories_df = categories_df['Product_Category']
    categories_df = categories_df.drop_duplicates()
    for i in range(len(categories_df)):
        categories_df.values[i] = isolate_category(categories_df.values[i])
    categories_df = pd.DataFrame(categories_df)
    categories_df = categories_df.drop_duplicates()
    categories_df.reset_index(inplace=True, drop=True)
    if('Unnamed: 0' in categories_df.columns.values):
        categories_df = categories_df.drop(columns=['Unnamed: 0'])
    categories_df.loc[len(categories_df.index)] = 'Miscellaneous'
    categories_df.to_csv("Categories.csv", line_terminator = "\n", sep="^",header=False)

def get_products():
    #product id, name, description, img_url, category
    products_df = pd.read_csv("/home/vcm/mini-amazon/db/generated/data_faker/ai_generated/products.csv", sep="^")
    relevant_columns = ["Product_ID", "Title", "Product_Description", "Image_URL_1", "Product_Category"]
    products_df = products_df[relevant_columns].dropna(subset=["Product_ID", "Image_URL_1"])
    products_df = products_df[relevant_columns].drop_duplicates(subset="Product_ID")

    for i in range(products_df.shape[0]):
        products_df.at[i,'Product_Category'] = isolate_category(products_df.at[i,'Product_Category'])
        if type(products_df.at[i,'Product_Description']) == float:
            products_df.at[i,'Product_Description'] = 'None'

    if('Unnamed: 0' in products_df.columns.values):
        products_df = products_df.drop(columns=['Unnamed: 0'])
    products_df.to_csv("Products.csv", sep="^", line_terminator="\n",header=False, index=False)


def get_inventory():
    relevant_columns = ['seller_id', 'seller_product_id', 'seller_quantity', 'seller_price']

    inventory_df = pd.read_csv('/home/vcm/mini-amazon/db/generated/data_faker/ai_generated/seller_data.csv', sep="^")
    inventory_df = inventory_df.drop_duplicates()
    if('Unnamed: 0' in inventory_df.columns.values):
        inventory_df = inventory_df.drop(columns=['Unnamed: 0'])
    inventory_df[['seller_id', 'seller_product_id', 'seller_quantity']] = inventory_df[['seller_id', 'seller_product_id', 'seller_quantity']].astype(int)
    inventory_df.to_csv("Inventory.csv", sep="^", header=False, index=False, line_terminator="\n")

def get_product_ratings():
    ratings_df = pd.read_csv('/home/vcm/mini-amazon/db/generated/data_faker/ai_generated/review_data.csv', sep='^')
    ratings_df[['uid', 'pid', 'stars']] = ratings_df[['uid', 'pid', 'stars']].astype(int)
    ratings_df = ratings_df.drop_duplicates(subset=['uid','pid'])
    if('Unnamed: 0' in ratings_df.columns.values):
        ratings_df = ratings_df.drop(columns=['Unnamed: 0'])
    ratings_df.to_csv("Ratings.csv", sep="^", line_terminator="\n",header=False, index=False)

def get_historys(): 
    sales_df = pd.read_csv('/home/vcm/mini-amazon/db/generated/data_faker/ai_generated/sale_data.csv', sep = '^')
    # sales_df = pd.DataFrame(columns=['buyer_id','order_number', 'product_id', 'seller_id', 'quantity', 'price','sell_date','sell_time', 'fullfill_date'])
    desired_cols = ['order_number', 'buyer_id', 'price', 'quantity', 'fullfill_date', 'sell_time']
    purchases_df = sales_df[desired_cols].groupby(by=['order_number', 'buyer_id','fullfill_date', 'sell_time'], as_index=False).sum()

    desired_cols = ['buyer_id', 'order_number', 'product_id', 'seller_id', 'quantity', 'price', 'fullfill_date']
    orders_df = sales_df[desired_cols]
    orders_df['fullfill_date'] = sales_df[['fullfill_date', 'sell_time']].agg(' '.join, axis=1)


    if('Unnamed: 0' in purchases_df.columns.values):
        purchases_df = purchases_df.drop(columns=['Unnamed: 0'])

    if('Unnamed: 0' in orders_df.columns.values):
        orders_df = orders_df.drop(columns=['Unnamed: 0'])

    purchases_df.to_csv("Purchases.csv", sep="^", line_terminator="\n",header=False, index=False)
    orders_df.to_csv("OrderHistory.csv", sep="^", line_terminator="\n",header=False, index=False)

def get_carts():
    carts_df = pd.read_csv('/home/vcm/mini-amazon/db/generated/data_faker/ai_generated/sale_data.csv', sep = '^')
    carts_df.to_csv("OrderHistory.csv", sep="^", line_terminator="\n",header=False, index=False)


get_users()
get_categories()
get_products()
get_inventory()
get_product_ratings()
get_historys()

def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for id in range(num_users):
            if id % 10 == 0:
                print(f'{id}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{id}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            user_address = profile['address']
            user_city = profile['current_location'][0]
            user_state = profile['current_location'][1]
            balance = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            writer.writerow([id, email,password, firstname, lastname, user_address, user_city, user_state, balance])
        print(f'{num_users} generated')
    return


def gen_products(num_products):
    available_pids = []
    with open('Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=2)[:-1]
            description = fake.paragraph(nb_sentences=4)
            img_url = f'https://picsum.photos/id/{fake.random_int(min=0, max=500)}/200'
            category = fake.random_element(elements=categories)
            available_pids.append(pid)
            writer.writerow([pid, name, description, img_url, category])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids

def gen_categories():
    with open('Categories.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Categories...', end=' ', flush=True)
        for category in categories:
            writer.writerow([category])
        print('generated')
    return


def gen_purchases(num_purchases, available_pids):
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            total_price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            num_of_items = fake.random_int(min=1, max = 20)
            order_status = fake.random_element(elements=['Ordered', 'Returned', 'En Route'])
            time_purchased = fake.date_time()
            writer.writerow([id, uid, total_price, num_of_items, order_status, time_purchased])
        print(f'{num_purchases} generated')
    return

def gen_inventory(num_users):
    
    with open('Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for id in range(num_users):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            if random.random() < 0.25:
                sid = id
                pids = random.sample([pid for pid in range(num_products)], random.randrange(1,100))
                for pid in pids:
                    count = random.randrange(0,5000)
                    price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
                    writer.writerow([int(sid), pid, count, price])
        # print(f'{num_users} generated; {len(available_pids)} available')
    return

def gen_products_real(num_products):
    available_pids = []
    df = pd.read_csv("data_faker/ai_generated/products.csv")
    df = df[["Title", "Product_Description","Image_URL_1", "Product_Category"]]
    with open('Real_Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(0,num_products):
            if pid > df.shape[0]:
                break
            available_pids.append(pid)
            name, description, img_url, category = df.iloc[pid]
            name = name.replace("\n", " ")
            name = name.replace(",", " ")
            if len(name) > 4096:
                name = name[:4096]
            if type(description) == str and len(description) > 8000:
                description = description[:8000]
            if type(description) != str:
                description = "Unavailable."
            else:
                description = description.replace("\n", "")
                description = description.replace(",", " ")
            if len(img_url) < 20 or len(img_url) > 1024 or "," in img_url:
                img_url = img_url[:1024]
                img_url = f'https://picsum.photos/id/{fake.random_int(min=0, max=500)}/200'
            category = fake.random_element(elements=categories)
            writer.writerow([pid, name, description, img_url, category])
    return available_pids


# available_pids = gen_products_real(num_products)
# gen_purchases(num_purchases, available_pids)
# get_products()

# gen_users(num_users)
# gen_categories()
# available_pids = gen_products(num_products)
# gen_purchases(num_purchases, available_pids)
# gen_inventory(num_users)