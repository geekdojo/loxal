import asyncio
import logging
import threading
import time
#from fastapi import FastAPI
from hubmanager.hubmanager import HubManager
#from typing import Union

async def main():
    event_loop = asyncio.get_running_loop()
    hubManager = HubManager(event_loop)
    hubManager.do_log('info')
    await hubManager.do_connect('192.168.201.20')

    hubManager.do_list()
    await hubManager.do_open(0,1)

    while True:
        time.sleep(1)

    hubManager.do_exit()

    # app = FastAPI()

    # @app.get("/")
    # def read_root():
    #     return {"Hello": "World"}


    # @app.get("/items/{item_id}")
    # def read_item(item_id: int, q: Union[str, None] = None):
    #     return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
    




