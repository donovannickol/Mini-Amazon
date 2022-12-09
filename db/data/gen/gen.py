import pandas as pd
import numpy as np
import random

from print_styles import bcolors
# from gen.print_styles import bcolors
from random import randint
from math import floor
from math import ceil
from time import perf_counter
from mimesis import Person
from mimesis import Address
from werkzeug.security import generate_password_hash
from mimesis import Datetime
from time import perf_counter

#SPECIAL VALUES
delimiter="^"


###SETUP
products_df = pd.read_csv("ai_supplemented/complete/products.csv", sep=delimiter)
products_df = products_df.drop(columns=["Unnamed: 0"])
ratings_df = pd.DataFrame()
# conversations_df = pd.DataFrame()
ratings_df = pd.read_csv("ai_supplemented/complete/reviews.csv", sep=delimiter)
# ratings_df = pd.read_csv("ai_supplemented/complete/ratings.csv", sep=delimiter)
# conversations_df = pd.read_csv("ai_supplemented/complete/conversations.csv", sep=delimiter)
# conversations_df = pd.read_csv("ai_supplemented/complete/conversations.csv", sep=delimiter)
sellers_df = pd.DataFrame()
sales_df = pd.DataFrame()
rng = np.random.default_rng()

##Global Variables -- values set within their respective functions
active_users = 300
# active_users=100
average_num_sellers = 8 ## Approximate number of sellers for each products
unmarked_category = "Miscellaneous" #Default label for any product that doesn't have a category
print_frequency = 25 ## How many times should each function indicate its progress
avg_orders_per_person = 4 ## How many orders the average person makes
avg_purchases_per_order = 6 ## How many products are in the average order
email_domains = ["stuffhub.com", "live.com", "outlook.com", "duke.edu", "gmail.com", "aol.com", "protonmail.com"]
curr_num_orders = 0

person = Person()
address = Address()
datetime = Datetime()
start_index = 0 # Helper variable for printing
curr_index = 0  # Helper variable for printing

def gen_all(num_users):
    global active_users, average_num_sellers
    active_users = num_users


    ###dummy declarations to be deleted
    global ratings_df, conversations_df
    # ratings_df = pd.DataFrame([[i, random.randint(1,5), "Good/Bad"] for i in range(products_df.shape[0])], columns=["Product_ID","Rating","Review"])
    conversations_df = pd.DataFrame([[i, True if i % 2 == 0 else False, "Hi/Bye"] for i in range(products_df.shape[0])])
    ####end dummies

    t_start = perf_counter()

    print(f"{bcolors.WARNING}CAUTION: Do NOT terminate the program after the first table has been generated.{bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}DETAILS: To satisfy SQL foreign key and uniqueness constraints, all data must be generated atomically. All datasets are dependent on the selected number of users and the number of products. Since these values can change at runtime (as duplicates are dropped), it is very important that the program is left to run to completion.{bcolors.ENDC}\n\n")

    gen_users()

    print(f"{bcolors.FAIL}WARNING: You MUST let the program run to completion at this point.{bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}DETAILS: Because the Users table has been generated at this point, terminating the program risks violating foreign key constraints. If you do terminate the program, be sure to run it again before loading any SQL table.{bcolors.ENDC}\n\n")

    gen_inventory()
    clean_up_products()
    gen_sales()
    # gen_ratings()
    gen_reviews()


    t_stop = perf_counter()

    add_amazon()

    if(t_stop > 60):
        print(f"\nGenerated all data in {ceil((t_stop - t_start)/60)} minute(s) and {ceil(((t_stop - t_start)/60 % 1)*60)} second(s).")
    else:
        print(f"\nGenerated all data in {ceil(t_stop - t_start)} second(s).")

def gen_users():
    global active_users, start_index, curr_index

    print_start("Users", active_users)

    df = pd.DataFrame([["","","","","","","",""]]*active_users, columns =["Email","Password","Firstname","Lastname","Address","City","State","Balance"])
    df = df.apply(generate_user_details,raw=True, axis=1)  
    password = "amazonsucks"
    df.loc[0] = ["beff.jezos@stuffhub.com", generate_password_hash(password),"Beff", "Jezos", "21218 76th Ave. S. Kent", "Seattle", "Washington", f"{117500000000+ random.random()}"] 
    df = df.drop_duplicates(subset=["Email"])
    df.reset_index(inplace=True,drop=True)
    active_users = df.shape[0]

    df.to_csv("complete/users.csv",quoting=1, quotechar='"', lineterminator="\n",header=False, sep=delimiter)

    df = pd.DataFrame()

    print_end("Users")

def gen_inventory():
    global sellers_df, curr_count
    sellers_df = products_df.copy(deep=True)
    sellers_df["Seller_ID"] = [""]*products_df.shape[0]
    sellers_df["Inventory"] = [""]*products_df.shape[0]
    sellers_df = sellers_df[["Seller_ID", "Product_ID", "Inventory", "Price"]] 

    print_start_counting("Sellers")

    sellers_df = sellers_df.apply(gen_seller_ids, raw=True, axis=1)
    sellers_df = sellers_df.explode("Seller_ID")

    print_start("Sellers", sellers_df.shape[0])

    sellers_df = sellers_df.apply(gen_seller_inventory, raw=True, axis=1)

    sellers_df.drop_duplicates(subset=["Seller_ID","Product_ID"],inplace=True)

    sellers_df.reset_index(inplace=True,drop=True)

    sellers_df.to_csv("complete/inventory.csv",header=False, index=False, lineterminator="\n", sep=delimiter)

    print_end("Sellers")

def gen_sales():
    global sales_df

    print_start_counting("Sales")

    sales_df = pd.DataFrame([["","","","","","","","",""]]*active_users, columns=["Buyer_ID","Personal_Order_Number","Personal_Purchase_Number","Product_ID","Seller_ID","Quantity","Price","Fullfill_Date","Sell_Time"])
    sales_df = sales_df.apply(determine_num_orders, raw=True, axis=1)
    sales_df = sales_df.explode("Personal_Order_Number","Personal_Purchase_Number")
    sales_df = sales_df.explode("Personal_Purchase_Number")
    sales_df.dropna(inplace=True)

    print_start("Sales", sales_df.shape[0])

    sales_df = sales_df.apply(make_purchases, raw=True, axis=1)

    sales_df.reset_index(inplace=True,drop=True)

    sales_df.to_csv("complete/sales.csv")

    print_end("Sales")

    print_start_counting("orders")
    # sales_df.sort_values("Fullfill_Date", inplace=True)


    sales_df.drop_duplicates(subset=["Buyer_ID","Personal_Order_Number","Product_ID","Seller_ID"],inplace=True)

    orders_df = sales_df[["Buyer_ID","Personal_Order_Number","Product_ID","Seller_ID","Quantity","Price","Fullfill_Date"]].copy(deep=True)
    # purchases_df = sales_df[["Personal_Order_Number","Buyer_ID","Price","Quantity","Fullfill_Date","Sell_Time"]].copy(deep=True)

    orders_df["Timestamp"] = sales_df["Fullfill_Date"] + " " + sales_df["Sell_Time"]
    # purchases_df["Fullfill_Date"] = orders_df["Timestamp"]


    orders_df = orders_df[["Buyer_ID","Personal_Order_Number","Product_ID","Seller_ID","Quantity","Price","Timestamp"]]
    # orders_df.sort_values("Timestamp",inplace=True)
    orders_df.reset_index(inplace=True,drop=True)

    purchases_df = orders_df[["Personal_Order_Number","Buyer_ID","Price","Quantity","Timestamp"]].copy(deep=True)

    # orders_df.drop_duplicates(subset=["Buyer_ID","Personal_Order_Number","Product_ID","Seller_ID"],inplace=True)

    orders_df.to_csv("complete/orderhistory.csv",header=False, index=False, lineterminator="\n", sep=delimiter)
    orders_df = pd.DataFrame()
    
    print_start_counting("purchases")

    purchases_df = purchases_df.groupby(by=['Personal_Order_Number', 'Buyer_ID','Timestamp'], as_index=False).sum()
    print("Finished grouping purchases", flush=True)
    # purchases_df["Timestamp"] = purchases_df["Fullfill_Date"]
    purchases_df["Fullfill_Date"] = ["Fullfilled"]*purchases_df.shape[0]
    # purchases_df = purchases_df[["Personal_Order_Number","Buyer_ID","Price","Quantity","Fullfill_Date","Timestamp"]]
    # purchases_df.sort_values("Fullfill_Date",inplace=True)
    purchases_df.reset_index(inplace=True, drop=True)

    purchases_df["Purchase_ID"] = purchases_df.index

    purchases_df = purchases_df[["Purchase_ID","Buyer_ID","Price","Quantity","Fullfill_Date","Timestamp","Personal_Order_Number"]]

    purchases_df.to_csv("complete/purchases.csv", header=False, index=False, lineterminator="\n", sep=delimiter)
    purchases_df = pd.DataFrame()

    print("Exported purchases", flush=True)

def gen_reviews():
    print_start_counting("Reviews")

    reviews_df = sales_df.copy(deep=True)
    reviews_df = reviews_df[["Buyer_ID","Product_ID","Seller_ID","Fullfill_Date"]]
    reviews_df["Rating"] = [""]*reviews_df.shape[0]
    reviews_df["Review"] = [""]*reviews_df.shape[0]
    # reviews_df = reviews_df[["Buyer_ID", "Product_ID", "Seller_ID", "Rating","Review","Fullfill_Date"]]
    reviews_df = reviews_df[["Buyer_ID", "Product_ID", "Seller_ID","Rating","Review","Fullfill_Date"]]

    print_start("Reviews", reviews_df.shape[0])

    # reviews_df = reviews_df.apply(fetch_review, raw=True, axis=1)
    # reviews_df = pd.merge(ratings_df, reviews_df, on="Product_ID")
    reviews_df = reviews_df.apply(fetch_review, raw=True, axis=1)
    reviews_df.reset_index(inplace=True,drop=True)

    # reviews_df.sort_values("Fullfill_Date")


    reviews_df = reviews_df[["Buyer_ID", "Product_ID", "Rating","Review", "Fullfill_Date"]]

    reviews_df.drop_duplicates(subset=["Buyer_ID","Product_ID"],inplace=True)

    reviews_df.to_csv("complete/reviews.csv", header=False, index=False, lineterminator="\n", sep=delimiter)

    print_end("Reviews")


def only_gen_reviews():
    global sales_df
    sales_df = pd.read_csv("complete/sales.csv")

    gen_ratings()
    gen_reviews()

def only_gen_users():
    print(f"{bcolors.FAIL}WARNING: After generating the users table, you MUST generate all other datasets again or risk violating foreign key constraints.{bcolors.ENDC}")

    gen_users()

def only_gen_sales():
    global active_users, sellers_df
    users_df = pd.read_csv("complete/users.csv")
    active_users = users_df.shape[0]
    users_df = pd.DataFrame()
    sellers_df = pd.read_csv("complete/inventory.csv")

    gen_sales()



def only_gen_reviews():
    global sales_df
    sales_df = pd.read_csv("complete/sales.csv")

    gen_ratings()
    gen_reviews()


##TODO: write the code to generate conversations
def gen_conversations():

    print_start_counting("Conversations")

    messages_df = sales_df.copy(deep=True)
    messages_df = messages_df[["Buyer_ID","Product_ID","Seller_ID","Fullfill_Date"]]
    messages_df["Rating"] = [""]*messages_df.shape[0]
    messages_df["Review"] = [""]*messages_df.shape[0]
    messages_df = messages_df[["Buyer_ID", "Product_ID", "Seller_ID", "Rating","Review","Fullfill_Date"]]

    print_start("Conversations", messages_df.shape[0])

    messages_df = messages_df.apply(fetch_review, raw=True, axis=1)

    print_end("Conversations")

def fetch_conversation(row):
    print_progress()
    valid_reviews = ratings_df.loc[ratings_df["Product_ID"] == row[1]]
    valid_reviews.reset_index(inplace=True, drop=True)
    index = random.randrange(0,valid_reviews.shape[0])
    row[3] = valid_reviews["Rating"][index]
    row[4] = valid_reviews["Review"][index]
    return row


#######
#HELPER FUNCTIONS
#######

def fetch_review(row):
    print_progress()
    valid_reviews = ratings_df.loc[ratings_df["Product_ID"] == row[1]]
    valid_reviews.reset_index(inplace=True,drop=True)
    index = random.randrange(0,valid_reviews.shape[0] - 1)
    row[3] = valid_reviews["Rating"][index]
    row[4] = valid_reviews["Review"][index]
    return row

def determine_num_orders(row):
    global curr_num_orders
    num_orders = random.randint(0,avg_orders_per_person*2)
    row[1] = np.arange(curr_num_orders,num_orders + curr_num_orders)
    curr_num_orders += num_orders
    row[2] = [np.arange(1,randint(1,avg_purchases_per_order*2)+1) for i in range(num_orders)]
    row[7] = str(datetime.date())
    row[8] = str(datetime.time()).split(".")[0]
    return row

def make_purchases(row):
    print_progress()
    seller_id = random.randrange(0,sellers_df.shape[0])
    buyer_id = random.randrange(0,active_users)
    while(buyer_id == seller_id):
        buyer_id = random.randrange(0,active_users)
    row[0] = buyer_id
    row[3] = sellers_df["Product_ID"][seller_id]
    row[4] = sellers_df["Seller_ID"][seller_id]
    row[5] = random.randint(1,250)
    row[6] = sellers_df["Price"][seller_id]
    return row
def clean_up_products():
    global products_df

    print_start("Products", products_df.shape[0])

    products_df = products_df.drop(columns=["Price"])

    products_df = products_df.apply(isolate_category, raw=True, axis=1)

    products_df.to_csv("complete/products.csv", header=False, index=False, lineterminator="\n", sep=delimiter)

    categories_df = pd.DataFrame(products_df["Product_Category"]).drop_duplicates()
    categories_df.reset_index(inplace=True,drop=True)
    categories_df.loc[categories_df.shape[0]] = ["Website"]
    categories_df["Index"] = categories_df.index
    categories_df = categories_df[["Index","Product_Category"]]

    categories_df.to_csv("complete/categories.csv", header=False, index=False, lineterminator="\n", sep=delimiter)

    print_end("Products")

def isolate_category(row):
    print_progress()
    long_category = row[4]
    output_category = long_category
    if type(long_category) != float:
         output_category = long_category.split(" in ")[-1].split("\n")[0] 
    else:
        output_category = unmarked_category
    row[4] = output_category
    return row

def add_amazon():
    global products_df, sellers_df

    num_products = products_df.shape[0]
    num_sellers = sellers_df.shape[0]
    
    products_df.loc[num_products] = [num_products, "Amazon.com", "An up-and-coming e-retailing platform based out of Washington.", "data:image/png;base64,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", "Website"]

    sellers_df.loc[num_sellers] = [0,num_products,1, 960280000000 + random.random()]
    sellers_df[["Seller_ID", "Product_ID","Inventory"]] = sellers_df[["Seller_ID", "Product_ID","Inventory"]].astype("int")

    products_df.to_csv("complete/products.csv",header=False, index=False, lineterminator="\n", sep=delimiter)
    sellers_df.to_csv("complete/inventory.csv",header=False, index=False, lineterminator="\n", sep=delimiter)

def print_start(data,quantity):
    global start_index, curr_index, curr_count
    curr_count = 0
    start_index, curr_index = quantity, quantity
    print(f"{bcolors.HEADER}Generating {quantity:,} {data}..{bcolors.ENDC}", end=" ", flush=True)

def print_end(data):
    print(f"\n{bcolors.HEADER}Finished generating {data}.{bcolors.ENDC}\n", flush=True)

def print_start_counting(data):
    print(f"Calculating number of {data}", flush=True)

def print_progress():
    global curr_index
    if(floor(curr_index % floor(start_index/print_frequency)) == 0):
        if(curr_index > floor(start_index*2/3)):
            print(f"{bcolors.OKBLUE}{curr_index:,}{bcolors.ENDC}", end=" ", flush=True)
        elif(curr_index > floor(start_index*1/3)):
            print(f"{bcolors.OKCYAN}{curr_index:,}{bcolors.ENDC}", end=" ", flush=True)
        else:
            print(f"{bcolors.OKGREEN}{curr_index:,}{bcolors.ENDC}", end=" ", flush=True)
    curr_index -= 1

def generate_user_details(row):
    print_progress()
    name = person.full_name().split(" ")
    return [person.email(email_domains), person.password(hashed=True), name[0], name[1], address.address(), address.city(), address.state(), random.randint(0,5000) + random.random()]

def gen_seller_ids(row):
    max_num_sellers = average_num_sellers*2 -1
    val = rng.integers(low=0, high=active_users, size=random.randint(1,max_num_sellers))
    row[0] = val
    return row


def gen_seller_inventory(row):
    print_progress()
    price = get_price(row[3])
    inventory = randint(0,6000)
    row[3] = price
    row[2] = inventory
    return row
    

def get_price(price):
    lower_bound = floor(price*0.9)
    upper_bound = ceil(price*1.1) 
    integer_component = randint(lower_bound, upper_bound)
    decimal_component = randint(0,99)
    return float(f'{str(integer_component)}.{decimal_component:02}')

row_num = 0

review_map = {1: "very negative", 2: "negative", 3:"neutral", 4:"positive", 5:"very positive"}

def gen_ratings():

    global row_num, ratings_df

    t1_start = perf_counter()

    df = pd.read_csv("ai_supplemented/complete/products.csv", sep="^")

    df["Rating"] = 0
    df["Review"] = 0
    df = df[["Product_ID", "Rating","Title", "Review"]]

    num_products = df.shape[0]


    print("Generating Product Review Distribution...", end=" ", flush=True)
    
    df = df.apply(gen_review_distribution, raw=True, axis=1)

    ## Expand out the list distribution so that each index is its own row
    df = df.explode("Rating")

    row_num = 0

    print("\nGenerating Product Reviews...", end=" ", flush=True)

    df = df.apply(gen_review, raw=True, axis=1)

    t2_stop = perf_counter()

    print("\nGenerated", row_num, "reviews for", num_products, "products in", t2_stop-t1_start, "seconds.")

    df = df.drop(columns=["Title"])
    # ratings_df = df
    # df.to_csv("complete/reviews.csv", sep="^")


def gen_review_distribution(row):
    global row_num
    if(row_num % 100 == 0):
        print(row_num, end=" ", flush=True)
    row_num += 1
    row[1] = [random.randint(1,5) for i in range(20)]
    return row

def gen_review(row):
    global row_num
    row[3] = review_map[row[1]]
    if(row_num % 100 == 0):
        print(row_num, end=" ", flush=True)
        if(row_num % 500 == 0) :
            print("Sample review:", row[3])
    row_num += 1
    return row

gen_all(active_users)