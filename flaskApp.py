from flask import Flask, render_template, escape, make_response, redirect,session, request,jsonify,json, flash,url_for
from flask import redirect,url_for,session,render_template,request,flash,make_response
from flask import jsonify,redirect,url_for,session,render_template,request,flash,make_response
from sendemail.mailer import Mail
from RegisterForm.RegisterForm import RegForm as Form
from loginFrom.LoginForm import LoginForm as LogForm
from models.requests.Request import  Request
from werkzeug.datastructures import  FileStorage
from werkzeug.utils import secure_filename
from models.user.User import Users
from models.user.restp import Restp
from models import constants as userconstants
from models.System_file import File_system
from models.comments.comment import Comments
from models.flask_wtf.register import RegisterForm
from models.flask_wtf.login import LoginForm
from models.flask_wtf.blogform import BlogForm
from models.flask_wtf.editeform import EditeForm
from models.flask_wtf.commentform import CommentForm
from common.Utils import utils
from models.blog.blogs import Blogs
from common.database import Database
from models.user import error as UserErrors
from bson.objectid import ObjectId
from models.activate.active_account import activate_account
from hashlib import md5
import os
import re
import uuid
import datetime

app = Flask(__name__)
UPLOAD_FOLDER = os.path.basename('static') + "/uploads"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)

#intializing the  Database
@app.before_first_request
def initialize_database():
    Database.initialize()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html')

@app.route('/')
def route():
    return redirect(url_for('desk'))
    
@app.route('/admin_login')
def admin_login():
    return  render_template('admin.html')
    
app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];
    return json.dumps({'status':'OK','user':user,'pass':password});

@app.route('/blogs/current_user/<string:email>/<string:_id>')
def allblog(email,_id):
    if utils.email_is_valid(email) ==  True and 'user' in session and session['login_email'] == email:
        ids = Users.id_one_user(_id)['_id']
        blog_id =  Users.get_by_email(email)['_id']
        dataemail = Users.bgemail_one(request.cookies.get('login_email'))
        dataemail = Users.get_by_email(session['user'])['email']
        if email ==  dataemail:
            return redirect(url_for('memebership',email=dataemail,_id=_id))
        else:
            flash("not good")
            render_template('page_not_found.html')

    return render_template('page_not_found.html')

@app.route('/memebers/<string:email>/<string:_id>')
def memebership(email,_id):
    loginform = LoginForm()
    cookie_email = request.cookies.get('email')
    blogs = Database.find("blogs",{"email": { "$nin":[cookie_email]} })
    if 'user' in session and  cookie_email == email:
        return render_template("maini.html", blogs=blogs)
    else:
        return render_template("login.html" , loginform=loginform)

@app.route('/likes' , methods=['POST', 'GET'])
def likes():
    loginform = LoginForm()
    title = request.get_json()['title']
    email = request.get_json()['email']
    _id =   request.get_json()['_id']
    
    current_clikes =   request.get_json()['current_num']
    print(title)
    print(email)
    print(_id)
    print(current_clikes)
    if  request.method == "POST":
        if utils.email_is_valid(email) == True and  Users.likes("blogs",_id, title)["likes"] < int(current_clikes):
            likes = Users.likes("blogs",_id, title)["likes"]
            thuplikes(current_clikes,_id, title)
            return render_template("error.html")
        else:
            return redirect(url_for('login_route'))
    return redirect(url_for('login_route'))

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    
    _id =   request.get_json()['_id']
    blogs = Users.get_id(int(_id))
    print(_id)
    print(blogs)
    
    if int(_id)  == blogs:
        Users.delete(int(_id))
        print("blog deleted")
        return redirect(url_for('login_route'))
            
        
    return redirect(url_for('login_route'))

# dislike route function
@app.route('/dislikes' , methods=['POST', 'GET'])
def dislikes():
    loginform = LoginForm()
    title = request.get_json()['title']
    email = request.get_json()['email']
    _id =   request.get_json()['_id']
    
    current_clikes =   request.get_json()['current_num']
    print(title)
    print(email)
    print(_id)
    print(current_clikes)
    if  request.method == "POST":
        if utils.email_is_valid(email) == True and Users.dislikes("blogs",_id,  title)['dislikes'] < int(current_clikes):
            likes = Users.dislikes("blogs", _id, title)["dislikes"]
            thupdislikes(current_clikes,_id, title)
            return render_template("error.html")
        else:
            return redirect(url_for('login_route'))
    return redirect(url_for('login_route'))
# dislike function
def thupdislikes(dislikes=None,blog_id=None, title=None):
        if dislikes is not None  and  title is  not None:
            Database.updates("blogs",{"title":title},{"$set": {"dislikes":dislikes}})
#likes function
def thuplikes(likes=None,blog_id=None, title=None):
        if likes is not None:
            Database.updates("blogs",{"title":title},{"$set": {"likes":likes}})
               
def check_likes(user,blogtitle):
        data = Database.find_one(user,{"title":blogtitle})
        if data['title'] == blogtitle:
            return data['likes']
            
def insert_likes(email,number, title):
        Database.updates("blogs",{"title":title},{"$addToSet": {"likes":number}})

@app.route('/thumbdown/<string:blogtitle>/<string:email>/<string:blog_id>')
def thumbdown(email,blogtitle,blog_id):
    loginform = LoginForm()
    if  'user' in session and blog_id.__len__() ==  32:
        ids = Users.id_one(blog_id)['_id']
        if utils.email_is_valid(email) == True and blog_id == ids:
            dislikes = Users.querytitlei(blogtitle)['dislikes']
            thdow(int(dislikes),blogtitle,blog_id)
            return render_template("dislikes.html")
        else:
            return redirect(url_for('login'))
    return redirect(url_for('login'))

def thdow(dislikes,blogtitle,blog_id):
    check_email = session['user']
    user = "user"
    user_dislikes = check_dislikes(user,check_email,blogtitle,blog_id)
    if user_dislikes !=  blogtitle:
        dislikes = dislikes + 1
        insert_dislikes(session['user'],blogtitle)
        Database.updates("blogs",{"_id":blog_id},{"$set": {"dislikes":dislikes}})
    else:
        return False

def check_dislikes(user,check_email,blogtitle,blog_id):
        data = Database.find_one(user,{"email":check_email})
        for items in data['dislikes']:
            return items
def insert_dislikes(email,titleblog):
        Database.updates("user",{"email":email},{"$addToSet": {"dislikes":titleblog}})

@app.route('/create/blog')
def create_blog():
    message = "You  are not a valiable user"
    if request.cookies.get('login_email') is not None:
           return render_template('blogform.html')
    else:
        return redirect(url_for('login_route',message=message))
        
@app.route('/user/blogs')
def userBlogs():
    message = "You  are not a logined user  please login"
    if request.cookies.get('login_email') is  not None:
        return redirect(url_for('asset'))
    return redirect(url_for('login_route', message=message))
    
    
@app.route('/blogs')
def asset():
    if  request.cookies.get('login_email') is not None:
        email  = request.cookies.get('login_email')
        data =  Database.find_one(userconstants.COLLECTION, {'email':email})
        blogs  = Database.find("blogs", {'email':email})
        return render_template('userblog.html', author=data['firstname'], lastname=data['lastname'], email=request.form['email'], blogs=blogs,  date = datetime.datetime.utcnow())

@app.route('/open/<string:email>/<string:blogtitle>/<string:blog_id>')
def open(email,blogtitle,blog_id):
        if utils.email_is_valid(email) == True and blog_id.__len__() ==  32:
            item = Users.bytitle_one(blogtitle)
            ids = Users.id_one(blog_id)["_id"]
            if  session['user'] == email and ids == blog_id:
                items =  Users.bytitle(blogtitle)
                return render_template('blogopen.html',items=items)
            else:
                flash("there is a problem contact Admin")
                return redirect(url_for('login'))
        flash("there is a problem please contact admin")
        return redirect(url_for('login'))
@app.route('/edite/blog/<string:email>/<string:titleblog>/<string:blog_id>')
def edite(email,titleblog,blog_id):
    properties = []
    editeform = EditeForm()
    loginform = LoginForm()

    if 'user' in session and session['user'] == email and blog_id and utils.email_is_valid(email) == True and blog_id.__len__() ==  32:
        data_id =       Users.get_by_email(email)["_id"]
        content = Users.bytitle(titleblog)
        for stuffs in content:
            ids = Users.id_one(blog_id)["_id"]
            if session['user'] == email and blog_id ==  ids:
                editeform.description.data = stuffs['content']
                return render_template('edite.html',editeform=editeform,email=email,blogtitle=titleblog,blog_id=blog_id)
            else:
                flash("checking problem")
                return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/editeprocess/<string:email>/<string:blogtitle>/<string:blog_id>', methods=('POST', 'GET'))
def editeprocess(email,blogtitle,blog_id):
    editeform = EditeForm()
    loginform = LoginForm()
    database_email = Users.get_by_email(email)["email"]
    if editeform.validate_on_submit() == True and 'user' in session and session['user'] == email and blog_id.__len__() ==  32:
        thins = Users.bytitle(blogtitle)
        ids = Users.id_one(blog_id)["_id"]
        for stuff in thins:
            if stuff['titleblog'] == blogtitle and stuff['email'] == session["user"] and blog_id == ids:
                description = editeform.description.data
                Database.updates("blogs",{"content":stuff['content']},{"$set": {"content":description}})
                return render_template('editemessage.html')
            else:
                redirect(url_for('login'))
    flash("these are technical errors please try login again")
    return render_template('login.html',loginform=loginform)


@app.route('/comment/<string:blogtitle>/<string:email>/<string:blog_id>')
def commentUser(blogtitle,email,blog_id):
    commentform = CommentForm()
    if utils.email_is_valid(email) == True and 'user' in session and blog_id.__len__() ==  32:
        ids = Users.id_one(blog_id)["_id"]
        if email and blog_id ==  ids:
            commentform.title.data = blogtitle
            return render_template('comment.html',commentform=commentform)
        else:
            flash("check problem")
            return redirect(url_for('login'))
    flash('there is a problem with you information')
    return redirect(url_for('login'))

# comment rout
@app.route('/commentdetails/<string:email>/<string:blogtitle>/<string:blog_id>')
def commentdetails(blogtitle,email,blog_id):
    if blog_id.__len__() ==  32:
        ids = Users.id_one(blog_id)['_id']
        if blog_id == ids and ids != False:
            item = Users.bytitle_one(blogtitle)
            totalcomment = Users.allcomments(blogtitle)
            blogs =  Users.bytitle(blogtitle)
            return render_template('totalcomment.html',totalcomment=totalcomment,blogs=blogs)
        else:
            flash(" big problem ")
            return redirect(url_for('login'))
    flash("big problem man")
    return redirect(url_for('login'))

#comment been process and store in the database
@app.route('/commente', methods=['POST', 'GET'])
def commente():   
        login = request.cookies.get('login_email')
        if  request.method  == 'POST' and login is not None:
            
            #blog detils
            titleBlog = request.get_json()['title']
            email = request.get_json()['email']
            comment = request.get_json()['comment']
            _id = request.get_json()['_id']
            
            # #who commenting
            # login_name = request.get_json()['name']
            # login_email = request.get_json()['mail']
            # login_id = request.get_json()['id']

            print(titleBlog)
            
            if Users.blogExists(titleBlog):
                comment = Comments(titleBlog=titleBlog,comment=comment, email=email, _id=_id)
                comment.save_to_mongo()
                return redirect(url_for('welcome'))
        return redirect(url_for('login'))

def number_title(comment,titleblog):
        comment = comment + 1
        Database.updates("blogs",{"titleblog":titleblog},{"$inc": {"comment":1}})

# this rout display blogs
@app.route('/allcomments/<string:titleblog>')
def details(titleblog):
    if titleblog ==  request.cookies.get('title') and 'user' in session:
        title = request.cookies.get('title')
        totalcomment = Users.allcomments(title)
        comment = Users.querytitlei(title)['comment']
        blogs =  Users.bytitle(title)
        number_title(comment,title)
        return render_template('totalcomment.html', totalcomment=totalcomment,blogs=blogs)
    return redirect(url_for('login'))


@app.route('/allcommentsofuser')
def detailsu(title):
    if 'user' in session and session['user'] == request.cookies.get('email'):
           totalcomment = Users.allcomments(title)
           blogs =  Users.bytitle(title)
           return render_template('totalcomment.html', totalcomment=totalcomment,blogs=blogs)
    else:
        redirect(url_for('login'))
#image upload
@app.route('/upload/successfull',methods=['POST'])
def upload():
        path = os.getcwd()
        if request.method == 'GET':
            filename = request.files['file']
            if filename is not None:
                filename.save(path +secure_filename(filename.filename))
#blog creation rout
@app.route('/blogform')
def Blogform():
        num  = 0;
        blogform = BlogForm(request.cookies.get("login_author") ,None, request.cookies.get('login_email'), request.cookies.get('login_id'),None,None, None)
        if utils.email_is_valid(request.cookies.get('login_email')):
            if request.cookies.get('login_email') != "" and blogform.author  == request.cookies.get('login_author'):
                return render_template('blogform.html', author=blogform.author, email=blogform.email)
            else:
                flash("things are bad")
                return redirect(url_for('login_route'))

        flash("not good")
        
        return redirect(url_for('login_route'))
        
#vid creation process
@app.route('/action', methods=['POST', 'GET'])
def video():
    if request.method == 'POST' and request.cookies.get('login_email') is  not  None:
      video_url  = request.form['video']
      if video_url  is not  None:
        Database.updates("user",{"email":request.cookies.get('login_email')},{"$set": {"youtube":video_url}})
        return render_template('uploadvideo.html',point="Thank  you for uploading a video")
    return redirect(url_for('login_route'))
    
#blog creation process
@app.route('/actions', methods=['POST', 'GET'])
def blog():
    blogform = BlogForm(request.form['author'], request.form['title'],request.form['email'],request.cookies.get('login_id'),request.form['description'], request.files['file'], request.form['vibeusers'])

    if request.method == 'POST' and request.cookies.get('login_email') is  not  None:
     
        vibeuser = blogform.vibeusers
        print(vibeuser)
        author  = blogform.author
        title =   blogform.title
        email =   blogform.email
        
        description = blogform.description
        titleblog =  title.lower()

        f = blogform.filename
        filename = secure_filename(f.filename)
        f.save(os.path.join(os.getcwd() +'/static/uploads', filename))
        
        print(Users.blogExists(request.form['title']))
    
        if Users.blogExists(request.form['title'])  == False and  request.form['vibeusers'] == "":
            userImage =  Database.find_one("user", {"firstname":author})['image']
            cookie = request.cookies.get('login_email')
            person = Users.get_by_email(cookie)
            blog = Blogs(author=author,titleblog=titleblog,description=description,email=email,filename=filename, userImage=userImage)
            blog.save_to_mongo()
            if request.cookies.get('login_email') ==  email:
                data =  Database.find_one(userconstants.COLLECTION, {"email":email})

                flash('you have successfull created a blog')
                response = make_response(redirect(url_for('welcome', author=data["firstname"], lastname=data['lastname'], email=request.form['email'])))
                response.set_cookie('login_email', request.form['email'])
                response.set_cookie('login_author', data['firstname'])
                response.set_cookie('login_id', data['_id'])
                return response
            else:
                return render_template('blogform.html',point=blogform.message("A blog with that name already exist") )
        elif Users.blogExists(request.form['title'])  == False and  request.form['vibeusers'] !="":
            
            userImage = Database.find_one("user", {"firstname":author})['image']
            cookie =    request.cookies.get('login_email')
            person =    Users.get_by_email(cookie)
            secondVibePerson = Users.get_by_email(request.form['vibeusers'])
    
            if request.cookies.get('login_email') ==  email and secondVibePerson == True:
                
                vibeemail = Users.vibeUserCheck(request.form['vibeusers'])
                vibeUsername  = Users.vibeGetname(request.form['vibeusers'])
            
                blog = Blogs(author=author,titleblog=titleblog,description=description,email=email,filename=filename, userImage=userImage)
                vibeBlog = Blogs(author=vibeUsername,titleblog=titleblog,description=description,email=vibeemail,filename=filename, userImage=userImage)
            
                vibeBlog.save_to_mongo()
                blog.save_to_mongo()
                data =  Database.find_one(userconstants.COLLECTION, {"email":email})

                flash('you have successfull created a blog')
                response = make_response(redirect(url_for('welcome', author=data["firstname"], lastname=data['lastname'], email=request.form['email'])))
                response.set_cookie('login_email', request.form['email'])
                response.set_cookie('login_author', data['firstname'])
                response.set_cookie('login_id', data['_id'])
                return response
            else:
                return render_template('blogform.html',point=blogform.message("A blog with that name already exist or  vibe user  not avaliable") )
        else:
            return render_template('blogform.html',point=blogform.message("A blog with that name already exist"))
    return redirect(url_for('login_route'))
    
@app.route('/help/blog')
def help():
    return render_template('create_blog.html')
        
@app.route('/log')
def logno():
    return redirect(url_for('login_route'))


@app.route('/auth/restpass',methods=['POST','GET'])
def pass_rest():
    if request.method == 'POST':
        email = request.form['email']
        object_file = File_system()
        users_conn =  Restp(email)
        mal = users_conn.checkmliame(email)
        mailer = users_conn.checkmail(mal)

        image = object_file.image(request.form['email'])
        if mailer is not None:
            response = make_response(redirect(url_for('change_user', email=request.form.get('email'),id=image['_id'])))
            response.set_cookie('email',request.form.get('email'))
            return response
        else:
            print("Error message")
    return redirect(url_for('login'))

@app.route('/change_system_password/change_users_password/<string:email>/<string:id>')
def change_user(email,id):
    return render_template("edit_pass.html")

#acccount activation
@app.route('/active/account/')
def update_activation_status():
    url = "activate.html"
    routeUrl = Urls()
    return render_template(routeUrl.update_activation_status_url(url))

@app.route('/activate')
def activate():
    print("hello")
    return render_template("activate.html")

#prompt user to enter email and password
@app.route('/authorized/account/activated', methods=['GET', 'POST'])
def activated():
    User_utils = utils()
    loginform =  LoginForm()

    if request.method == 'POST' and request.cookies.get('login_email') == "":

        password = request.form['password']
        email =  request.form['email']

        database_email = Users.get_by_email(request.form['email'])
        database_password =  Users.get_by_password(email,password)
        user_active =  Users.get_by_active(request.form['email'])

        if database_email and password != "" and  database_password ==  True:
            if not user_active:
                Database.updates("user", {"email": email}, {"$set": {"active": 1}})
                print("activated %d")
                flash("Thank you for activating you account")
                return render_template("login.html", loginform=loginform)

    flash("Please enter correct information inorder  to activate account")
    return render_template("activate.html", loginform=loginform)

@app.route('/home')
def index():
    return render_template('index.html', search='Voodoo', email='ithollie@yahoo.com', login='true')

@app.route('/sign_in')
def sign():
    session['email'] = None
    return render_template('login.html')
    
@app.route('/changepassword')
def changePassword():
    return  render_template('changepassword.html')
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    
@app.route('/java')
def java():
    return render_template('java.html')
    
@app.route('/python')
def python():
    return render_template('python.html')

@app.route('/php')
def php():
    return render_template('php.html')
    
@app.route('/software')
def desk():
    items  = Database.find("blogs", {}).limit(2)
    todolist = Database.find("todo", {}).limit(2)

    messagelogin  = "Thank  you"
    messageReg    = "Please register"

    if request.cookies.get('login_email') == "":
        flash("You  have  logged  out  successfully")
        return  redirect(url_for('login_route'))

    return render_template('ecommerce.html' , items=items, messagelogin=messagelogin,  messageReg=messageReg)

@app.route('/login')
def login_route():
    return render_template('login.html')

@app.route('/profile')
def profile():
    return redirect(url_for('index'))

# upload user profile picture
@app.route('/picture', methods=['GET', 'POST'])
def profile_picture():
    if request.method == 'POST':
        file = request.files['file']
        if file == '':
            print("No file  seleted file")

        if file.filename:

            email = request.cookies.get('login_email')
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            Users.save_image(email, filename)
            response = make_response(redirect(url_for('welcome', email=email)))
            response.set_cookie('login_email', request.cookies.get('login_email'))
            response.set_cookie('login_author', request.cookies.get('login_author'))
            response.set_cookie('login_id', request.cookies.get('login_id'))
            return response
        else:
            print("file type not allowed")

    return redirect(url_for('login_route'))


@app.route('/author_profile')
def author_profile():
    return render_template('author_profile.html')

@app.route('/user_request',methods=['GET','POST'] )
def user_request():
    if  request.method  ==  'POST':
        login_cookie_email = request.cookies.get('login_email')
        
        #login user  details 
        login_name = request.get_json()['login_name']
        login_email = request.get_json()['user_email']
        login_id = request.get_json()['login_id']
        
        #post user details
        post_user = request.get_json()['post_user']
        post_email = request.get_json()['post_email']
        post_id  = request.get_json()['post_id']
        
        accept = request.get_json()['accept']
        count = request.get_json()['count']
        buttonstate = request.get_json()['button_state']
        
        
        coll  = post_email +  "friend_request"
        Request.get_by_title_request(post_email,  login_email) == False
        
        if post_email != login_email:
            Request.requests(login_name,  login_email, login_id,buttonstate,accept, count, coll,post_user)
            return jsonify({"login_name":login_name, "login_email":login_email,"login_id":login_id,"accept":accept, "count":count})
        else:
            print({"message":"there is a problem you  can  request your","post_email":post_email,"login_email":login_email
            })
            
    return   jsonify({"message":"please check the code"})
    
@app.route('/successful_reg')
def success_full_reg():
    message = "You  have successful registered please sign in"
    if request.cookies.get('login_email') == "":
        return render_template('login.html',  message=message)
    return render_template('login.html',  message=message)

@app.route('/register/page')
def register_route():
   regform = Form()
   message = "You  have entered  registeration page"
   return render_template('register.html', title='registration', regform=regform, message=message)

@app.route('/register')
def register():
   regform = Form()
   response = make_response(redirect(url_for('register_route')))
   response.set_cookie('login_email', "")
   response.set_cookie('login_author', "")
   response.set_cookie('login_id', "")
   return response
   
@app.route('/loads', methods=['GET','POST'])
def uploads():
    if  request.method == 'POST':
        file = request.form['file'].lower()
        if file == '':
            print("No file  seleted file")
        if file and allowed_file(file):
            email = request.cookies.get('email')
            filename = secure_filename(file)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            Users.save_image(email, filename)
            response = make_response(redirect(url_for('welcome', email=email)))
            response.set_cookie('email', email)
            return response
    
    return redirect(url_for('login_route'))
    
@app.route('/request')
def viewRequest():
    if request.cookies.get('login_email') is not None:
        if  request is not None:
            return  redirect(url_for('viewRequestHtml1')) 
          
    return redirect(url_for('login_route'))
    
@app.route('/request_form')
def viewRequestHtml1():
    if request.cookies.get('login_email') is not None:
        requests  = Database.find("requests"+request.cookies.get('login_email') + "friend_request", {})
        return render_template('viewRequest.html', requests=requests)
        
    return redirect(url_for('login_route'))
    
@app.route('/create_message')
def viewCreateMessage():
    if request.cookies.get('login_email') is not None:
        requests  = Database.find("requests"+request.cookies.get('login_email'), {})
        if request is not None:
            return  render_template('viewCreateMessage.html', requests=requests)
    return redirect(url_for('login_route'))
    
@app.route('/uploadVide')
def uploadVideo():
    if request.cookies.get('login_email') is not None:
        requests  = Database.find("requests"+request.cookies.get('login_email'), {})
        if  request is not None:
            return  render_template('uploadvideo.html', requests=requests)
    return redirect(url_for('login_route'))
    
@app.route('/friends')
def viewFriends():
    if request.cookies.get('login_email') is not None:
        friends  = Database.find("requests"+request.cookies.get('login_email')+ "friend_request",{'accept':1})
        if  friends is not None:
            return  render_template('viewFriends.html', friends=friends)
    return redirect(url_for('login_route'))

@app.route('/message')
def viewMessage():
    if request.cookies.get('login_email') is not None:
        
        requests  = Database.find("messages"+request.cookies.get('login_email'), {})
        if  request is not None:
            return  render_template('ViewMessage.html', requests=requests)
    return redirect(url_for('login_route'))
    
@app.route('/register/process', methods=['GET', 'POST'])
def register_process():
    regform = Form(request.form)
    if request.method == 'POST' and  request.cookies.get('login_email')  == "":
            size=128
            dig = md5(request.form['email'].lower().encode('utf-8')).hexdigest()
            image = 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(dig, size)
            reg =  RegisterForm(request.form['firstname'],request.form['lastname'],request.form['email'],request.form['password'],request.form['confirm'],image)
            
            user_name = request.form['firstname'].lower()
            
            f  = reg.filename
            filename = secure_filename(image)
            email = request.form['email'].lower()
                
            password = request.form['password'].lower()
            confirm  = request.form['confirm'].lower()
         
            if  Users.get_by_email(request.form['email'].lower()) != True and  reg.PasswordMatch(password, confirm) == True and reg.notEmpty() == True:

                #f.save(os.path.join(os.getcwd() +'/static/uploads', filename))
                Users.registration(request.form['firstname'], request.form['lastname'] , request.form['email'], request.form['password'], "imgs", image=image)

                # send mail  to  registered  user
                mail =  Mail("boysthollie@gmail.com", email)
                mail.sendMail()
                return redirect(url_for('success_full_reg'))
            else:
                 
                flash("One or  more inputs  is  empty or ")
                flash("There is a user with that email")
                flash("please make sure every input  is entered")
                return render_template('register.html', title='register', regform=regform)

    flash("There is a problem")
    return render_template('register.html', title='register', regform=regform)

@app.route('/changepass', methods=['GET' , 'POST'])
def changepass():
    session.pop('_flashes', None)
    if request.method == 'POST':
        if Users.get_by_email(request.form['email']):
                response = make_response(redirect(url_for('reqs', email=request.form['email'])))
                response.set_cookie('vibe_resetUser_email', request.form['email'])
                return response
    else:    
        return render_template('login.html')
        
@app.route('/request/<string:email>')
def reqs(email):
    if Users.get_by_email(email):
        return render_template('resetpass.html', email=email, confirmEmail='True')
    else:
        return  render_template('login.html')
        
@app.route('/confirm', methods=['GET', 'POST'])
def  passwordChanged():
    if request.method  == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        email   = request.cookies.get('email')
        if  new_password  ==   confirm_password:
            print("They are equal")
            Users.resetPassword(request.cookies.get('vibe_resetUser_email'), Users.passhashed(new_password))
            response = make_response(redirect(url_for('login_route')))
            flash("password changed")
            response.set_cookie('vibe_resetUser_email', "")
            return  response

    return  render_template('login.html')
         

@app.route('/login/process', methods=['POST'])
def login_process():

   logform = LogForm()
   session.pop('_flashes', None)
   error = "There is a problem were you are not successfully logged in"
   print("Thank you")
   if request.method == 'POST' and  request.cookies.get('login_email') == "":

      email = request.form['email'].lower()
      password = request.form['password'].lower()

      data =  Database.find_one(userconstants.COLLECTION, {"email":email})
      active = Database.find_one(userconstants.COLLECTION, {"email":email})

      if active['active'] == 1 and Users.login_valid(request.form['email'],request.form['password']) != False  and utils.check_hash_password(password,data['password']) ==  True:
          
          response = make_response(redirect(url_for('welcome')))
          response.set_cookie('login_email', request.form['email'])
          response.set_cookie('login_author', data['firstname'])
          response.set_cookie('login_id', data['_id'])
          return response
         
      else:
           flash("some wrong")
           return redirect(url_for('logout'))
   flash('There is a problem were you are not successfully logged in')

   return redirect(url_for('logout'))

@app.route('/voodoo')
def voodoo():
   error = "There is an error"
   return render_template('error.html' , error=error)


@app.route('/welcome')
def welcome():
   session.pop('_flashes', None)
   message = "You have  not logged in  please try  again"
   img = "image"

   movie   =  ["ibrahim", "ibrahim", "ibrahim", "ibrahim", "ibrahim"]

   userInDatabase = Database.find_one("user", {"email": request.cookies.get('login_email')})

   if request.cookies.get('login_email') != "" and userInDatabase  is not None:
       
        check  = Database.find("blogs", {"email":request.cookies.get('login_email')})
        userb  = Database.find("blogs", {"email":request.cookies.get('login_email')})
        userInDatabase = Database.find_one("user", {"email":request.cookies.get('login_email')})
            
        date = datetime.datetime.utcnow()
        item = Database.find_one(userconstants.COLLECTION, {"email":request.cookies.get('login_email')})
        
        if item['email']:
            
            flash('Login is a success' + " "+ 'welcome' + " "+ request.cookies.get('login_email'))

            
            blogs      = Database.find("blogs", {"delete":0})
            youtube    = Database.find_one('user', {"email":request.cookies.get('login_email')})['youtube']
            
            postsu     = Database.find("blogs", {})
            postUsers  = Users.find(Database.find("blogs", {}),Database.find("blogs", {}).count())
            
            length     = Database.find("requests"+request.cookies.get('login_email'), {}).count()
            
            messageRe   = Database.find("requests"+request.cookies.get('login_email'), {}).count()
            
            requests   = Database.find("requests"+request.cookies.get('login_email')  +  "friend_request", {}).count()
            
            friends    = Database.find("requests"+request.cookies.get('login_email')+ "friend_request", {'accept':1}).count()
            acccepted  = Database.find("requests"+request.cookies.get('login_email'), {'accept':1}).count()
            
            messages   = Users.messages( Database.find("requests"+request.cookies.get('login_email'),{}) ,length)
            
            userblog   = Users.blogs( "blogs" ,item['email'])
            email      = request.cookies.get('login_email') 
            user       = Database.find_one('user', {"email":email})
            
        
            items = Database.find_one(userconstants.COLLECTION, {"email":request.cookies.get('login_email')})
            img = File_system.image(request.cookies.get('login_email'))
            
            return render_template('index.html',requests=requests, messageRe=messageRe,friends=friends, email=request.cookies.get('login_email'),firstname=items['firstname'],_id=items['_id'],lastname = items['lastname'],date=date, login='true',image=items['img'],blogs=blogs, posts=postsu , userblog=userblog,user=user, Database=Database, youtube=youtube)
          
        else:
          flash('There is a problem were you are not successfully logged in')
          
          return render_template('login.html')

        
   return redirect(url_for('login_route'))


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('out')))
    response.set_cookie('login_email', "", expires=0)
    response.set_cookie('login_author', "", expires=0)
    response.set_cookie('login_id', "", expires=0)
    return  response
 
 
@app.route('/outPage')
def  out():
    if request.cookies.get('login_email') is None:
        session.pop('_flashes', None)
        session.pop('login_email',None)
        response = make_response(redirect(url_for('desk')))
        response.set_cookie('login_email', "")
        response.set_cookie('login_author', "")
        response.set_cookie('login_id', "")
        return  response
    return redirect(url_for('logout', email="none"))

if __name__== '__main__':
    host = os.getenv('IP','127.0.0.1')
    port = int(os.getenv('PORT',9000))
    app.run(host=host, port=port,debug=True)
