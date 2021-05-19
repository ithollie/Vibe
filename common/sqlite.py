import sqlite3
import os

class sqlite(object):
	Uri = sqlite3.connect('tutorial.db')
	connection = Uri.cursor()
	def __init__(self):
		pass
	def create_table(self):
		conn = sqlite.connection.execute("CREATE TABLE login(EMAIL VARCHAR, USER VARCHAR, PIN INT)")
		if conn is not None:
			connection.commit()
			connection.close()
	@staticmethod
	def insert(email,user,pin):
		connection = sqlite.connection.execute("INSERT INTO login (EMAIL, USER , PIN) VALUES(?, ?, ? )", (email,user,pin))
		if connection is not None:
			connection.commit()
			connection.close()
		else:
			print("database created")

	def enter_dynamic_data():
		lang = input("What language? ")
		version = float(input("What version? "))
		skill = input("What skill level? ")
		connection = sqlite.connection.execute("INSERT INTO example (Language, Version, Skill) VALUES (?, ?, ?)", (lang, version, skill))
		connection.commit()
		connection.close()
		
	@staticmethod
	def read_from_database():
		sql = "SELECT * FROM login"
		for row in sqlite.connection.execute(sql):
			print(row)

