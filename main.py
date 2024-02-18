import asyncio
import logging
import sys, os, traceback
import threading
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status, HTTPException
from hubmanager.main import HubManager
from shadeManager.main import ShadeManager, InvalidShadeGroup
from shadeManager.models.position import Position

logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

shadeManager: ShadeManager
hubManager = HubManager(asyncio.get_running_loop())
hubManager.do_log('info')
shadeManager = ShadeManager(hubManager)

@asynccontextmanager
async def lifespan(app: FastAPI):
    #event_loop = asyncio.get_running_loop()
    #hubManager = HubManager(event_loop)
    await hubManager.do_connect('192.168.201.20')
    yield
    hubManager.do_exit()

app = FastAPI(lifespan=lifespan)

@app.get("/api/shade-control", status_code=status.HTTP_200_OK)
async def list_hub_and_shade_data(response: Response):
    try:
        hubList = hubManager.do_list()
        return hubList
    except Exception as e:
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)
        # print(e)
        # print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"{e}")

@app.get("/api/shade-control/shade-group/{shadeGroupId}")
def get_shade_position(shadeGroupId: str, request: Request, response: Response):
    try:
        position = shadeManager.GetShadeGroupPosition(shadeGroupId)        
        return {"position": position}

    except InvalidShadeGroup as err: 
        raise HTTPException(status_code=400, detail=f"{err.args[0]}")
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"{err}")


@app.put("/api/shade-control/shade-group/{shadeGroupId}", status_code=status.HTTP_204_NO_CONTENT)
async def update_shade_group_position(shadeGroupId: str, request: Request, response: Response):
    try:
        json = await request.json()
        if not "position" in json:
            raise ValueError("No position attribute specified in json body")

        position = json["position"]
        if position >= 0:
            return await shadeManager.SetShadeGroupPosition(shadeGroupId, json["position"])
        else:
            return await shadeManager.StopShade(shadeGroupId) 

    except InvalidShadeGroup as err: 
        raise HTTPException(status_code=400, detail=f"{err.args[0]}")
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"{err}")

    




