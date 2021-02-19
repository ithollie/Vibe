class RegisterForm():
    def __init__(self, firstname, lastname, email ,password, repectPassword,  filename):
        self.firstname = firstname
        self.lastname   = lastname 
        self.email  = email
        
        self.password = password
        self.repectPassword  =  repectPassword
        self.filename     = filename
        
    def  PasswordMatch(self, password,  repectPassword):
        if password  == repectPassword:
            return  True
        else:
            return False
        
    def notEmpty(self):
        if self.filename:
            return True
        else:
            return  False
    