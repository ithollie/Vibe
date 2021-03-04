from flask import Flask, session
from common.database import Database
from models.admin import *
from bson.objectid import ObjectId
from  models import constants as UserConstants
from models.System_file import File_system
import  models.user.error as UserErrors
from common.Utils import utils
from sendemail.mailer import Mail
import datetime
import uuid
import os

class Users(object):
	def __init__(self,firstname, lastname, email,password,image,img , date=datetime.datetime.utcnow(), _id=None):
		self.firstname =  firstname
		self.lastname  =  lastname
		self.email = email
		self.password = password
		self.image = image
		self.img   = img
		self.date =  date
		self.request = 0;
		self.messagesCollection = "messages_" + email
		self.requestsCollection = "requests_" + email
		self._id = uuid.uuid4().hex if _id is None else _id
		self.youtube ="https://www.youtube.com/embed/UE1YUC379fc"
		isfalse = False
		isTrue  = True
		
	
	@classmethod
	def get_by_id(cls,_id):
		data = Database.find_one(UserConstants.COLLECTION,{"_id":_id})
		if data is not None:
			return cls(**data)
		else:
			raise UserErrors.UserNotExistError("user does not exit")
	
	@classmethod
	def get_id(cls,ids):
		data_id = Database.find_one("blogs", {"id":ids})
		print()
		if data_id['id'] == ids: 
			return int(data_id['id'])
		else:
			return 1
    


	@staticmethod
	def fol():
		 blogs  = Database.find("blogs", {})
		 file  =  os.getcwd() + '/static/uploads'    
		 for  blog in   blogs:
		 	for file in os.listdir(file):
		 		if file == blog['img']:
		 			return False

	@classmethod
	def get_by_email(cls,email):
			data = Database.find_one(UserConstants.COLLECTION, {"email":email})
			if data is not None and data['email'] == email.lower():
				#return cls(**data)
				return True
			else:
				return False

	@staticmethod
	def get_by_active(email):
		data = Database.find_one(UserConstants.COLLECTION, {"email": email})
		if data["active"]  == "0":
			return  True
		else:
			return False

	@staticmethod
	def get_by_password(email, password):
		data = Database.find_one(UserConstants.COLLECTION, {"email": email})
		if  utils.check_hash_password(password, data['password']) is not None:
			return True
		else:
			return False

	# raise UserErrors.InvalideEmailError("invalid user")
	@classmethod
	def get_by_name(cls,email):
			data = Database.find_one(UserConstants.COLLECTION, {"email":email})
			if data is not None and data['email'] == email.lower():
				#return cls(**data)
				return data['email']
			else:
				return False

	@staticmethod
	def Database_password(password):
		data =  Database.find_one(UserConstants.COLLECTION,{"password":password})
		return data
		
	@staticmethod
	def  find(postObject,length):
		 
		 for items in  range(0, length):
		 	return  postObject[items]
	@staticmethod
	def  requests(postObject,length):
		 for items in  range(0, length):
		 	return  postObject[items]
		
	@staticmethod
	def friends(postObject, length):
		accept = 0
		for i  in range(0, length):
			if postObject[i]['accept'] == 1:
				accept = accept + 1
		return  accept
	@staticmethod
	def acceptedFriends(postObject , length):
		accept = 0
		for i  in range(0, length):
			if postObject[i]['accept'] == 1:
				accept = accept + 1
		return  accept
	@staticmethod
	def messages(postObject, length):
		accept = 0
		for i  in range(0, length):
			if postObject[i]['accept'] == 1:
				accept = accept + 1
		return  accept

		
	@staticmethod
	def blogs(collection, email):
		check  = Database.find(collection, {"email":email}).limit(1)
		if check is not None:
				return  check 
		else:
			return False
	@staticmethod
	def likes(collection,_id, title):
		data =  Database.find_one(collection,{"title":title})
		return data
	@staticmethod
	def dislikes(collection, _id, title):
		data =  Database.find_one(collection,{"title":title})
		return data
	
	@staticmethod
	def blogExists(title):
		data  = Database.find_one("blogs", {"title":title})
		if  data is not None and data['title']:
			  return  True
		else:
			 print("it is here")
			 return  False
		
	@staticmethod
	def isBlog(titleBlog=None):
		condition  = False;
		if titleBlog  is not None:
			data  = Database.find_one("blogs", {"title":titleBlog})
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
			if user == True and utils.check_hash_password(password,data['password']) is not None:
				return True
			else:
				return  False
				#raise UserErrors.InvalideEmailError("invalid user")
    
	@classmethod
	def registration(cls, firstname, lastname, email, password, imagename, image):
		if not cls.get_by_email(email):
			utils.email_is_valid(email)
			new_user = cls(firstname, lastname, email, utils.hash_password(password), imagename, image)
			new_user.save_to_mongo()
			session['email'] = email
			return True
		else:
			return "there is a user with that email"

	@classmethod
	def vibeUserCheck(cls ,  vibeemail):
		if vibeemail is not None and cls.get_by_email(vibeemail) ==  True:
			return vibeemail
		else:
			return  ""

	@classmethod
	def vibeGetname(cls , vibeemail):
		if vibeemail  is not None:
			return  cls.get_by_name(vibeemail)

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
	
	@classmethod
	def delete(cls , _id):
		Database.updates("blogs",{"id":_id}, { "$set": { "delete":1 }})
	
	def save_to_mongo(self):
		Database.insert(UserConstants.COLLECTION,self.json())
  
	@staticmethod
	def deleteBlogs(email):
		if  email is not  None:
			pass
 
	@classmethod
	def update_image(cls, email=None, image=None):
		if email  is  not None and  image  is not None:
			print("hello  wow")
			Database.updates("user",{"email":email}, {"$set":{"image":"1"}})
			Database.updates("user",{"email":email},{"$set": {"img":image}})
 
	@classmethod
	def  save_image(cls ,email , image):
		if cls.get_by_email(email):
			print("this is  the image condition")
			user = cls.get_by_email(email)
			utils.email_is_valid(email)
			cls.update_image(email, image)
		else:
			print("Image can not be inserted")

	def json(self):
		return {
			"firstname":self.firstname,
			"lastname":self.lastname,
			"email":self.email,
			"password":self.password,
			"_id":self._id,
			"active":0,
			"image":0,
			"youtube":self.youtube,
			"img":self.img,
			"date":self.date
		}
