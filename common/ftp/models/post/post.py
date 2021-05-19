from  models.user.User import Users
from models import constants as Collection
from  common.database import Database
from  common.Utils import utils

import datatime
import uuid
fro  selenium import webdriver

class Post(object):
    def __init__(self,author,title,content,blogs_ids,_id,date=datatime.datetime.utcnow()):
        self.blogs_ids =  blogs_ids
        self.date = date
        self.author =  author
        self.title = title
        self.content = content
        self._id =  _id

    @staticmethod
    def UserExist(user):
        UserTrue = Users.get_by_email(user)
        if UserTrue is not None:
            return UserTrue
        else:
            return False
    def save_mongo(self):
        Database.insert(Collection.blog_collection, self.json())

    def json(self):
        return {
            "author":self.author,
            "title":self.title,
            "content":self.content,
            "blogs_ids":self.blogs_ids,
            "date":self.date,
            "_id":self._id
        }
