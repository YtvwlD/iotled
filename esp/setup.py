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

print ("Connecting to WiFi...")
from config import WIFI_SSID, WIFI_PASS
from network import WLAN, STA_IF
s = WLAN(STA_IF)
s.active(True)
s.connect(WIFI_SSID, WIFI_PASS)
while not s.isconnected():
	pass
print ("Connected.")
