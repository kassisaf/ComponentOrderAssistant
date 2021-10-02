import sqlite3
from time import time as now


class Product:
    def __init__(self, name, url, sku, price, qty):
        self.name = name
        self.url = url
        self.sku = sku
        self.price = float(price)
        self.qty = int(qty)

    def __repr__(self):
        return f'{self.name}\n{self.url}\nSKU: {self.sku}\nPrice: ${self.price}\nIn stock: {self.in_stock()}'

    def in_stock(self):
        if self.qty < 0:
            return "Unknown"
        else:
            return self.qty > 0


class ProductDB:
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products
                               (name TEXT,
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

    def add_or_update(self, product):
        if not self.product_exists(product):
            self.cursor.execute(f"INSERT INTO products VALUES('{product.name}','{product.url}','{product.sku}',{product.price},{product.qty},{now()})")
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