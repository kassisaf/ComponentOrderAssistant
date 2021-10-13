import requests.utils
import order_assist.tayda as tayda
from order_assist import PKG_NAME, PKG_VERSION
from settings import email, delay_seconds
from order_assist.database import ProductDB
from order_assist.pedal import Pedal


class ConsoleUI:
    def __init__(self):
        self.app_string = f'{PKG_NAME} v{PKG_VERSION}'
        self.session = requests.Session()
        self.session.headers.update(
            {
                'User-Agent': f'{self.app_string}',
                'From': f'{email}',
            }
        )

    def start(self):
        print(f'{self.app_string}\n{"=" * len(self.app_string)}')
        main_menu_text = "[V]iew existing pedals\n" \
                         "[A]dd new pedal\n" \
                         "[U]pdate product database\n" \
                         "[Q]uit\n" \
                         "> "
        user_input = ''
        while user_input not in ['q', 'quit']:
            print(main_menu_text, end='')
            user_input = input().strip().lower()
            if user_input in ['v', 'view']:
                pass
            elif user_input in ['a', 'add']:
                pass
            elif user_input in ['u', 'update']:
                self.update_database()

    def update_database(self):
        db = ProductDB('products.db')
        tayda.update_all(self.session, db, delay_seconds)
        db.close()


def add_new_pedal():
    mfg = input('Project MFG: ')
    name = input('Project name: ')
    mfg_orig = input('Original MFG: ')
    name_orig = input('Original name: ')
    url = input('URL: ')
    # TODO run loop to add materials
    return Pedal(mfg=mfg, name=name, mfg_orig=mfg_orig, name_orig=name_orig, url=url)


def add_pedal_materials():
    pass
