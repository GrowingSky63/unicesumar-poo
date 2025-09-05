from dataclasses import dataclass, field
from uuid import uuid4

from domain.entities.receita import Receita

@dataclass
class Categoria:
    nome: str
    descricao: str
    receitas: list[Receita] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid4()))