import sqlite3
from pathlib import Path

DB_FILENAME = "data.sqlite3"
DB_PATH = Path(__file__).resolve().parent / DB_FILENAME

def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
  """Método responsável por fornecer uma conexão a um banco"""
  path = Path(db_path) if db_path is not None else DB_PATH
  conn = sqlite3.connect(path)
  # Definir uma row factory para os retornos das querys virem em dicionários ao invés de tuplas
  conn.row_factory = sqlite3.Row
  return conn

def init_db() -> None:
  """Método responsável por assegurar que o banco e as tabelas sejam criadas"""
  with get_connection() as conn:
    conn.execute(
      """
      CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        preco REAL NOT NULL CHECK (preco >= 0),
        quantidade INTEGER NOT NULL CHECK (quantidade >= 0)
      );
      """
    )
    conn.execute(
      """
      CREATE TABLE IF NOT EXISTS projetos (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL
      );
      """
    )
    conn.execute(
      """
      CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        projeto_id INTEGER NOT NULL,
        descricao TEXT NOT NULL,
        responsavel TEXT NOT NULL,
        status TEXT NOT NULL CHECK (status IN ('pendente','em_andamento','concluida')),
        FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE
      );
      """
    )
    conn.commit()
