from models import constants as Collection
from  common.database import Database
from  common.Utils import utils
from  selenium import webdriver
import datetime
import uuid


class Blog(object):
    def __init__(self,author,titleblog,description,filename,email,date=datetime.datetime.utcnow(),_id=None,blogs_ids="1234"):
        self.author =  author
        self.titleblog = titleblog
        self.description = description
        self.filename = filename
        self.email =  email
        self.date = date
        self.likes = 0
        self.dislikes = 0
        self.comments = 0;
        self._id = uuid.uuid4().hex if _id is None else _id
        self.blogs_ids = blogs_ids


    @staticmethod
    def UserExist(user):
        UserTrue = Users.get_by_email(user)
        if UserTrue is not None:
            return UserTrue
        else:
            return False
    def save_to_mongo(self):
        Database.insert(Collection.blog_collection, self.json())

	@staticmethod
	def Blogtitle(titleblog):
		data = Database.find("blogs", {"titleblog":titleblog})
		if data is not None:
			return data
		else:
			return False
	@staticmethod
	def get_by_id(_id):
		data = Database.find_one("blogs",{"_id":_id})
		if data is not None:
			return data
		else:
			raise UserErrors.UserNotExistError("user does not exit")

    def json(self):
        return {
            "author":self.author,
            "_id":self._id,
            "titleblog":self.titleblog,
            "content":self.description,
            "image":self.filename,
            "email":self.email,
            "likes":self.likes,
            "dislikes":self.dislikes,
            "comment":self.comments,
            "blogs_ids":self.blogs_ids,
            "date":self.date,
        }
