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

from werkzeug.wrappers import Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader
import os
from json import JSONDecoder, JSONEncoder
from jsonrequest import JSONRequest
from threading import Lock, Condition

jsondec = JSONDecoder()
jsonenc = JSONEncoder()

class App():
	def __init__(self):
		self.url_map = Map([
			Rule("/", endpoint="home"),
			Rule("/setup", endpoint="setup"),
			Rule("/manage", endpoint="manage"),
			Rule("/api/device/subscribe", endpoint="api_device_subscribe"),
			Rule("/api/device/poll/<hostname>", endpoint="api_device_poll"),
			Rule("/api/app/list", endpoint="api_app_list"),
			Rule("/api/app/<device>", endpoint="api_app_manage")
		])
		self.clients = {}
		self.clients_lock = Lock()
		self.commands_condition = Condition(self.clients_lock)
		template_path = os.path.join(os.path.dirname(__file__), 'templates')
		self.jinja_env = Environment(loader=FileSystemLoader(template_path),
			autoescape=True)

	@JSONRequest.application
	def dispatch_request(self, request):
		adapter = self.url_map.bind_to_environ(request.environ)
		try:
			endpoint, values = adapter.match()
			return getattr(self, 'on_' + endpoint)(request, **values)
		except HTTPException, e:
			return e

	def on_home(self, request):
		return self.render_template('home.html')

	def on_setup(self, request):
		return self.render_template('setup.html')

	def on_manage(self, request):
		return self.render_template('manage.html')

	def on_api_device_subscribe(self, request):
		assert request.method == "POST"
		data = request.json
		hostname = data["hostname"]
		leds = data["leds"]
		print ("Client {0} with LEDs {1} has subscribed.".format(hostname, leds))
		client = {"leds": leds, "commands": [{"command": "hello", "params": []}]}
		with self.clients_lock:
			if hostname not in self.clients:
				self.clients[hostname] = client
				return Response(status=201)
			else:
				return Response(status=100)

	def on_api_device_poll(self, request, hostname):
		self.clients_lock.acquire()
		if hostname not in self.clients:
			self.clients_lock.release()
			return Response(status=404)
		client = self.clients[hostname]
		while not client["commands"]:
			print ("Got nothing new for {0}. Waiting.".format(hostname))
			self.commands_condition.wait()
		command = client["commands"].pop(0)
		self.clients_lock.release()
		print("Sending command {0} to client {1}...".format(command, hostname))
		return Response(jsonenc.encode(command), mimetype="text/json", status=200)

	def on_api_app_list(self, request):
		with self.clients_lock:
			return Response(jsonenc.encode(list(self.clients)), mimetype="text/json")

	def on_api_app_manage(self, request, device):
		with self.clients_lock:
			client = self.clients[device]
			if request.method == "GET":
				return Response(jsonenc.encode(client["leds"]), mimetype="text/json")
			if request.method == "POST":
				command = request.form["command"]
				params = jsondec.decode(request.form["params"])
				client["commands"].append({"command": command, "params": params})
				print("Got the command {0} {1} for {2}.".format(command, params, device))
				self.commands_condition.notify_all()
				return Response(status=202)

	def render_template(self, template_name, **context):
		t = self.jinja_env.get_template(template_name)
		return Response(t.render(context), mimetype='text/html')


	def wsgi_app(self, environ, start_response):
		return self.dispatch_request(environ, start_response)

	def __call__(self, environ, start_response):
		return self.wsgi_app(environ, start_response)
