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
            ("Dining", ShadeGroup("192.168.201.20", "Dining", ["FLI", "EBH"])),
            ("Kitchen", ShadeGroup("192.168.201.20", "Kitchen", ["YQP"])),
            ("Primary", ShadeGroup("192.168.201.20", "Primary", ["KXJ"])),
            ("Studio", ShadeGroup("192.168.201.20", "Studio", ["NKK", "CYV"]))
        ])

        return shadeGroups
