# -*- coding: utf8 -*-
#
# toggletextwrapping.py
# This file is part of Toggle Text Wrapping, a plugin for gedit
#
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

from gi.repository import GObject, Gtk, Gedit

ui_str = """<ui>
	<menubar name="MenuBar">
		<menu name="ViewMenu" action="View">
			<placeholder name="ViewOps_2">
				<menuitem name="ToggleTextWrappingMenuItem" action="ToggleTextWrappingAction" />
			</placeholder>
		</menu>
	</menubar>
	<toolbar name="ToolBar">
		<separator />
		<toolitem name="ToggleTextWrappingToolItem" action="ToggleTextWrappingAction" />
	</toolbar>
</ui>
"""

class ToggleTextWrappingPlugin(GObject.Object, Gedit.WindowActivatable):
	__gtype_name__ = 'ToggleTextWrappingPlugin'

	window = GObject.property(type=Gedit.Window)

	TOGGLE_ACTION = 'ToggleTextWrappingAction'

	TOGGLE_ACCELERATOR = '<Ctrl><Shift>B'

	def __init__(self):
		GObject.Object.__init__(self)

	def do_toggle_text_wrap(self, action):
		view = self.window.get_active_view()
		current_action = self._action_group.get_action(self.TOGGLE_ACTION)
		if current_action.get_active():
			view.set_wrap_mode(2)
		else:
			view.set_wrap_mode(0)

	def do_activate(self):
		action_group = Gtk.ActionGroup("GeditTextWrapPluginActions")
		action_group.add_toggle_actions([(
				self.TOGGLE_ACTION,
				"gtk-ok",
				_("Text Wrap"),
				self.TOGGLE_ACCELERATOR,
				_("Toggle Current Text Wrap Setting"),
				self.do_toggle_text_wrap,
				False)])

		manager = self.window.get_ui_manager()
		manager.insert_action_group(action_group, -1)
		ui_id = manager.add_ui_from_string(ui_str)

		self._ui_id = ui_id
		self._action_group = action_group

		self.do_update_state()

	def do_deactivate(self):
		manager = self.window.get_ui_manager()
		manager.remove_ui(self._ui_id)
		manager.remove_action_group(self._action_group)
		manager.ensure_update()

		self._ui_id = None
		self._action_group = None

	def do_update_state(self):
		view = self.window.get_active_view()
		self._action_group.set_sensitive(self.window.get_active_document() != None)
		# self._action_group.set_sensitive(bool(view and view.get_editable()))
		try:
			# Get initial state from word wrapping in this view (if any)
			current_wrap_mode = view.get_wrap_mode()
			# Get our action and set state according to current wrap mode
			current_action = self._action_group.get_action(self.TOGGLE_ACTION)
			if current_wrap_mode == 0:
				current_action.set_active(False)
			else:
				current_action.set_active(True)
		except:
			return
