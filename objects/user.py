from .person import Person


class User(Person):
    def __init__(self, name, email, city, zip_code, phone, img_url, hashed_pass):
        super().__init__(name, email, city, zip_code, phone, img_url, hashed_pass)
