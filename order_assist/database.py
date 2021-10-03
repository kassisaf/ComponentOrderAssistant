import sqlite3
from time import time as now


class ProductDB:
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products
                               (category TEXT,
                                name TEXT,
                                url TEXT,
                                sku TEXT,
                                price REAL,
                                qty INTEGER,
                                timestamp REAL)''')
        print(f'Database initialized successfully ({filename}).')

    def product_exists(self, product):
        return self.cursor.execute(f"SELECT EXISTS(SELECT 1 FROM products WHERE name='{product.name}' AND sku='{product.sku}')").fetchone()[0]

    def get_rowid(self, product):
        return self.cursor.execute(f"SELECT ROWID FROM products WHERE name='{product.name}' AND sku='{product.sku}'").fetchone()[0]

    def add_or_update(self, product, category=''):
        if not self.product_exists(product):
            self.cursor.execute(f"INSERT INTO products VALUES('{category}','{product.name}','{product.url}','{product.sku}',{product.price},{product.qty},{now()})")
            print('Added to database')
        else:
            id = self.get_rowid(product)
            self.cursor.execute(f"UPDATE products SET price={product.price}, qty={product.qty}, timestamp={now()} WHERE ROWID={id}")
            print('Updated price and quantity')

    def save(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def save_and_close(self):
        self.save()
        self.close()

    def changes(self):
        return self.connection.total_changes
