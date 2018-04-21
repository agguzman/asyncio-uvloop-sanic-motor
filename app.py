import asyncio
import socket

from sanic import Sanic
from sanic.response import json
from motor.motor_asyncio import AsyncIOMotorClient
import uvloop


###### Setup ######

# todo: learn about this line. Is is necessary
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = Sanic(__name__)
db = None

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
    return json({'Hostname': host_name, 'HostIP': host_ip})

@app.route("/")
async def list(request):
    data = await db.contacts.find().to_list(20)
    for x in data:
        x['id'] = str(x['_id'])
        del x['_id']

    return json(data)

@app.route("/new")
async def new(request):
    # contact = request.json
    insert = await db.contacts.insert_one({'name': 'alejandro'})
    return json('Inserted.')


###### Entry point ######

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, workers=3, debug=True)
