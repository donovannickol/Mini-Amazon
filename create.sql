CREATE TABLE users (
    id INT GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255),
    firstname VARCHAR(255),
    lastname VARCHAR(255)
);

CREATE TABLE products (
    pid INT NOT NULL PRIMARY KEY,
    product_name VARCHAR(255) UNIQUE,
    price FLOAT,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE purchases (
    order_nr INT NOT NULL PRIMARY KEY,
    uid INT NOT NULL,
    pid INT NOT NULL,
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);
