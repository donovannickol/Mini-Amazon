from flask import current_app as app


class Product:
    def __init__(self, id, name, description, img_url, price, category, stock):
        self.id = id
        self.name = name
        self.description = description
        self.img_url = img_url
        self.price = price
        self.category = category
        self.stock = stock

    @staticmethod
    # get a product by id
    def get(id):
        rows = app.db.execute('''
SELECT id, name, description, img_url, price, category, stock
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    # get all products
    def get_all():
        rows = app.db.execute('''
SELECT id, name, description, img_url, price, category, stock
FROM Products
'''
        )
        return [Product(*row) for row in rows]

    @staticmethod
    # use sqlalchemy to get top k products by price
    def get_k_most_expensive(k):
        rows = app.db.execute('''
SELECT id, name, description, img_url, price, category, stock
FROM Products
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
        }
        rows = app.db.execute(f'''
SELECT id, name, description, img_url, price, category, stock
FROM Products
WHERE {category_select} AND (LOWER(name) LIKE LOWER(:search_term) OR LOWER(description) LIKE LOWER(:search_term))
ORDER BY {sort_map[sort_by]}
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
WHERE {category_select}  AND (name LIKE :search_term OR description LIKE :search_term)
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