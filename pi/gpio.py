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

from RPi import GPIO

PORTS = {
	"LED": {
		"BLUE": 3,
		"GREEN": 4,
		"RED": 14
	},
	"BUTTON": {
		"POWER": 15
	}
}

def setup():
	GPIO.setmode(GPIO.BCM)

	for led in PORTS["LED"]:
		GPIO.setup(PORTS["LED"][led], GPIO.OUT)

	for button in PORTS["BUTTON"]:
		GPIO.setup(PORTS["BUTTON"][button], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def turn_on(led):
	GPIO.output(PORTS["LED"][led], GPIO.HIGH)

def turn_off(led):
	GPIO.output(PORTS["LED"][led], GPIO.LOW)

def setup_push_callback(button, func):
	GPIO.add_event_detect(PORTS["BUTTON"][button], GPIO.RISING, callback=lambda channel: func())
