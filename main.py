import requests.utils
import order_assist.tayda as tayda
from order_assist.database import ProductDB
from settings import user_agent, email

# Create global requests session with the appropriate headers to be used for all HTTP requests
session = requests.Session()
session.headers.update(
    {
        'User-Agent': f'{user_agent}',
        'From': f'{email}',
    }
)


if __name__ == '__main__':
    # db = ProductDB('products.db')
    #
    # metal_resistors = tayda.get_products(session, tayda.urls['resistors_metal'], limit=5)
    # for product in metal_resistors:
    #     print(product)
    #     db.add_or_update(product, category='resistor')
    #     print()
    #
    # print(db.changes())
    # db.save_and_close()
    tayda.update_all(session)
