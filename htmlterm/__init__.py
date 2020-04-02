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

"""HTML rendering from ANSI terminal input

The htmlterm package can be used to render terminal output (e.g., that "screen"
can send to a logfile) to HTML. The contained ANSI escape sequences for
coloring are translated into either 'style' or 'class' attributes, depending on
the choice of the user and the resulting code is kept fairly minimal.

Its use is relatively simple. This example generates inline CSS (using the
'style' attribute of 'span' elements):

import htmlterm

color_scheme = htmlterm.ColorScheme.create_by_name("tango")
css_generator = htmlterm.CSSGenerator(color_scheme, external_stylesheet = False)
ansi_interpreter = htmlterm.ANSIInterpreter(css_generator)

terminal_text = "Foobar! \\x1b[44m Barfoo \\x1b[32m Foobar"
html = ansi_interpreter.render(terminal_text)
print(html)

But you can also have htmlterm create an external CSS file. The resulting
classes are generated on-demand and multiple render runs collect all required
classes so just one single CSS file needs to be emitted.

css_generator = htmlterm.CSSGenerator(color_scheme, external_stylesheet = True)
ansi_interpreter = htmlterm.ANSIInterpreter(css_generator)

html = ansi_interpreter.render(terminal_text)
print(html)
print(css_generator.generate_css())

All of the above can also be realized with a simple wrapper class that is
included for convenience:

ansi_renderer = htmlterm.SimpleInterpreter("tango", external_stylesheet = True)
print(ansi_renderer.html(terminal_text))
print(ansi_renderer.css)
"""

from htmlterm.ANSIInterpreter import ANSIInterpreter
from htmlterm.CSSGenerator import CSSGenerator
from htmlterm.ColorScheme import ColorScheme
from htmlterm.SimpleInterpreter import SimpleInterpreter
