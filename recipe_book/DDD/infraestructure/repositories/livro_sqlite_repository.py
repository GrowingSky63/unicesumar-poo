from datetime import datetime
from typing import Optional, List
import sqlite3

from domain.entities.livro_receitas import LivroReceitas
from domain.entities.receita import Receita
from domain.entities.categoria import Categoria
from domain.entities.ingrediente import Ingrediente
from uuid import uuid4
from domain.value_objects.autor import Autor
from domain.value_objects.quantidade import Quantidade
from domain.repository import Repository
from infraestructure.database import get_connection

class LivroReceitasSQLiteRepository(Repository[LivroReceitas]):
    def add(self, entity: LivroReceitas) -> LivroReceitas:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO livros (id, titulo, autor, data_criacao) VALUES (?, ?, ?, ?)',
                    (entity.id, entity.titulo, str(entity.autor), entity.data_criacao.isoformat()))
        # categorias
        for cat in entity.categorias:
            cur.execute('INSERT INTO categorias (id, nome, descricao, livro_id) VALUES (?, ?, ?, ?)',
                        (cat.id, cat.nome, cat.descricao, entity.id))
        # receitas
        for rec in entity.receitas:
            cur.execute('INSERT INTO receitas (id, nome, tempo_preparo, rendimento, modo_preparo, livro_id) VALUES (?, ?, ?, ?, ?, ?)',
                        (rec.id, rec.nome, rec.tempo_preparo, rec.rendimento, rec.modo_preparo, entity.id))
            # ingredientes
            for ing in rec.ingredientes:
                # Se o mesmo objeto ingrediente for compartilhado entre receitas, gerar novo id para evitar conflito
                ing_id = getattr(ing, 'id', None)
                if ing_id in [row[0] for row in cur.execute('SELECT id FROM ingredientes')]:
                    ing_id = str(uuid4())
                else:
                    if ing_id is None:
                        ing_id = str(uuid4())
                cur.execute('INSERT INTO ingredientes (id, nome, quantidade, receita_id) VALUES (?, ?, ?, ?)',
                            (ing_id, ing.nome, str(ing.quantidade), rec.id))
        # relações categoria_receita
        for cat in entity.categorias:
            for rec in cat.receitas:
                cur.execute('INSERT OR IGNORE INTO categoria_receita (categoria_id, receita_id) VALUES (?, ?)',
                            (cat.id, rec.id))
        conn.commit()
        conn.close()
        return entity

    def get(self, entity_id: str) -> Optional[LivroReceitas]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, titulo, autor, data_criacao FROM livros WHERE id = ?', (entity_id,))
        row = cur.fetchone()
        if not row:
            conn.close()
            return None
        livro_id, titulo, autor_str, data_str = row
        # categorias
        cur.execute('SELECT id, nome, descricao FROM categorias WHERE livro_id = ?', (livro_id,))
        categoria_rows = cur.fetchall()
        categorias: List[Categoria] = []
        cat_map = {}
        for cid, nome, desc in categoria_rows:
            cat = Categoria(nome=nome, descricao=desc, receitas=[] , id=cid)  # type: ignore
            categorias.append(cat)
            cat_map[cid] = cat
        # receitas
        cur.execute('SELECT id, nome, tempo_preparo, rendimento, modo_preparo FROM receitas WHERE livro_id = ?', (livro_id,))
        receita_rows = cur.fetchall()
        receitas: List[Receita] = []
        rec_map = {}
        for rid, nome, tempo, rendimento, modo in receita_rows:
            # ingredientes
            cur.execute('SELECT id, nome, quantidade FROM ingredientes WHERE receita_id = ?', (rid,))
            ing_rows = cur.fetchall()
            ingredientes: List[Ingrediente] = []
            for ing_id, ing_nome, ing_qtd in ing_rows:
                # Quantidade armazenada como string; mantemos string simples (não reconstrói unidade original complexa)
                ingredientes.append(Ingrediente(nome=ing_nome, quantidade=ing_qtd, id=ing_id))  # type: ignore
            rec = Receita(nome=nome, tempo_preparo=tempo, rendimento=rendimento, modo_preparo=modo, ingredientes=ingredientes, id=rid)  # type: ignore
            receitas.append(rec)
            rec_map[rid] = rec
        # relacionar categorias/receitas
        cur.execute('SELECT categoria_id, receita_id FROM categoria_receita WHERE categoria_id IN ({seq})'.format(
            seq=','.join(['?'] * len(cat_map))) , tuple(cat_map.keys()))
        rel_rows = cur.fetchall()
        for cid, rid in rel_rows:
            if cid in cat_map and rid in rec_map:
                cat_map[cid].receitas.append(rec_map[rid])
        conn.close()
        livro = LivroReceitas(titulo=titulo, autor=Autor(autor_str), data_criacao=datetime.fromisoformat(data_str), receitas=receitas, categorias=categorias)
        # forçamos o id original
        livro.id = livro_id  # type: ignore
        return livro

    def list(self) -> List[LivroReceitas]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id FROM livros')
        ids = [r[0] for r in cur.fetchall()]
        conn.close()
        resultados: List[LivroReceitas] = []
        for i in ids:
            obj = self.get(i)
            if obj is not None:
                resultados.append(obj)
        return resultados

    def remove(self, entity_id: str) -> None:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM livros WHERE id = ?', (entity_id,))
        conn.commit()
        conn.close()

    def update(self, entity: LivroReceitas) -> LivroReceitas:
        # estratégia simples: remover e inserir novamente (idempotente)
        self.remove(entity.id)
        return self.add(entity)
