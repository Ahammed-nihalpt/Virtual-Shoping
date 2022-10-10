from flask import Flask, render_template, request, redirect, session, jsonify
from DBConnection import Db
import time
import datetime

app = Flask(__name__)
app.secret_key="hi"
staticpath = "E:\\Projectbackups\\virtual\\virtual_shoping\\static\\"

@app.route('/')
def launching_index():
    return render_template('launching_index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/login_index")
def login_index():
    return render_template("login_index.html")

@app.route('/login_post',methods=['post'])
def login_post():
    u_name = request.form['textfield']
    ps_word = request.form['textfield2']
    db = Db()
    qry = "SELECT * FROM login WHERE `user_name`='"+u_name+"' AND `pass_word`='"+ps_word+"'"
    res = db.selectOne(qry)
    if res!=None:
        session['lid']=res['login_id']
        if res['type']=='admin':
            return '''<script>alert('Login Success');window.location='/a'</script>'''
        elif res['type']=='store':
            return '''<script>alert('Login Success');window.location='/store_index'</script>'''
        else:
            return '''<script>alert('Invalid User');window.location='/'</script>'''
    else:
        return '''<script>alert('Invalid User');window.location='/'</script>'''

@app.route('/admin_home')
def admin_home():
    return render_template('Admin/admin_home.html')

@app.route('/category_add')
def category_management():
    return render_template('Admin/category_management_add.html')
@app.route('/category_add_post',methods=['post'])
def category_add_post():
    category_name = request.form['textfield']


    db = Db()
    qry = "INSERT INTO category(category_name) VALUES('"+category_name+"')"
    res = db.insert(qry)
    print(res)

    return '''<script>alert('Added Successfuly');window.location='/view_category_management'</script>'''


@app.route('/view_category_management')
def view_category_management():
    db= Db()
    qry = "SELECT * FROM category"
    res=db.select(qry)
    return render_template('Admin/view_category_management.html', data=res)

@app.route('/search_category', methods=['post'])
def search_category():
    search_name = request.form['searchfield']
    db = Db()
    qry = "SELECT * FROM category WHERE category_name LIKE '%"+search_name+"%'"
    res = db.select(qry)
    return render_template('Admin/view_category_management.html', data=res)

@app.route('/delete_category/<id>')
def delete_category(id):
    db = Db()
    qry = " DELETE FROM category WHERE category_id = '"+id+"'"
    res = db.delete(qry)
    return '''<script>alert('deleted Successfuly');window.location='/view_category_management'</script>'''

@app.route('/edit_category/<id>')
def edit_category(id):
    db = Db()
    qry = "select * from category WHERE category_id = '" + id + "'"
    res = db.selectOne(qry)

    return render_template('Admin/edit_category_management.html',data=res)



@app.route('/edit_category_post',methods=['post'])
def edit_category_post():
    id = request.form['cid']
    edit_category_name = request.form['textfield']
    db = Db()
    qry = "UPDATE category SET category_name ='"+edit_category_name+"' WHERE category_id= '"+id+"'"
    res = db.update(qry)
    return redirect("/view_category_management")



@app.route('/send_reply/<id>')
def send_reply(id):
    db = Db()
    qry = "select * from complaint WHERE complaint_id = '" + id + "'"
    res = db.selectOne(qry)
    return render_template('Admin/send_reply.html', data=res)



@app.route('/send_reply_post',methods=['post'])
def send_reply_post():
    reply = request.form['textarea']
    id = request.form['complaint_id']
    db = Db()
    qry2 = "UPDATE complaint SET reply='"+reply+"' WHERE complaint_id='"+id+"'"
    res2=db.update(qry2)
    return '''<script>alert('Successfully replied');window.location='/view_complaints_about_store'</script>'''

@app.route('/store_approve_reject')
def store_approve_reject():

    db= Db()
    qry = "SELECT store.* FROM store WHERE store.status='pending'"
    res=db.select(qry)
    return render_template('Admin/store_approve_reject.html', data=res)

@app.route('/store_approve/<id>')
def store_approve(id):
    db = Db()
    qry = " UPDATE store set status= 'approved' where store_login_id='"+id+"'"
    res = db.update(qry)
    qry1 = "UPDATE login set `type`= 'store' where login_id='"+id+"'"
    res1 = db.update(qry1)
    return '''<script>alert('Approved');window.location='/store_approve_reject'</script>'''

@app.route('/store_reject/<id>')
def store_reject(id):
    db = Db()
    qry = " UPDATE store set status= 'rejected' where store_login_id='"+id+"'"
    res = db.update(qry)
    return redirect('/store_approve_reject')




@app.route('/view_approved_store')
def view_approved_store():
    db = Db()
    qry = "SELECT store.* FROM store WHERE store.status='approved'"
    res = db.select(qry)
    return render_template('Admin/view_approved_store.html', data=res)

@app.route('/search_approved_store_search', methods=['post'])
def search_approved_store_search():
    search_name = request.form['searchfield']
    db = Db()
    qry = "SELECT store.* FROM store WHERE store.status='approved' AND store_name like '%"+search_name+"%'"
    res = db.select(qry)
    return render_template('Admin/view_approved_store.html', data=res)




@app.route('/store_rating_report')
def store_rating_report():
    db = Db()
    qry = "SELECT store.store_name,rating.* FROM rating INNER JOIN store ON rating.store_lid=store.store_login_id"
    res = db.select(qry)
    return render_template('Admin/store_rating_report.html', data=res)

    return render_template('Admin/store_rating_report.html')

@app.route('/store_rating_report_search', methods=['post'])
def store_rating_report_search():
    search_name = request.form['searchfield']
    db = Db()
    qry = "SELECT store.store_name,rating.* FROM rating INNER JOIN store ON rating.store_lid=store.store_login_id AND store_name like '%"+search_name+"%'"
    res = db.select(qry)
    return render_template('Admin/store_rating_report.html', data=res)




@app.route('/view_complaints_about_store')
def view_complaints_about_store():
    db = Db()
    qry = "SELECT customer.user_name,customer.user_image,complaint.*,store.store_name,store.store_place FROM complaint INNER JOIN customer ON complaint.user_lid=customer.user_lid INNER JOIN store ON store_login_id=complaint.store_id"
    res = db.select(qry)
    return render_template('Admin/view_complaints_about_store.html', data=res)


@app.route('/view_reject_store')
def view_reject_store():
    db = Db()
    qry = "SELECT store.* FROM store WHERE store.status='rejected'"
    res = db.select(qry)
    return render_template('Admin/view_reject_store.html', data=res)

@app.route('/view_store_booking_report')
def view_store_booking_report():
    db = Db()
    qry = "SELECT store.store_name, COUNT(order_id) AS num, SUM(`total_amount`) AS total, order_main.date  FROM store INNER JOIN order_main ON store.store_login_id = order_main.store_lid GROUP BY `order_main`.`store_lid`,  order_main.date"
    res = db.select(qry)
    return render_template('Admin/view_store_booking _report.html', data=res)


@app.route('/view_store_booking_report_post', methods=['post'])
def view_store_booking_report_post():
    start = request.form['textfield']
    last = request.form['textfield2']
    db = Db()
    qry = "SELECT store.store_name, COUNT(order_id) AS num, SUM(`total_amount`) AS total, order_main.date  FROM store INNER JOIN" \
          " order_main ON store.store_login_id = order_main.store_lid where order_main.date between '"+start+"' and '"+last+"' GROUP BY `order_main`.`store_lid`,  order_main.date"
    res = db.select(qry)
    return render_template('Admin/view_store_booking _report.html', data=res)

@app.route('/view_users')
def view_users():
    db = Db()
    qry = "SELECT * FROM customer"
    res = db.select(qry)
    return render_template('Admin/view_users.html', data=res)






#module store

@app.route('/store_index')
def store_index():
    return render_template('Store/store_index.html')

@app.route('/store_registration_index')
def registration_index():
    return render_template('Store/registration_index.html')


@app.route('/store_home')
def store_home():
    return render_template('Store/store_home.html')

@app.route('/store_registration')
def store_registration():
    return render_template('Store/registration.html')

@app.route('/store_registration_post',methods=['post'])
def store_registration_post():
    store_name = request.form['textfield']
    store_Phone = request.form['textfield2']
    store_email = request.form['textfield3']

    store_image = request.files['fileField']
    print(store_image.filename)
    gg=str(store_image.filename)
    yy=gg.split(".")
    print("=============================================",yy[1])

    if yy[1]=="jpg" or yy[1]=="jpeg" or yy[1]=="png":
        dt = time.strftime('%Y%m%d-%H%M%S')
        store_image.save(staticpath+"store_img\\"+dt+".jpg")
        url = "/static/store_img/"+dt+".jpg"

        store_place = request.form['textfield4']
        store_pin = request.form['textfield5']
        store_post = request.form['textfield6']
        store_lic_no = request.form['textfield7']
        owner_name = request.form['textfield8']
        owner_phone = request.form['textfield9']
        Store_longitude = request.form['textfield10']
        Store_latitude = request.form['textfield11']
        Store_acc_no= request.form['textfield12']
        new_paswrd = request.form['textfield13']
        cnf_password = request.form['textfield14']
        if new_paswrd==cnf_password:
            db = Db()
            qry = "INSERT INTO login(`user_name`,`pass_word`,`type`) VALUES('"+store_email+"','"+cnf_password+"','pending')"
            res = db.insert(qry)
            qry1 = "INSERT INTO store(store_name, store_contact, store_email, store_place, store_pin, store_lic_no, owner_name, owner_contact, store_latitude, store_longitude,store_login_id, store_acc_no,status,store_post,store_image) VALUES ('" + store_name + "','" + store_Phone + "','" + store_email + "','" + store_place + "','" + store_pin + "','" + store_lic_no + "','" + owner_name + "','" + owner_phone + "','" + Store_latitude + "','" + Store_longitude + "','"+str(res)+"','" + Store_acc_no + "','pending','" + store_post + "','"+url+"')"
            res1 = db.insert(qry1)
            print(res1)
            return '''<script>alert('Registration Successfull');window.location='/login_index'</script>'''
        else:
            return '''<script>alert('password do not match');window.location='/store_registration_index'</script>'''
    else:
        return '''<script>alert('Please provide a correct image');window.location='/store_registration_index'</script>'''







@app.route('/store_view_profile')
def store_view_profile():
    db = Db()
    qry = "SELECT * FROM store WHERE `store_login_id`='"+str(session['lid'])+"'"
    res = db.selectOne(qry)
    return render_template('Store/view_profile.html', data=res)

@app.route('/store_edit_profile')
def store_edit_profile():
    db = Db()
    qry = "select * from store WHERE `store_login_id`='"+str(session['lid'])+"'"
    res = db.selectOne(qry)
    return render_template('Store/edit_profile.html',data=res)

@app.route('/edit_store_profile_post',methods=['post'])
def edit_profile():
    store_name = request.form['textfield']
    store_email = request.form['textfield3']
    store_Phone = request.form['textfield2']
    store_place = request.form['textfield4']
    store_pin = request.form['textfield5']
    store_post = request.form['textfield6']
    store_lic_no = request.form['textfield7']
    owner_name = request.form['textfield8']
    owner_phone = request.form['textfield9']
    Store_longitude = request.form['textfield10']
    Store_latitude = request.form['textfield11']
    Store_acc_no = request.form['textfield12']

    db = Db()
    if 'fileField' in request.files:
        store_image = request.files['fileField']
        if store_image.filename != "":
            print("-------------")
            dt = time.strftime('%Y%m%d-%H%M%S')
            store_image.save(staticpath + "store_img\\" + dt + ".jpg")
            url = "/static/store_img/" + dt + ".jpg"
            qry = "UPDATE store SET `store_name`='"+store_name+"',`store_contact`='"+store_Phone+"',`store_email`='"+store_email+"',`store_place`='"+store_place+"',`store_pin`='"+store_pin+"',`store_lic_no`='"+store_lic_no+"',`owner_name`='"+owner_name+"',`owner_contact`='"+owner_phone+"',`store_latitude`='"+Store_latitude+"',`store_longitude`='"+Store_longitude+"',`store_acc_no`='"+Store_acc_no+"',`store_post`='"+store_post+"',`store_image`='"+url+"'  WHERE `store_login_id`='"+str(session['lid'])+"'"
            res = db.update(qry)
            return redirect("/store_view_profile")
        else:
            qry1="UPDATE store SET `store_name`='"+store_name+"',`store_contact`='"+store_Phone+"',`store_email`='"+store_email+"',`store_place`='"+store_place+"',`store_pin`='"+store_pin+"',`store_lic_no`='"+store_lic_no+"',`owner_name`='"+owner_name+"',`owner_contact`='"+owner_phone+"',`store_latitude`='"+Store_latitude+"',`store_longitude`='"+Store_longitude+"',`store_acc_no`='"+Store_acc_no+"',`store_post`='"+store_post+"'   WHERE `store_login_id`='"+str(session['lid'])+"'"
            res1=db.update(qry1)
            return redirect("/store_view_profile")
    else:
        qry2 = "UPDATE store SET `store_name`='" + store_name + "',`store_contact`='" + store_Phone + "',`store_email`='" + store_email + "',`store_place`='" + store_place + "',`store_pin`='" + store_pin + "',`store_lic_no`='" + store_lic_no + "',`owner_name`='" + owner_name + "',`owner_contact`='" + owner_phone + "',`store_latitude`='" + Store_latitude + "',`store_longitude`='" + Store_longitude + "',`store_acc_no`='" + Store_acc_no + "',`store_post`='" + store_post + "'   WHERE `store_login_id`='" + str(session['lid']) + "'"
        res2 = db.update(qry2)
        return redirect("/store_view_profile")

@app.route('/store_add_product')
def store_add_product():
    db = Db()
    qry="SELECT * FROM category"
    res = db.select(qry)
    print(res)
    return render_template('Store/Add_product.html', data=res)

@app.route('/store_add_product_post', methods=['post'])
def store_add_product_post():
    product_name = request.form['textfield']
    product_stock = request.form['textfield2']
    product_price = request.form['textfield3']
    product_image = request.files['fileField']
    cat = request.form['select']
    dt = time.strftime('%Y%m%d-%H%M%S')
    product_image.save(staticpath + "store_product_image\\" + dt + ".jpg")
    url = "/static/store_product_image/" + dt + ".jpg"

    db = Db()
    qry = "INSERT INTO products(product_name, stock_available, price,product_image,store_lid,category_id) VALUES ('"+product_name+"','"+product_stock+"','"+product_price+"','"+url+"','" + str(session['lid']) + "','"+cat+"')"
    res = db.insert(qry)
    print(res)
    return '''<script>alert('add Successfull');window.location='/store_view_product'</script>'''

@app.route('/store_view_product')
def store_view_product():
    db = Db()
    qry = "SELECT `products`.*, `category`.`category_name` FROM `category` INNER JOIN `products` ON `products`.`category_id`=`category`.`category_id` WHERE store_lid='" + str(session['lid']) + "'"
    res = db.select(qry)
    print(res)
    return render_template('Store/View_Product.html', data=res)




@app.route('/store_product_search', methods=['post'])
def search_products():
    search_product = request.form['searchfield']
    db = Db()
    qry = "SELECT `products`.*, `category`.`category_name` FROM `category` INNER JOIN `products` ON `products`.`category_id`=`category`.`category_id`  WHERE product_name LIKE '%" + search_product + "%' AND store_lid='" + str(session['lid']) + "'"
    res = db.select(qry)
    return render_template('Store/View_Product.html', data=res)

@app.route('/store_edit_product/<id>')
def store_edit_product(id):
    db = Db()
    qry1="SELECT * FROM category"
    res1=db.select(qry1)
    qry = "SELECT `products`.*, `category`.`category_name` FROM `category` INNER JOIN `products` ON `products`.`category_id`=`category`.`category_id` WHERE product_id='" + id + "'"
    res = db.selectOne(qry)
    return render_template('Store/Edit_Product.html', data=res,data1=res1)

@app.route('/store_edit_product_post', methods=['post'])
def store_edit_product_post():
    product_name = request.form['textfield']
    product_stock = request.form['textfield2']
    product_price = request.form['textfield3']
    id=request.form['pid']
    cat = request.form['select']
    db = Db()
    if 'fileField' in request.files:
        product_image = request.files['fileField']
        if product_image.filename != "":
            print("-------------")
            dt = time.strftime('%Y%m%d-%H%M%S')
            product_image.save(staticpath + "store_product_image\\" + dt + ".jpg")
            url = "/static/store_product_image/" + dt + ".jpg"
            qry = "UPDATE products SET `product_name`='" + product_name + "',`stock_available`='" + product_stock + "',`price`='" + product_price + "',`product_image`='" + url + "',category_id='"+cat+"'  WHERE product_id='"+id+"'"
            res = db.update(qry)
            return redirect("/store_view_product")
        else:
            qry = "UPDATE products SET `product_name`='" + product_name + "',`stock_available`='" + product_stock + "',`price`='" + product_price + "',category_id='"+cat+"' WHERE product_id='"+id+"'"
            res = db.update(qry)
            return redirect("/store_view_product")
    else:
        qry = "UPDATE products SET `product_name`='" + product_name + "',`stock_available`='" + product_stock + "',`price`='" + product_price + "',category_id='"+cat+"' WHERE product_id='"+id+"'"
        res = db.update(qry)

        return render_template('Store/Edit_Product.html')


@app.route('/store_delete_product/<id>')
def store_delete_product(id):
    db = Db()
    qry = " DELETE FROM products WHERE product_id = '"+id+"'"
    res = db.delete(qry)
    return '''<script>alert('deleted Successfuly');window.location='/store_view_product'</script>'''


@app.route('/store_product_review')
def store_product_review():
    db = Db()
    qry = "SELECT `review`.*, `products`.`product_image`, `products`.`product_name`, `customer`.`user_name`, `customer`.`user_email`,`category`.`category_name` FROM `products` INNER JOIN `review` ON `review`.`product_id`=`products`.`product_id` INNER JOIN `customer` ON `customer`.`user_lid`=`review`.`user_id` INNER JOIN `category` ON `products`.`category_id`=`category`.`category_id` WHERE products.store_lid='" + str(session['lid']) + "'"
    res=db.select(qry)
    return render_template('Store/view_product_review.html', data=res)

@app.route('/store_view_order_and_confirmation')
def store_view_order_and_conformation():
    db = Db()
    qry = "SELECT `customer`.`user_name`,`order_main`.`order_id`,`order_main`.`delivery_address`,`order_main`.`total_amount`,`order_main`.`date`,`order_main`.`time`,order_main.order_status FROM `order_main` INNER JOIN `customer` ON `order_main`.`user_id`=`customer`.`user_lid` WHERE `order_main`.store_lid='" + str(session['lid']) + "'  AND order_main.order_status='pending' or order_main.order_status='confirmed'"
    print(qry)
    res = db.select(qry)
    print(res)
    return render_template('Store/view_orders_send_conformation.html', data=res)

@app.route('/view_ordered_products/<id>')
def store_view_ordered_products(id):
    db = Db()
    qry = "SELECT `products`.`product_name`,`products`.`product_image`,`order_sub`.`quantity` FROM products INNER JOIN `order_sub` ON `products`.`product_id`=`order_sub`.`product_id` WHERE order_sub.order_id='"+id+"'"
    res = db.select(qry)

    return render_template('Store/view_ordered_products.html', data=res)

@app.route('/order_confirm/<id>')
def order_confirm(id):
    db=Db()
    qry = "UPDATE `order_main` SET `order_status` = 'paid' WHERE order_id='"+id+"'"
    res=db.update(qry)
    print(res)
    return '''<script>alert('Order Confirmed');window.location='/store_view_order_and_confirmation'</script>'''

@app.route('/order_decline/<id>')
def order_decline(id):
    db=Db()
    qry = "UPDATE `order_main` SET `order_status` = 'declined' WHERE order_id='"+id+"'"
    res=db.update(qry)
    return '''<script>alert('Order Declined');window.location='/store_view_order_and_confirmation'</script>'''

@app.route('/order_payment/<id>')
def order_payment(id):
    db=Db()
    qry = "UPDATE `order_main` SET `order_status` = 'paid' WHERE order_id='"+id+"'"
    qry1= "update `payment` set `payment_status`='paid' where `order_id`='"+id+"'"
    res2 = db.update(qry1)
    res=db.update(qry)
    return '''<script>alert('Order Paid');window.location='/store_view_order_and_confirmation'</script>'''

@app.route('/store_view_order_history')
def store_view_order_history():
    db=Db()
    qry = "SELECT `customer`.`user_name`,`order_main`.`order_id`,`order_main`.`total_amount`,`order_main`.`date`,`order_main`.`time`,`order_main`.`order_status` FROM order_main INNER JOIN customer ON `order_main`.`user_id`=`customer`.`user_lid` WHERE `order_main`.store_lid='" + str(session['lid']) + "' AND order_status!= 'pending'"
    res=db.select(qry)
    return render_template('Store/view_order_history.html', data=res)



@app.route('/store_payment')
def store_payment():
    db=Db()
    qry ="SELECT `customer`.`user_name`,`order_main`.`total_amount`,`payment`.`payment_status` FROM `order_main` INNER JOIN `customer` ON `customer`.`user_lid`=`order_main`.`user_id` INNER JOIN `payment` ON `payment`.`order_id`=`order_main`.`order_id` WHERE `order_main`.`date`=CURDATE()"
    res = db.select(qry)
    return render_template('Store/payment_store.html',data=res)

@app.route('/store_chat_with_customer')
def store_chat_with_customer():
    db=Db()
    qry="SELECT `order_main`.*,`customer`.* FROM `order_main` INNER JOIN `customer` ON `customer`.`user_lid`=`order_main`.`user_id` WHERE `order_main`.`store_lid`='" + str(session['lid']) + "' GROUP BY `order_main`.user_id"
    res=db.select(qry)
    return render_template('Store/chat_customer.html', data=res)

@app.route('/store_view_rating')
def store_view_rating():
    db=Db()
    qry="SELECT `rating`.*,`customer`.`user_name` FROM rating INNER JOIN customer ON `customer`.`user_lid`=`rating`.`user_lid` WHERE rating.store_lid='" + str(session['lid']) + "'"
    res=db.select(qry)
    return render_template('Store/view_rating.html', data=res)


@app.route("/a")
def a():
    return render_template("Admin/admin_index.html")

@app.route("/chat_user/<lid>")
def chat_user(lid):
    return render_template("Store/store_chat_user.html", toid=lid)

@app.route('/store_chat_view',methods=['post'])
def store_chat_view():
    db = Db()
    if session.get('lid') is None:
        return redirect("/")
    lid = session['lid']
    toid = request.form['idd']
    qry = db.select("SELECT * FROM `chat` WHERE ((`form_id`='"+str(lid)+"' AND `to_id`='"+toid+"')OR(`form_id`='"+toid+"' AND `to_id`='"+str(lid)+"')) order by `chat_id` DESC")
    print(qry)
    return jsonify(qry)


@app.route('/store_chat_add',methods=['post'])
def store_chat_add():
    db = Db()
    if session.get('lid') is None:
        return redirect("/")
    lid = session['lid']
    toid = request.form['hid']
    msg = request.form['ta']
    qry = db.insert("INSERT INTO `chat`(`form_id`,`to_id`,`message`,`date`)VALUES('"+str(lid)+"','"+toid+"','"+msg+"',curdate())")
    return render_template("Store/store_chat_user.html", toid=toid)







# module 3 (customer)

@app.route('/customer_login',methods=['post'])
def customer_login():
    u_name = request.form['u_name']
    ps_word = request.form['u_pass']
    db = Db()
    qry = "SELECT * FROM login WHERE `user_name`='" + u_name + "' AND `pass_word`='" + ps_word + "'"
    res = db.selectOne(qry)

    if res is not None:
        return jsonify(status="ok",lid=res["login_id"],type = res['type'])
    else:
        return jsonify(status="no")


@app.route('/customer_registration', methods=['post'])
def customer_registration():
    cus_name= request.form['c_name']
    cus_contact = request.form['c_contact']
    cus_email = request.form['c_email']
    cus_email = cus_email.lower()
    cus_image = request.form['c_image']
    cus_place = request.form['c_place']
    cus_pin = request.form['c_pin']
    cus_post = request.form['c_post']
    cus_password = request.form['c_password']
    import time, datetime
    from encodings.base64_codec import base64_decode
    import base64

    timestr = time.strftime("%Y%m%d-%H%M%S")
    print(timestr)
    a = base64.b64decode(cus_image)
    fh = open(staticpath+"cus_img\\" + timestr + ".jpg", "wb")
    path = "/static/cus_img/" + timestr + ".jpg"
    fh.write(a)
    fh.close()
    db = Db()
    qry = "INSERT INTO login(`user_name`,`pass_word`,`type`) VALUES('" + cus_email + "','" + cus_password + "','customer')"
    res = db.insert(qry)
    qry1 = "INSERT INTO customer(user_name, user_contact, user_email, user_image, user_place, user_pin, user_post,user_lid) VALUES ('" + cus_name + "','" + cus_contact + "','" + cus_email + "','" + path + "','" + cus_place + "','" + cus_pin + "','" + cus_post + "','"+str(res)+"')"
    res1 = db.insert(qry1)
    return jsonify(status="ok")


# @app.route('/view_payment', method=['post'])
# def view_payment():
#     return ()




@app.route('/customer_view_profile', methods=['post'])
def customer_view_profile():
    lid = request.form['lid']
    db = Db()
    qry = "SELECT * FROM `customer` WHERE `user_lid`='"+lid+"'"
    res = db.selectOne(qry)
    print(res)
    return jsonify(status="ok", name=res['user_name'],user_image=res["user_image"],contact=res['user_contact'], email=res['user_email'],image=res['user_image'],place=res['user_place'],pin=res['user_pin'],post=res['user_post'])

@app.route('/edit_profile_post', methods=['post'])
def customer_edit_profile():
    lid = request.form['lid']
    cus_name = request.form['c_name']
    cus_contact = request.form['c_contact']
    cus_email = request.form['c_email']
    cus_image = request.form['c_image']
    cus_place = request.form['c_place']
    cus_pin = request.form['c_pin']
    cus_post = request.form['c_post']
    db = Db()
    qry = "UPDATE `customer` SET `user_name`='"+cus_name+"',`user_contact`='"+cus_contact+"',`user_email`='"+cus_email+"',`user_image`='"+cus_image+"',`user_place`='"+cus_place+"',`user_pin`='"+cus_pin+"',`user_post`='"+cus_post+"' WHERE `user_id`='"+lid+"'"
    res = db.select(qry)
    return jsonify(status="ok")
#_____________________________________
@app.route('/customer_view_store', methods=['post'])
def customer_view_store():
    db = Db()
    lati=request.form["lat"]
    logi=request.form["lon"]
    # qry = "SELECT * FROM store"
    qry="SELECT `login`.*, `store`.*,SQRT(POW(69.1 * (`store_latitude` -'"+lati+"'),2) +POW(69.1 *('"+logi+"' - `store_longitude`) * COS(`store_latitude`/57.3),2)) AS distance FROM `store` INNER JOIN `login` ON `login`.`login_id`=`store`.`store_login_id` WHERE `login`.`type`='store' ORDER BY distance"
    res = db.select(qry)
    return jsonify(status="ok",users=res)

@app.route('/customer_view_product', methods=['post'])
def customer_view_product():
    shop_lid=request.form["shop_lid"]
    db = Db()
    qry = "SELECT * FROM products where store_lid='"+shop_lid+"' order by pos DESC,neu DESC,neg ASC"
    res = db.select(qry)
    print(res)
    return jsonify(status="ok",data=res)
@app.route('/addtocart', methods=['post'])
def add_to_cart():
    pid=request.form['pid']
    sid=request.form['sid']
    uid=request.form['uid']
    count=request.form['count']
    db=Db()
    qry="INSERT INTO `cart`(`product_id`,`store_id`,`user_id`,`date`,`count`) VALUES ('"+pid+"','"+sid+"','"+uid+"',curdate(),'"+count+"')"
    res=db.insert(qry)
    return jsonify(status="ok")
@app.route('/customer_view_cart', methods=['post'])
def customer_view_cart():
    lid = request.form['lid']
    sid = request.form['sid']
    db = Db()
    qry = "SELECT `products`.*,cart.* FROM products INNER JOIN cart ON cart.`product_id`=`products`.`product_id` WHERE cart.user_id='"+lid+"' and `cart`.`store_id`='"+sid+"'"
    res = db.select(qry)
    return jsonify(status="ok", data=res)
@app.route("/delete_cart", methods=['post'])
def delete_cart():
    cart_id=request.form['cart_id']
    print(cart_id)
    qry = "DELETE FROM `cart` WHERE `cart_id`='"+cart_id+"'"
    print(qry)
    db=Db()
    res=db.delete(qry)
    print(res)
    return jsonify(status="ok")

@app.route("/buy_product", methods=['post'])
def buy_product():
    db=Db()
    print("hi")
    bank_name = request.form['bank_name']
    print("hoi")
    accno = request.form['account_no']
    password = request.form['pass']
    selerid = request.form['selerid']
    lid=request.form['lid']

    address=request.form["address"]
    place=request.form["place"]
    pin=request.form["pin"]
    post=request.form["post"]

    qry="SELECT * FROM bank WHERE bank_name = '"+bank_name+"'and account_number= '"+accno+"'and pin_number='"+password+"'"
    ress=db.selectOne(qry)
    if ress is None:
        return jsonify(status="no")
    else:
        qry="SELECT * FROM `cart` WHERE `user_id`='"+lid+"' AND `store_id`='"+selerid+"'"
        res=db.select(qry)
        tot=0
        for i in res:
            pid=i["product_id"]
            qty=i["count"]
            qry1="SELECT `price` FROM `products` WHERE `product_id`='"+str(pid)+"'"
            res1=db.selectOne(qry1)
            pr=res1['price']
            tot+=float(pr)*float(qty)
            print(tot)

        if  float(ress['balance']) > tot:
            qry="INSERT INTO `order_main` (`user_id`,`order_status`,`date`,`total_amount`,`store_lid`,`time`,`delivery_address`,`delivery_place`,`delivery_pin`,`delivery_post`) VALUES('"+str(lid)+"','pending',CURDATE(),'"+str(tot)+"','"+str(selerid)+"',curtime(),'"+address+"','"+place+"','"+pin+"','"+post+"')"
            orderid=db.insert(qry)

            for i in res:
                pid = i["product_id"]
                qty = i["count"]
                qry="INSERT INTO `order_sub` (`order_id`,`product_id`,`quantity`) VALUES ('"+str(orderid)+"','"+str(pid)+"','"+str(qty)+"')"
                db.insert(qry)

                up="UPDATE `products` SET `stock_available`=`stock_available`-'"+str(qty)+"' WHERE `product_id`='"+str(pid)+"'"
                db.update(up)

            db.delete("DELETE FROM `cart` WHERE `user_id`='"+str(lid)+"' AND `store_id`='"+selerid+"'")

            qry="INSERT INTO `payment` (`order_id`,`payment_date`,`amount`,`payment_status`) VALUES ('"+str(orderid)+"',CURDATE(),'"+str(tot)+"','paid')"
            db.insert(qry)
        return jsonify(status="ok")

@app.route('/customer_view_store_rating', methods=['post'])
def customer_view_store_review():
    db = Db()
    qry = "SELECT `store`.*,`rating`.* FROM store INNER JOIN rating ON `rating`.`store_lid`=`store`.`store_id`"
    res = db.select(qry)
    return jsonify(status="ok",)

@app.route('/customer_change_password', methods=['post'])
def customer_change_password():
    lid = request.form['lid']

    new_pass=request.form['confpass']
    db = Db()


    qry="UPDATE `login` SET `pass_word`='"+str(new_pass)+"' WHERE `login_id`='"+str(lid)+"' "
    db.update(qry)
    return jsonify(status='ok')



@app.route('/and_rating_sadd', methods=['post'])
def and_rating_sadd():
    rating = request.form["rating"]
    uid = request.form["uid"]
    slid = request.form["sid"]
    db = Db()
    qry = "INSERT INTO `rating` (`user_lid`,`date`,`rating`,`store_lid`) VALUES ('" + uid + "',CURDATE(),'" + rating + "','" + slid + "')"
    print(qry)
    db.insert(qry)

    return jsonify(status='ok')


@app.route('/and_view_store_rating',methods=["post"])
def and_view_store_rating():
    slid=request.form["slid"]
    q="SELECT `customer`.`user_name`,`customer`.`user_email`,`customer`.`user_image`,rating.* FROM`customer` INNER JOIN `rating` ON `customer`.`user_lid`=`rating`.`user_lid` WHERE `rating`.`store_lid`='"+slid+"'"
    d=Db()
    res=d.select(q)
    print(q)
    print(res)
    return jsonify(status="ok",users=res)


@app.route("/and_reviews", methods=['post'])
def send_ratingandreview():
    re = request.form["review"]
    uid = request.form["uid"]
    pid = request.form["pid"]
    db = Db()
    qry = "INSERT INTO `review` (`product_id`,`review`,`user_id`,`date`) VALUES('"+pid+"','"+re+"','"+uid+"',CURDATE())"
    db.insert(qry)

    print("ok")

    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    analyser = SentimentIntensityAnalyzer()

    sent = re

    score = analyser.polarity_scores(sent)
    print(score['neu'], score['pos'], score['neg'])

    if score['neg'] > score['pos'] and score['neg'] > score['neu']:
        print("its negative")
        qry = "UPDATE `products` SET neg=neg+1 WHERE `product_id`='" + pid + "'"
        db.update(qry)
    elif score['pos'] > score['neg'] and score['pos'] > score['neu']:
        print("its positive")
        qry = "UPDATE `products` SET pos=pos+1 WHERE `product_id`='" + pid + "'"
        db.update(qry)
    else:
        qry = "UPDATE `products` SET neu=neu+1 WHERE `product_id`='" + pid + "'"
        db.update(qry)
        print("its neutral")

    return jsonify(status="ok")

@app.route('/customer_view_product_review', methods=['post'])
def customer_view_product_review():
    pid=request.form["pid"]
    db = Db()
    qry = "SELECT `review`.*,`customer`.* FROM review INNER JOIN `customer` ON `review`.`user_id` = `customer`.`user_lid`WHERE `review`.`product_id`='"+pid+"' "
    res = db.select(qry)
    return jsonify(status="ok",users=res)



@app.route('/customer_view_pre_order', methods=['post'])
def customer_view_pre_order():
    db = Db()
    lid=request.form['lid']
    qry = "SELECT `store`.*,`order_main`.* FROM `order_main` INNER JOIN `store` ON `store`.`store_login_id`=`order_main`.`store_lid` WHERE `order_main`.`user_id`='"+lid+"'"
    res = db.select(qry)
    print(qry)
    return jsonify(status="ok",data=res)

@app.route('/customer_view_pre_order_more', methods=['post'])
def customer_view_pre_order_more():
    db = Db()
    oid=request.form['oid']
    qry = "SELECT `products`.*,`order_sub`.* FROM `order_sub` INNER JOIN `products` ON `order_sub`.`product_id`=`products`.`product_id` WHERE `order_sub`.`order_id`='"+oid+"'"
    res = db.select(qry)
    return jsonify(status="ok",data=res)

@app.route("/send_complaint", methods=['post'])
def send_complaint():
    print("hhh")
    complaint = request.form['complaint']
    lid= request.form['lid']
    slid= request.form['slid']
    qry="INSERT INTO `complaint` (`user_lid`,`date`,`complaint`,`reply`,`store_id`) VALUES ('"+lid+"',CURDATE(),'"+complaint+"','pending','"+slid+"')"
    print(qry)
    db = Db()
    res = db.insert(qry)
    return jsonify(status="ok", data=res)

@app.route("/viewreply", methods=['post'])
def viewreply():
    lid=request.form['lid']
    slid=request.form['slid']
    print(lid)
    qry="SELECT `complaint`,`reply`,`date` FROM `complaint` WHERE `user_lid`='"+lid+"' and store_id='"+slid+"' "
    db=Db()
    res = db.select(qry)
    print(res)
    return jsonify(status="ok",data=res)

@app.route('/in_message', methods=['POST'])
def message():
    fr_id = request.form["fid"]
    to_id = request.form["toid"]
    message = request.form["msg"]
    query7 = "INSERT INTO `chat`(`form_id`,`to_id`,`message`,DATE) VALUES ('" + fr_id + "' ,'" + to_id + "','" + message + "',CURDATE())"
    print(query7);
    d=Db()
    d.insert(query7)
    return jsonify(status='ok')


@app.route('/view_message', methods=['POST'])
def msg():
    fid = request.form["fid"]
    toid = request.form["toid"]
    # name = request.form["name"]
    lmid = request.form['lastmsgid'];

    #  query = "select *  from chat_coach_user where (sender_id='" + fr_id + "' and receiver_id='" + to_id + "') or (sender_id='" + to_id + "'  and receiver_id='" + fr_id + "')"
    query="SELECT `form_id` as from_id,`message`,date,`chat_id` FROM `chat` WHERE `chat_id`>'"+lmid+"' AND ((`to_id`='"+toid+"' AND  `form_id`='"+fid+"') OR (`to_id`='"+fid+"' AND `form_id`='"+toid+"')  )  ORDER BY `chat_id` ASC"
    d=Db()
    res=d.select(query)

    if len(res)>0:


        return jsonify(status='ok', res1=res)

    else:
        return jsonify(status='not found')


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
