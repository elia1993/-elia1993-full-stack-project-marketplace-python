from database.password_hasher import get_hashed_password


class Person:
    def __init__(self, name, email, city, zip_code, phone, img_url, hashed_pass):
        self.name = name
        self.email = email
        self.city = city
        self.zip_code = zip_code
        self.phone = phone
        self.img_url = img_url
        self.hashed_pass = get_hashed_password(hashed_pass).decode('utf-8')
