from flask import Flask, session
from common.database import Database
from models.admin.master import Master
from models.mail.sendemail import Mail
from models import constants as UserConstants
from models.System_file import File_system
import models.user.error as UserErrors
from models.activate.active_account import activate_account
from common.Utils import utils
from models.blog.blog import Blog
from models.comments.comment import Comments
import datetime
import uuid
from bson.objectid import ObjectId
from selenium import webdriver
global datauser

class Users(object):
	def __init__(self,name,lastname,email,password,birthdate,filename,date=datetime.datetime.utcnow(), _id=None):
		self.name = name
		self.lastname =  lastname
		self.email = email
		self.password = password
		self.birthdate = birthdate
		self.filename = filename
		self.date =  date
		self.active = 0
		self.register = "true"
		self.likes = []
		self.dislikes = []
		self._id = uuid.uuid4().hex if _id is None else _id
	@staticmethod
	def queryAll(email):
		data = Database.find(UserConstants.blog_collection, {"email":email})
		if data is not None:
			return data
		else:
			return False
	@staticmethod
	def queryfrontpage():
		data = Database.find(UserConstants.blog_collection, {})
		if data is not None:
			return data
		else:
			return False
	@staticmethod
	def arrayblogs(items):
 		blog = []
		for  item in items:
			blog = item
		return blog

	@staticmethod
	def queryone(titleblog):
		data = Database.find(UserConstants.blog_collection, {'titleblog':titleblog})
		if data is not None:
			return data
		else:
			return  "no"

	@staticmethod
	def alluser():
		data = Database.find(UserConstants.blog_collection, {})
		if data is not None:
			return data

	@staticmethod
	def allcomments(title):
		data = Database.find(UserConstants.blogs_comments, {"title":title})
		if data is not None:
			return data
		else:
			return "error"
	@staticmethod
	def bytitle(titleblog):
		data = Database.find("blogs", {"titleblog":titleblog})
		if data is not None:
			return data
		else:
			return "error"
	@staticmethod
	def bytitle_one(titleblog):
		data = Database.find_one("blogs", {"titleblog":titleblog})
		if data is not None:
			return data
		else:
			return "error"
	@staticmethod
	def byid_one(user_id):
		data = Database.find_one("blogs", {"_id":user_id})
		if data is not None:
			return data
		else:
			return False
	@staticmethod
	def id_one(user_id):
		data = Database.find_one("blogs", {"_id":user_id})
		if data is not None:
			return data
		else:
			return False
	@staticmethod
	def id_one_user(user_id):
		data = Database.find_one("user", {"_id":user_id})
		if data is not None:
			return data
		else:
			return False
	@staticmethod
	def bgtitle(titleblog):
		data = Database.find("blogs", {"titleblog":titleblog})
		if data:
			return data
		else:
			return False

	@staticmethod
	def bgemail(email):
		data = Database.find("blogs", {"email":email})
		if data is not None:
			return data
		else:
			return "error"
	@staticmethod
	def bgemail_one(email):
		data = Database.find_one("blogs", {"email":email})
		if data is not None:
			return data
		else:
			return "error"
	@staticmethod
	def query(blogauthor):
		data = Database.find(UserConstants.blog_collection, {"author":blogauthor})
		if data is not None:
			return  data
		else:
			return False
	@staticmethod
	def queryu(titleblog):
		data = Database.find(UserConstants.blog_collection, {"titleblog":titleblog})
		if data is not None:
			return  data
		else:
			return False
	@staticmethod
	def querytitle(titleblog):
		data = Database.find(UserConstants.blog_collection, {"titleblog":titleblog})
		if data is not None:
			return data
		else:
			return False
	@staticmethod
	def querytitlei(titleblog):
		data = Database.find_one(UserConstants.blog_collection, {"titleblog":titleblog})
		if data is not None:
			return data
		else:
			return False
	@staticmethod
	def getone(blogid):
		data = Database.find(UserConstants.blog_collection, {"blogid":blogid})
		if data is not None:
			return data
		else:
			return False
	@staticmethod
	def getitems(blogid):
		data = Database.find(UserConstants.blog_collection, {"blogid":blogid})
		if data is not None:
			return data
		else:
			return False
	@staticmethod
	def removes(_id):
		Database.remove(UserConstants.blog_collection,{"_id":_id})

	@staticmethod
	def get_image(author):
		data = Database.find_one(UserConstants.blog_collection, {"author":author})
		if data is not None:
			return data
		else:
			return False
	@staticmethod
	def blogExists(titleblog):
		data = Database.find_one(UserConstants.blog_collection, {"titleblog":titleblog})
		if data is not None:
			return data['titleblog']
		else:
			return False
	@staticmethod
	def blogExistsi(titleblog):
		data = Database.find_one(UserConstants.blog_collection, {"titleblog":titleblog})
		if data is not None:
			return data
		else:
			return False
	@staticmethod
	def increment_comment(title):
		increment_comment = 0
		increment_comment = increment_comment + 1
		if title is not None:
			Database.updates(UserConstants.blog_collection,{"titleblog":title},{"$set": {"comment":increment_comment}})
		else:
			return False
	@staticmethod
	def arrayblogs(items):
 		blog = []
		for  item in items:
			blog = item
		return blog

	@classmethod
	def get_by_id(cls,_id):
		data = Database.find_one(UserConstants.COLLECTION,{"_id":_id})
		if data is not None:
			return cls(**data)
		else:
			raise UserErrors.UserNotExistError("user does not exit")
	@staticmethod
	def get_by_email(email):
		data = Database.find_one(UserConstants.COLLECTION, {"email":email})
		if data is not None:
			return data
		else:
			return False
	@staticmethod
	def get_by_person(name):
		data = Database.find_one(UserConstants.COLLECTION, {"name":name})
		if data is not None:
			return data
		else:
			return False
	@staticmethod
	def get_by_password(password):
		data = Database.find_one(UserConstants.COLLECTION, {"password":password})
		if data is not None:
			return data
		else:
			return False
	@staticmethod
	def isRegister(email):
		data = Database.find_one(UserConstants.COLLECTION, {"email":email})
		if data is not None:
			return True
		else:
			return False
	@classmethod
	def password(cls,password):
		data =  Database.find_one(UserConstants.COLLECTION,{"password":password})
		if data is not None:
			return cls(**data)
		else:
			return False
	@staticmethod
	def login_valid(email,password):
		if Users.activateds(email) ==  True:
			data =  Database.find(UserConstants.COLLECTION,{"email":email})
			for datas in data:
				hashpassword = utils.check_hash_password(password,datas['password'])
				if hashpassword:
					return  True
				else:
					return False
					#raise UserErrors.InvalideEmailError("invalid user")
	@staticmethod
	def activateds(email):
		datas = Database.find(UserConstants.COLLECTION,{"email":email})
		for data in datas:
			if data['activate'] == 1:
				return True
			else:
				return False
	@classmethod
	def registration(cls,name ,lastname,email,password,date,filename):
		user = cls.get_by_email(email)
		#mail = utils.hash_email(password)
		account = activate_account(email)
		if user is not None:
			utils.email_is_valid(email)
			new_user = cls(name,lastname,email,utils.hash_password(password),date,filename)
			account
			new_user.save_to_mongo()
			session['email'] = email
			return True
		else:
			return False
	def forgetpass(email):
		pass
	@staticmethod
	def login(email):
		session['email'] = email

	def save_to_mongo(self):
		Database.insert(UserConstants.COLLECTION,self.json())
	def json(self):
		return {
			"name":self.name,
			"lastname":self.lastname,
			"email":self.email,
			"password":self.password,
			"birthdate":self.birthdate,
			"image":self.filename,
			"_id":self._id,
			"date":self.date,
			"likes":self.likes,
			"dislikes":self.dislikes,
			"register":self.register,
			"activate":self.active
		}
