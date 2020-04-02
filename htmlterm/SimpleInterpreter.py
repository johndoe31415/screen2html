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

from htmlterm import ColorScheme, CSSGenerator, ANSIInterpreter

class SimpleInterpreter():
	def __init__(self, colorscheme_name, external_stylesheet = True):
		color_scheme = ColorScheme.create_by_name(colorscheme_name)
		self._css_generator = CSSGenerator(color_scheme, external_stylesheet = external_stylesheet)
		self._ansi_interpreter = ANSIInterpreter(self._css_generator)

	@property
	def css(self):
		return self._css_generator.generate_css()

	def html(self, ansi_text):
		return self._ansi_interpreter.render(ansi_text)
