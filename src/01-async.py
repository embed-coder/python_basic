import asyncio

async def get_chat_id(name):
    await asyncio.sleep(3)
    print("get_chat_id: " + name)
    return "chat-%s" % name

async def main():
    print("Test async")
    id_coroutine = get_chat_id("django")
    # await get_chat_id("django")
    # id_coroutine = "tmp"
    print("wait for " + str(id_coroutine))
    result = await id_coroutine
    print("result: " + result)
    print("done")

asyncio.run(main())
