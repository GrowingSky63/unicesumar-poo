import sqlite3
from pathlib import Path

_DB_NAME = 'livro_receitas.db'
_BASE_DIR = Path(__file__).resolve().parent
_DB_PATH = _BASE_DIR / _DB_NAME

def get_connection():
    conn = sqlite3.connect(_DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    # Tabelas
    cur.execute("""
    CREATE TABLE IF NOT EXISTS livros (
        id TEXT PRIMARY KEY,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        data_criacao TEXT NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        descricao TEXT,
        livro_id TEXT NOT NULL,
        FOREIGN KEY(livro_id) REFERENCES livros(id) ON DELETE CASCADE
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS receitas (
        id TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        tempo_preparo REAL NOT NULL,
        rendimento TEXT NOT NULL,
        modo_preparo TEXT NOT NULL,
        livro_id TEXT NOT NULL,
        FOREIGN KEY(livro_id) REFERENCES livros(id) ON DELETE CASCADE
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS categoria_receita (
        categoria_id TEXT NOT NULL,
        receita_id TEXT NOT NULL,
        PRIMARY KEY(categoria_id, receita_id),
        FOREIGN KEY(categoria_id) REFERENCES categorias(id) ON DELETE CASCADE,
        FOREIGN KEY(receita_id) REFERENCES receitas(id) ON DELETE CASCADE
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ingredientes (
        id TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        quantidade TEXT,
        receita_id TEXT NOT NULL,
        FOREIGN KEY(receita_id) REFERENCES receitas(id) ON DELETE CASCADE
    )
    """)
    conn.commit()
    conn.close()
