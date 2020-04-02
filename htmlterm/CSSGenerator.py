#	screen2html - Convert ANSI-color containing terminal output to HTML.
#	Copyright (C) 2017-2020 Johannes Bauer
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

import colorsys
import textwrap

class CSSGenerator():
	def __init__(self, color_scheme, external_stylesheet = True, create_full_css = False, fg_color_index = 7, bg_color_index = 0, pre_classname = "terminal", additional_pre_styles = None):
		self._color_scheme = color_scheme
		self._external_stylesheet = external_stylesheet
		self._required_classes = set()
		self._fg_color_index = fg_color_index
		self._bg_color_index = bg_color_index
		self._pre_classname = pre_classname
		self._additional_pre_styles = additional_pre_styles
		if create_full_css:
			self._add_all_classes()

	def _add_all_classes(self):
		self._required_classes |= set([ "italics", "underline" ])
		for index in range(16):
			for prefix in "fFbB":
				self._required_classes.add(prefix + str(index))

	def get_color(self, index, increased_intensity = False):
		if not increased_intensity:
			return self._color_scheme[index]
		else:
			return self._color_scheme.bright(index)

	@property
	def pre_classname(self):
		return self._pre_classname

	@classmethod
	def _html_color(cls, rgb):
		return "#%06x" % (rgb)

	def pre_styles(self):
		attributes = {
			"color":				self._html_color(self.get_color(self._fg_color_index)),
			"background-color":		self._html_color(self.get_color(self._bg_color_index)),
			"white-space":			"pre-wrap",
		}
		if self._additional_pre_styles is not None:
			attributes.update(self._additional_pre_styles)
		return [ "%s: %s" % (key, value) for (key, value) in sorted(attributes.items()) ]

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

	def generate_css(self):
		css = "pre.%s {\n" % (self._pre_classname)
		for style in self.pre_styles():
			css += "	" + style + ";\n"
		css += "}\n"
		for classname in sorted(self._required_classes):
			css += "pre.%s > span.%s { %s }\n" % (self._pre_classname, classname, "; ".join(self.class_attribute(classname)))
		return css

	def get_attributes(self, classes):
		if not self._external_stylesheet:
			# Inline style
			attributes = [ self.class_attribute(classname) for classname in classes ]
			attributes = [ item for sublist in attributes for item in sublist ]
			return "style=\"%s\"" % ("; ".join(attributes))
		else:
			# Class style
			self._required_classes |= set(classes)
			return "class=\"%s\"" % (" ".join(classes))
