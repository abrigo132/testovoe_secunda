class BuildingNotFound(Exception):
    def __init__(self, building_id: int) -> None:
        self.building_id = building_id
        super().__init__(f"Building with id:{building_id} not found")
