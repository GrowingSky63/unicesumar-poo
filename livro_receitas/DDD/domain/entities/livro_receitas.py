from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from domain.entities.receita import Receita
from domain.entities.categoria import Categoria
from domain.value_objects.autor import Autor

@dataclass
class LivroReceitas:
    titulo: str
    autor: Autor
    data_criacao: datetime
    receitas: list[Receita] = field(default_factory=list)
    categorias: list[Categoria] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid4()), init=False)

    def __init__(self, titulo: str, autor: Autor, data_criacao: datetime,
                 receitas: list[Receita] | None = None,
                 categorias: list[Categoria] | None = None,
                 receitas_avulsas: list[Receita] | None = None):
        # Atribuições básicas
        object.__setattr__(self, 'titulo', titulo)
        object.__setattr__(self, 'autor', autor)
        object.__setattr__(self, 'data_criacao', data_criacao)
        object.__setattr__(self, 'categorias', categorias if categorias is not None else [])
        object.__setattr__(self, 'receitas', [])
        object.__setattr__(self, 'id', str(uuid4()))
        # Coletar todas as receitas das categorias
        receitas_categorias: list[Receita] = []
        for cat in self.categorias:
            receitas_categorias.extend(cat.receitas)
        # Adicionar receitas avulsas (não vinculadas a categorias)
        if receitas_avulsas is not None:
            todas = receitas_categorias + [r for r in receitas_avulsas if r not in receitas_categorias]
        elif receitas is not None:
            todas = receitas
        else:
            todas = receitas_categorias
        object.__setattr__(self, 'receitas', todas)
        # Ajustar listas de cada categoria
        for cat in self.categorias:
            cat.receitas = [r for r in cat.receitas if r in self.receitas]
