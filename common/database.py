import pymongo
import urllib 
import os

class Database(object):
    DATABASE = None

    def __init__(self):
        pass
    
    @staticmethod
    def initialize():
            
            username = urllib.parse.quote_plus('hawaibrahB1a1')
            password = urllib.parse.quote_plus('hawaibrahB1a1')
            
            #cli = pymongo.MongoClient("mongodb://%s:%s@cluster0.scnlr.mongodb.net/vibeDatabase?retryWrites=true&w=majority" % (username, password))
            client = pymongo.MongoClient("mongodb+srv://%s:%s@cluster0.scnlr.mongodb.net/vibeDatabase?retryWrites=true&w=majority" % (username, password))
            Database.DATABASE = client['vibeDatabase']
            
    @staticmethod
    def connectUrl(uri_connection, online_connection):
        if online_connection is not None:
            return online_connection

    @staticmethod
    def collectionexists(collection):
        if Database.DATABASE[collection]:
            return True
        else:
            return False

    @staticmethod
    def dropCollection(collection):
        Database.DATABASE[collection].drop()


    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def updates(collection, data, data1):
        Database.DATABASE[collection].update(data, data1)

    @staticmethod
    def delete(collection, data):
        Database.DATABASE[collection].remove(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
