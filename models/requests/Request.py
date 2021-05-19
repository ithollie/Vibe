from flask import Flask, session
from common.database import Database
from models.admin import *
from models import constants as UserConstants
from models.System_file import File_system
from common.Utils import utils
import datetime
import uuid
import os
import  models.user.error as UserErrors

class Request(object):
	def __init__(self,name,email,user_id,buttonstate,accept ,count,collection,receiver, date=datetime.datetime.utcnow(), _id=None):
	    self.name =  name
	    self.email   = email
	    self.user_id = user_id
	    self.buttonstate = buttonstate
	    self.accept = accept
	    self.count  =  count
	    self.collection = collection
	    self.receiver   =  receiver
	    
	    self.date =  date
	    self._id = uuid.uuid4().hex if _id is None else _id

	@classmethod
	def get_by_id(cls,_id):
		data = Database.find_one(UserConstants.COLLECTION,{"_id":_id})
		if data is not None:
			return cls(**data)
		else:
			raise UserErrors.UserNotExistError("user does not exit")

	@staticmethod
	def fol():
		 blogs  = Database.find("blogs", {})
		 file  =  os.getcwd() + '/static/uploads'    
		 for  blog in   blogs:
		 	for file in os.listdir(file):
		 		if file == blog['img']:
		 			return False	
		 			
	@staticmethod
	def get_by_email_no_static(email):
		data = Database.find_one("user", {"email":email})
		if data is not None:
			return data['email']
		else:
			return False
	@classmethod
	def get_by_email(cls,email):
			data = Database.find_one("user", {"email":email})
			if data is not None:
				return data['email']
			else:
				return False
	@classmethod
	def get_by_title_request(cls,post_email, login_email):
			data = Database.find_one("requests"+post_email, {"email":login_email})
			if data is not None:
				if data['email'] == login_email :
					return True
			else:
				return False
	@staticmethod
	def Database_password(password):
		data =  Database.find_one(UserConstants.COLLECTION,{"password":password})
		return data
		
	@staticmethod
	def blogs(collection, email):
		check  = Database.find(collection, {"email":email}).limit(1)
		if check is not None:
				return  check 
		else:
			return False
	@staticmethod
	def likes(collection, title):
		data =  Database.find_one(collection,{"title":title})
		return data
	
	@staticmethod
	def blogExists(title):
		data  = Database.find_one("blogs", {"title":title})
		return data
		
	@staticmethod
	def isBlog(titleBlog=None):
		condition  = False;
		if    titleBlog  is not None:
			data  = Database.find("blogs", {"title":titleBlog})
			for item  in data:
				if item['title']   ==  titleBlog:
					condition   =  True
					return   condition
				else:
					return  condition
		else:
			return 0
			
		
	@staticmethod
	def login_valid(email,password):
			data =  Database.find_one(UserConstants.COLLECTION,{"email":email})
			user =  Users.get_by_email(email)
			if user == email and utils.check_hash_password(password,data['password']) is not None:
				return True
			else:
				return  False
				#raise UserErrors.InvalideEmailError("invalid user")
  
	@classmethod
	def requests(cls, name,email,_id,buttonstate,accept ,count, collection, receiver):
	
		if  email is not None:
			print({"person":name, "email":email,"button":buttonstate,"count":count,"coll":collection,"receiver":receiver})
			
			new_request = cls(name,email,_id,buttonstate,accept ,count, collection, receiver)
			new_request.save_to_mongo(collection)
			print(new_request.name)
			
			return True
		else:
			print("there is a user with the email" )
			
	@classmethod
	def passhashed(cls,password):
		if  password is not None:
			return  utils.hash_password(password)
			
	@staticmethod
	def findByEmail(email):
		Database.find_one(UserConstants.COLLECTION,{"email":email})
		
	@staticmethod
	def login(email):
		session['email'] = email

	@classmethod
	def resetPassword(cls ,email,  hash_password):
		Database.updates(UserConstants.COLLECTION,{"email":email}, { "$set": { "password":hash_password }})
	
		
	def save_to_mongo(self, collection):
		Database.insert("requests" + collection,self.json())
	
	@classmethod
	def update_image(cls, email, image):
		Database.updates(UserConstants.COLLECTION,{"email":email },{"$set": {"image":image}})
 
	@classmethod
	def  save_image(cls ,email , image):
		if cls.get_by_email(email) == True:
			user = cls.get_by_email(email)
			utils.email_is_valid(email)
			cls.update_image(email, image)
			
    
	def json(self):
		return {
		  
			"name":self.name,
			"email":self.email,
			"user_id":self.user_id,
			"buttonstate":self.buttonstate,
			"accept":self.accept,
			"count":self.count,
			"collection":self.collection,
			"_id":self._id,
		    "date":self.date,
		    "test":"true"
		}
