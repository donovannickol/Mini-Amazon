from functools import lru_cache
import json
import pandas as pd
  


def load_address_dict(filename):
    f = open(filename)
    data = json.load(f)['addresses']
    return data

def convert_to_df(dict):
    addresses = pd.DataFrame.from_dict(dict)
    coords = list(addresses['coordinates'])
    coords = pd.DataFrame(coords)
    addresses[['latitude','longitude']] = coords
    addresses = addresses.drop(columns=['coordinates'])
    addresses = addresses.drop_duplicates(['address1', 'address2', 'city', 'state'])
    return addresses

def df_to_csv(destfile, df, delimiter):
    df.to_csv(destfile + "/addresses.csv", sep=delimiter, header=False, index=False, line_terminator="\n")
    
def clean_json(sourcefile, destfile, delimiter):
    filename = 'addresses-us-all.json'
    data = load_address_dict(sourcefile + "/" + filename)
    df = convert_to_df(data)
    df_to_csv(destfile, df, delimiter)
