class ActivityNotFound(Exception):
    def __init__(self, activity_name: str) -> None:
        self.activity_name = activity_name
        super().__init__(f"Building with activity name:{activity_name} not found")


class ActivityNotFoundPathTree(Exception):
    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__(f"Building with activity name:{path} not found")
