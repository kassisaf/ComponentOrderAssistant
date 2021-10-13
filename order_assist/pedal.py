class Pedal:
    def __init__(self, mfg, name, mfg_orig, name_orig, url, materials_dict=None):
        self.mfg = mfg
        self.name = name
        self.mfg_orig = mfg_orig
        self.name_orig = name_orig
        self.url = url
        self.materials_dict = materials_dict


# TODO seed some pedals
# TODO add to database
# each pedal will have its own table, each row of which will be:
# part description, qty needed, foreign key to products db or just the SKU to make it independent of rowid
