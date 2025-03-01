from dataclasses import dataclass


@dataclass
class ProductDTO:
    pk: int
    name: str
    description: str
    cost: float
    discount: int
    status: str


@dataclass
class ProductCreateDTO:
    name: str
    description: str
    cost: float
    discount: int
    status: str
    archived: bool
    created_by: int
