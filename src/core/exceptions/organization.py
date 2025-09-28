class OrganizationNotFoundById(Exception):
    def __init__(self, organization_id: int) -> None:
        self.organization_id = organization_id
        super().__init__(f"Organization with id:{organization_id} not found")


class OrganizationNotFoundByName(Exception):
    def __init__(self, organization_name: str) -> None:
        self.organization_name = organization_name
        super().__init__(f"Organization with name:{organization_name} not found")
