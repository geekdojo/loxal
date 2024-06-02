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
            ("All", ShadeGroup("192.168.201.20", "All", ["FLI", "EBH", "YQP", "LZU", "TOA", "RXG", "ATR", "KTB", "KXJ", "NKK", "CYV"])),
            ("Dining", ShadeGroup("192.168.201.20", "Dining", ["FLI", "EBH"])),
            ("Kitchen", ShadeGroup("192.168.201.20", "Kitchen", ["YQP"])),
            ("LivingEast", ShadeGroup("192.168.201.20", "LivingEast", ["LZU","TOA","RXG"])),
            ("LivingSouth", ShadeGroup("192.168.201.20", "LivingSouth", ["ATR"])),
            ("BalconyDoor", ShadeGroup("192.168.201.20", "BalconyDoor", ["KTB"])),
            ("Primary", ShadeGroup("192.168.201.20", "Primary", ["KXJ"])),
            ("Studio", ShadeGroup("192.168.201.20", "Studio", ["NKK", "CYV"]))            
        ])

        return shadeGroups
