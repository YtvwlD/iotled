#!/usr/bin/env python

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

print ("IoT for LEDs  Copyright (C) 2016  Niklas Sombert")
print ("This program comes with ABSOLUTELY NO WARRANTY.")
print ("This is free software, and you are welcome to redistribute it")
print ("under certain conditions.")

from time import sleep

import gpio
import poweroff
from client import Client, ConnectionLost

print ("Preparing GPIO...")
gpio.setup()
gpio.setup_push_callback("POWER", poweroff.poweroff)
while True:
	try:
		print ("Connecting to the cloud...")
		client = Client()
		client.connect(list(gpio.PORTS["LED"]))
		print ("Connection established.")
		while True:
			print ("Polling...")
			cmd_param = client.poll()
			print(cmd_param)
			if cmd_param:
				if cmd_param[0] == "turn_on":
					gpio.turn_on(cmd_param[1][0])
				if cmd_param[0] == "turn_off":
					gpio.turn_off(cmd_param[1][0])

	except ConnectionLost:
		print ("Connection lost.")
		continue
