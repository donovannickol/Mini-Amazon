from flask import current_app as app


class Product:
    def __init__(self, id, name, description, img_url, price, category, stock, average_rating, num_ratings):
        self.id = id
        self.name = name
        self.description = description
        self.img_url = img_url
        self.price = price
        self.category = category
        self.stock = stock
        self.average_rating = average_rating
        self.num_ratings = num_ratings

    @staticmethod
    # get a product by id
    def get(id):
        rows = app.db.execute('''
SELECT id, name, description, img_url, price, category, stock, average_rating, num_ratings
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    # get all products
    def get_all():
        rows = app.db.execute('''
SELECT id, name, description, img_url, price, category, stock, average_rating, num_ratings
FROM Products
'''
        )
        return [Product(*row) for row in rows]

    @staticmethod
    # use sqlalchemy to get top k products by price
    def get_k_most_expensive(k):
        rows = app.db.execute('''
SELECT id, name, description, img_url, price, category, stock, average_rating, num_ratings
FROM Products
WHERE price <> 'NaN'
ORDER BY price DESC
LIMIT :k
''',
                              k=k)
        return [Product(*row) for row in rows]

    @staticmethod
    # get a page of products matching all the given criteria
    def get_page_of_products(page=0, limit=8, search_term="", sort_by="Default", category="All"):
        category_select = "1=1" if category == "All" else f"category = \'{category}\'"
        sort_map = {
            "Default": "id",
            "Price: Low to High": "price ASC",
            "Price: High to Low": "price DESC",
            "Rating: Low to High": "average_rating ASC",
            "Rating: High to Low": "NULLIF(average_rating, 'NaN') DESC NULLS LAST"
        }
        rows = app.db.execute(f'''
SELECT id, name, description, img_url, price, category, stock, average_rating, num_ratings
FROM Products
WHERE {category_select} AND (LOWER(name) LIKE LOWER(:search_term) OR LOWER(description) LIKE LOWER(:search_term))
ORDER BY (stock != 0) DESC, {sort_map[sort_by]}
LIMIT {limit}
OFFSET {(page - 1) * limit}
''',
                              search_term='%' + search_term + '%')
        return [Product(*row) for row in rows]

    @staticmethod
    # get the number of products matching all the given criteria
    def get_num_matching_products(search_term="", category="All"):
        category_select = "1=1" if category == "All" else f"category = \'{category}\'"
        rows = app.db.execute(f'''
SELECT COUNT(*)
FROM Products
WHERE {category_select} AND (LOWER(name) LIKE LOWER(:search_term) OR LOWER(description) LIKE LOWER(:search_term))
''',
                              search_term='%' + search_term + '%')
        return rows[0][0]


    @staticmethod
    # get a list of all categories
    def get_all_categories():
        rows = app.db.execute('''
SELECT DISTINCT category
FROM Products
'''
        )
        return ["All"] + [row[0] for row in rows]

    # TODO: update this method to require the user to be logged in and collect th id of the user so that the price and stock are added to inventory
    @staticmethod
    def add_product(uid, name, description, img_url, category, price, stock):
        try:
            # insert the product into the database and return the new id
            rows = app.db.execute('''
INSERT INTO Products (name, description, img_url, category)
VALUES (:name, :description, :img_url, :category)
RETURNING id
''',
                                    name=name,
                                    description=description,
                                    img_url=img_url,
                                    category=category,
                                    price=price,
                                    stock=stock)
            # update Inventory as well
            app.db.execute('''
INSERT INTO Inventory (uid, pid, price, count)
VALUES (:uid, :pid, :price, :stock)
''',
                            uid=uid,
                            pid=rows[0][0],
                            price=price,
                            stock=stock)
            return rows[0][0]
        except Exception as e:
            print(str(e))

    @staticmethod
    def update_product(uid, id, name, description, img_url, category, price, stock):
        try:
            rows = app.db.execute('''
UPDATE Products
SET name = :name, description = :description, img_url = :img_url, category = :category
WHERE id = :id
''',
                                  id=id,
                                  name=name,
                                  description=description,
                                  img_url=img_url,
                                  category=category)

            # update Inventory as well
            app.db.execute('''
UPDATE Inventory
SET price = :price, count = :stock
WHERE uid = :uid AND pid = :pid
''',
                            uid=uid,
                            pid=id,
                            price=price,
                            stock=stock)
            return rows
        except Exception as e:
            print(str(e))

    @staticmethod
    def delete_product(id):
        try:
            rows = app.db.execute('''
DELETE FROM Products
WHERE id = :id
''',
                                  id=id)
            return rows[0][0]
        except Exception as e:
            print(str(e))