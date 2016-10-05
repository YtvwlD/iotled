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

from werkzeug.utils import cached_property
from werkzeug.wrappers import Request
from json import JSONDecoder

jsondec = JSONDecoder()

class JSONRequest(Request):
	# accept up to 4MB of transmitted data.
	max_content_length = 1024 * 1024 * 4

	@cached_property
	def json(self):
		if self.headers.get('content-type') == 'application/json':
			return jsondec.decode(self.data)
