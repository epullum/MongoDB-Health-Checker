'''
Created on Dec 20, 2018

@author: edwardpullum
'''


import pymongo as py


class Database:
    
    def __init__(self):
        self.client=py.MongoClient()
        self.collections = []
        self.databases = []
        
        
    
    def getDatabases(self):
        cursor = self.client.list_database_names()
        for c in cursor:
            self.databases.append(c)
        return self.databases

    def getCollections(self, db):
        cursor = self.client[db].list_collection_names()
        for c in cursor:
            self.collections.append(c)
        return self.collections
    
    def getLastError(self, db):
        cursor = self.client[db].command("getLastError")
        #for c in cursor:
        return cursor
    
    def getBuildinfo(self, db):
        cursor = self.client[db].command("buildinfo")
        return cursor
    
    def getDBStats(self, db):
        cursor = self.client[db].command("dbstats")
        return cursor
    
    def getCollStats(self, db, coll):
        cursor = self.client[db].command("collstats", coll)
        cursor.pop("indexDetails")
        cursor.pop("wiredTiger")
        return cursor
    
    def getTransactionCount(self, db = "admin"):
        cursor = self.client[db].command("serverStatus")["metrics"]["document"]
        return cursor
    
    def getConnectionCount(self, db="admin"):
        cursor = self.client[db].command("serverStatus")["connections"]
        return cursor
    
    def viewConnectionInfo(self, db="admin"):
        cursor = self.client[db].current_op(True)
        return cursor