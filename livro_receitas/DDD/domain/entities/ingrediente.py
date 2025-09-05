from dataclasses import dataclass, field
from uuid import uuid4

from domain.value_objects.quantidade import Quantidade

@dataclass
class Ingrediente:
    nome: str
    quantidade: Quantidade
    id: str = field(default_factory=lambda: str(uuid4()))