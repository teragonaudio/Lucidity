import os
import sqlite3

#noinspection PyDefaultArgument
class Database:
    def __init__(self, absolutePath:"str", schemaPath:"str"):
        self.absolutePath = absolutePath
        self.schemaPath = schemaPath

    def query(self, statement:"str", args:"list"=[], commit:"bool"=False): pass

#noinspection PyDefaultArgument
class Sqlite3Database(Database):
    def __init__(self, absolutePath:"str", schemaPath:"str"):
        Database.__init__(self, absolutePath, schemaPath)
        self._connection = self.getConnection(absolutePath)

    def getConnection(self, absolutePath:"str"):
        if not os.path.exists(absolutePath):
            self.createDatabase(absolutePath)
        return sqlite3.connect(absolutePath)

    def createDatabase(self, absolutePath:"str"):
        connection = sqlite3.connect(absolutePath)
        schemaFile = open(self.schemaPath, 'r')
        connection.executescript(schemaFile.read())
        schemaFile.close()
        connection.commit()
        connection.close()

    def query(self, statement:"str", args:"list"=[], commit:"bool"=False):
        cursor = self._connection.cursor()
        cursor.execute(statement, args)
        if commit:
            self._connection.commit()
        return cursor