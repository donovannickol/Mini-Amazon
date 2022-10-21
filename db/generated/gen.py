from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_products = 2000
num_purchases = 2500

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


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
            # generate random valid img url
            # img_url = f'https://picsum.photos/id/{fake.random_int(min=0, max=500)}/200'
            # generate img url using faker
            img_url = fake.image_url(width=200, height=200)
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            category = fake.random_element(elements=['Books', 'Movies', 'Music'])
            available_pids.append(pid)
            writer.writerow([pid, name, description, img_url, price, category])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids

def gen_categories():
    with open('Categories.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Categories...', end=' ', flush=True)
        for category in ['Books', 'Movies', 'Music']:
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


gen_users(num_users)
gen_categories()
available_pids = gen_products(num_products)
gen_purchases(num_purchases, available_pids)