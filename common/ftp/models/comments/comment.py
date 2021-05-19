from models import constants as Collections
import datetime
from common.Utils import utils
import uuid
from common.database import Database

class Comments(object):
    def __init__(self,titleblog,comment,_id=None,date = datetime.datetime.utcnow()):
            self.titleblog = titleblog
            self.comment = comment
            self.date = date

    def insert(self):
        Database.insert(Collections.Activities,self.json())
    def save_to_mongo(self):
        Database.insert(Collections.blogs_comments, self.json())
    def json(self):
        return {
            "title":self.titleblog,
            "comment":self.comment,
            "date":self.date,

        }
