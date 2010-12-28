import os
import sqlite3

#noinspection PyDefaultArgument
class Database:
    def __init__(self, absolutePath:"str", schemaPath:"str"):
        self.absolutePath = absolutePath
        self.schemaPath = schemaPath

    def query(self, statement:"str", args:"list"=[], commit:"bool"=False): pass
    def verifyDatabase(self, absolutePath:"str", schemaPath:"str"): pass

#noinspection PyDefaultArgument
class Sqlite3Database(Database):
    def __init__(self, absolutePath:"str", schemaPath:"str"):
        Database.__init__(self, absolutePath, schemaPath)
        self._connection = self._getConnection(absolutePath, schemaPath)

    def _getConnection(self, absolutePath:"str", schemaPath:"str"):
        if not os.path.exists(absolutePath):
            self._createDatabase(absolutePath, schemaPath)
        else:
            self.verifyDatabase(absolutePath, schemaPath)
        return sqlite3.connect(absolutePath)

    def _createDatabase(self, absolutePath:"str", schemaPath:"str"):
        connection = sqlite3.connect(absolutePath)
        schemaFile = open(schemaPath, 'r')
        connection.executescript(schemaFile.read())
        schemaFile.close()
        connection.commit()
        connection.close()

    def verifyDatabase(self, absolutePath:"str", schemaPath:"str"):
        # TODO: Add missing columns from schema, max/min values
        pass

    def query(self, statement:"str", args:"list"=[], commit:"bool"=False):
        cursor = self._connection.cursor()
        cursor.execute(statement, args)
        if commit:
            self._connection.commit()
        return cursor