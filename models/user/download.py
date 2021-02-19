
from flask import request
from models.User import User

class Download(object):
    def __init__(self,file_name,database):
        self.file_name = file_name
        self.database = database
