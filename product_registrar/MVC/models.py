from typing import Any
from enum import Enum


class Produto:
  """Classe que representa o modelo de uma entidade Produto"""
  def __init__(self, id: int, nome: str, preco: float, quantidade: int) -> None:
    # Inicialização da classe
    self._id = int(id)
    self._nome = str(nome)
    self.set_preco(preco)
    self.set_quantidade(quantidade)

  # GETTERS E SETTERS
  def get_id(self) -> int:
    return self._id

  def set_id(self, novo_id: int) -> None:
    self._id = int(novo_id)

  def get_nome(self) -> str:
    return self._nome

  def set_nome(self, novo_nome: str) -> None:
    self._nome = str(novo_nome)

  def get_preco(self) -> float:
    return self._preco

  def set_preco(self, novo_preco: float) -> None:
    valor = float(novo_preco)
    if valor < 0:
      raise ValueError("Preço não pode ser negativo")
    self._preco = valor

  def get_quantidade(self) -> int:
    return self._quantidade

  def set_quantidade(self, nova_qtd: int) -> None:
    qtd = int(nova_qtd)
    if qtd < 0:
      raise ValueError("Quantidade não pode ser negativa")
    self._quantidade = qtd

  def to_dict(self) -> dict[str, Any]:
    """Método para converter os atributos da entidade em um dicionário"""
    return {
      "id": self.get_id(),
      "nome": self.get_nome(),
      "preco": self.get_preco(),
      "quantidade": self.get_quantidade(),
    }

  def __repr__(self) -> str:
    return f"Produto(id={self.get_id()}, nome='{self.get_nome()}', preco={self.get_preco():.2f}, quantidade={self.get_quantidade()})"


class StatusTarefa(Enum):
  """Enum que representa os possíveis status de uma tarefa."""
  PENDENTE = "pendente"
  EM_ANDAMENTO = "em_andamento"
  CONCLUIDA = "concluida"


class Tarefa:
  """Classe que representa o modelo de uma entidade Tarefa"""
  def __init__(self, descricao: str, responsavel: str, status: str | StatusTarefa = StatusTarefa.PENDENTE) -> None:
    self.set_descricao(descricao)
    self.set_responsavel(responsavel)
    self.set_status(status)

  # GETTERS/SETTERS
  def get_descricao(self) -> str:
    return self._descricao

  def set_descricao(self, descricao: str) -> None:
    descricao = str(descricao).strip()
    if not descricao:
      raise ValueError("Descrição da tarefa não pode ser vazia")
    self._descricao = descricao

  def get_responsavel(self) -> str:
    return self._responsavel

  def set_responsavel(self, responsavel: str) -> None:
    responsavel = str(responsavel).strip()
    if not responsavel:
      raise ValueError("Responsável não pode ser vazio")
    self._responsavel = responsavel

  def get_status(self) -> str:
    return self._status

  def set_status(self, status: str | StatusTarefa) -> None:
    if isinstance(status, StatusTarefa):
      value = status.value
    else:
      value = str(status).strip().lower().replace(" ", "_")
    if value not in {s.value for s in StatusTarefa}:
      raise ValueError("Status inválido. Use: pendente, em_andamento ou concluida")
    self._status = value

  def to_dict(self) -> dict[str, Any]:
    return {
      "descricao": self.get_descricao(),
      "responsavel": self.get_responsavel(),
      "status": self.get_status(),
    }

  def __repr__(self) -> str:
    return f"Tarefa(descricao='{self.get_descricao()}', responsavel='{self.get_responsavel()}', status='{self.get_status()}')"


class Projeto:
  """Classe que representa o modelo de uma entidade Projeto"""

  def __init__(self, id: int, nome: str, tarefas: list[Tarefa] | None = None) -> None:
    self._id = int(id)
    self.set_nome(nome)
    self._tarefas: list[Tarefa] = list(tarefas) if tarefas is not None else []

  # GETTERS/SETTERS
  def get_id(self) -> int:
    return self._id

  def set_id(self, novo_id: int) -> None:
    self._id = int(novo_id)

  def get_nome(self) -> str:
    return self._nome

  def set_nome(self, nome: str) -> None:
    nome = str(nome).strip()
    if not nome:
      raise ValueError("Nome do projeto não pode ser vazio")
    self._nome = nome

  # Tarefas
  def adicionar_tarefa(self, tarefa: Tarefa) -> None:
    self._tarefas.append(tarefa)

  def listar_tarefas(self) -> list[Tarefa]:
    return list(self._tarefas)

  def tarefas_por_status(self, status: str | StatusTarefa) -> list[Tarefa]:
    if isinstance(status, StatusTarefa):
      value = status.value
    else:
      value = str(status).strip().lower().replace(" ", "_")
    return [t for t in self._tarefas if t.get_status() == value]

  def to_dict(self) -> dict[str, Any]:
    return {
      "id": self.get_id(),
      "nome": self.get_nome(),
      "tarefas": [t.to_dict() for t in self._tarefas],
    }

  def __repr__(self) -> str:
    return f"Projeto(id={self.get_id()}, nome='{self.get_nome()}', tarefas={len(self._tarefas)})"

