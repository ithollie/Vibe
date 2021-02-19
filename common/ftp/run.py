
from flask import Flask,redirect,request,url_for,session,render_template,request,flash,make_response
from common.database import Database
from models.user import error as ErrorMessage
from models.user.User import Users
from user.User import Userss
from common.Utils import utils
from models.user import error as UserError
from ftp.download import Download
import datetime
import uuid
from ftplib import FTP, error_perm
import os


class ftp_download(object):
    def __init__(self,date=datetime.datetime.utcnow(),_id=None):
        self.date = date
        self._id = uuid.uuid4.hex() if _id is not None else _id
        Database.initialize()
		
    def register(self):
        email = raw_input("Enter Email")
        password = raw_input("Enter password")
        image = raw_input("Enter image name")
        mail = Userss(email,password,image)
        db = mail.get_by_email(email)
        if db is not None:
            self.login_user()
        else:
            Userss.registration(email,password,image)
            self.login_user()
    #the first method to run  the software
    def login_user(self):
        #users enter username and password
        print("plese enter user name and password to login")
        email = raw_input("Enter Email")
        password = raw_input("Enter password")
        if Userss.login_valid(email,password):
            self.ftpi()
        else:
            self.register()

    def ftpi(self):
        print("Enter ftp details to access and download files")
        ids = ["010010-99999","010014-99999","010015-99999","010020-99999"]
        station = raw_input("Enter stationId")
        startY = int(raw_input("Enter startYear"))
        endY = int(raw_input("Enter endYear"))


        dow =  Download()
        dow.ftpDownloader(station,startY,endY)

    @staticmethod
    def access_to_userAccount(self,_id):
        Data =  Database.find_one(Database_Collection,{"_id":_id})
        return Data

    @staticmethod
    def iflogin(self,user_name):
        Database.find_one(Database_Collection,{"name":user_name})
        if Data_Dasebase is not None:
            for data in Data_Database:
                return cls(**data)
    def CheckUsers():
        database = Database.find(Database_Collection,{})
        for data in database:
            return  data
    @classmethod
    def member(cls,contient,country):
        Data_Database = Database.find_one(Database_collection,{"country":country,"contient":contient})
        if Data_Database is not None:
            return CLS(**Data_Database)
        else:
            raise ErrorMessage.InputError("Country not found")

    def save_to_mongo(self):
        Database.insert("user",json())
    def json(self):
        return {
            "country_name":self.country,
            "continent":self.continent,
            "place_view":self.place_view
        }
