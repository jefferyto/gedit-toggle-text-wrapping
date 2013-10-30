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

	TOGGLE_ACCELERATOR = '<Ctrl><Shift>B'

	DEFAULT_WRAP_MODE = Gtk.WrapMode.WORD # or Gtk.WrapMode.CHAR

	HANDLER_IDS = 'ToggleTextWrappingPluginHandlerIds'

	def __init__(self):
		GObject.Object.__init__(self)

	def do_activate(self):
		action_group = Gtk.ActionGroup('ToggleTextWrappingPluginActions')
		action_group.set_translation_domain('gedit')
		action = Gtk.ToggleAction('ToggleTextWrappingPluginToggle', _("Enable Text Wrapping"), _("Toggle text wrapping for the current document"), Gtk.STOCK_OK)
		action_group.add_action_with_accel(action, self.TOGGLE_ACCELERATOR)

		self._connect_handlers(action, ('activate',), 'toggle_action')

		manager = self.window.get_ui_manager()
		manager.insert_action_group(action_group, -1)
		ui_id = manager.add_ui_from_string(ui_str)

		self._ui_id = ui_id
		self._action = action
		self._action_group = action_group

		self.do_update_state()

	def do_deactivate(self):
		self._disconnect_handlers(self._action)

		manager = self.window.get_ui_manager()
		manager.remove_ui(self._ui_id)
		manager.remove_action_group(self._action_group)
		manager.ensure_update()

		self._ui_id = None
		self._action = None
		self._action_group = None

	def do_update_state(self):
		self._set_sensitivity()
		self._update_ui()

	def on_toggle_action_activate(self, action):
		view = self.window.get_active_view()
		if view:
			view.set_wrap_mode(self.DEFAULT_WRAP_MODE if action.get_active() else Gtk.WrapMode.NONE)

	def _set_sensitivity(self):
		self._action.set_sensitive(self.window.get_active_document() is not None)

	def _update_ui(self):
		view = self.window.get_active_view()
		self._action.set_active(view is not None and view.get_wrap_mode() != Gtk.WrapMode.NONE)

	def _connect_handlers(self, obj, signals, m, *args):
		HANDLER_IDS = self.HANDLER_IDS
		l_ids = getattr(obj, HANDLER_IDS) if hasattr(obj, HANDLER_IDS) else []

		for signal in signals:
			if type(m).__name__ == 'str':
				method = getattr(self, 'on_' + m + '_' + signal.replace('-', '_').replace('::', '_'))
			else:
				method = m
			l_ids.append(obj.connect(signal, method, *args))

		setattr(obj, HANDLER_IDS, l_ids)

	def _disconnect_handlers(self, obj):
		HANDLER_IDS = self.HANDLER_IDS
		if hasattr(obj, HANDLER_IDS):
			for l_id in getattr(obj, HANDLER_IDS):
				obj.disconnect(l_id)

			delattr(obj, HANDLER_IDS)

	def _block_handlers(self, obj):
		HANDLER_IDS = self.HANDLER_IDS
		if hasattr(obj, HANDLER_IDS):
			for l_id in getattr(obj, HANDLER_IDS):
				obj.handler_block(l_id)

	def _unblock_handlers(self, obj):
		HANDLER_IDS = self.HANDLER_IDS
		if hasattr(obj, HANDLER_IDS):
			for l_id in getattr(obj, HANDLER_IDS):
				obj.handler_unblock(l_id)
