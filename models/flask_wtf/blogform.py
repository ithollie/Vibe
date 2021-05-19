class  BlogForm(object):
    def __init__(self, author,title, email, _id, description, filename):
        self.author = author
        self.email   = email 
        self.title   = title
        self.description  = description
        self.filename     = filename
        self._id     = _id
    
    @staticmethod
    def message(message=None):
        if message is not None:
            return  message