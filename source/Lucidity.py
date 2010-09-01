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
# Lucidity is a bit different than other DJ software when it comes to playback.  When
# you start up Lucidity, you will notice that the channel grid is already moving and
# that playback has begun.  Lucidity is designed to always be playing, and it treats
# the act of stopping playback more seriously than other software.
#
# If you want to pause Lucidity for a moment, you can double-click the play/pause
# button in the upper right-hand corner of the screen.  If you click it once, this
# button lights up briefly to let you know that it's listening, but that you must
# really mean it before you ask it to stop.  Likewise, playback can be restarted by
# double-clicking this button.
#
# Lucidity also has a key command for playing and pausing as well, but it's not what
# you would expect.  Rather than using the largest key on the entire keyboard for an
# action that is usually performed only twice during one performance, and in the worst
# case pressed by accident during a performance, Lucidity uses the space bar for
# something more useful: searching.  Pressing the space bar brings up the music browser
# and allows you to find music to insert into the set.  To pause or resume playback,
# press ctrl+p instead.
#
# @subsection Browsing For Music
# After Lucidity has scanned your files, you can browse for music by clicking on the
# music browser panel, which is also accessible by pressing the spacebar for quick
# access.  The browser popup shows all of your music, and you can filter the results
# by simply starting to type a search term.  The browser panel considers both the
# filename and metadata when searching, and songs which you play more often will be
# shown nearer to the top.  If you decide that you want a fresh start, you can reset
# Lucidity's search history in the preferences.
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
# When inserting music into the channel grid, the tempo of the track is automatically
# matched to the global tempo by repitching.  When Lucidity scans your music library,
# it performs BPM detection on all tracks, saving this information into an internal
# library, along with the start and stop points.  Lucidity can also save this
# information to the digital metadata, but this is not enabled by default and must be
# switched on in the preferences.
#
# If you notice that Lucidity has mis-detected the tempo or starting/stopping time
# of a song, you should correct this by editing the song's metadata in a media player
# such as iTunes.
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
# When looming out, Lucidity uses a logarithmic zooming algorithm which allows you to see
# the tracks on the left hand side of the screen more clearly while still zoomed out.
# This allows you to continue planning your set in advance while easily seeing what is
# currently playing.  However, at the default resolution, the logarithmic zoom is not
# noticeable.
#
# If you move the cursor back to the left after zooming out, then Lucidity will zoom back
# in.  But, if you inserted more music to the right, then Lucidity will slowly zoom back
# in as the music reaches the playhead.  Basically, Lucidity keeps everything you've placed
# on the screen in plain view.  However, Lucidity does not shrink to zero if all music has
# been played -- it keeps you zoomed out far enough to at least see a few minutes of music.
#
# Likewise, moving the cursor down past the last channel will insert a new channel into
# the grid.  As with zooming to the right, channels are automatically removed when the music
# placed there has finished playing.  Lucidity keeps at least eight channels in the grid
# at all times, but this value can be configured in the preferences.  Also, Lucidity will
# remember any MIDI mappings for extra channels you have added, even if they are removed
# from the screen during playback.
#
# @subsection Editing Music
# Lucidity has only a few editing operations, which are all visible in the toolbar to
# the right of the navigation controls.  Immediately to the right of the navigation
# controls are the old favorites undo/redo, and to the right of these are the block
# operations.
#
# All of the editing operations apply to the space selected by the cursor, or if no
# selection is made, then the cursor itself.  The cursor represents a space as wide as
# global quantization, which is set in the lower right-hand corner of the software in
# the browser bar, next to the tempo.  By default, this value is one bar of music.
#
# The first button in this panel allows one to make a selection.  When pressed (either
# by clicking, pressing the shift key, or pressing a MIDI-assigned key) and held down,
# move the cursor to select a given area of audio.  The selected area will appear with
# a transparently colored overlay until an operation is performed on the selection, or
# until another selection is made.  You can also quickly press and release the select
# button again to deselect the current selection.
#
# To the right of select is delete, which removes the current selection.  If no selection
# has been made, then delete will remove the entire track underneath the cursor.  But
# fear not!  If you press delete by mistake on top of a currently playing track, it will
# continue to play the last block of audio currently at the playhead.  The amount of
# audio played here is determined by the value of the global quantize, which is also the
# width of the cursor.  At the default setting of one bar, this gives you enough time to
# quickly hit undo and restore the track.  If you don't manage to undo the delete by the
# time the last block of audio is finished playing, then there will be silence.  However,
# you can still press undo, which will insert the track back into the channel set starting
# exactly at the point where the last block finished playing.
#
# Next to the delete button is the copy/clone button.  When pressed, it will first copy
# the area under the selection to the copy buffer, and move the cursor one block past
# the end of the selection.  Now when pressed again, it will paste the contents of the
# copy buffer at the cursor point.  In this manner, you can easily cut a loop out of a
# track and make several copies of it, building up entire sequences by copying and
# repasting.
#
# Finally, there is the bounce button to the right of copy/clone.  This button allows you
# to export selections of audio to disk for future playback.  While Lucidity itself has
# no concept of saving or opening documents, you can save small chunks of audio in an
# arrangement for future use by bouncing them down as loops.  The default save location
# and format options for bounced items can be set in Lucidity's preferences.  When pressed,
# the bounce button will display a small popup window underneath it where you can enter
# a filename, which has by default a suggested filename based on the current selection.
# As the suggested filename is selected, you can simply start typing if you would like
# something else, or you can press the escape key or bounce key again to cancel the bounce.
#
# To save the bounce, either press the return key after choosing a filename, or click the
# OK button in the filename popup window.
#
# @subsection Filtering and Mixing
# Lucidity allows one to mix tracks either in realtime or in advance, but one should
# keep in mind that these actions are performed differently.  Mixing actions applied
# in advance actually work the same way as applying effects, but the actual effects
# applied are simply mixing preset scripts.  For more information, please refer to the
# "Applying Effects" section.  This section refers only to mixing in realtime.
#
# In Lucidity, each channel is equipped with a basic mixer and volume control.  These
# controls can be seen to the left of the playhead.  Each channel has a small equalizer
# display which shows a preview of the current mixer settings, and beneath it a volume
# slider which also shows the current track volume.  The volume slider can be manipulated
# with the mouse, but to access the mixer controls, one must click on the equalizer's
# preview image.  When doing this, then a small popup is displayed with a larger version
# of the volume slider, and each of the equalizer knobs.
#
# While it is possible to mix using only the mouse, Lucidity was designed with the idea
# that laptop DJ's perform with at least one MIDI device, as knobs are a much more
# comfortable way to mix than the keyboard/mouse.  So, the mixer panel is primarily an
# interface for one to access the various mixing controls to map them to a controller
# (see the section about MIDI Mapping for more information).
#
# The mixer in each channel is not configurable, but offers a complete selection of
# familiar filters.  The largest four knobs in the middle of the panel configure a
# four-band equalizer, with configurable frequency cutoffs, which are accessible with
# a set of smaller knobs directly above each respective frequency band.
#
# To the right and left ends of the four-band equalizer sit two slightly smaller knobs,
# which are for high-pass and low-pass filtering, respectively.  The high-pass and
# low-pass filter also have a smaller knob above them, which controls the sidechain
# signal gain.  By default, this knob is disabled and set to -Infinity dB.  When
# enabled, this knob determines the strength of the sidechain subtracted signal which
# is re-added to the input signal.
#
# This filter allows one to play the lower or upper parts of a track but to subtract
# out frequencies present on all other tracks.  The end result allows for a very clean
# and precise method for filtering out basslines, kickdrums, or hat lines by playing
# through only the parts of a track which are not present in all other tracks.
#
# @subsection Applying Effects
#
# @section MIDI Mapping
#
# @section Key Commands
# @include KeyCommands.py
#
# @section Configuring Lucidity
#
# @subsection Main Preferences
#
# @subsection Sound Card Configuration
#
# @subsection MIDI Device Configuration
#
# @subsection Plug-In Configuration
#

