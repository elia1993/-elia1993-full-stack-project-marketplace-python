import base64
from flask import Flask, render_template, request, session, Response, redirect, url_for,flash, g
from objects.owner import Owner
from objects.user import User
from objects.item import Item
from database.methods import *
import os
import datetime
import xlsxwriter
import pandas as pd
import matplotlib.pyplot as plt
def create_app():
    app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
    app.secret_key = "BL0ckN0nAdmIN"
    app.config['SECRET_KEY'] = app.secret_key
    items = []
    template = "masterpage.html"
    @app.before_request
    def before_request():
        g.some_variable = "value"
    @app.route('/')
    def root():
        user = "tishreen12@gmail.com"
        owners = get_owners()
        cutomers_likes = []
        for ow in owners:
            cutomers_likes.append(get_cutomers_likes(ow['email']))
        categories = [x['categories'] for x in get_categories()]
        categories.append("All")
        return render_template('index.html',user=user , owners=owners,categories=list(set(categories)),cutomers_likes=cutomers_likes, var=template)


    @app.route('/register')
    def register():
        return render_template('main_register.html')


    @app.route('/edit/<name>', methods=['GET'])
    def edit(name):
        user = get_user(session["user_email"])
        item = get_items(session["user_email"], name)[0]
        return render_template('edit_item.html', item=item,user=user )

    @app.route('/edit_owner/<name>', methods=['GET'])
    def edit_owner(name):
        user = get_user(session["user_email"])
        owner = get_owner(session["user_email"])
        return render_template('edit_owner.html', owner=owner,user=user)
    g
    @app.route('/delete')
    def delete():
        id = request.args.get('id')
        com_id = request.args.get('com_id')
        id_pic = request.args.get('id_pic')
        args = ""
        args_com = ""
        args_pic = ""
        comments = None
        owner_items = None
        user_email = session["user_email"]
        try:
            if id != None:
                args = "id"
                email = user_email
                owner_items = get_items(email)
                delete_item(id,args)
            elif com_id != None:
                email = get_comments_by_owner(com_id)
                args_com = "com_id"
                delete_item(com_id,args_com)
            else:
                email = user_email
                args_pic = "id_pic"
                delete_item(id_pic, args_pic)
            owner_items = get_items(email)
            comments = get_comments(email)
            pictures = get_pictures(email)
        except:
            pass
        owner = get_owner(email)
        return render_template('about_owner.html', owner_items=owner_items, owner=owner, var=template, user=user_email,
                                       comments=comments, pictures=pictures)


    @app.route('/update')
    def update_picture():
        img_url =  request.args.get('img_url')
        args = ""
        comments = None
        owner_items = None
        email = session["user_email"]
        try:
            if img_url != None:
                update_owner_picture(email,img_url)
        except:
            pass
        owner_items = get_items(email)
        comments = get_comments(email)
        pictures = get_pictures(email)
        owner = get_owner(email)
        return render_template('about_owner.html', owner_items=owner_items, owner=owner, var=template,
                               user=session['user_email'],
                               comments=comments, pictures=pictures)


    @app.route('/edit/<name>', methods=['POST'])
    def edit_item(name):
        data = request.form
        # if data["img_url"]:
        #     update_img(data["img_url"])
        if data["img_url"] == "" and data["name"] == "" and data["price"] == "" and data["img_url"] == "" and data["info"] == "" and data["sale"] == "" and data["sale_description"] == "":
             flash("An empty form cannot be updated!!")
             return redirect(url_for('about', em=session["user_email"]))
        update_item(data, session["user_email"], name)
        return redirect(url_for('about', em=session["user_email"]))

    @app.route('/edit_owner', methods=['POST'])
    def update_owner():
        data = request.form
        if data["name"] == ""  and data["phone"] == "" and data["city"] == "" and data["zip_code"] == "" and data["img_url"] == "":
            flash("An empty form cannot be updated!!")
            return redirect(url_for('about', em=session["user_email"]))
        update_owner_profile(data,session["user_email"])
        return redirect(url_for('about', em=session["user_email"]))

    @app.route('/logout')
    def logout():
        global template
        session["user_email"] = None
        template = "masterpage.html"
        return redirect(url_for('root'))


    @app.route('/about')
    def about():
        email = request.args.get('em')
        date_month =  get_like_date(email)
        rows = []
        for i in date_month:
            month = i.get('month')
            count = i.get('count')
            rows.append([month,count])
        with xlsxwriter.Workbook('test.xlsx') as workbook:
            worksheet = workbook.add_worksheet()
            worksheet.write('A1', 'month')
            worksheet.write('B1', 'count')
            for row_num, data in enumerate(rows):
                worksheet.write_row(row_num+1, 0, data)
        var = pd.read_excel("test.xlsx")
        x = list(var['month'])
        y = list(var['count'])
        data = {'month': x,
                'count': y
                }
        df = pd.DataFrame(data, columns=['month', 'count'])
        df.plot(x='month', y='count', kind='bar', title='Likes By month')
        plt.xticks(rotation=65)
        plt.savefig('static/chart.png')
        fig1, ax1 = plt.subplots()
        ax1.pie(y, labels=x,autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')
        plt.legend()
        plt.title("Likes By months percentage")
        plt.savefig('static/chart_pie.png')
        total_like = 0
        for i in y:
            total_like += i
        print(total_like)
        comments = None
        owner_items = None
        pictures = None
        if "user_email" in session:
            user = session["user_email"]
        else:
            user = None
        try:
            owner_items = get_items(email)
            comments = get_comments(email)
            pictures = get_pictures(email)
        except:
            pass
        owner = get_owner(email)
        return render_template('about_owner.html', owner_items=owner_items, owner=owner, var=template, user=user, comments=comments, pictures=pictures, total_like=total_like)


    @app.route('/compare')
    def compare():
        user = get_user(session["user_email"])
        left = request.args.get('left')
        right = request.args.get('right')
        left_items = None
        right_items = None
        try:
            left_items = get_items(left)
            right_items = get_items(right)

        except:
            pass
        left_owner = get_owner(left)
        right_owner = get_owner(right)
        return render_template('comparison.html',user=user, var=template, left_items=left_items, right_items=right_items,
                               left_owner=left_owner, right_owner=right_owner)





    @app.route('/category')
    def sort_category():
        user = get_user(session["user_email"])
        cat = request.args.get('cat')
        if cat == 'All':
            owners = get_owners()
        else:
            owners = get_owners(cat)
        categories = [x['categories'] for x in get_categories()]
        categories.append("All")
        return render_template('index.html',user=user, owners=owners, categories=list(set(categories)), var=template)


    @app.route('/category')
    def sort_likes():
        cat = request.args.get('cat')
        if cat == 'high-rating' or cat == 'low-rating':
            owners = get_owners()
        return render_template('index.html', owners=owners, var=template)

    @app.route('/like')
    def like_handling():
        owner = request.args.get('owner')
        date = datetime.date.today()
        add_like(session["user_email"], owner,date)
        return root()


    @app.route('/search', methods=['POST'])
    def search_owner():
        user = get_user(session["user_email"])
        owner_name = request.form['search']
        location = request.form['selected_search']
        owners = get_search(owner_name,location)
        categories = [x['categories'] for x in get_categories()]
        categories.append("All")
        return render_template('index.html', owners=owners,user=user, categories=list(set(categories)), var=template)


    @app.route('/login')
    def login():
        user = "tishreen12@gmail.com"
        return render_template('login.html',user=user)

    @app.route('/website_owner')
    def website_owner():
        user = get_user(session["user_email"])
        return render_template('website_owner.html',user=user)


    @app.route('/login', methods=['POST'])
    def login_user():
        global template
        data = request.form
        email = data["email"]
        password = data["password"]
        try:
            res = is_owner(email, password)
            if res == True:
                session['user_email'] = email
                template = "masterpage_loggedin.html"
            else:
                flash('Invalid Email or password ')
                return render_template('login.html')
        except OwnerDoesntExist:
            return root()
        return root()


    @app.route("/register/owner", methods=['GET'])
    def do_search():
        global items
        full_name = request.args.get('fullName')
        email = request.args.get('email')
        city = request.args.get('city')
        zip_code = request.args.get('zip_code')
        phone_number = request.args.get('mobileNo')
        busninessType = request.args.get('busninessType')
        description = request.args.get('comment')
        img_url = request.args.get('itemUrl')
        password = request.args.get('password')
        owner = Owner(full_name, email, city, zip_code, phone_number, busninessType, description, img_url, password)
        try:
            insert(owner, 0, items)
        except UserAlreadyExists as e:
            return "User already exists"
        items = []
        return redirect(url_for('root'))


    @app.route("/register/user")
    def register_user():
        full_name = request.args.get('fullName')
        email = request.args.get('email')
        city = request.args.get('city')
        zip_code = request.args.get('userzip_code')
        phone_number = request.args.get('usermobileNo')
        img_url = request.args.get('itemUrl')
        password = request.args.get('password')
        user = User(full_name, email, city, zip_code, phone_number, img_url, password)
        try:
            insert(user, 1)
        except UserAlreadyExists as e:
            return Response("User already exists")
        return redirect(url_for('root'))


    @app.route("/add_item", methods=['GET'])
    def add_item():
        global items
        item_name = request.args.get('itemName')
        price = request.args.get('Price')
        item_url = request.args.get('itemUrl')
        description = request.args.get('comment')
        item = Item(item_name, price, item_url, description,"","")
        items.append(item)
        return Response("", 204)


    @app.route('/register', methods=['POST'])
    def upload_file():
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            img_url = os.path.join('Images/', uploaded_file.filename)
            a = uploaded_file.save(img_url)
        return ""


    @app.route("/add_comment", methods=['GET'])
    def add_comment():
        owner = request.args.get('owner')
        comment = request.args.get('comment')
        insert_comment(session['user_email'], owner, comment)
        owner_items = get_items(owner)
        comments = get_comments(owner)
        pictures = get_pictures(owner)
        owner = get_owner(owner)
        return render_template('about_owner.html', owner_items=owner_items, owner=owner, var=template, user=session['user_email'],
                           comments=comments, pictures=pictures)


    @app.route("/add_picture", methods=['GET'])
    def add_picture():
        owner = request.args.get('owner')
        desc = request.args.get('desc')
        img_url = request.args.get('img_url')
        insert_picture(owner,img_url,desc)
        owner_items = get_items(owner)
        comments = get_comments(owner)
        pictures = get_pictures(owner)
        owner = get_owner(owner)
        if(img_url == None):
            return ""
        return redirect(url_for('about', em=session["user_email"]))


    @app.route("/add_new_item", methods=['GET'])
    def add_new_item():
        global items
        item_name = request.args.get('itemName')
        price = request.args.get('Price')
        item_url = request.args.get('itemUrl')
        description = request.args.get('comment')
        sale = ""
        sale_description = ""
        item = Item(item_name, price, item_url, description,sale,sale_description)
        items.append(item)
        insert_item(session['user_email'],price,description,item_name,item_url,sale,sale_description)
        comments = None
        owner_items = None
        pictures = None
        if "user_email" in session:
            user = session["user_email"]
        else:
            user = None
        try:
            owner_items = get_items(session['user_email'])
            comments = get_comments(session['user_email'])
            pictures = get_pictures(session['user_email'])
        except:
            pass
        owner = get_owner(session['user_email'])
        return redirect(url_for('about', em=session["user_email"]))

    return app

app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)  # Change the port number as needed

