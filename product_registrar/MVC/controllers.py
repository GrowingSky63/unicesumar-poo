from .models import Produto, Projeto, Tarefa, StatusTarefa
from .repositories import ProdutoRepository, ProjetoRepository, TarefaRepository


class ProdutoController:
  """Classe responsável por implementar as regras de negócio da aplicação"""
  def __init__(self, repo: ProdutoRepository | None = None) -> None:
    self._repo = repo or ProdutoRepository()

  def adicionar_produto(self, id: int, nome: str, preco: float, quantidade: int) -> Produto:
    if self.buscar_por_id(id) is not None:
      raise ValueError("Já existe um produto com esse ID")
    produto = Produto(id=id, nome=nome, preco=preco, quantidade=quantidade)
    self._repo.add(produto)
    return produto

  def listar_produtos(self) -> list[Produto]:
    return self._repo.list()

  def atualizar_quantidade(self, id: int, nova_quantidade: int) -> bool:
    # Atualiza diretamente no repositório
    return self._repo.update_quantidade(id, nova_quantidade)

  def remover_produto(self, id: int) -> bool:
    return self._repo.remove(id)

  def buscar_por_id(self, id: int) -> Produto | None:
    return self._repo.get(id)


class ProjetoController:
  """Controlador de projetos: gerencia criação e consulta de projetos"""

  def __init__(self, repo: ProjetoRepository | None = None) -> None:
    self._repo = repo or ProjetoRepository()

  def adicionar_projeto(self, id: int, nome: str) -> Projeto:
    if self.buscar_por_id(id) is not None:
      raise ValueError("Já existe um projeto com esse ID")
    projeto = Projeto(id=id, nome=nome)
    self._repo.add(projeto)
    return projeto

  def listar_projetos(self) -> list[Projeto]:
    return self._repo.list()

  def buscar_por_id(self, id: int) -> Projeto | None:
    return self._repo.get(id)


class TarefaController:
  """Controlador de tarefas por projeto"""

  def __init__(self, projeto_controller: ProjetoController, repo: TarefaRepository | None = None) -> None:
    self._projeto_controller = projeto_controller
    self._repo = repo or TarefaRepository()

  def adicionar_tarefa(self, projeto_id: int, descricao: str, responsavel: str, status: str | StatusTarefa = StatusTarefa.PENDENTE) -> Tarefa:
    projeto = self._projeto_controller.buscar_por_id(projeto_id)
    if projeto is None:
      raise ValueError("Projeto não encontrado")
    tarefa = Tarefa(descricao=descricao, responsavel=responsavel, status=status)
    self._repo.add(projeto_id, tarefa)
    return tarefa

  def listar_tarefas(self, projeto_id: int) -> list[Tarefa]:
    projeto = self._projeto_controller.buscar_por_id(projeto_id)
    if projeto is None:
      raise ValueError("Projeto não encontrado")
    return self._repo.list_by_projeto(projeto_id)

  def filtrar_tarefas(self, projeto_id: int, status: str | StatusTarefa) -> list[Tarefa]:
    projeto = self._projeto_controller.buscar_por_id(projeto_id)
    if projeto is None:
      raise ValueError("Projeto não encontrado")
    return self._repo.list_by_projeto_and_status(projeto_id, status)

