import uuid
import datetime
import requests
import re
from bs4 import BeautifulSoup
from sendemail import Mail
from common.database import Database
import constants as AlertConstants
#from src.models.items.item import Item

__author__ = 'jslvtr'


class Alert(object):
	def __init__(self,_id=None):
		self.last_checked = datetime.datetime.utcnow()
		self._id = uuid.uuid4().hex if _id is None else _id

	def __repr__(self):
		return "<Alert for {} on item {} with price {}>".format(self.user_email)

	def load_price(self):
		url = "http://127.0.0.1/?page=catalogue&category=3"
		request = requests.get(url)
		content = request.content
		soup = BeautifulSoup(content, "html.parser")
		element = soup.find("div", {"class":"catalogue_wrapper_right"})
		string_price = element.text.strip()

		pattern = re.compile("(\d+.\d+)")
		match = pattern.search(string_price)
		self.price = float(match.group())

		return self.price

	@classmethod
	def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
		last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
		return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,{self.last_check_database:
													   {"$lte": last_updated_limit},
											  "active": True
												   })]
	def send_email_if_price_reached(self):
		price = self.load_price()
		price_limit = 18.94
		if  price < price_limit:
			mail = Mail("ithollie@yahoo.com","price reached the limited","from admain")
			mail.send()
