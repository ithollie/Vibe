from models import constants as Collections
import datetime
from models.user.User import Users
from common.Utils import utils
import uuid
from common.database import Database

class Clicks(object):
    def __init__(self,email):
        self.email = email
    @staticmethod
	def likes(email):
		increment  =  0
        number = User.get_by_email(email)['activate']
		activate_account = 0
		if number >= 0:
            increment = increment + 1
			Database.updates(UserConstants.COLLECTION,{"email":email},{"$set": {"activate":increment}})
		else:
			return False
    def dislikes(email):
		increment  =  0
        number = User.get_by_email(email)['activate']
		activate_account = 0
		if number >= 0:
            increment = increment + 1
			Database.updates(UserConstants.COLLECTION,{"email":email},{"$set": {"activate":increment}})
		else:
			return False
