import random
from os.path import join

from flask import Flask, render_template, request, jsonify
from flask.globals import session
from dbconnection import Db
import datetime

app = Flask(__name__)
app.secret_key='aaa'
static_path="D:\\shopmee\\static\\"
@app.route('/')
def hello_world():
    return render_template("login_temp.html")
@app.route('/adminhome')
def adminhome():
    return render_template("admin/admin_home.html")
@app.route("/login_post",methods=['post'])
def login_post():
    username=request.form['username']
    password=request.form['pass']
    qry="SELECT * FROM login WHERE username='"+username+"' and PASSWORD='"+password+"'"
    db=Db()
    res=db.selectOne(qry)
    if res is not None:
        session['lid']=res['login_id']
        if res['usertype']=='admin':
            return adminhome()
        elif res['usertype']=='seller':
            return sellerhome()
        elif res['usertype']=='store':
            return render_template('/store/home.html')

        elif res['usertype'] == 'rejected':
            return "<script>window.location='/';alert('You are Not Registered..........')</script>"
    else:
        return "<script>window.location='/';alert('Invalid')</script>"





    return 'ok'

@app.route("/adm_add_category")
def adm_add_category():
    return render_template("admin/add category.html")
@app.route("/adm_add_category_post",methods=['post'])
def adm_add_category_post():
    category=request.form['textfield']
    db=Db()
    db.insert("INSERT INTO category VALUES(null,'"+category+"')")
    print("INSERT INTO category VALUES(null,'"+category+"')")
    return render_template("admin/add category.html",s="1")

@app.route("/adm_complaint")
def adm_complaint():
    db=Db()
    res=db.select("SELECT complaint.*,customer.`customer_name`,customer.`email_id`,`customer`.`login_id` FROM `complaint` INNER JOIN `customer` ON `complaint`.`customer_l_id`=`customer`.`login_id` where complaint.status='pending' ORDER BY `complaint`.`date` DESC")
    return render_template("admin/complaint.html",data=res)

@app.route("/adm_complaint_post",methods=['post'])
def adm_complaint_post():
    reply=request.form['reply']
    db = Db()

    return 'ok'

@app.route("/adm_edit_category/<c_id>")
def adm_edit_category(c_id):
    db = Db()
    session["c_id"]=c_id
    qry="select*from category where category_id='"+c_id+"'"
    res=db.selectOne(qry)
    return render_template("admin/edit_category.html",data=res)

@app.route("/adm_update_category",methods=['post'])
def adm_update_category():
    edit_category=request.form["textfield"]
    id=session['c_id']
    qry="UPDATE category SET category_name='"+str(edit_category)+"' WHERE category_id='"+id+"'"
    db=Db()
    db.update(qry)
    return "<script>alert('updated succesfully');window.location='/view category'</script>"

@app.route("/adm_delete_category/<c_id>")
def adm_delete_category(c_id):
    db = Db()
    qry="DELETE FROM category WHERE category_id='"+str(c_id)+"'"
    db.delete(qry)
    return view_category()



@app.route("/adm_reply/<c_id>/")
def adm_reply(c_id):
    db = Db()
    session["c_id"]=c_id
    qry="SELECT * FROM complaint WHERE complaint_id='"+str(c_id)+"'"
    res=db.selectOne(qry)
    return render_template("admin/reply.html",data=res)

@app.route("/adm_reply_post",methods=['post'])
def adm_reply_post():
    reply=request.form['textfield2']
    db = Db()
    c_id=session["c_id"]
    qry="UPDATE complaint SET reply='"+reply+"',status='replied' WHERE complaint_id='"+str(session['c_id'])+"'"
    db.update(qry)
    return '''<script>alert("reply sent");window.location="/adm_complaint"</script>'''


@app.route("/adm_update_reply",methods=['post'])
def adm_update_reply():
    reply=request.form["textfield2"]
    return 'ok'

@app.route("/view category")
def view_category():
    db = Db()
    res = db.select("SELECT * from category")
    return render_template("admin/view category.html",data=res)


@app.route("/viewcategory_search",methods=['POST'])
def viewcategory_search():
    db = Db()

    s=request.form["search"]

    res = db.select("SELECT * from category where category_name like '%"+s+"%'")
    return render_template("admin/view category.html",data=res)







@app.route("/approve_or_reject_seller")
def view_seller_approval():
    db=Db()
    qry="SELECT*FROM seller INNER JOIN login WHERE seller.login_id=login.login_id AND  login.usertype='pending'"
    res=db.select(qry)
    return render_template("admin/view_seller_approval.html",data=res)

@app.route("/adm_reject_pending_seller/<id>")
def adm_reject_pending_seller(id):
    db = Db()
    qry="update login set usertype='rejected' WHERE login_id='"+str(id)+"'"
    db.update(qry)
    return view_seller_approval()

@app.route("/adm_approved_pending_seller/<id>")
def adm_approved_pending_seller(id):
    db = Db()
    qry="update login set usertype='seller' WHERE login_id='"+str(id)+"'"
    db.update(qry)
    return view_seller_approval()




@app.route("/view_approved_seller")
def view_approved_seller():
    db = Db()
    qry = "SELECT*FROM seller INNER JOIN login WHERE seller.login_id=login.login_id AND  login.usertype='seller'"
    res = db.select(qry)
    return render_template("admin/view_approved_seller.html",data=res)

@app.route("/adm_reject_seller",methods=['post'])
def adm_reject_seller():
    ids=request.form.getlist('ids')
    for id in ids:
        db = Db()
        qry="update login set usertype='rejected' WHERE login_id='"+str(id)+"'"
        db.update(qry)
    return view_approved_seller()


@app.route("/view_rejected_seller")
def view_rejected_seller():
    db = Db()
    qry = "SELECT*FROM seller INNER JOIN login WHERE seller.login_id=login.login_id AND  login.usertype='rejected'"
    res = db.select(qry)
    return render_template("admin/view_rejected_seller.html",data=res)

@app.route("/adm_approved_seller",methods=['post'])
def adm_approved_seller():
    ids=request.form.getlist('ids')
    for id in ids:
        db = Db()
        qry="update login set usertype='seller' WHERE login_id='"+str(id)+"'"
        db.update(qry)
    return view_rejected_seller()



@app.route("/approving_or_rejecting_seller")
def view_approving_or_rejected_seller():
    return render_template("admin/view_rejected_seller.html")
@app.route("/adm_view_seller_approval", methods=['post'])
def adm_view_seller_approval():
        return 'ok'



@app.route("/adm_index")
def adm_index():
    return render_template("admin/index.html")
# ------------seller-------------------



@app.route('/sellerhome')
def sellerhome():
    return render_template("seller/seller_home.html")

@app.route("/seller_delivery_boy_management")
def seller_delivery_boy_management():
    return render_template("seller/delivery boy management.html")
@app.route("/seller_delivery_boy_management_post",methods=['post'])
def seller_delivery_boy_management_post():
    deliveryboy=request.form['textfield']
    Email=request.form['textfield2']
    phno=request.form['textfield3']
    house=request.form['textfield4']
    city=request.form['textfield5']
    district = request.form['select']
    state = request.form['textfield6']
    post = request.form['textfield7']
    pincode = request.form['textfield8']
    image=request.files['fileField']
    image.save(static_path+"deliveryboy\\"+image.filename)
    path="/static/deliveryboy/"+image.filename
    password=random.randint(0000,9999)

    db=Db()
    loginid=db.insert("INSERT INTO `login`(`username`,`password`,`usertype`)VALUES('"+Email+"','"+str(password)+"','delivery_boy')")

    db.insert("INSERT INTO delivery_boy VALUES(null,'"+deliveryboy+"','"+Email+"','"+phno+"','"+house+"','"+city+"','"+district+"','"+state+"','"+post+"','"+pincode+"','"+path+"','"+str(loginid)+"','"+str(session["lid"])+"')")
    print("INSERT INTO delivery_boy VALUES(null,'"+deliveryboy+"','"+Email+"','"+phno+"','"+house+"','"+city+"','"+district+"','"+state+"','"+post+"','"+pincode+"','"+path+"')")
    # return seller_delivery_boy_management()
    return '''<script>alert("Delivery boy added succesfully");window.location="/seller_view_deliveryboy"</script>'''

@app.route("/seller_delete_deliveryboy",methods=['post'])
def seller_delete_deliveryboy():
    did = request.form.getlist("ids")

    print(did)
    for i in did:
        db = Db()
        qry = "DELETE FROM delivery_boy WHERE login_id='" + str(i) + "'"
        db.delete(qry)
    return seller_view_deliveryboy()


@app.route("/seller_view_order")
def seller_view_order():
    db = Db()
    sid=str(session['lid'])
    res = db.select("SELECT `customer`.`customer_name`,`customer`.`image`,`orders`.`date`,`orders`.`order_id`,`payment`.`amount` FROM orders INNER JOIN `customer` ON `orders`.`customer_l_id`=`customer`.`login_id` INNER JOIN `payment` ON `orders`.`order_id`=`payment`.`order_id` WHERE orders.seller_id='"+sid+"'")
    return render_template("seller/view_order.html",data=res)

@app.route("/seller_view_deliveryboy")
def seller_view_deliveryboy():
    db = Db()
    sid=str(session['lid'])
    res = db.select("SELECT *FROM `delivery_boy` WHERE seller_l_id='"+sid+"'")
    return render_template("seller/view_deliveryboy.html",data=res)





@app.route("/seller_view_item/<oid>")
def seller_view_item(oid):
    db=Db()
    res=db.select("SELECT `order_sub`.`order_id`,`order_sub`.`quantity`,`product`.`product_name`,`product`.`price` FROM product INNER JOIN `order_sub` ON `product`.`product_id`=`order_sub`.`product_id` WHERE `order_sub`.`order_id`='"+oid+"'")
    return render_template("seller/view_item.html",data=res)


@app.route("/seller_order_assign/<oid>")
def seller_order_assign(oid):
    session['oid']=oid
    db = Db()
    res = db.select("SELECT * FROM delivery_boy where seller_l_id='"+str(session['lid'])+"'")
    return render_template("seller/order assign.html",data=res)
@app.route("/seller_order_assign_post",methods=['post'])
def seller_order_assign_post():
    deliveryboy = request.form.get('select')
    oid=session['oid']
    db=Db()
    res=db.insert("INSERT INTO order_assign VALUES(NULL,'"+oid+"','"+deliveryboy+"','pending',CURDATE())")

    return seller_view_order()

@app.route("/seller_view_delivery_status/<oid>")
def seller_view_delivery_status(oid):
    session['oid'] = oid
    db = Db()
    qry="SELECT `order_assign`.*,`orders`.*,`delivery_boy`.* ,`order_assign`.`status` AS delstatus FROM `order_assign`,`orders`,`delivery_boy` WHERE `order_assign`.`order_id`='"+str(oid)+"' AND `order_assign`.`deliveryboy_l_id`=`delivery_boy`.`login_id`"
    res=db.selectOne(qry)
    return render_template('seller/view_delivery_status.html',data=res)

@app.route("/seller_view_review_rating")
def seller_view_review_rating():
    db=Db()
    qry="SELECT `raiting`.*,`customer`.* FROM `customer`,`raiting` WHERE `customer`.`login_id`=`raiting`.`customer_l_id`"
    res=db.select(qry)
    return  render_template("seller/view rating and review.html",data=res)



@app.route("/admin_viewraing")
def admin_viewraing():
    db=Db()
    qry="SELECT `raiting`.*,`customer`.* FROM `customer`,`raiting` WHERE `customer`.`login_id`=`raiting`.`customer_l_id`"
    res=db.select(qry)
    return  render_template("admin/ratings.html",data=res)




@app.route("/seller_Register")
def seller_register():
    return render_template("seller/registration.html")
@app.route("/seller_register_post",methods=['post'])
def seller_register_post():
    sellername=request.form['textfield']
    dob = request.form['textfield11']
    email=request.form['textfield2']
    phno=request.form['textfield3']
    store_name=request.form['textfield4']
    city = request.form['textfield5']
    district =request.form['textfield6']
    state=request.form['textfield7']
    longitude=request.form['textfielda']
    latitude= request.form['textfieldb']
    image = request.files['fileField']
    password = random.randint(0000, 9999)
    image.save("C:\\Users\\user\\PycharmProjects\\shopmee\\static\\seller\\"+image.filename)
    path="static/seller/"+image.filename

    db = Db()
    res = db.insert("INSERT INTO `login`(`username`,`password`,`usertype`)VALUES('" + email + "','" + str( password) + "','seller')")

    db.insert("INSERT INTO seller VALUES(null,'" + sellername + "','" + dob + "','" + email + "','" + phno + "','"+str(res)+"','"+ store_name +"','" + city + "','" + district + "','" + state + "','" + longitude + "','"+latitude+"','" + path + "')")
    return "<script>alert('Registration success');window.location='/'</script>"

@app.route("/seller_product_management")
def seller_product_mangement():
    db=Db()
    res=db.select("SELECT * FROM category")
    print(res)
    return render_template("seller/product_management.html",res=res)

@app.route("/view_product")
def view_product():
    db = Db()
    res = db.select("SELECT `product`.*,`category`.`category_id`,`category`.`category_name` FROM `category`,`product` WHERE `category`.`category_id`=`product`.`category_id`")
    return render_template("seller/view_product.html",data=res)

@app.route("/seller_edit_product/<c_id>")
def seller_edit_product(c_id):
    db = Db()
    session["c_id"]=c_id
    qry="SELECT`product`.*,`category`.* FROM product INNER JOIN `category` ON `category`.`category_id`=`product`.`category_id` WHERE `product`.product_id='"+c_id+"'"
    res=db.selectOne(qry)
    qry1="select * from `category`"
    res1=db.select(qry1)

    return render_template("seller/edit_product.html",data=res,data1=res1,pid=c_id)


@app.route("/seller_update_product", methods=['post'])
def seller_update_product():
    pid=request.form["pid"]
    catid = request.form["select"]
    product_name=request.form["textfield"]
    price=request.form["textfield2"]
    quantity=request.form["textfield3"]

    description=request.form["textarea"]

    if 'fileField' in request.files:
        image = request.files["fileField"]
        print("xx")

        if image.filename!='':
            print("xXx")
            image.save("C:\\Users\\user\\PycharmProjects\\shopmee\\static\\product\\"+image.filename)
            path="/static/product/"+image.filename

            qry = "UPDATE product SET product_name='" +product_name+ "',category_id='" +catid+ "',price='"+ price +"',quantity='"  +quantity+ "',description='" +description+ "',image='"+path+"' WHERE product_id='" + pid + "'"
            db = Db()
            db.update(qry)
            return "<script>alert('updated succesfully');window.location='/view_product'</script>"
        else:
            print("xbx")
            qry = "UPDATE product SET product_name='" + product_name + "',category_id='" + catid + "',price='" + price + "',quantity='" + quantity + "',description='" + description + "' WHERE product_id='" + pid + "'"
            db = Db()
            db.update(qry)
            return "<script>alert('updated succesfully');window.location='/view_product'</script>"
    else:
        print("xx1")
        qry = "UPDATE product SET product_name='" + product_name + "',category_id='" + catid + "',price='" + price + "',quantity='" + quantity + "',description='" + description + "' WHERE product_id='" + pid + "'"
        db = Db()
        db.update(qry)
        return "<script>alert('updated succesfully');window.location='/view_product'</script>"




@app.route("/seller_product_management_post",methods=['post'])
def seller_product_management_post():
    category=request.form['select']
    product = request.form['textfield']
    price = request.form['textfield2']
    quantity = request.form['textfield3']
    image=request.files['fileField']
    image.save(static_path+"product\\"+image.filename)
    path="/static/product/"+image.filename
    description = request.form['textarea']
    db = Db()
    db.insert("INSERT INTO `product`(`category_id`,`seller_id`,`product_name`,`price`,`quantity`,`image`,`description`) VALUES('"+category+"','"+str(session['lid'])+"','" + product + "','" + price + "','" + quantity + "','" + path + "','" + description + "')")

    return '''<script>alert("Product added successfully");window.location="/seller_product_management"</script>'''


@app.route("/seller_add_store1")
def seller_add_store1():
    return render_template("seller/add_store.html")








@app.route("/seller_add_store",methods=['post'])
def seller_add_store():
    storename=request.form['textfield']
    email = request.form['textfield2']
    phone = request.form['textfield3']
    place = request.form['textfield4']
    latitude = request.form['textfield5']
    longitude = request.form['textfield6']
    managername = request.form['textfield7']
    managerphone = request.form['textfield8']
    image=request.files['fileField']
    image.save(static_path+"store\\"+image.filename)
    path="/static/store/"+image.filename

    password=random.randint(10000000,99999999)

    db = Db()
    res=db.insert("INSERT INTO `login`(`username`,`password`,`usertype`)VALUES('" + email + "','" + str(password) + "','store')")
    db = Db()
    res1=db.insert("INSERT INTO store(store_name,email_id,phone,place,latitude,longitude,manager_name,manager_phone,manager_image,login_id,seller_lid)values('"+storename+"','"+email+"','"+phone+"','"+place+"','"+latitude+"','"+longitude+"','"+managername+"','"+managerphone+"','"+path+"','"+str(res)+"','"+str(session['lid'])+"')")
    return render_template("seller/add_store.html")



@app.route("/seller_view_store")
def seller_view_store():
    db=Db()

    # q="SELECT `store`.*,SQRT(POW(69.1 * (`store_latitude` -'"+lati+"'),2) +POW(69.1 *('"+logi+"' - `store_longitude`) * COS(`store_latitude`/57.3),2)) AS distance FROM `store` ORDER BY distance"
    res = db.select("SELECT * from store")
    return render_template("seller/store.html", data=res)


@app.route("/seller_edit_store/<nn>")
def seller_edit_store(nn):
    session['sid'] = nn
    db=Db()

    r = db.selectOne("SELECT * FROM store WHERE login_id='" +nn+ "'")
    return render_template("seller/edit_store.html",data=r)




@app.route("/seller_edit_store_post",methods=['post'])
def seller_edit_store_post():
    sid=session['sid']
    storename=request.form['textfield']
    email=request.form['textfield2']
    phn=request.form['textfield3']
    place=request.form['textfield4']
    latitude= request.form['textfield5']
    longitude=request.form['textfield6']
    mngrname=request.form['textfield7']
    mngrphn=request.form['textfield8']

    if 'fileField' not in request.files:
        db=Db()
        qry="UPDATE `store` SET `email_id`='"+email+"',`store_name`='"+storename+"',`phone`='"+phn+"',`place`='"+place+"',`latitude`='"+latitude+"',`longitude`='"+longitude+"',`manager_name`='"+mngrname+"',`manager_phone`='"+mngrphn+"' WHERE `login_id`='"+str(sid)+"'"
        db.update(qry)
    else:
        image = request.files['fileField']
        if image.filename=='':
            db = Db()
            qry = "UPDATE `store` SET `email_id`='" + email + "',`store_name`='" + storename + "',`phone`='" + phn + "',`place`='" + place + "',`latitude`='" + latitude + "',`longitude`='" + longitude + "',`manager_name`='" + mngrname + "',`manager_phone`='" + mngrphn + "' WHERE `login_id`='" + str(sid) + "'"
            db.update(qry)
        else:
            image.save("C:\\Users\\User1\\Desktop\\shopmee\\static\\seller\\" + image.filename)
            path = "/static/seller/" + image.filename
            db = Db()
            qry = "UPDATE `store` SET `email_id`='" + email + "',`store_name`='" + storename + "',`phone`='" + phn + "',`place`='" + place + "',`latitude`='" + latitude + "',`longitude`='" + longitude + "',`manager_name`='" + mngrname + "',`manager_phone`='" + mngrphn + "',manager_image='"+path+"' WHERE `login_id`='" + str(sid) + "'"
            db.update(qry)
        return "<script>alert('Edited successfully');window.location='/seller_view_store'</script>"


@app.route("/seller_delete_store/<c_id>")
def seller_delete_store(c_id):
    db = Db()
    qry="DELETE FROM store WHERE store_id='"+str(c_id)+"'"
    db.delete(qry)
    return seller_view_store()


@app.route("/seller_view_profile")
def seller_view_profile():
    db=Db()
    r=db.selectOne("SELECT * FROM seller WHERE login_id='"+str(session['lid'])+"'")
    return render_template("seller/view_profile.html", data=r)

@app.route("/seller_edit_profile")
def seller_edit_profile():
    db=Db()
    r = db.selectOne("SELECT * FROM seller WHERE login_id='" + str(session['lid']) + "'")
    return render_template("seller/editprofile.html",data=r)
@app.route("/seller_edit_profiles_post",methods=['post'])
def seller_edit_profiles_post():
    sellername=request.form['textfield']
    dob = request.form['textfield11']
    email=request.form['textfield2']
    phno=request.form['textfield3']
    store_name=request.form['textfield4']
    city = request.form['textfield5']
    district =request.form['textfield6']
    state=request.form['textfield7']
    longitude=request.form['textfielda']
    latitude= request.form['textfieldb']
    image = request.files['fileField']
    password = random.randint(0000, 9999)
    image.save("C:\\Users\\user\\PycharmProjects\\shopmee\\static\\seller\\"+image.filename)
    path="static/seller/"+image.filename

    db = Db()
    res = db.insert("INSERT INTO `login`(`username`,`password`,`usertype`)VALUES('" + email + "','" + str( password) + "','seller')")

    db.insert("INSERT INTO seller VALUES(null,'" + sellername + "','" + dob + "','" + email + "','" + phno + "','"+str(res)+"','"+ store_name +"','" + city + "','" + district + "','" + state + "','" + longitude + "','"+latitude+"','" + path + "')")
    return "<script>alert('Registration success');window.location='/'</script>"

################################android
@app.route("/amd_login",methods=['post'])
def amd_login():
    username=request.form['username']
    password=request.form['pass']
    qry="SELECT * FROM login WHERE username='"+username+"' and PASSWORD='"+password+"'"
    db=Db()
    res=db.selectOne(qry)


    if res is not None:
        return jsonify(status="ok",type=res['usertype'],id=res['login_id'])
    else:
        return jsonify(status="no")

@app.route("/and_registration", methods=['post'])
def amd_registration():
    print("haiii")
    customer_name = request.form['customer_name']
    email_id = request.form['email_id']
    ph_no = request.form['ph_no']
    house_name = request.form['house_name']
    city = request.form['city']
    district = request.form['district']
    state = request.form['state']
    latitude=request.form['lattitude']
    print(latitude)
    longitude=request.form['longitude']
    post = request.form['post']
    pincode = request.form['pincode']
    image = request.files['pic']
    image.save(static_path + "customer\\" + image.filename)
    path = "/static/customer/" + image.filename
    password = request.form['pass']
    print(password)
    gender=request.form['gender']
    date_of_birth = request.form['date_of_birth']
    print("kk="+date_of_birth)
    qry1="INSERT INTO login(username,password,usertype)values('"+email_id+"','"+password+"','user')"
    db=Db()
    lid=db.insert(qry1)


    qry="INSERT INTO  customer(customer_name,email_id,gender,date_of_birth,ph_no,house_name,city,district,state,latitude,longitude,post,pincode,image,login_id)values('"+customer_name+"','"+email_id+"','"+gender+"','"+date_of_birth+"','"+ph_no+"','"+house_name+"','"+city+"','"+district+"','"+state+"','"+latitude+"','"+longitude+"','"+post+"','"+pincode+"','"+path+"','"+str(lid)+"')"
    db.insert(qry)
    return jsonify(status="ok")

@app.route("/viewnearbyseller", methods=['post'])
def viewnearbyseller():
    lati=request.form['lati']
    logi = request.form['logi']
    qry="SELECT `seller`.*,SQRT(POW(69.1 * (`latitude` -'"+lati+"'),2) +POW(69.1 *('"+logi+"' - `longitude`) * COS(`latitude`/57.3),2)) AS distance FROM seller ORDER BY distance"
    db=Db()
    res = db.select(qry)
    print(res)
    return jsonify(status="ok",data=res)

@app.route("/vproductsofeachseller", methods=['post'])
def vproductsofeachseller():
    lid=request.form['lid']
    print(lid)
    qry="SELECT product.*,`category`.category_name FROM product,category WHERE product.category_id=category.category_id and product.seller_id='"+lid+"' order by pos DESC,neu DESC,neg ASC"
    db=Db()
    res = db.select(qry)
    print(res)
    return jsonify(status="ok",data=res)

@app.route("/addtocart", methods=['post'])
def addtocart():
    customer_l_id = request.form['customer_l_id']
    product_id = request.form['product_id']
    quantity = request.form['quantity']
    seller_id=request.form["sellerlid"]
    qry="INSERT INTO cart(customer_l_id,product_id,quantity,sellerlid)VALUES('"+customer_l_id+"','"+product_id+"','"+quantity+"','"+seller_id+"')"
    db=Db()
    res = db.insert(qry)
    return jsonify(status="ok")




@app.route("/deletefromcart", methods=['post'])
def deletefromcart():
    cart_id = request.form['cart_id']
    qry="delete from cart where cart_id='"+cart_id+"'"
    db=Db()
    res=db.delete(qry)
    return jsonify(status="ok")



@app.route("/payment", methods=['post'])
def payment():
    order_id = request.form['order_id']
    date = request.form['date']
    amount = request.form['amount']
    qry1="INSERT INTO payment(order_id,`date`,amount)VALUES('"+order_id+"',curdate(),'"+amount+"')"
    db=Db()
    res = db.insert(qry1)
    return \
        jsonify(status="ok")


@app.route("/deliveryboy_viewprofile", methods=['post'])
def deliveryboy_viewprofile():
    lid=request.form['lid']
    qry="SELECT * FROM delivery_boy where login_id='"+lid+"'"
    db=Db()
    res = db.selectOne(qry)
    return jsonify(status="ok",name=res["deliveryboy_name"],email_id=res["email_id"],ph_no=res["ph_no"],house_name=res["house_name"],city=res["city"],district=res["district"],state=res["state"],post=res["post"],pincode=res["pincode"],image=res["image"])

@app.route("/and_changepassword", methods=['post'])
def and_changepassword():
    print("hlwwww")
    lid=request.form['lid']
    print("qqq")
    current_password = request.form['currentpassword']
    new_password = request.form['newpassword']
    qry = "SELECT * FROM login WHERE login_id='"+lid+"'and password='" + current_password + "'"
    db = Db()
    res = db.selectOne(qry)
    if res is not None:
        qry="UPDATE login SET password='"+new_password+"' WHERE login_id='"+lid+"'"
        db = Db()
        res = db.update(qry)
        return jsonify(status="ok")
    else:
        return jsonify(status="no")

@app.route("/dbvao", methods=['post'])
def deliveryboy_viewallocatedorders():
    lid = request.form['lid']
    qry="SELECT `customer`.*,`orders`.*,`order_assign`.* FROM orders INNER JOIN `customer` ON `orders`.`customer_l_id`=`customer`.login_id INNER JOIN `order_assign` ON `orders`.`order_id`=`order_assign`.`order_id` WHERE `order_assign`.`deliveryboy_l_id`='"+lid+"' AND order_assign.`status`='pending'"
    db = Db()
    res=db.select(qry)
    return jsonify(status="ok",data=res)

@app.route("/update_status", methods=['post'])
def update_status():
    print("hii")
    oid = request.form['orderid']
    print(oid)
    status=request.form['status']
    print(status)
    qry="UPDATE `orders` SET `status`='"+status+"' WHERE order_id='"+oid+"'"
    db = Db()
    res = db.update(qry)
    return jsonify(status="ok", data=res)

@app.route("/and_reviews", methods=['post'])
def send_ratingandreview():
    re=request.form["review"]
    uid=request.form["uid"]
    pid=request.form["pid"]
    db=Db()
    qry="INSERT INTO `productratings` (`pid`,`review`,`uid`,`date`) VALUES('"+pid+"','"+re+"','"+uid+"',CURDATE())"
    db.insert(qry)
    
    print("ok")
    
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    
    
    analyser = SentimentIntensityAnalyzer()
    
    
    sent=re

    score = analyser.polarity_scores(sent)
    print(score['neu'],score['pos'],score['neg'])

    if score['neg'] > score['pos'] and score['neg'] > score['neu']:
        print("its negative")
        qry="UPDATE `product` SET neg=neg+1 WHERE `product_id`='"+pid+"'"
        db.update(qry)
    elif score['pos'] > score['neg'] and  score['pos'] > score['neu']:
        print("its positive")
        qry="UPDATE `product` SET pos=pos+1 WHERE `product_id`='"+pid+"'"
        db.update(qry)
    else:
        qry="UPDATE `product` SET neu=neu+1 WHERE `product_id`='"+pid+"'"
        db.update(qry)
        print("its neutral")

    return jsonify(status="ok")

@app.route("/send_complaint", methods=['post'])
def send_complaint():
    print("hhh")
    complaint = request.form['complaint']
    lid= request.form['lid']
    qry="INSERT INTO complaint (`customer_l_id`,`date`,`complaint`,`status`) VALUES ('"+lid+"',CURDATE(),'"+complaint+"','pending')"
    print(qry)
    db = Db()
    res = db.insert(qry)
    return jsonify(status="ok", data=res)

@app.route("/viewreply", methods=['post'])
def viewreply():
    lid=request.form['lid']
    print(lid)
    qry="SELECT `complaint`,`reply`,`date`FROM `complaint` WHERE `customer_l_id`='"+lid+"'"
    db=Db()
    res = db.select(qry)
    print(res)
    return jsonify(status="ok",data=res)



@app.route("/viewpreviousorder", methods=['post'])
def viewpreviousorder():
    lid = request.form['lid']
    qry="SELECT `order_sub`.*,orders.`customer_l_id`,orders.`date`,`orders`.`seller_id`,`seller`.`seller_name`,`seller`.`seller_id`,`product`.`product_id`,`product`.`product_name`, `product`.`image` FROM `order_sub`,product,orders,`seller` WHERE `order_sub`.`order_id`=`orders`.`order_id` AND `order_sub`.`product_id`=`product`.`product_id` AND `orders`.`seller_id`=`seller`.`login_id` AND `orders`.`customer_l_id`='"+lid+"'"
    print(qry)
    db=Db()
    res=db.select(qry)
    # print(res)
    return jsonify(status="ok", data=res)



@app.route("/viewcart", methods=['post'])
def viewcart():
    lid=request.form['lid']
    sellerid=request.form["sellerid"]
    qry = "select cart.*,product.product_id,product.product_name,product.image,product.price from cart,product where cart.product_id=product.product_id and `cart`.`customer_l_id`='"+lid+"' and `cart`.`sellerlid`='"+sellerid+"'"
    db=Db()
    res=db.select(qry)
    print(res)
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

    qry="SELECT * FROM bank WHERE bank_name = '"+bank_name+"'and account_number= '"+accno+"'and pin_number='"+password+"'"
    ress=db.selectOne(qry)
    if ress is None:
        return jsonify(status="no")
    else:
        qry=" SELECT * FROM cart WHERE `customer_l_id`='"+lid+"' and sellerlid='"+selerid+"'"
        res=db.select(qry)
        tot=0
        for i in res:
            pid=i["product_id"]
            qty=i["quantity"]
            qry1="SELECT price FROM `product` WHERE `product_id`='"+str(pid)+"'"
            res1=db.selectOne(qry1)
            pr=res1['price']
            tot+=float(pr)*float(qty)
            print(tot)

        if  float(ress['balance']) > tot:
            qry="INSERT INTO `orders` (`customer_l_id`,`status`,`date`,`total`,seller_id) VALUES('"+str(lid)+"','pending',CURDATE(),'"+str(tot)+"','"+str(selerid)+"')"
            orderid=db.insert(qry)

            for i in res:
                pid = i["product_id"]
                qty = i["quantity"]
                qry="INSERT INTO `order_sub` (`order_id`,`product_id`,`quantity`,seller_id) VALUES ('"+str(orderid)+"','"+str(pid)+"','"+str(qty)+"','"+str(selerid)+"')"
                db.insert(qry)

            db.delete("DELETE FROM `cart` WHERE customer_l_id='"+str(lid)+"' and sellerlid='"+selerid+"'")

            qry="INSERT INTO `payment` (`order_id`,`date`,`amount`) VALUES ('"+str(orderid)+"',CURDATE(),'"+str(tot)+"')"
            db.insert(qry)
        return jsonify(status="ok") 

@app.route("/buy_products", methods=['post'])
def buy_products():
    db=Db()
    print("hi")
    bank_name = request.form['bank_name']
    print("hoi")
    accno = request.form['account_no']
    password = request.form['pass']
    selerid = request.form['selerid']
    lid=request.form['lid']

    pid=request.form["pid"]
    price=request.form["price"]
    qty=request.form["qty"]

    qry="SELECT * FROM bank WHERE bank_name = '"+bank_name+"'and account_number= '"+accno+"'and pin_number='"+password+"'"
    ress=db.selectOne(qry)
    if ress is None:
        return jsonify(status="no")
    else:
        qry=" SELECT * FROM cart WHERE `customer_l_id`='"+lid+"' and sellerlid='"+selerid+"'"
        res=db.select(qry)
        tot=0
        tot=float(price)*float(qty)
        print(tot)

        if  float(ress['balance']) > tot:
            qry="INSERT INTO `orders` (`customer_l_id`,`status`,`date`,`total`,seller_id) VALUES('"+str(lid)+"','pending',CURDATE(),'"+str(tot)+"','"+str(selerid)+"')"
            orderid=db.insert(qry)

            qry="INSERT INTO `order_sub` (`order_id`,`product_id`,`quantity`,seller_id) VALUES ('"+str(orderid)+"','"+str(pid)+"','"+str(qty)+"','"+str(selerid)+"')"
            db.insert(qry)

            qry="INSERT INTO `payment` (`order_id`,`date`,`amount`) VALUES ('"+str(orderid)+"',CURDATE(),'"+str(tot)+"')"
            db.insert(qry)
        return jsonify(status="ok")






    # return jsonify(status="ok",total_amount=total)


@app.route("/customer_viewprofile", methods=['post'])
def customer_viewprofile():
    lid=request.form['lid']
    qry="SELECT * FROM customer where login_id='"+lid+"'"
    db=Db()
    res = db.selectOne(qry)
    print(res)
    return jsonify(status="ok",name=res["customer_name"],email_id=res["email_id"],date_of_birth=str(res["date_of_birth"]),gender=res["gender"],ph_no=res["ph_no"],house_name=res["house_name"],city=res["city"],district=res["district"],state=res["state"],post=res["post"],pincode=res["pincode"],image=res["image"])

@app.route("/viewallocatedorders", methods=['post'])
def viewallocatedorders():
    lid=request.form['lid']
    orderid=request.form['order_id']
    qry = "SELECT `orders`.*,`order_assign`.*,`product`.* FROM `product`,`order_assign`,`orders` WHERE `order_assign`.`order_id`=`orders`.`order_id` AND `order_assign`.`deliveryboy_l_id`='"+lid+"' AND `orders`.`order_id`='"+orderid+"'"
    print(qry)
    db=Db()
    res=db.select(qry)
    print(res)
    return jsonify(status="ok",data=res)

@app.route("/viewproductcust",methods=['POST'])
def viewproductcust():
    db=Db()
    res = db.select("SELECT `product`.*,`category`.`category_id`,`category`.`category_name` FROM `category`,`product` WHERE `category`.`category_id`=`product`.`category_id` order by pos DESC, neu DESC,neg ASC")
    print(res)
    return jsonify(status="ok", data=res)


@app.route("/bysearch",methods=['POST'])
def bysearch():
    db=Db()
    name=request.form['name']
    res = db.select("SELECT `product`.*,`category`.`category_id`,`category`.`category_name` FROM `category`,`product` WHERE `category`.`category_id`=`product`.`category_id`AND `product`.`product_name` LIKE '%"+name+"%'")
    print(res)
    return jsonify(status="ok", data=res)


@app.route("/andreview",methods=['post'])
def andddreview():

    re=request.form["review"]
    uid=request.form["uid"]
    pid=request.form["pid"]
    db=Db()
    qry="INSERT INTO `productratings` (`pid`,`review`,`uid`,`date`) VALUES('"+pid+"','"+re+"','"+uid+"',CURDATE())"
    db.insert(qry)

    return jsonify(status='ok')


@app.route('/storehome')
def storehome():
    return render_template('/store/home.html')


@app.route('/storeviewprofile')
def storeviewprofile():
    db=Db()
    qry="SELECT *FROM `store` WHERE `login_id`='"+str(session['lid'])+"'"
    res=db.selectOne(qry)
    print(res)
    return render_template('store/viewprofile.html',data=res)

@app.route('/storeviewproducts')
def storeviewproducts():
    db=Db()
    qry="SELECT product.*,category.* FROM product,category WHERE `product`.`category_id`=`category`.`category_id` AND `product`.`seller_id` IN (SELECT `seller_lid` FROM `store` WHERE `login_id`='"+str(session['lid'])+"')"
    res=db.select(qry)

    return render_template('store/view_product.html',data=res)

@app.route('/storeadddamageditem')
def storeadddamageditem():
    db=Db()
    qry="SELECT * FROM product WHERE `seller_id` IN (SELECT `seller_lid` FROM `store` WHERE `login_id`='"+str(session['lid'])+"')"
    res=db.select(qry)

    return render_template('store/reportdamagepoducts.html',res=res)

@app.route('/storedamageditempost',methods=['post'])
def dentry():
    db=Db()
    pid=request.form["pid"]
    qty=request.form['qty']
    lid=str(session['lid'])
    qry="INSERT INTO `damageditems` (`pid`,`qty`,`store_id`) VALUES('"+pid+"','"+qty+"','"+lid+"')"
    db.insert(qry)
    return "<script>alert('Damaged item saved');window.location='/storeadddamageditem'</script>"
@app.route('/storeviewdamageditems')
def storeviewdamageditems():
    db=Db()
    qry="SELECT `damageditems`.*,`product`.`product_id`,`product`.`product_name`,`product`.`price` FROM `damageditems`,`product` WHERE `product`.`product_id`=`damageditems`.`pid` AND `damageditems`.`store_id`='"+str(session['lid'])+"'"
    res=db.select(qry)

    return render_template('store/viewdamageditems.html',res=res)


@app.route('/storerequestproduct')
def storerequestproduct():
    db=Db()
    qry="SELECT * FROM product WHERE `seller_id` IN (SELECT `seller_lid` FROM `store` WHERE `login_id`='"+str(session['lid'])+"')"
    res=db.select(qry)

    return render_template('store/sentproductrequesttoseller.html',data=res)

@app.route('/storerequestproductpost',methods=['post'])
def storerequestproductpost():
    db=Db()
    pid=request.form["pid"]
    qty=request.form['qty']
    lid=str(session['lid'])
    qry="INSERT INTO `productreq` (`pid`,`qty`,`lid`,datetime) VALUES ('"+pid+"','"+qty+"','"+str(lid)+"',curdate())"
    db.insert(qry)
    return "<script>alert('Product request sent successfully');window.location='/storerequestproduct'</script>"



@app.route('/storeviewsentrequests')
def storeviewsentrequests():
    db=Db()
    qry="SELECT `productreq`.*,`product`.`product_id`,`product`.`product_name` FROM `product`,`productreq` WHERE `product`.`product_id`=`productreq`.`pid` AND`productreq`.`lid`='"+str(session['lid'])+"'"
    res=db.select(qry)
    return render_template('store/view_product_request.html',res=res)



@app.route('/and_reviewsadd',methods=['post'])
def and_reviewsadd():
    rating=request.form["rating"]
    uid=request.form["uid"]
    review=request.form["review"]
    db=Db()
    qry="INSERT INTO `raiting` (`customer_l_id`,`date`,`rating`,`review`) VALUES ('"+uid+"',CURDATE(),'"+rating+"','"+review+"')"
    print(qry)
    db.insert(qry)

    return jsonify(status='ok')










if __name__ == '__main__':
    app.run(debug=True,port=5005,host="0.0.0.0")
