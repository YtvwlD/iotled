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

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.utils import redirect

class App():
	@Request.application
	def dispatch_request(self, request):
		return Response("Hello World!")

	def wsgi_app(self, environ, start_response):
		return self.dispatch_request(environ, start_response)

	def __call__(self, environ, start_response):
		return self.wsgi_app(environ, start_response)
