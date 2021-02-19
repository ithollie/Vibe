import os
from common.database import Database
from models import constants as UserConstants
from models import constants as const
from models.user import error as UserErrors
import datetime


class File_system(object):
		def __init__(self,date=datetime.datetime.utcnow(),_id=None):
			self.date = date
			self._id  = _id
			
		@staticmethod
		def image(email):
			data = Database.find(const.COLLECTION, {"email":email})
			if data is not None:
				for datas in data:
					return datas

		@staticmethod
		def get_by_email(email):
			data = Database.find_one(UserConstants.COLLECTION, {"email":email})
			if data is not None:
				return data

		
