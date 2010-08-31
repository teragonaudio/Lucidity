__author__ = 'nik'

##+
# @section About Lucidity
# Lucidity is software for performing digital music.  It allows the DJ to mix in both
# realtime and to lay out their mixes a bit in advance.  Lucidity is an uncompromising
# approach to digital media, and aims to take full advantage of the laptop as a
# performance tool.
#
# The fundamental idea behind Lucidity is that the DJ is planning their mixes out
# a bit in advance, but not too much.  The amount of preparation time spent in the
# software itself is minimal, allowing you to focus instead on the music.  The interface
# resembles a software sequencer, but behaves much differently.  Place the music on the
# grid, and moves left to the playhead.  While the track is playing, you have time to
# find your next several tracks and lay them out on the grid.  Effects and filtering can
# be applied to your transitions in advance, but still manipulated in realtime.
#
# Navigation in Lucidity is designed to be simple and quick, and allows for powerful
# MIDI mapping in comfortably customize the software.  Lucidity's end goal is to be
# fluid and invisible; an unobtrusive way to play digital media with infinite
# possibilities.
#
# @section Main Window
# Lucidity has only one window, and does not have tabs, hidden views, or any unseen
# user interface elements.  What you see on the main screen is what you get.  Other
# windows, such as those used for configuring channels or browsing for music, appear
# as pop-up overlays which are dismissed with the escape key (ESC).
#
# The main window has three sections: a toolbar, the channel grid, and the browser bar.
#
# <ul>
# <li><b>The Toolbar</b> contains buttons used for navigating around the software
# and editing operations.  It also contains buttons used for accessing the preferences
# and the current playback state.</li>
# <li><b>The Channel Grid</b> takes up most of the space in the main window, and is
# where music is placed to be played.</li>
# <li><b>The Browser Bar</b> contains panels used to browse for music and effects, and
# also some status indication icons.
# </ul>
#
# @subsection Playing Music
# When Lucidity first starts up, it will ask you for a location where you store your
# digital music.  Your music directory will be scanned, and automatically rescanned
# on startup.  Likewise, Lucidity will scan your system audio plug-ins when starting
# up.  These scans are always performed in the background, and their status can be
# seen in the music browser panel and the effects panel in the browser bar.
#
# After Lucidity has scanned your files, it's ready to go.  Now you can browse for
# music by clicking on the music browser panel, which is also accessible by pressing
# the spacebar for quick access.  The browser popup shows all of your music, and you
# can filter the results by simply starting to type a search term.  The browser panel
# considers both the filename and metadata when searching, and songs which you play
# more often will be shown nearer to the top.  If you decide that you want a fresh
# start, you can reset Lucidity's search history in the preferences.
# @subsection Browsing For Music
#
# When the music browser popup is open, the up/down buttons in the toolbar can be
# used to select tracks.  The right arrow button selects a track and closes the music
# browser, and the cue button previews the song, and you would expect. Likewise, the
# same keystrokes and assigned MIDI mappings of the navigation buttons work in the
# music browser.
#
# Once you have selected a track, you can now insert it into the channel grid by doing
# any of the following:
#
# <ul>
# <li>Clicking the insert button in the upper right-hand corner of the music panel</li>
# <li>Dragging the music panel into the channel grid with the mouse</li>
# <li>Pressing the "enter" key to place the track at the cursor point</li>
# <li>Pressing a MIDI key which you have assigned to the insert button</li>
# </ul>
#
# You can insert tracks on top of each other in the channel grid, and they will appear
# stacked.  Stacking tracks provides a convenient way to add loops on top of a track,
# or to quickly drop a new track on an old one.  However, the stacked tracks will simply
# play back together when they reach the playhead, so you lose the ability to filter
# or mix them separately.  Similarly, editing operations are applied to all items in
# the stack, so be careful about placing items on top of each other.  If you accidentally
# place something on the grid where you didn't mean to, you can move it either by dragging
# it with the mouse, or you can undo the operation by pressing the undo button in the
# toolbar.
#
# @subsection Navigation
# The first group of buttons in the button bar manipulate the cursor, which is the
# empty rectangle visible in the channel grid.  These buttons move the cursor around
# the current channel grid and to preview playback at the cursor point.  When the cursor
# is at the far right-hand side of the screen, moving it further to the right will zoom
# the channel grid out, allowing you to see and plan ahead further into the future.
# Lucidity doesn't limit how far out you can zoom in terms of time, but rather in terms
# of screen size.  However, even modestly-sized laptops with lower screen resolutions
# can zoom out several minutes in advance.
#
# If you move the cursor back to the left after zooming out, then Lucidity will zoom back
# in.  But, if you inserted more music to the right, then Lucidity will slowly zoom back
# in as the music reaches the playhead.  Basically, Lucidity keeps everything you've placed
# on the screen in plain view.  However, Lucidity does not shrink to zero if all music has
# been played -- it keeps you zoomed out far enough to at least
#
# Likewise, moving the cursor down past the last channel will insert a new channel into
# the grid.  As with zooming to the right, channels are automatically removed when the music
# placed there has finished playing.  Lucidity keeps at least eight channels in the grid
# at all times, but this value can be configured in the preferences.  Also, Lucidity will
# remember any MIDI mappings for extra channels you have added, even if they are removed
# from the screen during playback.
#
# @subsection Editing Music
# @subsection Editing Operations
# @subsection Filtering and Mixing
# @subsection Applying Effects
# @section MIDI Mapping
# @section Key Commands
# @include KeyCommands.py
#
# @section Configuring Lucidity
# @subsection Main Preferences
# @subsection Sound Card Configuration
# @subsection MIDI Device Configuration
# @subsection Plug-In Configuration
