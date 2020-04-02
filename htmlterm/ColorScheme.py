#	screen2html - Convert ANSI-color containing terminal output to HTML.
#	Copyright (C) 2020-2020 Johannes Bauer
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

class ColorScheme():
	_KNOWN_COLOR_SCHEMES = {
		"tango":	(0x000000, 0xcc0000, 0x4e9a06, 0xc4a000, 0x3465a4, 0x75507b, 0x06989a, 0xd3d7cf,
						0x555753, 0xef2929, 0x8ae234, 0xfce94f, 0x729fcf, 0xad7fa8, 0x34e2e2, 0xeeeeec),
		"linux":	(0x000000, 0xaa0000, 0x00aa00, 0xaa5500, 0x0000aa, 0xaa00aa, 0x00aaaa, 0xaaaaaa,
						0x555555, 0xff5555, 0x55ff55, 0xffff55, 0x5555ff, 0xff55ff, 0x55ffff, 0xffffff),
		"xterm":	(0x000000, 0xcd0000, 0x00cd00, 0xcdcd00, 0x1e90ff, 0xcd00cd, 0x00cdcd, 0xe5e5e5,
						0x4c4c4c, 0xff0000, 0x00ff00, 0xffff00, 0x4682b4, 0xff00ff, 0x00ffff, 0xffffff),
		"rxvt":		(0x000000, 0xcd0000, 0x00cd00, 0xcdcd00, 0x0000cd, 0xcd00cd, 0x00cdcd, 0xfaebd7,
						0x404040, 0xff0000, 0x00ff00, 0xffff00, 0x0000ff, 0xff00ff, 0x00ffff, 0xffffff),
	}

	def __init__(self, colors):
		self._colors = colors

	@staticmethod
	def _split(rgb):
		return ((rgb >> 16) & 0xff, (rgb >> 8) & 0xff, (rgb >> 0) & 0xff)

	@staticmethod
	def _combine(rgbtuple):
		return (rgbtuple[0] << 16) | (rgbtuple[1] << 8) | (rgbtuple[2])

	@staticmethod
	def _clamp(value):
		if value < 0:
			value = 0
		elif value > 255:
			value = 255
		return value

	def bright(self, index, brighten_value = 40):
		rgbtuple = self._split(self[index])
		(h, s, v) = colorsys.rgb_to_hsv(*rgbtuple)
		v = self._clamp(v + brighten_value)
		bright_rgbtuple = tuple(self._clamp(round(value)) for value in colorsys.hsv_to_rgb(h, s, v))
		return self._combine(bright_rgbtuple)

	@classmethod
	def create_by_name(cls, name):
		return cls(cls._KNOWN_COLOR_SCHEMES[name])

	def __getitem__(self, index):
		return self._colors[index]
