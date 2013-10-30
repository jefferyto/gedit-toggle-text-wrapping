# -*- coding: utf8 -*-
# Toggle Text Wrapping Gedit plugin
#
# This file is part of the Toggle Text Wrapping plugin for Gedit
# Copyright (C) 2008-2009 Christian Hartmann <christian.hartmann@berlin.de>
# Copyright (C) 2011 Francisco Franchetti <nixahn@gmail.com>
# Copyright (C) 2013 Jeffery To <jeffery.to@gmail.com>
# https://github.com/jefferyto/gedit-toggle-text-wrapping
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This plugin is intended to ease the setting of Text Wrap (aka Line Wrap,
# Word Wrap) by either a Keyboard Shortcurt (currently sticked to Shift-Ctrl-B),
# a new entry in the View Menu or by an Icon in the Toolbar. The use of either 
# option works as a toggle (de- or activate text wrap). The initial setting for 
# new or new opened files is taken from the setting in the Preferences dialog 
# and remembered per file as long thew file is open. 

# This plugin was developed for gedit 2 by Christian Hartmann at <christian.hartmann@berlin.de>. Parts of this plugin are based on the work of Mike Doty <mike@psyguygames.com>
# who wrote the infamous SplitView plugin. The rest is inspired from the Python
# Plugin Howto document and the Python-GTK documentation.

# CHANGELOG
# =========
# * 2008-10-10:
#   0.1 initial release for private use only
# * 2009-04-26:
#   0.2 changed filenames from textwrap to TextWrap as it conflicts with 
#   /usr/lib/python2.6/textwrap.py when loading the plugin. Unfortunately
#   i have no real clue what actualy is causing this conflict. This might
#   be reasoned by a change in the Gedit Python Plugin Loader, as this has
#   not been happening before upgrading gedit or a prerequisite of it through
#   an upgrade of my Ubuntu to 8.10 or 9.04. Added a couple documentst mainly
#   to ease the burdon of installation for gedit plugin beginners and made it
#   public available on my company website: http://hartmann-it-design.de/gedit
# * 2011-11-05:
#   migration to gedit 3 by Francisco Franchetti. things changed are
#   in the .py file
#   _ dont use the enums in capital letters; look up the numbers online and use those
#   _ gtk -> Gtk
#	_ add the do_ in front of activate, deactivate, update_state (not update_ui); a good practice would be to add it to the custom methods too
#   _ def statements don't have the window argument (defined for the class in the beginning)
#   _ import statements are different
#	_ class definition, init are different
#   _ delete first line with the !/dev...
#   in the .plugin file
#   _ [Gedit plugin] -> [Plugin]
#   _ IAge=3

# import basic requisites
from gi.repository import GObject, Gtk, Gdk, Gedit

# just a constant used in several places herein
prefix = "Plugin TextWrap "

# a common ui definition for menu and toolbar additions
ui_str = """<ui>
  <menubar name="MenuBar">
	<menu name="ViewMenu" action="View">
	  <placeholder name="ViewOps_2">
		<menuitem name="ToggleTextWrap" action="TTextWrap" />
	  </placeholder>
	</menu>
  </menubar>
  <toolbar name="ToolBar">
	<separator />
	<toolitem name="ToggleTextWrap" action="TTextWrap" />
  </toolbar>
</ui>
"""

# define the plugin class (helper class is not needed anymore cause gtk3 has windowactivatable)
class ToggleTextWrap(GObject.Object,Gedit.WindowActivatable):
	__gtype_name__= "ToggleTextWrap"
	window=GObject.property(type=Gedit.Window)

	def __init__(self):
		GObject.Object.__init__(self)

	def do_toggle_text_wrap(self, action):
		view = self.window.get_active_view()
		current_action = self._action_group.get_action("TTextWrap")
		if current_action.get_active():
			view.set_wrap_mode(2)
		else:
			view.set_wrap_mode(0)

	def do_activate(self):
		
		# Get initial state from text wrapping in this view (not available
		# on gedit startup but if plugin is enabled during the gedit session
		# and for what ever reason we do not have an update ui signal on init)
		view = self.window.get_active_view()
		try:
			current_wrap_mode = view.get_wrap_mode()
			# the order gives the numbers, starting at 0 for WRAP_NONE
			# typedef enum {
			# 	GTK_WRAP_NONE,
			# 	GTK_WRAP_CHAR,
			# 	GTK_WRAP_WORD,
			# 	GTK_WRAP_WORD_CHAR
			# } GtkWrapMode;
			if current_wrap_mode == 0:
				self._initial_toggle_state = False
			else:
				self._initial_toggle_state = True
		except:
			# Define default initial state for the plugin (should read this from the preferences file)
			self._initial_toggle_state = False
			# view.set_wrap_mode(0)	

		# Add "Toggle Text Wrap" to the View menu and to the Toolbar
		# Get the GtkUIManager
		self._manager = self.window.get_ui_manager()
		# Create a new action group
		self._action_group = Gtk.ActionGroup("GeditTextWrapPluginActions")
		self._action_group.add_toggle_actions([(
				"TTextWrap", 
				"gtk-ok", 
				_("Text Wrap"), 
				"<Ctrl><Shift>B", 
				_("Toggle Current Text Wrap Setting"), 
				self.do_toggle_text_wrap,
				self._initial_toggle_state)])
		# Insert the action group
		self._manager.insert_action_group(self._action_group)
		# Add my item to the "Views" menu and to the Toolbar
		self._ui_id = self._manager.add_ui_from_string(ui_str)
		# Debug merged ui
		self._manager.ensure_update()

	def do_deactivate(self):
		# Remove the ui
		self._manager.remove_ui(self._ui_id)
		self._ui_id = None
		# Remove action group
		self._manager.remove_action_group(self._action_group)
		self._action_group = None
		# ensure that manager updates
		self._manager.ensure_update()

	def do_update_state(self):
		view = self.window.get_active_view()
		self._action_group.set_sensitive(self.window.get_active_document() != None)
		# self._action_group.set_sensitive(bool(view and view.get_editable()))
		try:
			# Get initial state from word wrapping in this view (if any)
			current_wrap_mode = view.get_wrap_mode()
			# Get our action and set state according to current wrap mode
			current_action = self._action_group.get_action("TTextWrap")
			if current_wrap_mode == 0:
				current_action.set_active(False)
			else:
				current_action.set_active(True)
		except:
			return

		

#	def _console(self, vartext):
#		if self._DEBUG:
#			print prefix, vartext	

