class Blogs(object):
    def __init__(self):
        pass
    @staticmethod
    def UserExist(user):
        UserTrue = Users.get_by_email(user)
        if UserTrue is not None:
            return UserTrue
        else:
            return False

	@staticmethod
	def Blogtitle(titleblog):
		data = Database.find("blogs", {"titleblog":titleblog})
		if data is not None:
			return data
		else:
			return False
	@staticmethod
	def get_by_id(_id):
		data = Database.find_one("blogs",{"_id":_id})
		if data is not None:
			return data
		else:
			raise UserErrors.UserNotExistError("user does not exit")
