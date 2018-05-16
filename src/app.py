# Copyright (C) 2018  Alejandro Guzman <a.guillermo.guzman@gmail.com>
#
# A simple example program to learn Sanic and Motor.
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import socket

from sanic import Sanic
from sanic.response import json, text
from motor.motor_asyncio import AsyncIOMotorClient
import uvloop
from sanic_openapi import swagger_blueprint, openapi_blueprint
from sanic_openapi import doc

###### Setup ######

# todo: learn about this line. Is is necessary
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = Sanic(__name__)
db = None

app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)

@app.listener('before_server_start')
async def setup_db(app, loop):
    global db
    client = AsyncIOMotorClient(host='mongodb', io_loop=loop)
    db = client['motor_test']


###### Routes ######

@app.route("/ping")
async def list(request):
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    return json({'Hostname': host_name, 'HostIP': host_ip, 'RequestHeaders': request.headers})

@app.route("/users", methods=['GET'])
@doc.summary('Fetches all users')
@doc.produces({'name': str, 'id': str})
async def list(request):
    data = await db['users'].find().to_list(20)
    for x in data:
        x['id'] = str(x['_id'])
        del x['_id']

    return json(data)

@app.route("/user", methods=['POST'])
async def new(request):
    insert = await db['users'].insert_one(request.json)

    return text('Inserted.')


###### Entry point ######

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, workers=3, debug=True)
