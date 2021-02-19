
from ftplib import FTP,error_perm
from common.database import Database
from  models import constants as ADMIN
from common.Utils import utils
from models.user.User import *
import datetime
import uuid
import os

class Master(object):
    def __init__(self,Email,password,date=datetime.datetime.utcnow(),_id=None):
        self.Email = Email
        self.password = password
        self.date = date
        self._id = uuid.uuid4().hex if _id is None else _id

    def setup(self):
        self.Email_user = raw_input("Enter user name please")
        self.user_password = raw_input("Enter user password")

        self.webA = raw_input("Enter the website")
        self.webP = raw_input("Enter the webpass")
        self.stid = input("Enter the stationId")
        self.staY = input("Enter startYear")
        self.endY = input("Enter endY")

        if self.Email_user is not None:
            if Master.login_user(self.Email_user,self.user_password) is not None:
                Master.host(self.webA,self.webP,self.stid,self.staY,self.endY)
        else:
            Master.registration_link(user_name,user_password)
    @staticmethod
    def host(weba,webp,stationId,startYear,endYear):
        ftp = FTP("ftp.pyclass.com")
        ftp.login(weba,webp)
        if not os.path.exists("c:\\in"):
            os.makedirs("C:\\in")
        os.chdir("c:\\in")
        for year in range(startYear,endYear+1):
            fullpath ='/Data/%s/%s-%s.gz' % (year,stationId,year)
            filename=os.path.basename(fullpath)
            try:
                with open(filename,'wb') as file:
                    ftp.retrbinary('RETR %s' % fullpath,file.write)
                    print("%s successfully downlaoded" % filename)
            except error_perm:
                    print("%s is not available" % filename)
                    os.remove(filename)
        ftp.close()
    @staticmethod
    def login_user(name,password):
        if Master.downlaod(name,password):
            return "that is good"
    @classmethod
    def admin(cls,admin):
        data = Database.find_one(ADMIN.COLLECTION,{"email":admin})
        return cls(**data)


    @classmethod
    def registration_link(cls,Email_user,user_password):
        check = Master.admin(Email_user)
        if check["email"] is None:
            registration = cls(Email_user,utils.hash_password(user_password))
            registration.save_to_mongo()
            return
        else:
            return False

    @staticmethod
    def downlaod(name,password):
        if name and password is not None:
            return True
        else:
            return False

    def json(self):
        return {"email":self.Email,"password":self.password,"_id":self._id}

    def save_to_mongo():
        Database.insert(ADMIN.COLLECTION,self.json())
