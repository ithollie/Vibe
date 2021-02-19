import os
from common.database import Database
from models import constants as UserConstants
from models import constants as const
from models.user import error as UserErrors
import datetime


class File_system(object):
		def __init__(self,image,email,date=datetime.datetime.utcnow(),_id=None):
			self.image = image
			self.date = date
			self._id  = _id
			self.email =  email
			self.password = password

		@staticmethod
		def image(email):
			data = Database.find(const.COLLECTION, {"email":email})
			if data is not None:
				for database in data:
					return database
				else:
					return  None
			else:
				raise UserErrors.IncorrectDatabaseStatment("cant find email")

		@staticmethod
		def get_by_email(email):
			data = Database.find_one(UserConstants.COLLECTION, {"email":email})
			if data is not None:
				return data

		def save_to_mongo(self):
			data = Database.insert(UserConstants.COLLECTION,self.json())

		def json(self):
			return {
				"date":self.date,
				"image":self.image

			}
