from dataclasses import dataclass, field
from uuid import uuid4

from domain.entities.ingrediente import Ingrediente

@dataclass
class Receita:
    nome: str
    tempo_preparo: float
    rendimento: str
    modo_preparo: str
    ingredientes: list[Ingrediente]
    id: str = field(default_factory=lambda: str(uuid4()))