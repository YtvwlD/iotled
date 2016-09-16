# IoT for LEDs
# Copyright (C) 2016  Niklas Sombert
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

from json import JSONDecoder, JSONEncoder
from werkzeug.wrappers import Response
from time import sleep

jsondec = JSONDecoder()
jsonenc = JSONEncoder()

class Client():
	def __init__(self, hostname, leds):
		self.hostname = hostname
		self.leds = jsondec.decode(leds)
		self.commands = []

	def getCommand(self):
		try:
			command = self.commands.pop()
			return jsonenc.encode(command)
		except IndexError:
			sleep(60)
			return ""
