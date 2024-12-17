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
            ("All", [ShadeGroup("192.168.201.20", "All", ["FLI", "EBH", "YQP", "KTB", "KXJ", "NKK", "CYV"]), ShadeGroup("192.168.201.30", "All", ["CIH","GOV","UUJ", "EIF", "CGZ", "BPG"])]),
            ("Dining", [ShadeGroup("192.168.201.30", "Dining", ["BPG"]), ShadeGroup("192.168.201.20", "Dining", ["FLI"])]),
            ("Kitchen", [ShadeGroup("192.168.201.20", "Kitchen", ["YQP"])]),
            ("LivingEast", [ShadeGroup("192.168.201.30", "LivingEast", ["CIH","GOV","UUJ"])]),
            ("LivingSouth", [ShadeGroup("192.168.201.30", "LivingSouth", ["EIF"])]),
            ("BalconyDoor", [ShadeGroup("192.168.201.30", "BalconyDoor", ["CGZ"])]),
            ("Primary", [ShadeGroup("192.168.201.20", "Primary", ["KXJ"])]),
            ("Studio", [ShadeGroup("192.168.201.20", "Studio", ["NKK", "CYV"])])            
        ])

        return shadeGroups
