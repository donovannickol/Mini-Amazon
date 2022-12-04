-- \COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Users FROM '/home/vcm/mini-amazon/db/generated/Users.csv' WITH DELIMITER '^' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Categories FROM '/home/vcm/mini-amazon/db/generated/Categories.csv' WITH DELIMITER '^' NULL '' CSV
-- \COPY Categories FROM 'Categories.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.categories_id_seq',
                         (SELECT MAX(id)+1 FROM Categories),
                         false);    

\COPY Products (id, name, description, img_url, category) FROM '/home/vcm/mini-amazon/db/generated/Products.csv' WITH DELIMITER '^' NULL '' CSV
-- \COPY Products (id, name, description, img_url, category) FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);  
                         
\COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.purchases_id_seq',
                         (SELECT MAX(id)+1 FROM Purchases),
                         false);

\COPY Inventory FROM '/home/vcm/mini-amazon/db/generated/Inventory.csv' WITH DELIMITER '^' NULL ''  CSV;
-- \COPY Inventory FROM 'Inventory.csv' WITH DELIMITER ',' NULL ''  CSV;
-- \COPY Inventory FROM 'Inventory.csv' WITH DELIMITER ',' NULL ''  CSV;

\COPY Cart FROM 'Cart.csv' WITH DELIMITER ',' NULL '' CSV;


\COPY OrderHistory FROM '/home/vcm/mini-amazon/db/generated/OrderHistory.csv' WITH DELIMITER '^' NULL '' CSV;
-- \COPY OrderHistory FROM 'OrderHistory.csv' WITH DELIMITER ',' NULL '' CSV;



\COPY productRating FROM '/home/vcm/mini-amazon/db/generated/Ratings.csv' WITH DELIMITER '^' NULL '' CSV
-- \COPY productRating FROM 'productRating.csv' WITH DELIMITER ',' NULL '' CSV

\COPY sellerRating FROM 'sellerRating.csv' WITH DELIMITER ',' NULL '' CSV
