import pandas as pd
from decimal import Decimal

def clean_data():
    desired_columns = ["ASIN", "Color", "Country_of_Origin", "Dimensions", "Image_URL_1", "Item_Weight", "Manufacturer_Name", "Price",
    "Product_Bread_Crumb_Path", "Product_Category", "Product_Description", "Product_Details", "Product_Dimensions", "Product_Information",
    "Title", "Star_Rating"]

    df = combine_data()
    df = df[desired_columns]
    df = drop_missing(df)


    df = filter_amazon_prods(df)
    df = remove_free(df)
    
    df.to_csv("combined.csv")


def remove_free(df):
    df['Price'] = df['Price'].str.replace(',', '')
    df['Price'] = df['Price'].str.replace('$', '')
    df['Price'] = df['Price'].astype(float)

    return df[df['Price'] > 1]

def drop_missing(df):
    essential_columns = ["ASIN", "Image_URL_1", "Price", "Title"]

    return df.dropna(subset=essential_columns)

def combine_data():
    df1 = pd.read_csv("amazonasin_a.csv")
    df2 = pd.read_csv("amazonasin_b.csv")


    frames = [df1,df2]

    return pd.concat(frames, sort=True)

def filter_amazon_prods(df):
    df = df[df["Title"].str.contains("amazon")==False]
    df = df[df["Title"].str.contains("Amazon")==False]
    df = df[df["Title"].str.contains("AMAZON")==False]

    return df


clean_data()