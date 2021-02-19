class  BlogForm(object):
    def __init__(self, author,title, email, _id, description, filename, vibeusers):
        self.author = author
        self.email   = email 
        self.title   = title
        self.description  = description
        self.filename     = filename
        self.vibeusers    = vibeusers
        self._id     = _id
    
    @staticmethod
    def message(message=None):
        if message is not None:
            return  message