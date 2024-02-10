import asyncio
import logging
import threading
import time
#from fastapi import FastAPI
from hubmanager.hubmanager import HubManager
#from typing import Union

async def main():
    event_loop = asyncio.get_running_loop()
    manager = HubManager(event_loop)
    manager.do_log('debug')
    #manager.async_add_job(manager.do_connect, '192.168.201.20')
    await manager.do_connect('192.168.201.20')
    
    manager.do_open(0,0)

    while True:
        manager.do_list()
        time.sleep(1)

    manager.do_exit()

    # app = FastAPI()

    # @app.get("/")
    # def read_root():
    #     return {"Hello": "World"}


    # @app.get("/items/{item_id}")
    # def read_item(item_id: int, q: Union[str, None] = None):
    #     return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
    




