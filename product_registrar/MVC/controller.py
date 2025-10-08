from typing import List, Optional

from .models import Produto


class ProdutoController:
    """
    Classe responsável por implementar as regras de negócio da aplicação
    """
    def __init__(self) -> None:
        self._produtos: List[Produto] = []

    def adicionar_produto(self, id: int, nome: str, preco: float, quantidade: int) -> Produto:
        if self.buscar_por_id(id) is not None:
            raise ValueError("Já existe um produto com esse ID")
        produto = Produto(id=id, nome=nome, preco=preco, quantidade=quantidade)
        self._produtos.append(produto)
        return produto

    def listar_produtos(self) -> List[Produto]:
        return list(self._produtos)

    def atualizar_quantidade(self, id: int, nova_quantidade: int) -> bool:
        produto = self.buscar_por_id(id)
        if produto is None:
            return False
        produto.set_quantidade(nova_quantidade)
        return True

    def remover_produto(self, id: int) -> bool:
        produto = self.buscar_por_id(id)
        if produto is None:
            return False
        self._produtos.remove(produto)
        return True

    def buscar_por_id(self, id: int) -> Optional[Produto]:
        for p in self._produtos:
            if p.get_id() == int(id):
                return p
        return None

