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
		self.leds = leds
		requests.post("https://iotled.ytvwld.de/api/device/subscribe", json={
			"hostname": self.hostname,
			"leds": leds
		})

	def poll(self):
		req = requests.get("https://iotled.ytvwld.de/api/device/poll/{}".format(self.hostname))
		if req.status_code == 404:
			raise ConnectionLost
		if req.status_code == 204:
			return
		if req.status_code != 200:
			print ("Error:", req.status_code)
			return
		txt = req.text
		dec = jsondec.decode(req.text)
		command = dec["command"]
		params = dec["params"]
		return command, params

class ConnectionLost(Exception):
	pass
