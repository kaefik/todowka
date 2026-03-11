from typing import List
from app.repositories.context import ContextRepository
from app.schemas.context import ContextResponse
from app.exceptions import NotFoundException


class ContextService:
    def __init__(self, context_repo: ContextRepository):
        self.context_repo = context_repo

    def create(self, name: str, icon: str = None, color: str = None) -> ContextResponse:
        context = self.context_repo.create(name=name, icon=icon, color=color)
        return ContextResponse.model_validate(context)

    def get_all(self) -> List[ContextResponse]:
        contexts = self.context_repo.get_all()
        return [ContextResponse.model_validate(ctx) for ctx in contexts]

    def get_by_id(self, id: int) -> ContextResponse:
        context = self.context_repo.get(id)
        if not context:
            raise NotFoundException(f"Context with id {id} not found")
        return ContextResponse.model_validate(context)

    def update(self, id: int, name: str = None, icon: str = None, color: str = None) -> ContextResponse:
        if not self.context_repo.exists(id):
            raise NotFoundException(f"Context with id {id} not found")
        updated = self.context_repo.update(id, name=name, icon=icon, color=color)
        return ContextResponse.model_validate(updated)

    def delete(self, id: int) -> None:
        if not self.context_repo.exists(id):
            raise NotFoundException(f"Context with id {id} not found")
        self.context_repo.delete(id)
