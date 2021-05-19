from common.database import Database
import uuid
import random
import re

class Blogs(object):
    def __init__(self,author,  titleblog ,email,  description, filename=None, userImage=None):
        self.author = author
        self.titleblog  =  titleblog
        self.email      =  email
        self.description  =  description
        self.filename     =  filename
        self.userImage    =  userImage
        self.soon   =  "soon.png"
        self.likes        =  0
        self.dislikes     =  0
        self.add          =  "3781476276"
        self.checker      =   self.add
        self.numberOfcomments =  0  
        self.image()
        self.getImage()
        self.unid =  self.uniqueid()
        self.seed =  random.getrandbits(32)
     
        
    
    
    def uniqueid(self):
        while True:
            self.seed += 1
            yield self.seed
            
    def  getImage(self):
        if self.userImage  is not None:
            self.userImage =  self.userImage
        else:
            self.userImage  = self.soon
            
    def save_to_mongo(self):
    		Database.insert("blogs",self.json())
    		Database.insert(self.author,self.json())
    		
    def image(self):
        if self.filename  is not None:
            self.filename =  self.filename
        else:
            self.filename  = self.soon
            
    def json(self):
            return {
                "author":self.author,
                "title":self.titleblog,
                "email":self.email,
                "uniqueId":self.seed,
                "checker":self.checker + self.email,
                "description":self.description,
                "img":self.filename,
                "userImage":self.userImage,
                "likes":self.likes,
                "dislikes":self.dislikes,
                "numberOfcomments":self.numberOfcomments
            }

