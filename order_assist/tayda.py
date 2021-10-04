from time import sleep
from bs4 import BeautifulSoup
from order_assist.product import Product
from order_assist.database import ProductDB

# Product category URLs used for scraping SKUs
urls = {
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


def get_products(session, url, limit=2):
    # Translate limit of 0 to 'all' for Tayda API
    if limit == 0:
        limit = 'all'

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


def update_category(session, database: ProductDB, category):
    if category in urls.keys():
        for product in get_products(session, urls[category], limit=0):
            database.add_or_update(product, category)
        database.save()


def update_all(session, database: ProductDB, delay=10):
    for category, url in urls.items():
        update_category(session, database, category)
        print(f'Waiting {delay} seconds...')
        sleep(delay)
    print(f'Added/updated {database.changes()} fields from {len(urls)} categories.')
