from dataclasses import dataclass

from domain.entities.receita import Receita

@dataclass
class Categoria:
    nome: str
    descricao: str
    receitas: list[Receita] = None