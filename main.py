import csv
import sqlite3
import time

import requests.utils
from bs4 import BeautifulSoup

# Product category URLs used for scraping SKUs
tayda_urls = {
    # Append `?product_list_limit=all` to show all instead of 50
    'resistors_metal': 'https://www.taydaelectronics.com/resistors/1-4w-metal-film-resistors.html',
    'resistors_carbon': 'https://www.taydaelectronics.com/resistors/1-4w-carbon-film-resistors.html',
    'caps_electrolytic': 'https://www.taydaelectronics.com/capacitors/electrolytic-capacitors.html',
    'caps_ceramic': 'https://www.taydaelectronics.com/capacitors/ceramic-disc-capacitors.html',
    'caps_film': 'https://www.taydaelectronics.com/capacitors/polyester-mylar-film-capacitors.html',
    'caps_film_box': 'https://www.taydaelectronics.com/capacitors/polyester-film-box-type-capacitors.html',
    'pots_a_type': 'https://www.taydaelectronics.com/potentiometer-variable-resistors/rotary-potentiometer/logarithmic.html',
    'pots_b_type': 'https://www.taydaelectronics.com/potentiometer-variable-resistors/rotary-potentiometer/linear.html',
    'pots_c_type': 'https://www.taydaelectronics.com/potentiometer-variable-resistors/rotary-potentiometer/anti-log-reverse.html'
}

# Create global requests session with the appropriate headers to be used for all HTTP requests
user_agent = 'OrderAssistant v0.01'
email = 'kassisaf@gmail.com'  # TODO move this to a config file
session = requests.Session()
session.headers.update(
    {
        'User-Agent': f'{user_agent}',
        'From': f'{email}',
    }
)


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

    def get_product_rowid(self, product):
        return self.cursor.execute(f"SELECT ROWID FROM products WHERE name='{product.name}' AND sku='{product.sku}'").fetchone()[0]

    def add_product(self, product):
        if not self.product_exists(product):
            self.cursor.execute(f"INSERT INTO products VALUES('{product.name}','{product.url}','{product.sku}',{product.price},{product.qty},{time.time()})")
            print('Added to database')
        else:
            id = self.get_product_rowid(product)
            self.cursor.execute(f"UPDATE products SET price={product.price}, qty={product.qty}, timestamp={time.time()} WHERE ROWID={id}")
            print('Updated price and quantity')

    def save(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def save_and_close(self):
        self.save()
        self.close()


def get_products_from_tayda_page(url, limit=5):
    # Request the page and parse it
    page = session.get(f'{url}?product_list_limit={limit}')
    soup = BeautifulSoup(page.content, 'html.parser')
    product_rows = soup.select('#maincontent > div.columns > div.column.main > div.products.wrapper.list.products-list > ol > li > div > div')
    products = []

    # Parse product names, skus, url, quantity in stock, and price
    for row in product_rows:
        name_and_url = row.find('a', {'class': 'product-item-link'})
        name = name_and_url.text.strip()
        url = name_and_url.get('href')

        sku_and_qty = row.find('div', {'class': 'sku-qty'}).text.strip()
        if 'group product' in sku_and_qty.lower():
            sku = sku_and_qty.split('SKU: ')[-1].strip()
            qty = -1
        else:
            sku_and_qty = sku_and_qty.split()
            sku = sku_and_qty[1].strip()
            qty = sku_and_qty[-1].strip()

        price = row.find('span', {'class': 'price-wrapper'}).get('data-price-amount')

        products.append(Product(name, url, sku, price, qty))

    return products


if __name__ == '__main__':
    db = ProductDB('products.db')

    metal_resistors = get_products_from_tayda_page(tayda_urls['resistors_metal'], limit=5)
    for product in metal_resistors:
        print(product)
        db.add_product(product)
        print()

    db.save_and_close()
