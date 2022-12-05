import os
import openai

import pandas as pd
import numpy as np
import random
import openai_keys as keys
from time import perf_counter


#SETUP
openai.organization = keys.config['ORG_KEY']
openai.api_key = os.getenv(keys.config['SECRET_KEY'])
openai.api_key=keys.config['SECRET_KEY']
model=keys.model
max_tokens=keys.max_tokens
temp=keys.temp


row_num = 0

def gen_conversations():
    global row_num

    t1_start = perf_counter()

    df = pd.read_csv("complete/products.csv", sep="^")

    df["FROM_SELLER"] = False
    df["Message"] = 0
    df = df[["Product_ID", "FROM_SELLER","Title","Message"]]

    num_products = df.shape[0]

    print("Generating Product Conversation Distribution...", end=" ", flush=True)

    df = df.apply(gen_conversation_distribution, raw=True, axis=1)
    
    ## Expand out the list distribution so that each index is its own row
    df = df.explode("FROM_SELLER")

    row_num = 0

    print("\nGenerating Product Conversations...", end=" ", flush=True)

    df = df.apply(gen_conversation, raw=True, axis=1)


    t2_stop = perf_counter()

    print("\nGenerated", row_num, "conversations for", num_products, "products in", t2_stop-t1_start, "seconds.")

    df = df.drop(columns=["Title"])
    df.to_csv("complete/conversations.csv", sep="^")


def gen_conversation_distribution(row):
    global row_num
    if(row_num % 100 == 0):
        print(row_num, end=" ", flush=True)
    row_num += 1
    row[1] = [True for i in range(5)] + [False for i in range(5)]
    return row

def gen_conversation(row):
    global row_num
    sender = "seller"
    recepient = "buyer"
    if(not row[1]):
        sender = "buyer"
        recepient = "seller"
    prompt = "Write a message from a " + sender + " to a " + recepient + " about \"" + row[2] + "\"" 
    tokens = max_tokens - len(prompt) - 1
    row[3] = openai.Completion.create(
        model=model,
        prompt=prompt,
        max_tokens=tokens,
        temperature=temp
    )["choices"][0]['text']
    if(row_num % 100 == 0):
        print(row_num, end=" ", flush=True)
        if(row_num % 500 == 0) :
            print("Sample message:", row[3])
    row_num += 1
    return row

# gen_conversations()