
from dataclasses import dataclass, field
from datetime import datetime
from typing import Set, List, Optional

from domain.entities.receita import Receita
from domain.entities.categoria import Categoria
from domain.value_objects.autor import Autor

@dataclass
class LivroReceitas:
    titulo: str
    autor: Autor
    data_criacao: datetime
    receitas: List[Receita] = field(default_factory=list)
    categorias: List[Categoria] = field(default_factory=list)

    def __init__(self, titulo: str, autor: Autor, data_criacao: datetime,
                 receitas: Optional[List[Receita]] = None,
                 categorias: Optional[List[Categoria]] = None,
                 receitas_avulsas: Optional[List[Receita]] = None):
        self.titulo = titulo
        self.autor = autor
        self.data_criacao = data_criacao
        self.categorias = categorias if categorias is not None else []
        # Coletar todas as receitas das categorias
        receitas_categorias = []
        for cat in self.categorias:
            receitas_categorias.extend(cat.receitas)
        # Adicionar receitas avulsas (não vinculadas a categorias)
        if receitas_avulsas is not None:
            self.receitas = receitas_categorias + [r for r in receitas_avulsas if r not in receitas_categorias]
        elif receitas is not None:
            self.receitas = receitas
        else:
            self.receitas = receitas_categorias
        # Atualizar as listas de cada categoria para garantir que apontam para objetos do principal
        for cat in self.categorias:
            cat.receitas = [r for r in cat.receitas if r in self.receitas]
