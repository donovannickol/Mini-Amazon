\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Categories FROM 'Categories_ms2.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.categories_id_seq',
                         (SELECT MAX(id)+1 FROM Categories),
                         false);      

\COPY Products FROM 'Products_ms2.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false); 

\COPY Purchases FROM 'Purchases_ms2.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.purchases_id_seq',
                         (SELECT MAX(id)+1 FROM Purchases),
                         false);
\COPY Cart FROM 'Cart_ms2.csv' WITH DELIMITER ',' NULL '' CSV

\COPY OrderHistory FROM 'OrderHistory_ms2.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Inventory FROM 'Inventory_ms2.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Seller FROM 'Seller_ms2.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Sales FROM 'Sales_ms2.csv' WITH DELIMITER ',' NULL '' CSV
\COPY productRating FROM 'productRating_ms2.csv' WITH DELIMITER ',' NULL '' CSV

\COPY sellerRating FROM 'sellerRating_ms2.csv' WITH DELIMITER ',' NULL '' CSV

\COPY message FROM 'message_ms2.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.message_id_seq',
                         (SELECT MAX(id)+1 FROM message),
                         false);

\COPY messageThread FROM 'messageThread_ms2.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.messageThread_id_seq',
                         (SELECT MAX(id)+1 FROM messageThread),
                         false);

