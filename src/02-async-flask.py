import asyncio
from flask import Flask
from flask import request

app = Flask(__name__)

async def get_chat_id(name):
    await asyncio.sleep(3)
    print("get_chat_id: " + name)
    return "chat-%s" % name

# curl --cacert cert.pem -L -X GET 'http://localhost:5000/api/v1/network/requestip?id=5j1EtX0a+hkoZW0e3s3RSaYwAVZrLS0ZiBNTHd4sRmU='
# curl -L -X GET 'http://localhost:5000/api/v1/test'
@app.route('/api/v1/test', methods=['GET'])
async def test():
    print("Test api")
    return {"res": "Returned from test api"}

async def main():
    print("Test async")
    id_coroutine = get_chat_id("django")
    # await get_chat_id("django")
    # id_coroutine = "tmp"
    print("wait for " + str(id_coroutine))
    result = await id_coroutine
    print("result: " + result)
    print("done")

    from waitress import serve
    serve(app, host="0.0.0.0", port=5000, url_scheme='https')

asyncio.run(main())
