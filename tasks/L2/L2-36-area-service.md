# L2-36 — Создать AreaService (CRUD)

## Цель
Определить AreaService с бизнес-логикой.

## Вход
Area репозиторий (L1-29), Area схемы (L1-21).

## Выход
app/services/area.py.

## Готово когда
AreaService с методами CRUD.

## Подсказка для LLM
Создайте app/services/area.py с классом AreaService. Методы: __init__(self, area_repo: AreaRepository), create(self, name: str, description: Optional[str] = None, color: Optional[str] = None) -> AreaResponse, get_all(self) -> List[AreaResponse], get_by_id(self, id: int) -> AreaResponse (бросает NotFoundException), update(self, id: int, **kwargs) -> AreaResponse, delete(self, id: int).

## Оценка усилия
S

## Файлы для создания
- app/services/area.py

## Класс AreaService
```python
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
```
