class Error(object):
    def __init__(self,message):
        self.message = message

class IncorrectDatabaseStatment(Error):
        pass
