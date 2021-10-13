import sqlite3
from time import time as now


class ProductDB:
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
        self.create_product_table()
        print(f'Database initialized successfully ({filename}).')

    def create_product_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                category TEXT,
                name TEXT,
                sku TEXT,
                url TEXT,
                price REAL,
                qty INTEGER,
                timestamp REAL
            )
        ''')

    def product_exists(self, product):
        return self.cursor.execute(f"SELECT EXISTS(SELECT 1 FROM products WHERE name='{product.name}' AND sku='{product.sku}')").fetchone()[0]

    def get_rowid(self, product):
        return self.cursor.execute(f"SELECT ROWID FROM products WHERE name='{product.name}' AND sku='{product.sku}'").fetchone()[0]

    def add_or_update(self, product, category=''):
        if not self.product_exists(product):
            self.cursor.execute(f"INSERT INTO products VALUES('{category}','{product.name}','{product.sku}','{product.url}',{product.price},{product.qty},{now()})")
            print(f'Added to database: {product.name}')
        else:
            id = self.get_rowid(product)
            self.cursor.execute(f"UPDATE products SET price={product.price}, qty={product.qty}, timestamp={now()} WHERE ROWID={id}")
            print(f'Updated price and quantity for product: {product.name}')

    def save(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def save_and_close(self):
        self.save()
        self.close()

    def changes(self):
        return self.connection.total_changes
