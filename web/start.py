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

from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.serving import run_simple
import os

from app import App

app = App()
app = SharedDataMiddleware(app.wsgi_app, {
	"/static": os.path.join(os.path.dirname(__file__), "static")
})

if __name__ == "__main__":
	run_simple('0.0.0.0', 5000, app, use_debugger=True, use_reloader=True)
