CREATE TABLE IF NOT EXISTS `locations` (
  'id' INTEGER NOT NULL PRIMARY KEY,
  'absolutePath' TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS `files` (
  'id' INTEGER NOT NULL PRIMARY KEY,
  'location' INTEGER NOT NULL,
  'relativePath' TEXT NOT NULL,
  'title' TEXT DEFAULT NULL,
  'timeInSeconds' INTEGER NOT NULL,
  'tempo' NUMERIC(3,2) DEFAULT NULL,
  'startTimeInSeconds' FLOAT DEFAULT NULL,
  'stopTimeInSeconds' FLOAT DEFAULT NULL,
  'artist' INTEGER DEFAULT NULL,
  'album' TEXT DEFAULT NULL,
  'albumArtist' INTEGER DEFAULT NULL,
  'lastModified' DATE NOT NULL,
  'lastPlayed' DATE DEFAULT NULL,
  'playCount' INTEGER DEFAULT '0');

CREATE TABLE IF NOT EXISTS `artists` (
  'id' INTEGER NOT NULL PRIMARY KEY,
  'name' TEXT NOT NULL);
