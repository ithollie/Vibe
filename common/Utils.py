from passlib.hash import pbkdf2_sha512
import re

class utils(object):
	@staticmethod
	def hash_password(password):
		#hash_a_password
		return pbkdf2_sha512.encrypt(password)
	@staticmethod
	def hash_email(email):
		#hash_a_password
		return pbkdf2_sha512.encrypt(email)
	@staticmethod
	def check_hash_password(password,hash_password):
		hash = pbkdf2_sha512.verify(password,hash_password)
		return hash
	@staticmethod
	def check_hash_email(email,hash_email):
		hash = pbkdf2_sha512.verify(email,hash_email)
		return hash
	@staticmethod
	def email_is_valid(email):
		email_address_matcher =  re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
		if email_address_matcher.match(email):
			return True
		else:
			False
			
	@staticmethod
	def email_is_valid_check(email):
		email_address_matcher =  re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
		if email_address_matcher.match(email):
			return email
		else:
			return False

	@staticmethod
	def check_day(day):
		#day = birth[2:4]
		if day and day.isdigit():
			days = int(day)
			if day > 0 and days <= 31:
				return days
	@staticmethod
	def check_month(month):
		#month = brith[0:2]
		if month and month.isdigit():
			months = int(month)
			if months > 0 and months <= 12:
				return months
	@staticmethod
	def check_year(year):
		#yeah = birth[5:8]
		if year and year.isdigit():
			years = int(year)
			if years.__sizeof__() ==  4 and years > 2017:
				return years
