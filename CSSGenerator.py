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

import configparser
import colorsys
import textwrap

class CSSGenerator(object):
	def __init__(self, color_config_filename, color_scheme, fg_color_index = 7, bg_color_index = 0, pre_classname = "terminal"):
		self._config = configparser.ConfigParser()
		self._config.read(color_config_filename)
		self._fg_color_index = fg_color_index
		self._bg_color_index = bg_color_index
		self._pre_classname = pre_classname

		self._colors = { }
		for (name, color) in self._config[color_scheme].items():
			if name.startswith("col"):
				index = int(name[3:])
				color = self._parse_color(color)
				self._colors[index] = color

	def get_color(self, index, increased_intensity = False):
		if not increased_intensity:
			return self._colors[index]
		else:
			return self._brighten(self._colors[index])

	@classmethod
	def _clamp(cls, value):
		if value < 0:
			value = 0
		elif value > 255:
			value = 255
		return value

	@classmethod
	def _brighten(cls, rgb):
		(h, s, v) = colorsys.rgb_to_hsv(*rgb)
		v = cls._clamp(v + 40)
		rgb = tuple(cls._clamp(round(value)) for value in colorsys.hsv_to_rgb(h, s, v))
		return rgb

	@staticmethod
	def _parse_color(color):
		assert(len(color) == 6)
		rgb = (int(color[0 : 2], 16), int(color[2 : 4], 16), int(color[4 : 6], 16))
		return rgb

	@staticmethod
	def _hex(rgb):
		return "%02x%02x%02x" % (rgb[0], rgb[1], rgb[2])

	@classmethod
	def _html_color(cls, rgb):
		return "#%s" % (cls._hex(rgb))

	def pre_attributes(self):
		arguments = {
			"pre_classname":	self._pre_classname,
			"foreground":		self._html_color(self.get_color(self._fg_color_index)),
			"background":		self._html_color(self.get_color(self._bg_color_index)),
		}

		attributes = [
			"color: %(foreground)s" % (arguments),
			"background-color: %(background)s" % (arguments),
			"padding: 20px",
			"border: 1px dotted white",
			"white-space: pre-wrap",
		]
		return attributes

	def class_attribute(self, classname):
		assert(len(classname) > 0)
		if classname[0] in "fFbB":
			increased_intensity = classname[0] in "FB"
			index = int(classname[1:])
			color = self._html_color(self.get_color(index, increased_intensity = increased_intensity))
			key = "color" if (classname[0] in "fF") else "background-color"
			return [ "%s: %s" % (key, color) ]
		elif classname == "italics":
			return [ "font-style: italic" ]
		elif classname == "underline":
			return [ "text-decoration: underline" ]
		else:
			raise Exception("Cannot get class attribute for class '%s'." % (classname))

	def generate(self, used_classes = None):
		css = "pre.%s {\n" % (self._pre_classname)
		for attribute in self.pre_attributes():
			css += "	" + attribute + ";\n"
		css += "}\n\n"

		if used_classes is None:
			used_classes = [ "italics", "underline" ]
			for index in range(16):
				for prefix in "fFbB":
					used_classes.append(prefix + str(index))
		else:
			used_classes = sorted(used_classes)
		for classname in used_classes:
			css += "pre.%s > span.%s { %s }\n" % (self._pre_classname, classname, "; ".join(self.class_attribute(classname)))
		return css

if __name__ == "__main__":
	css = CSSGenerator("color_schemes.ini", "linux")
	print(css.generate(used_classes = [ "f9", "b3" ]))
	print(css.pre_attributes())
	print(css([ "f8", "b3" ]))
