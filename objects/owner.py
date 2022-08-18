from .person import Person


class Owner(Person):
    def __init__(self, name, email, city, zip_code, phone, cat, info, img_url, hashed_pass):
        super().__init__(name, email, city, zip_code, phone, img_url, hashed_pass)
        self.cat = cat
        self.info = info
        self.likes = 0
