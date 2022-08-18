from config import connection
from database.password_hasher import check_password


class OwnerAlreadyExists(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class OwnerDoesntExist(Exception):
    pass


def get_user(email):
    result = None
    with connection.cursor() as cursor:
        query = f"SELECT * FROM users where email = '{email}'"
        cursor.execute(query)
        result = cursor.fetchone()
    return result


def insert_user(name, email, city, zip_code, phone, img_url, password):
    with connection.cursor() as cursor:
        query = f"SELECT * FROM users where name = '{name}' and phone = '{phone}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            raise UserAlreadyExists()
        else:
            query = f"INSERT INTO users (name, email, city, zip_code, phone, img_url, pass_hash) VALUES " \
                    f"('{name}', '{email}', '{city}', '{zip_code}', '{phone}', '{img_url}', '{password}')"
            cursor.execute(query)
            connection.commit()
        query = f"SELECT * FROM users where name = '{name}' and phone = '{phone}'"
        cursor.execute(query)
        result = cursor.fetchone()
        return result["id"]


def insert_owner(name, email, city, zip_code, phone, img_url, cat, info, password):
    with connection.cursor() as cursor:
        query = f"SELECT * FROM owners where name = '{name}' and phone = '{phone}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result is not None:
            raise OwnerAlreadyExists()
        else:
            password = '"' + password + '"'
            query = f"INSERT INTO owners (name, email, city, zip_code, phone, categories, info, img_url, pass_hash) VALUES " \
                    f"('{name}', '{email}', '{city}', '{zip_code}', '{phone}', '{cat}', '{info}', '{img_url}', {password})"
            cursor.execute(query)
            connection.commit()
        query = f"SELECT * FROM owners where name = '{name}' and phone = '{phone}'"
        cursor.execute(query)
        result = cursor.fetchone()
        return result["id"]


def insert_new(obj, type_):  # type_ is binary: 0 -> business owner, 1 -> client
    return_em = obj.email
    with connection.cursor() as cursor:
        result = get_user(obj.email)
        if result is not None:
            raise UserAlreadyExists()
        else:
            password = '"' + obj.hashed_pass + '"'
            if type_ == 0:
                query = f"INSERT INTO owners (email, categories, info) VALUES " \
                        f"('{obj.email}', '{obj.cat}', '{obj.info}')"
                cursor.execute(query)
                query = f"INSERT INTO users (owner, name, email, city, zip_code, phone, type, img_url, pass_hash) VALUES " \
                        f"('{return_em}', '{obj.name}', '{obj.email}', '{obj.city}', '{obj.zip_code}', '{obj.phone}', " \
                        f"{type_}, '{obj.img_url}'," \
                        f" {password})"
            else:
                query = f"INSERT INTO users (name, email, city, zip_code, phone, type, img_url, pass_hash) VALUES " \
                        f"('{obj.name}', '{obj.email}', '{obj.city}', '{obj.zip_code}', '{obj.phone}', " \
                        f"{type_}, '{obj.img_url}'," \
                        f" {password})"
            cursor.execute(query)
    connection.commit()
    return return_em


def get_owners(cat=None):
    with connection.cursor() as cursor:
        if cat is None:
            query = f"SELECT owners.email, users.name,owners.info, users.img_url,count(likes.customer_email) counter FROM likes  RIGHT JOIN users ON users.email = likes.business_email JOIN owners on owners.email=users.email GROUP BY  users.name,owners.info, users.img_url "
        elif cat == 'high-rating':
            query = f"SELECT owners.email, users.name,owners.info, users.img_url,count(likes.customer_email) counter FROM likes  RIGHT JOIN users ON users.email = likes.business_email JOIN owners on owners.email=users.email GROUP BY  users.name,owners.info, users.img_url ORDER BY counter desc"
        elif cat == 'low-rating':
            query = f"SELECT owners.email, users.name,owners.info, users.img_url,count(likes.customer_email) counter FROM likes  RIGHT JOIN users ON users.email = likes.business_email JOIN owners on owners.email=users.email GROUP BY  users.name,owners.info, users.img_url  ORDER BY counter,users.name "
        else:
            query = f"SELECT owners.email, users.name,owners.info, users.img_url,count(likes.customer_email) counter FROM likes  RIGHT JOIN users ON users.email = likes.business_email JOIN owners on owners.email=users.email where owners.categories = '{cat}' GROUP BY  users.name,owners.info, users.img_url "
        cursor.execute(query)
        result = cursor.fetchall()
        return result

def get_cutomers_likes(email):
    with connection.cursor() as cursor:
        query = f"SELECT users.name,l.business_email,l.customer_email  FROM likes l join users on users.email = l.customer_email WHERE l.business_email = '{email}'"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

def get_search(search,location):
    with connection.cursor() as cursor:
        if location == "name" or location == "a":
           query = f"SELECT users.city, owners.email, users.name,owners.info, users.img_url,count(likes.customer_email) counter FROM likes  RIGHT JOIN users ON users.email = likes.business_email JOIN owners on owners.email=users.email  where name LIKE '{search}%' GROUP BY users.city, users.name,owners.info, users.img_url  ORDER BY counter,users.name"
        else:
            query = f"SELECT users.city, owners.email, users.name,owners.info, users.img_url,count(likes.customer_email) counter FROM likes  RIGHT JOIN users ON users.email = likes.business_email JOIN owners on owners.email=users.email  where city LIKE '{search}%' GROUP BY users.city, users.name,owners.info, users.img_url  ORDER BY counter,users.name "
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def get_owner(email):
    with connection.cursor() as cursor:
        query = f"SELECT * FROM users where email = '{email}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result["type"] == '0':
            query = f"SELECT * FROM owners join users on owners.email=users.owner where users.owner = '{email}'"
            cursor.execute(query)
            result = cursor.fetchone()
        return result


def get_items(owner_em, item_name=None):
    with connection.cursor() as cursor:
        if item_name:
            query = f"SELECT * FROM items where owner = '{owner_em}' and name = '{item_name}' order by price"
        else:
            query = f"SELECT * FROM items where owner = '{owner_em}'  order by price"
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def delete_item(id , args):
    with connection.cursor() as cursor:
        if(args == "id"):
            query = f"DELETE FROM `items` WHERE id = '{id}'"
        elif(args =="com_id"):
            query = f"DELETE FROM `comment` WHERE id = '{id}'"
        else:
            query = f"DELETE FROM `gallery` WHERE id = '{id}'"
        cursor.execute(query)
        connection.commit()



def update_item(item_attr, email, name):
    with connection.cursor() as cursor:
        query = f"update items set "
        for key, val in item_attr.items():
            if val:
                query += f"{key} = '{val}', "
        query = query.strip(', ')
        query += f"where owner = '{email}' and name = '{name}'"
        cursor.execute(query)
        connection.commit()

def update_owner_profile(owner_attr,email):
    with connection.cursor() as cursor:
        query = f"update users set "
        for key, val in owner_attr.items():
            if val:
                query += f"{key} = '{val}', "
        query = query.strip(', ')
        query += f"where email = '{email}'"
        cursor.execute(query)
        connection.commit()

def update_img(new_url, prev_url):
    with connection.cursor() as cursor:
        query = f"update images set img_url = '{new_url}' where img_url = '{prev_url}'"
        cursor.execute(query)
        connection.commit()


def get_categories():
    with connection.cursor() as cursor:
        query = f"SELECT owners.email,categories, COUNT(likes.business_email) as counter FROM owners join likes on likes.business_email = owners.email group by  owners.email,categories"
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def insert_image(owner_em, img_url):
    with connection.cursor() as cursor:
        query = f"INSERT INTO images (owner, img_url) VALUES ('{owner_em}', '{img_url}')"
        cursor.execute(query)
        connection.commit()


def insert_picture(owner_em, img_url , desc):
    with connection.cursor() as cursor:
        query = f"INSERT INTO `gallery`(`id`, `owner_email`, `img`,`description`) VALUES ('','{owner_em}','{img_url}', '{desc}')"
        cursor.execute(query)
        connection.commit()

def insert_item(owner_em, price, info, name, img_url,sale,sale_description):
    with connection.cursor() as cursor:
        query = f"INSERT INTO items (owner, price, info, img_url, name,sale,sale_description) VALUES ('{owner_em}', {price}, '{info}'" \
                f", '{img_url}', '{name}','{sale}', '{sale_description}')"
        cursor.execute(query)
    connection.commit()


def insert(person, type_, items=None):
    try:
        if type_ == 0:
            owner_em = insert_new(person, 0)
            for item in items:
                # insert_image(owner_em, item.img_url)
                insert_item(owner_em, item.price, item.info, item.name, item.img_url,item.sale,item.sale_description)
        else:
            insert_new(person, 1)
    except UserAlreadyExists:
        raise


def is_owner(email, password):
    result = get_user(email)
    if result is not None:
        return check_password(password, result["pass_hash"])
    return OwnerDoesntExist


def get_likes(email):
    with connection.cursor() as cursor:
        query = f"SELECT COUNT(customer_email) FROM likes WHERE business_email = '{email}'"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0]["COUNT(customer_email)"]



def add_like(customer_email, business_email):
    with connection.cursor() as cursor:
        query = f"SELECT COUNT(customer_email) FROM likes WHERE business_email = '{business_email}' AND customer_email = '{customer_email}'"
        cursor.execute(query)
        res = cursor.fetchall()
        if customer_email == None:
            return ""

        if res[0]["COUNT(customer_email)"] == 0:
            query = f"INSERT INTO likes (customer_email, business_email) VALUES ('{customer_email}', '{business_email}')"
            cursor.execute(query)
            connection.commit()
        else:
            remove_like(customer_email, business_email)


def insert_comment(customer_email, business_email, comment):
    with connection.cursor() as cursor:
        query = f"INSERT INTO comment (customer_email, business_email, comment) VALUES ('{customer_email}', '{business_email}', '{comment}')"
        cursor.execute(query)
        connection.commit()


def remove_like(customer_email, business_email):
    with connection.cursor() as cursor:
        query = f"DELETE FROM likes where customer_email = '{customer_email}' AND business_email = '{business_email}'"
        cursor.execute(query)
    connection.commit()


def get_comments(owner):
    with connection.cursor() as cursor:
        query = f"SELECT comment.id,users.email, users.name, comment FROM comment JOIN users ON users.email = comment.customer_email WHERE " \
                f"comment.business_email = '{owner}' AND comment != '' "
        cursor.execute(query)
        return cursor.fetchall()


def get_pictures(owner):
    with connection.cursor() as cursor:
        query = f"SELECT `id`, `owner_email`, `img`, `description` FROM `gallery` WHERE owner_email = '{owner}'"
        cursor.execute(query)
        return cursor.fetchall()

def update_owner_picture(email,img_url):
    with connection.cursor() as cursor:
        query = f"UPDATE `users` SET `img_url`= '{img_url}' WHERE email = '{email}'"
        cursor.execute(query)
        return cursor.fetchall()

def get_comments_by_owner(id):
    with connection.cursor() as cursor:
        query = f"SELECT `business_email` FROM `comment` WHERE `id` = '{id}'"
        cursor.execute(query)
        result = cursor.fetchall()
        return result[0]["business_email"]

