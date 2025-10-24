from .models import Produto, Projeto, Tarefa, StatusTarefa
from .database import get_connection


class ProdutoRepository:
  def add(self, produto: Produto) -> Produto:
    with get_connection() as conn:
      conn.execute(
        "INSERT INTO produtos (id, nome, preco, quantidade) VALUES (?, ?, ?, ?)",
        (produto.get_id(), produto.get_nome(), produto.get_preco(), produto.get_quantidade()),
      )
      conn.commit()
    return produto

  def list(self) -> list[Produto]:
    with get_connection() as conn:
      rows = conn.execute("SELECT id, nome, preco, quantidade FROM produtos ORDER BY id").fetchall()
      return [Produto(id=row["id"], nome=row["nome"], preco=row["preco"], quantidade=row["quantidade"]) for row in rows]

  def get(self, id_: int) -> Produto | None:
    with get_connection() as conn:
      row = conn.execute(
        "SELECT id, nome, preco, quantidade FROM produtos WHERE id = ?",
        (int(id_),),
      ).fetchone()
      if row is None:
        return None
      return Produto(id=row["id"], nome=row["nome"], preco=row["preco"], quantidade=row["quantidade"]) 

  def update_quantidade(self, id_: int, nova_quantidade: int) -> bool:
    with get_connection() as conn:
      cur = conn.execute(
        "UPDATE produtos SET quantidade = ? WHERE id = ?",
        (int(nova_quantidade), int(id_)),
      )
      conn.commit()
      return cur.rowcount > 0

  def remove(self, id_: int) -> bool:
    with get_connection() as conn:
      cur = conn.execute("DELETE FROM produtos WHERE id = ?", (int(id_),))
      conn.commit()
      return cur.rowcount > 0


class ProjetoRepository:
  def add(self, projeto: Projeto) -> Projeto:
    with get_connection() as conn:
      conn.execute(
        "INSERT INTO projetos (id, nome) VALUES (?, ?)",
        (projeto.get_id(), projeto.get_nome()),
      )
      conn.commit()
    return projeto

  def list(self) -> list[Projeto]:
    with get_connection() as conn:
      rows = conn.execute("SELECT id, nome FROM projetos ORDER BY id").fetchall()
      return [Projeto(id=row["id"], nome=row["nome"]) for row in rows]

  def get(self, id_: int) -> Projeto | None:
    with get_connection() as conn:
      row = conn.execute("SELECT id, nome FROM projetos WHERE id = ?", (int(id_),)).fetchone()
      if row is None:
        return None
      # tarefas serão buscadas sob demanda
      return Projeto(id=row["id"], nome=row["nome"]) 


class TarefaRepository:
  def add(self, projeto_id: int, tarefa: Tarefa) -> Tarefa:
    with get_connection() as conn:
      conn.execute(
        "INSERT INTO tarefas (projeto_id, descricao, responsavel, status) VALUES (?, ?, ?, ?)",
        (int(projeto_id), tarefa.get_descricao(), tarefa.get_responsavel(), tarefa.get_status()),
      )
      conn.commit()
    return tarefa

  def list_by_projeto(self, projeto_id: int) -> list[Tarefa]:
    with get_connection() as conn:
      rows = conn.execute(
        "SELECT descricao, responsavel, status FROM tarefas WHERE projeto_id = ? ORDER BY id",
        (int(projeto_id),),
      ).fetchall()
      return [Tarefa(descricao=row["descricao"], responsavel=row["responsavel"], status=row["status"]) for row in rows]

  def list_by_projeto_and_status(self, projeto_id: int, status: str | StatusTarefa) -> list[Tarefa]:
    if isinstance(status, StatusTarefa):
      st = status.value
    else:
      st = str(status).strip().lower().replace(" ", "_")
    with get_connection() as conn:
      rows = conn.execute(
        "SELECT descricao, responsavel, status FROM tarefas WHERE projeto_id = ? AND status = ? ORDER BY id",
        (int(projeto_id), st),
      ).fetchall()
      return [Tarefa(descricao=row["descricao"], responsavel=row["responsavel"], status=row["status"]) for row in rows]
