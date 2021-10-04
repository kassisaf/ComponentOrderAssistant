import requests.utils
import order_assist.tayda as tayda
from order_assist.database import ProductDB
from settings import user_agent, email, delay_seconds

# Create global requests session with the appropriate headers to be used for all HTTP requests
session = requests.Session()
session.headers.update(
    {
        'User-Agent': f'{user_agent}',
        'From': f'{email}',
    }
)


if __name__ == '__main__':
    db = ProductDB('products.db')
    tayda.update_all(session, db, delay_seconds)
    db.close()
