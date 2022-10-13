-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    user_address VARCHAR(255) NOT NULL,
    user_city VARCHAR(255) NOT NULL,
    user_state VARCHAR(255) NOT NULL,
    balance DECIMAL(12, 2) NOT NULL,
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description VARCHAR(255),
    img_url VARCHAR(511)
    price DECIMAL(12,2) NOT NULL,
    category VARCHAR(255) FOREGIN KEY REFERENCES Category(name)
);

CREATE TABLE Categories (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) NOT NULL PRIMARY KEY
)

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    total_price DECIMAL(12,2) NOT NULL,
    num_of_items INT NOT NULL,
    order_status VARCHAR(255) NOT NULL,
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);