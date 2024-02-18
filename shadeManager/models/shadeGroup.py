class ShadeGroup():
    hubId: str
    shadeGroupId: str
    shadeIds: list[str]

    def __init__(self, hubId: str, shadeGroupId: str, shadeIds: list[str]):
        """Init command interface."""
        self.hubId = hubId
        self.shadeGroupId = shadeGroupId
        self.shadeIds = shadeIds
        super().__init__()

    @staticmethod
    def Populate():
        shadeGroups = dict([
            ("Studio", ShadeGroup("192.168.201.20", "Studio", ["NKK", "CYV"])),
            ("Kitchen", ShadeGroup("192.168.201.20", "Kitchen", ["VVE"])),
            ("Primary", ShadeGroup("192.168.201.20", "Primary", ["KXJ"]))
        ])

        return shadeGroups
