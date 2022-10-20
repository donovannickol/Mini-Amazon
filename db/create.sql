-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    user_address VARCHAR(255) NOT NULL,
    user_city VARCHAR(255) NOT NULL,
    user_state VARCHAR(255) NOT NULL,
    balance DECIMAL(12, 2) NOT NULL
);

CREATE TABLE Categories (
    id INT NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) NOT NULL PRIMARY KEY
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(511) NOT NULL,
    img_url VARCHAR(511) NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    category VARCHAR(255) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    FOREIGN KEY (category) REFERENCES Categories(name)
);

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    total_price DECIMAL(12,2) NOT NULL,
    num_of_items INT NOT NULL,
    order_status VARCHAR(255) NOT NULL,
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Cart(
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    sellerid INT NOT NULL REFERENCES Users(id),
    quantity INT NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    PRIMARY KEY(uid, pid, sellerid)
);

CREATE TABLE Inventory (
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    count INT NOT NULL,
    PRIMARY KEY(uid, pid)
);

CREATE TABLE OrderHistory(
    uid INT NOT NULL REFERENCES Users(id),
    order_number INT NOT NULL,
    pid INT NOT NULL REFERENCES Products(id),
    sellerid INT NOT NULL REFERENCES Users(id),
    quantity INT NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    fullfilldate timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    PRIMARY KEY(uid,order_number, pid, sellerid)
);


-- triggers

create or replace function update_product_stock()
returns trigger as $$
begin
    if (TG_OP = 'INSERT') then
        update products set stock = stock + new.count where id = new.pid;
    elsif (TG_OP = 'DELETE') then
        update products set stock = stock - old.count where id = old.pid;
    elsif (TG_OP = 'UPDATE') then
        update products set stock = stock - old.count + new.count where id = new.pid;
    end if;
    return null;
end;
$$ language plpgsql;

create trigger update_product_stock
after insert or delete or update on Inventory
for each row execute procedure update_product_stock();