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

import requests
from platform import node
from json import JSONDecoder, JSONEncoder

jsondec = JSONDecoder()
jsonenc = JSONEncoder()

class Client():
	def connect(self, leds):
		self.hostname = node()
		requests.post("https://iotled.ytvwld.de/api/raspi/subscribe", data={
			"hostname": self.hostname,
			"leds": jsonenc.encode(leds)
		})

	def poll(self):
		req = requests.get("https://iotled.ytvwld.de/api/raspi/poll", data={"hostname": self.hostname})
		txt = req.text
		if txt:
			dec = jsondec.decode(req.text)
			command = dec["command"]
			params = dec["params"]
			return command, params
		else:
			sleep(10)
