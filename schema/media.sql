CREATE TABLE IF NOT EXISTS `locations` (
  'id' INTEGER NOT NULL PRIMARY KEY,
  'absolutePath' TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS `files` (
  'id' INTEGER NOT NULL PRIMARY KEY,
  'location' INTEGER NOT NULL,
  'filename' TEXT NOT NULL,
  'title' TEXT NOT NULL,
  'timeInSeconds' INTEGER NOT NULL,
  'tempo' NUMERIC(3,2) NOT NULL,
  'startTimeInSeconds' FLOAT DEFAULT '0',
  'stopTimeInSeconds' FLOAT DEFAULT '0',
  'artist' INTEGER NOT NULL,
  'album' TEXT DEFAULT NULL,
  'albumArtist' INTEGER NOT NULL,
  'lastModified' DATE NOT NULL,
  'lastPlayed' DATE DEFAULT NULL,
  'playCount' INTEGER DEFAULT '0');

CREATE TABLE IF NOT EXISTS `artists` (
  'id' INTEGER NOT NULL PRIMARY KEY,
  'name' TEXT NOT NULL);
