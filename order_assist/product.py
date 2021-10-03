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
