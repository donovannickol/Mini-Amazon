-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    balance DECIMAL(18, 2) NOT NULL
);

CREATE TABLE Categories (
    id INT NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) NOT NULL PRIMARY KEY
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(8000) NOT NULL,
    description VARCHAR(16000) NOT NULL,
    img_url VARCHAR(8000) NOT NULL,
    category VARCHAR(8000) NOT NULL,
    price DECIMAL(18,2) NOT NULL DEFAULT 'NaN',
    stock INT NOT NULL DEFAULT 0,
    average_rating DECIMAL(12,2) NOT NULL DEFAULT 'NaN',
    num_ratings INT NOT NULL DEFAULT 0,
    FOREIGN KEY (category) REFERENCES Categories(name)
);

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    total_price DECIMAL(16,2) NOT NULL,
    num_of_items INT NOT NULL,
    order_status VARCHAR(255) NOT NULL,
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    order_number INT NOT NULL
);

CREATE TABLE Cart(
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    sellerid INT NOT NULL REFERENCES Users(id),
    quantity INT NOT NULL,
    price DECIMAL(16,2) NOT NULL,
    PRIMARY KEY(uid, pid, sellerid)
);

CREATE TABLE Inventory (
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    count INT NOT NULL,
    price DECIMAL(16,2) NOT NULL,
    PRIMARY KEY(uid, pid)
);

CREATE TABLE OrderHistory(
    uid INT NOT NULL REFERENCES Users(id),
    order_number INT NOT NULL,
    pid INT NOT NULL REFERENCES Products(id),
    sellerid INT NOT NULL REFERENCES Users(id),
    quantity INT NOT NULL,
    price DECIMAL(16,2) NOT NULL,
    fullfilldate timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    PRIMARY KEY(uid,order_number, pid, sellerid)
);

CREATE TABLE productRating (
	user_id INT NOT NULL REFERENCES Users(id),
	pid INT NOT NULL REFERENCES Products(id),
	starsOutOfFive INT NOT NULL,
	ratingContent varchar(5000),
	submissionDate timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
	PRIMARY KEY(user_id, pid)
    );

CREATE TABLE sellerRating (
	user_id INT NOT NULL REFERENCES Users(id),
	seller_id INT NOT NULL REFERENCES Users(id),
	starsOutOfFive INT NOT NULL,
	ratingContent varchar(5000),
	submissionDate timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
	PRIMARY KEY(user_id, seller_id)
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


create or replace function update_product_lowest_price()
returns trigger as $$
begin
    update products set price = (select COALESCE(min(price), 'NaN') from inventory where pid = new.pid) where id = new.pid;
    return null;
end;
$$ language plpgsql;

create trigger update_product_lowest_price
after insert or delete or update on Inventory
for each row execute procedure update_product_lowest_price();



create or replace function update_product_average_rating()
returns trigger as $$
begin
    update products set average_rating = (select COALESCE(avg(starsOutOfFive), 'NaN') from productRating where pid = new.pid) where id = new.pid;
    return null;
end;
$$ language plpgsql;

create trigger update_product_average_rating
after insert or delete or update on productRating
for each row execute procedure update_product_average_rating();


create or replace function update_product_num_ratings()
returns trigger as $$
begin
    update products set num_ratings = (select count(*) from productRating where pid = new.pid) where id = new.pid;
    return null;
end;
$$ language plpgsql;

create trigger update_product_num_ratings
after insert or delete or update on productRating
for each row execute procedure update_product_num_ratings();


/*
create or replace function checkpPairs()
returns trigger as $$
begin  
    update productRating set (starsOutOfFive, ratingContent, submissionDate) = (new.starsOutOfFive, new.ratingContent, new.submissionDate)
                                                                                 where user_id = new.user_id and pid = new.pid;
    return null;
end;
$$ language plpgsql;

create trigger update_productRating
after insert on productRating 
for each row execute procedure checkPairs();



create or replace function update_sellerRating()
returns trigger as $$
begin  
    update sellerRating set (starsOutOfFive, ratingContent, submissionDate) = (new.starsOutOfFive, new.ratingContent, new.submissionDate)
                                                                                 where user_id = new.user_id and seller_id = new.seller_id;
    return null;
end;
$$ language plpgsql;

create trigger update_sellerRating
after update on sellerRating 
for each row execute procedure update_sellerRating();
*/