from common.database import Database

class Comments(object):
    def __init__(self,titleBlog, comment, email , _id):
      self.title =  titleBlog
      self.comment  = comment
      self.email    = email
      self._id      = _id
      
    def save_to_mongo(self):
        data = Database.find_one("blogs", {"title":self.title})['numberOfcomments']
        Database.insert("comments"+self.title, self.json());
        Database.updates("blogs",{"title":self.title},{"$set":{"numberOfcomments":data + 1}})
    
    def json(self):
        return {
            
            "title":self.title,
            "email":self.email,
            "id":self._id,
            "comment":self.comment
        }