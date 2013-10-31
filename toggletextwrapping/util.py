# -*- coding: utf8 -*-
#
# util.py
# This file is part of Toggle Text Wrapping, a plugin for gedit
#
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

def connect_handlers(self, obj, signals, m, *args):
	HANDLER_IDS = self.HANDLER_IDS
	l_ids = getattr(obj, HANDLER_IDS) if hasattr(obj, HANDLER_IDS) else []

	for signal in signals:
		if type(m).__name__ == 'str':
			method = getattr(self, 'on_' + m + '_' + signal.replace('-', '_').replace('::', '_'))
		else:
			method = m
		l_ids.append(obj.connect(signal, method, *args))

	setattr(obj, HANDLER_IDS, l_ids)

def disconnect_handlers(self, obj):
	HANDLER_IDS = self.HANDLER_IDS
	if hasattr(obj, HANDLER_IDS):
		for l_id in getattr(obj, HANDLER_IDS):
			obj.disconnect(l_id)

		delattr(obj, HANDLER_IDS)

def block_handlers(self, obj):
	HANDLER_IDS = self.HANDLER_IDS
	if hasattr(obj, HANDLER_IDS):
		for l_id in getattr(obj, HANDLER_IDS):
			obj.handler_block(l_id)

def unblock_handlers(self, obj):
	HANDLER_IDS = self.HANDLER_IDS
	if hasattr(obj, HANDLER_IDS):
		for l_id in getattr(obj, HANDLER_IDS):
			obj.handler_unblock(l_id)
