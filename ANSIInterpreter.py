#!/usr/bin/python3
#
#	screen2html - Convert ANSI-color containing terminal output to HTML.
#	Copyright (C) 2017-2017 Johannes Bauer
#
#	This file is part of screen2html.
#
#	screen2html is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	screen2html is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with screen2html; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>
#

import sys
import re

class ANSIInterpreter(object):
	_ESCAPE_CONTROL_SEQUENCE_RE = re.compile("\x1b(\[(?P<args_csi>.*?)(?P<cmd_csi>[A-Za-z])|(?P<cmd_tabset>H +))")

	def __init__(self, default_fg_color = 7, default_bg_color = 0):
		self._default_fg_color = default_fg_color
		self._default_bg_color = default_bg_color
		self._attrs = None
		self._reset_terminal()
		self._output = [ ]
		self._active_classes = None
		self._used_classes = set()
		self._set_attributes()

	def _reset_terminal(self):
		self._attrs = {
			"bright":				False,
			"underline":			False,
			"italics":				False,
			"high_intensity_fg":	False,
			"high_intensity_bg":	False,
			"fgcolor":				self._default_fg_color,
			"bgcolor":				self._default_bg_color,
			"tabsize":				8,
		}

	@property
	def html(self):
		return "".join(self._output)

	def _add_text(self, text):
		text = text.replace("<", "&lt;")
		text = text.replace(">", "&gt;")
		self._output.append(text)

	def _get_classes(self):
		fg_col = self._attrs["fgcolor"]
		bg_col = self._attrs["bgcolor"]
		if self._attrs["bright"]:
			fg_col += 8

		classes = [ ]
		if self._attrs["underline"]:
			classes.append("underline")
		if self._attrs["italics"]:
			classes.append("italics")
		if self._attrs["high_intensity_fg"]:
			classes.append("F%d" % (fg_col))
		else:
			classes.append("f%d" % (fg_col))
		if self._attrs["high_intensity_bg"]:
			classes.append("B%d" % (bg_col))
		else:
			classes.append("b%d" % (bg_col))
		return classes

	def _set_attributes(self):
		new_classes = self._get_classes()
		if new_classes != self._active_classes:
			if self._active_classes is not None:
				self._output.append("</span>")
			self._used_classes |= set(new_classes)
			self._output.append("<span class=\"%s\">" % (" ".join(new_classes)))
			self._active_classes = new_classes


	def _interpret_command_csi(self, command):
		if command["args"] == "":
			command["args"] = "0"
		if command["cmd"] == "m":
			args = command["args"].split(";")
			changed_attrs = { }
			for arg in args:
				arg = int(arg)
				if arg == 0:
					self._reset_terminal()
				elif arg == 1:
					self._attrs.update({ "bright": True })
				elif arg == 3:
					self._attrs.update({ "italics": True })
				elif arg == 4:
					self._attrs.update({ "underline": True })
				elif arg == 22:
					self._attrs.update({ "bright": False })
				elif arg == 23:
					self._attrs.update({ "italics": False })
				elif arg == 24:
					self._attrs.update({ "underline": False })
				elif arg in [ 7, 27 ]:
					# Invert / cancel invert
					self._attrs.update({ "bgcolor": self._attrs["fgcolor"], "fgcolor": self._attrs["bgcolor"] })
				elif 30 <= arg <= 37:
					self._attrs.update({ "fgcolor": arg - 30 })
				elif arg == 39:
					self._attrs.update({ "fgcolor": self._default_fg_color })
				elif 40 <= arg <= 47:
					self._attrs.update({ "bgcolor": arg - 40 })
				elif arg == 49:
					self._attrs.update({ "bgcolor": self._default_bg_color })
				elif 90 <= arg <= 97:
					self._attrs.update({ "fgcolor": arg - 90, "high_intensity_fg": True })
				elif 100 <= arg <= 107:
					self._attrs.update({ "bgcolor": arg - 100, "high_intensity_bg": True })
				else:
					print("Warning: Unable to interpret CSI 'm' argument %d: %s" % (arg, str(command)), file = sys.stderr)
			self._set_attributes()
		elif command["cmd"] == "H":
			# Position X/Y -- we ignore this.
			pass
		elif command["cmd"] == "C":
			# Cursor forward
			space_cnt = 1 + int(command["args"])
			old_attrs = self._attrs
			self._reset_terminal()
			self._add_text(" " * space_cnt)
			self._attrs = old_attrs
		elif command["cmd"] == "g":
			# TODO: Clear tab? No idea how to handle. Ingore.
			pass
		else:
			print("Warning: Unable to interpret CSI command: %s" % (str(command)), file = sys.stderr)

	def _interpret_command_tabset(self, command):
		self._attrs["tabsize"] = len(command) - 1

	def _interpret_command(self, command):
		if command.get("args_csi") is not None:
			command = {
				"args":	command["args_csi"],
				"cmd":	command["cmd_csi"],
			}
			return self._interpret_command_csi(command)
		elif command.get("cmd_tabset") is not None:
			return self._interpret_command_tabset(command["cmd_tabset"])
		else:
			raise Exception("Parsed unknown command entirely: %s" % (str(command)))

	def parse(self, data):
		offset = 0
		for result in self._ESCAPE_CONTROL_SEQUENCE_RE.finditer(data):
			(begin, end) = result.span()
			text = data[offset : begin]
			offset = end
			self._add_text(text)
			command = result.groupdict()
			self._interpret_command(command)
		text = data[offset : ]
		self._add_text(text)

		if self._active_classes is not None:
			self._output.append("</span>")
			self._active_classes = None

if __name__ == "__main__":
	text = "\x1b[H    \x1b[H     Foobar"
	ansi = ANSIInterpreter()
	ansi.parse(text)
	print(ansi.html)
