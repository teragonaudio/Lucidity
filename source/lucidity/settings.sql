CREATE TABLE IF NOT EXISTS `settings` (
  'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  'name' TEXT NOT NULL,
  'value' TEXT DEFAULT NULL
);

-- Default settings values
-- INSERT INTO `settings` (`name`, `value`) VALUES ('', '');
INSERT INTO `settings` (`name`, `value`) VALUES ('app.debug', '0');
INSERT INTO `settings` (`name`, `value`) VALUES ('gui.fullscreen', '0');
INSERT INTO `settings` (`name`, `value`) VALUES ('gui.doublebuf', '0');
INSERT INTO `settings` (`name`, `value`) VALUES ('gui.hwsurface', '0');
INSERT INTO `settings` (`name`, `value`) VALUES ('gui.opengl', '0');
INSERT INTO `settings` (`name`, `value`) VALUES ('midi.enable', '1');
