from dataclasses import dataclass
from typing import Optional


# TODO посмотреть как работает библиотека Auto-Dataclass
#  https://github.com/OleksandrZhydyk/Auto-Dataclass

@dataclass
class BaseProductDto:
    def to_dict(self) -> dict[str, Optional[str]]:
        return {key: value for key, value in self.__dict__.items()}


@dataclass
class ProductDTO(BaseProductDto):
    pk: int
    name: str
    description: str
    cost: float
    discount: int
    status: str
    archived: bool
    created_by: int


@dataclass
class ProductCreateDTO(BaseProductDto):
    name: str
    description: str
    cost: float
    discount: int
    status: str
    archived: bool
    created_by: int


@dataclass
class ProductUpdateDTO(BaseProductDto):
    pk: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[float] = None
    discount: Optional[int] = None
    status: Optional[str] = None
    archived: Optional[bool] = None
    created_by: Optional[int] = None
