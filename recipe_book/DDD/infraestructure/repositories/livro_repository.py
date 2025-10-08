from typing import Optional, List

from domain.entities.livro_receitas import LivroReceitas
from domain.entities.receita import Receita
from domain.entities.categoria import Categoria
from .in_memory import InMemoryRepository

class LivroReceitasRepository(InMemoryRepository[LivroReceitas]):
    def add(self, entity: LivroReceitas) -> LivroReceitas:
        # Garantir consistência de receitas nas categorias
        self._sincronizar(entity)
        return super().add(entity)

    def update(self, entity: LivroReceitas) -> LivroReceitas:
        self._sincronizar(entity)
        return super().update(entity)

    def _sincronizar(self, livro: LivroReceitas) -> None:
        # Recalcula a lista de receitas considerando categorias + avulsas
        receitas_cat = []
        for c in livro.categorias:
            for r in c.receitas:
                if r not in receitas_cat:
                    receitas_cat.append(r)
        # Mantém qualquer receita já listada manualmente
        for r in livro.receitas:
            if r not in receitas_cat:
                receitas_cat.append(r)
        livro.receitas = receitas_cat
        # Limpa duplicatas em cada categoria e garante referência
        for c in livro.categorias:
            unique = []
            for r in c.receitas:
                if r in livro.receitas and r not in unique:
                    unique.append(r)
            c.receitas = unique
