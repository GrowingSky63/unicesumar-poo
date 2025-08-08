from dataclasses import dataclass

from domain.entities.ingrediente import Ingrediente

@dataclass
class Receita:
    nome: str
    tempo_preparo: float
    rendimento: str
    modo_preparo: str
    ingredientes: list[Ingrediente]