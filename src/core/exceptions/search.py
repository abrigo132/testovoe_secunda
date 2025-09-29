class GeoSearchRadiusNotFoundOrganizations(Exception):
    def __init__(self, radius: float) -> None:
        self.radius = radius
        super().__init__(
            f"No buildings were found within a radius of {radius} km from the specified point"
        )
