from dataclasses import dataclass

from domain.value_objects.quantidade import Quantidade

@dataclass
class Ingrediente:
    nome: str
    quantidade: Quantidade