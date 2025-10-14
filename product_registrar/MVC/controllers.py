from typing import List, Optional

from .models import Produto, Projeto, Tarefa, StatusTarefa


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


class ProjetoController:
    """
    Controlador de projetos: gerencia criação e consulta de projetos
    """

    def __init__(self) -> None:
        self._projetos: List[Projeto] = []

    def adicionar_projeto(self, id: int, nome: str) -> Projeto:
        if self.buscar_por_id(id) is not None:
            raise ValueError("Já existe um projeto com esse ID")
        projeto = Projeto(id=id, nome=nome)
        self._projetos.append(projeto)
        return projeto

    def listar_projetos(self) -> List[Projeto]:
        return list(self._projetos)

    def buscar_por_id(self, id: int) -> Optional[Projeto]:
        for p in self._projetos:
            if p.get_id() == int(id):
                return p
        return None


class TarefaController:
    """
    Controlador de tarefas por projeto
    """

    def __init__(self, projeto_controller: ProjetoController) -> None:
        self._projeto_controller = projeto_controller

    def adicionar_tarefa(self, projeto_id: int, descricao: str, responsavel: str, status: str | StatusTarefa = StatusTarefa.PENDENTE) -> Tarefa:
        projeto = self._projeto_controller.buscar_por_id(projeto_id)
        if projeto is None:
            raise ValueError("Projeto não encontrado")
        tarefa = Tarefa(descricao=descricao, responsavel=responsavel, status=status)
        projeto.adicionar_tarefa(tarefa)
        return tarefa

    def listar_tarefas(self, projeto_id: int) -> List[Tarefa]:
        projeto = self._projeto_controller.buscar_por_id(projeto_id)
        if projeto is None:
            raise ValueError("Projeto não encontrado")
        return projeto.listar_tarefas()

    def filtrar_tarefas(self, projeto_id: int, status: str | StatusTarefa) -> List[Tarefa]:
        projeto = self._projeto_controller.buscar_por_id(projeto_id)
        if projeto is None:
            raise ValueError("Projeto não encontrado")
        return projeto.tarefas_por_status(status)

