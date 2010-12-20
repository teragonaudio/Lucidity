from lucidity.database import Sqlite3Database
from lucidity.paths import PathFinder

class Setting:
    def __init__(self, name:"str", value:"str"):
        self.name = name
        self.strValue = value
        self.intValue = int(value)
        self.floatValue = float(value)

class Settings:
    def __init__(self, absolutePath):
        self.absolutePath = absolutePath
        schemaLocation = PathFinder.findModule("settings.sql")
        self._database = Sqlite3Database(absolutePath, schemaLocation)
        self._settingsKeys = self._readSettings(self._database)

    def _readSettings(self, database:"Database"):
        result = {}

        cursor = database.query("SELECT `name`, `value` FROM `settings`")
        for (name, value) in cursor:
            result[name] = Setting(name, value)

        return result

    def get(self, key:"str"):
        if key in self._settingsKeys:
            return self._settingsKeys[key]
        else:
            return None

    def getString(self, key:"str"):
        result = self.get(key)
        if result is not None:
            return result.strValue
        else:
            return ""

    def getInt(self, key:"str"):
        result = self.get(key)
        if result is not None:
            return result.intValue
        else:
            return -1

    def getFloat(self, key:"str"):
        result = self.get(key)
        if result is not None:
            return result.floatValue
        else:
            return -1.0

    def put(self, key:"str", value):
        if key in self._settingsKeys:
            self._database.query("UPDATE `settings` SET `value` = ? WHERE `name` = ?", [str(value), key], True)
        else:
            raise Exception("Unknown setting '" + key + "'")