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
from jinja2 import Environment, FileSystemLoader
import os

from client import Client

class App():
	def __init__(self):
		self.url_map = Map([
			Rule("/", endpoint="home"),
			Rule("/setup", endpoint="setup"),
			Rule("/manage", endpoint="manage"),
			Rule("/api/raspi/subscribe", endpoint="api_raspi_subscribe"),
			Rule("/api/raspi/poll", endpoint="api_raspi_poll"),
			Rule("/api/app/list", endpoint="api_app_list"),
			Rule("/api/app/<device>", endpoint="api_app_manage")
		])
		self.clients = []
		template_path = os.path.join(os.path.dirname(__file__), 'templates')
		self.jinja_env = Environment(loader=FileSystemLoader(template_path),
			autoescape=True)

	@Request.application
	def dispatch_request(self, request):
		adapter = self.url_map.bind_to_environ(request.environ)
		try:
			endpoint, values = adapter.match()
			return getattr(self, 'on_' + endpoint)(request, **values)
		except HTTPException, e:
			return e

	def on_home(self, request):
		return self.render_template('home.html')

	def on_api_raspi_subscribe(self, request):
		#assert request.method == "POST"
		hostname = request.args.get("hostname")
		leds = request.args.get("leds")
		for client in self.clients:
			if client.hostname == hostname:
				self.clients.remove(client)
		client = Client(hostname, leds, state)
		self.clients.append(client)
		client.commands.append({"command": "hello"})
		return Response(status=201)

	def on_api_raspi_poll(self, request):
		hostname = request.args.get("hostname")
		for client in self.clients:
			if client.hostname == hostname:
				command = client.getCommand()
				if command:
					return Response(command, mimetype="text/json", status=200)
				else:
					return Response(status=204)
		return Response(status=404)

	def render_template(self, template_name, **context):
		t = self.jinja_env.get_template(template_name)
		return Response(t.render(context), mimetype='text/html')


	def wsgi_app(self, environ, start_response):
		return self.dispatch_request(environ, start_response)

	def __call__(self, environ, start_response):
		return self.wsgi_app(environ, start_response)