from typing import Iterable

from .models import Produto


class ProdutoView:

    def listar_produtos(self, produtos: Iterable[Produto]) -> str | Iterable:
        """
        Método responsável por montar a visualização da lista de produtos
        """
        lista_produtos = [f"ID: {p.get_id()} | Nome: {p.get_nome()} | Preço: R$ {p.get_preco():.2f} | Quantidade: {p.get_quantidade()}" for p in produtos]
        if len(lista_produtos) <= 0:
            return "Nenhum produto cadastrado."
        return lista_produtos

    def mostrar_produto(self, produto: Produto | None) -> str:
        """
        Método responsável por montar a visualização de um produto
        """
        if produto is None:
            return "Produto não encontrado."
        return f"ID: {produto.get_id()} | Nome: {produto.get_nome()} | Preço: R$ {produto.get_preco():.2f} | Quantidade: {produto.get_quantidade()}"

