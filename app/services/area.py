from typing import List
from app.repositories.area import AreaRepository
from app.schemas.area import AreaResponse
from app.exceptions import NotFoundException


class AreaService:
    def __init__(self, area_repo: AreaRepository):
        self.area_repo = area_repo

    def create(self, name: str, description: str = None, color: str = None) -> AreaResponse:
        area = self.area_repo.create(name=name, description=description, color=color)
        return AreaResponse.model_validate(area)

    def get_all(self) -> List[AreaResponse]:
        areas = self.area_repo.get_all()
        return [AreaResponse.model_validate(area) for area in areas]

    def get_by_id(self, id: int) -> AreaResponse:
        area = self.area_repo.get(id)
        if not area:
            raise NotFoundException(f"Area with id {id} not found")
        return AreaResponse.model_validate(area)

    def update(self, id: int, name: str = None, description: str = None, color: str = None) -> AreaResponse:
        if not self.area_repo.exists(id):
            raise NotFoundException(f"Area with id {id} not found")
        updated = self.area_repo.update(id, name=name, description=description, color=color)
        return AreaResponse.model_validate(updated)

    def delete(self, id: int) -> None:
        if not self.area_repo.exists(id):
            raise NotFoundException(f"Area with id {id} not found")
        self.area_repo.delete(id)
