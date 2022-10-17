from flask import current_app as app


class Product:
    def __init__(self, id, name, description, img_url, price, category):
        self.id = id
        self.name = name
        self.description = description
        self.img_url = img_url
        self.price = price
        self.category = category

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, description, img_url, price, category
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT id, name, description, img_url, price, category
FROM Products
'''
        )
        return [Product(*row) for row in rows]

    @staticmethod
    # use sqlalchemy to get top k products by price
    def get_k_most_expensive(k):
        rows = app.db.execute('''
SELECT id, name, description, img_url, price, category
FROM Products
ORDER BY price DESC
LIMIT :k
''',
                              k=k)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_page_of_products(page=0, limit=8, search_term="", sort_by="Default"):
        sort_map = {
            "Default": "id",
            "Price: Low to High": "price ASC",
            "Price: High to Low": "price DESC",
        }
        print(sort_map[sort_by])
        rows = app.db.execute('''
SELECT id, name, description, img_url, price, category
FROM Products
WHERE name LIKE :search_term OR description LIKE :search_term
ORDER BY ''' + sort_map[sort_by] + '''
LIMIT :limit
OFFSET :page
''',
                              search_term='%' + search_term + '%',
                              page=page*limit,
                              limit=limit)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_num_matching_products(search_term=""):
        rows = app.db.execute('''
SELECT COUNT(*)
FROM Products
WHERE name LIKE :search_term OR description LIKE :search_term
''',
                              search_term='%' + search_term + '%')
        return rows[0][0]