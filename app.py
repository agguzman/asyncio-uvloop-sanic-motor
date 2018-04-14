import asyncio
import uvloop
from motor.motor_asyncio import AsyncIOMotorClient
from sanic import Sanic
from sanic.response import json


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


mongo_connection = AsyncIOMotorClient('localhost')
contacts = mongo_connection.sanic_motor_test_db.contacts


app = Sanic(__name__)


@app.route("/")
async def list(request):
    data = await contacts.find().to_list(20)
    for x in data:
        x['id'] = str(x['_id'])
        del x['_id']

    return json(data)


@app.route("/new")
async def new(request):
    contact = request.json
    insert = await contacts.insert_one(contact)
    return json({"inserted_id": str(insert.inserted_id)})


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app.run(host="0.0.0.0", port=8000, workers=3, debug=True)
