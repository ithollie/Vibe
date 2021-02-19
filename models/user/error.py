class UserError(Exception):
	def __init__(self,message):
		self.message = message
class UserNotExistError(UserError):
	pass 
	
	
class UserAreadyRegisteredError(UserError):
	pass
	
class InvalideEmailError(UserError):
	pass
	
class IncorrectPasswordError(UserError):
	pass
	
class IncorrectDatabaseStatment(UserError):
	pass