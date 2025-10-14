from typing import Iterable

from .models import Produto, Projeto, Tarefa


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


class ProjetoView:
    def listar_projetos(self, projetos: Iterable[Projeto]) -> str | Iterable:
        lista = [f"ID: {p.get_id()} | Nome: {p.get_nome()} | Tarefas: {len(p.listar_tarefas())}" for p in projetos]
        return lista if lista else "Nenhum projeto cadastrado."

    def mostrar_projeto(self, projeto: Projeto | None) -> str:
        if projeto is None:
            return "Projeto não encontrado."
        return f"ID: {projeto.get_id()} | Nome: {projeto.get_nome()} | Tarefas: {len(projeto.listar_tarefas())}"


class TarefaView:
    def listar_tarefas(self, tarefas: Iterable[Tarefa]) -> str | Iterable:
        lista = [f"Descrição: {t.get_descricao()} | Responsável: {t.get_responsavel()} | Status: {t.get_status()}" for t in tarefas]
        return lista if lista else "Nenhuma tarefa cadastrada."

    def mostrar_tarefa(self, tarefa: Tarefa | None) -> str:
        if tarefa is None:
            return "Tarefa não encontrada."
        return f"Descrição: {tarefa.get_descricao()} | Responsável: {tarefa.get_responsavel()} | Status: {tarefa.get_status()}"

