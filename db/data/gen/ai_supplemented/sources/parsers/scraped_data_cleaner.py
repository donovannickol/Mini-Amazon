import pandas as pd
from decimal import Decimal

def clean_scraped_data(source_directory, dest_directory, delimiter):
    desired_columns = ["ASIN", "Color", "Country_of_Origin", "Dimensions", "Image_URL_1", "Item_Weight", "Manufacturer_Name", "Price",
    "Product_Bread_Crumb_Path", "Product_Category", "Product_Description", "Product_Details", "Product_Dimensions", "Product_Information",
    "Title", "Star_Rating"]

    df = combine_data(source_directory)
    df = df[desired_columns]
    df = drop_missing(df)

    df = filter_amazon_prods(df)
    df = remove_free(df)

    df = remove_corrupted(df, delimiter)

    df.reset_index(inplace=True, drop=True)

    df['ASIN'] = df.index

    df['Product_ID'] = df['ASIN']

    df = df.drop(columns=['ASIN'])

    df.to_csv(dest_directory +"/combined.csv", sep=delimiter, index=False)


def remove_free(df):
    df['Price'] = df['Price'].str.replace(',', '')
    df['Price'] = df['Price'].str.replace('$', '')
    df['Price'] = df['Price'].astype(float)
    return df[df['Price'] > 1]

def drop_missing(df):
    essential_columns = ["ASIN", "Image_URL_1", "Price", "Title"]
    return df.dropna(subset=essential_columns)

def combine_data(source_directory):
    df1 = pd.read_csv(source_directory + "/amazonasin_a.csv")
    df2 = pd.read_csv(source_directory + "/amazonasin_b.csv")
    frames = [df1,df2]
    return pd.concat(frames, sort=True)

def remove_corrupted(df, delimiter):
    columns = df.columns.values
    for column in columns:
        if df[column].dtype == str:
            df[column] = df[df[column].str.contains(delimiter)==False]
    return df

def filter_amazon_prods(df):
    df = df[df["Title"].str.contains("amazon")==False]
    df = df[df["Title"].str.contains("Amazon")==False]
    df = df[df["Title"].str.contains("AMAZON")==False]
    return df
