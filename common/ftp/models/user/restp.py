from common.database import Database
from models.passrest.mail.sendemail import Mail
from models import constants as UserConstants
class Restp(object):
	def __init__(self,email):
		self.email =  email
		self.netmail = self.sendmail(self.email,self.json()['url'],self.json()['subject'])

	@staticmethod
	def checkmail(email):
		data =  Database.find_one(UserConstants.COLLECTION,{"email":email})
		if data is not None:
			return data
		else:
			return None;
			
	@staticmethod
	def checkmliame(email):
		data =  Database.find(UserConstants.COLLECTION,{})
		for datas in data:
			dat = datas["email"] 
			if dat == email:
				return email
			
	@staticmethod
	def Update(emailnow,emailupdated):
		if emailnow is not None:
	 		Database.updates(UserConstants.COLLECTION,{"email":emailnow},{"$set": {"email":emailupdated}} )
	@classmethod
	def check_mail(self,email):
		namail = self.checkmliame(email)
		data =  Database.find_one(UserConstants.COLLECTION,{"email":namail})
		if data is not None:
			return data
		else:
			return False
		
	def Valid(self):
			cridential={"email":self.check_mail(self.email)['email'],"id":self.check_mail(self.email)['_id']}
			return cridential
	@staticmethod
	def sendmail(email,url,subject):
		mail = Mail(email,url,subject)
		if mail is not None:
			mail.send()

	def json(self):
		return  {"url":"http://127.0.0.1:8000/change_system_password/change_users_password/"+self.Valid()['email']+"/"+self.Valid()['id'],"subject":"please rest password"}
