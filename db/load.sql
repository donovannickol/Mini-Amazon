-- \COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Users FROM '/home/vcm/mini-amazon/db/data/gen/complete/users.csv' WITH DELIMITER '^' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Categories FROM '/home/vcm/mini-amazon/db/data/gen/complete/categories.csv' WITH DELIMITER '^' NULL '' CSV
-- \COPY Categories FROM 'Categories.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.categories_id_seq',
                         (SELECT MAX(id)+1 FROM Categories),
                         false);    

\COPY Products (id, name, description, img_url, category) FROM '/home/vcm/mini-amazon/db/data/gen/complete/products.csv' WITH DELIMITER '^' NULL '' CSV
-- \COPY Products (id, name, description, img_url, category) FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);  
                         
\COPY Purchases FROM '/home/vcm/mini-amazon/db/data/gen/complete/purchases.csv' WITH DELIMITER '^' NULL '' CSV
SELECT pg_catalog.setval('public.purchases_id_seq',
                         (SELECT MAX(id)+1 FROM Purchases),
                         false);

\COPY Inventory FROM '/home/vcm/mini-amazon/db/data/gen/complete/inventory.csv' WITH DELIMITER '^' NULL ''  CSV;
-- \COPY Inventory FROM 'Inventory.csv' WITH DELIMITER ',' NULL ''  CSV;
-- \COPY Inventory FROM 'Inventory.csv' WITH DELIMITER ',' NULL ''  CSV;

\COPY Cart FROM 'Cart.csv' WITH DELIMITER ',' NULL '' CSV;


\COPY OrderHistory FROM '/home/vcm/mini-amazon/db/data/gen/complete/orderhistory.csv' WITH DELIMITER '^' NULL '' CSV;
-- \COPY OrderHistory FROM 'OrderHistory.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY productRating FROM '/home/vcm/mini-amazon/db/data/gen/complete/reviews.csv' WITH DELIMITER '^' NULL '' CSV
-- \COPY productRating FROM 'productRating.csv' WITH DELIMITER ',' NULL '' CSV

\COPY sellerRating FROM '/home/vcm/mini-amazon/db/data/gen/complete/reviews.csv' WITH DELIMITER '^' NULL '' CSV

-- \COPY message FROM 'messageThread.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.messagethread_thread_id_seq',
                         (SELECT MAX(thread_id)+1 FROM messageThread),
                         false);

-- \COPY message FROM 'message.csv' WITH DELIMITER ',' NULL '' CSV


-- this is mostly an aesthetic table; SHOULD NOT BE USED FOR BUILDING THIS WEBSITE
CREATE TABLE pRatingNAMES AS
SELECT Users.firstname, Users.lastname, productRating.user_id, productRating.pid, productRating.starsOutOfFive, productRating.ratingContent, productRating.submissionDate, Products.name
FROM Users, productRating, Products
WHERE Users.id = productRating.user_id
AND productRating.pid = Products.id;



CREATE TABLE sRatingNAMES AS  
SELECT user_id, seller_id, starsOutOfFive, ratingContent, submissionDate, seller.firstname, seller.lastname
FROM Users AS seller, SellerRating
WHERE SellerRating.seller_id = seller.id;

/*
create or replace function insert_productRating()
returns trigger as 
$$
begin  
    insert into productRating (user_id, pid, starsOutOfFive, ratingContent, submissionDate)
    VALUES(NEW.user_id, NEW.pid, NEW.starsOutOfFive, NEW.ratingContent, NEW.submissionDate);
    RETURN null;
end;
$$ 
language plpgsql;

create trigger insert_productRating
AFTER insert on productRating 
for each row execute procedure insert_productRating();
*/
