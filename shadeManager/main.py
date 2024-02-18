#!/usr/bin/env python3
import time
from shadeManager.models.shadeGroup import ShadeGroup
from hubmanager.main import HubManager


class InvalidShadeGroup(Exception):
    pass

class ShadeManager():
    
    def __init__(self, hubManager: HubManager):
        """Init command interface."""
        self.hubManager = hubManager
        self.shadeGroups = ShadeGroup.Populate()
        super().__init__()

    async def SetShadeGroupPosition(self, shadeGroupId: str, position: int):
        shadeGroup: ShadeGroup

        if not shadeGroupId in self.shadeGroups :
            raise InvalidShadeGroup("Cannot find shade group {shadeGroupId}")
        else:
            shadeGroup = self.shadeGroups[shadeGroupId]
        
        for shade in shadeGroup.shadeIds :
            await self.hubManager.do_moveto(shadeGroup.hubId, shade, position)

    async def StopShade(self, shadeGroupId: str):
        shadeGroup: ShadeGroup

        if not shadeGroupId in self.shadeGroups :
            raise InvalidShadeGroup("Cannot find shade group {shadeGroupId}")
        else:
            shadeGroup = self.shadeGroups[shadeGroupId]
        
        for shade in shadeGroup.shadeIds :
            await self.hubManager.do_stop(shadeGroup.hubId, shade)


    def GetShadeGroupPosition(self, shadeGroupId: str):
        if not shadeGroupId in self.shadeGroups :
            raise InvalidShadeGroup("Cannot find shade group {shadeGroupId}")
        else:
            shadeGroup = self.shadeGroups[shadeGroupId]
        
        totalPositions = 0
        for shade in shadeGroup.shadeIds :
            position = self.hubManager.get_position(shadeGroup.hubId, shade)
            totalPositions+=position

        return totalPositions / len(shadeGroup.shadeIds)