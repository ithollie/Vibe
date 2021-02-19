from flask import Flask,redirect,url_for,session,render_template,request,flash,make_response
from models.user.User import Users
from models.System_file import File_system
from common.database import Database
from common.Utils import utils
from models.user import error as UserErrors
from  file.router  import routerview
import os
from templates import Templates
from werkzeug.contrib.fixers import LighttpdCGIRootFix

class mainRouters(object):
	def __init__(self,app):
		fullpath ="c:\\Users\hacker\desktop\startup\machine\static\Assets\images"
		app.config['UPLOAD_FOLDER'] = fullpath
		app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

	#initialize the database
	@app.before_first_request
	def initialize_database():
		Database.initialize()

	#this is the route to rest password
	@app.route(Tenplates.rest('/rest'))
	def forget():
		return render_templates(Templates.restpass("restpass.html"))

	#this is the route to rest password
	@app.route(Templates.HOME_ROUTER('/'))
	def home():
		return render_templates(Templates.homeIndex("index.html"))
	#this is the route for the login 
	@app.route(Templates.LOGIN_ROUTER('/login'))
	def login():
		return render_templates(Templates.log_in("login.html"))

	#this is the route for sigup
	@app.route(Templates.SIGNUP_ROUTER('/signup'))
	def signup():
		return render_template(Templates("signup.html"))
	#this is the route  for upload
	@app.route('/uploads/<filename>')
	def uploaded_file(filename):
		return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

	#signup end point
	@app.route(Templates.ftp_ROUTER('/ftp'))
	def ftp():
		return render_template("ftp.html")
	#thisis is the route for the 
	@app.route(Templates.login_url_router('/auth/login/'),Templates.login_post_router(methods=['POST','GET']))
	def login_user():
		error = None

		if request.method == 'POST':
			email =  request.form['email']
			password = request.form['password']

			if Users.login_valid(request.form['email'],request.form['password']):
					user = Users.login(email)
					img  = File_system.image(email)

					flash("you have Succesfuly logged in")
					response = make_response(redirect(url_for('welcome',email=request.form.get('email'),image=img['image'],id=img['_id'])))
					response.set_cookie('email',request.form.get('email'))
					return  response


			else:
					error = 'User'+" "+ request.form['email']+" "+'does not exist'
					session['email'] =  None
					return render_template("login.html",error=error)

		return render_template("profile.html", email=request.form.get('email'))

	@app.route(Templates.url('/auth/ftp/'),Templates.urlr(methods=['POST','GET']))
	def ftps():
		if request.method == 'POST':
			email =  request.form['email']
			password = request.form['password']
			reg = Userss(email,password,"nopicture")
			mail = reg.get_by_email(email)
			if mail is None:
				reg.registration(request.form['email'],request.form['password'],"ithollie")
			else:
				return redirect(url_for('loginend_point'))
		return render_template("download.html")
	#logout router
	@app.route(Templates.Logout('/logout'))
	def logout():
		response = make_response(redirect(url_for('login')))
		response.set_cookie('email_set', '', expires=0)
		return response

	def allowed_file(filename):
		return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

	@app.route('/welcome/<string:email>/<image>/<id>')
	def welcome(email,image,id):
		make_cook = request.cookies.get('email')
		if make_cook is not None:
			return render_template('portfolio.html',email=email,image=image)
		else:
			return redirect(url_for('loginend_point'))
	#reg router
	@app.route(Templates.Reg('/auth/signup'), Templates.Reg(methods=['POST','GET']))
	def register_user():
		name = request.form['name']
		lastname = request.form['lastname']
		email =  request.form['email']
		password = request.form['password']
		phote = request.files['file']


		if phote and allowed_file(phote.filename):
			    # Make the filename safe, remove unsupported chars
			filename = secure_filename(phote.filename)
			    # Move the file form the temporal folder to
			    # the upload folder we setup
			if not os.path.exists(fullpath):
				#The folder to send the file if something is goes wrong
				PATH  ='C:\\Users\hacker\desktop\startup\machine\Assets\empyt_folder'
				#config path folder
				app.config['UPLOAD_FOLD'] = PATH
				#changing dir
				os.chdir('C:\\users\hacker\desktop\startup\machine\static\Assets')
				# make a new folder
				os.mkdir("empyt_folder")
				file_name =  secure_filename(phote.filename)
				phote.save(os.path.join(app.config['UPLOAD_FOLD'],file_name))
				Users.registration(reguest.form['name'], request.form['lastname'], equest.form['email'],request.form['password'],filename)
			else:
				filename =  secure_filename(phote.filename)
				phote.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				Users.registration(request.form['name'] ,request.form['lastname'],request.form['email'],request.form['password'],filename)
			#return redirect(url_for('uploaded_file',filename=filename))
		return redirect(url_for(Templates.elslogin('login')))
		#check this code

