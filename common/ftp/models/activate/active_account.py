from common.database import Database
from models.passrest.mail.sendemail import Mail
from models import constants as UserConstants
from common.Utils import utils
import datetime
import uuid
from common.database import Database
from flask import Flask, session

class activate_account(object):
	def __init__(self,email, date= datetime.datetime.utcnow(),_id=None):
		self.email =  email
		self.date = date
		self._id = uuid.uuid4().hex if _id is None else _id
		self.netmail = self.sendmail(self.check_String_mail(),self.json()['url'],self.json()['subject'])

	def check_String_mail(self):
		mail = self.email
		if mail is not None:
			 return mail
		else:
			return False
	@staticmethod
	def checkmail(email):
		data =  Database.find_one(UserConstants.COLLECTION,{"email":email})
		if data is not None:
			return  data
		else:
			return False
	@staticmethod
	def getEmail(email):
		data =  Database.find_one(UserConstants.COLLECTION,{"email":email})
		if data is not None:
			return  data
		else:
			return False
	@staticmethod
	def checkpassword(password):
		data =  Database.find(UserConstants.COLLECTION,{"password":password})
		for datas in data:
			hash_password  = utils.check_hash_password(password,datas['password'])
			if hash_password:
				return True
			else:
				return  False
		else:
			return False
	@staticmethod
	def Update(email):
		activate_account_increasement = 1
		activate_account = 0
		if activate_account == 0:
			Database.updates(UserConstants.COLLECTION,{"activate":activate_account},{"$set": {"activate":activate_account_increasement}})
		else:
			return False

	@classmethod
	def check_mail(self,email):
		data =  Database.find_one(UserConstants.COLLECTION,{"email":email})
		if data is not None:
			return data
		else:
			return False


	def Valid(self):
		return {"email":self.email,"id":self.check_mail(self.email)['_id']}

	@staticmethod
	def sendmail(email,url,subject):
		mail = Mail(email,url,subject)
		if mail is not None:
			mail.send()

	def json(self):
		return  {"url":"http://127.0.0.1:8000/active/account/",
				"subject":"please click the link above in order to active your account"
		}
