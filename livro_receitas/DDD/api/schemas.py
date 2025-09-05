from domain.entities.livro_receitas import LivroReceitas
from domain.entities.receita import Receita
from domain.entities.categoria import Categoria
from domain.entities.ingrediente import Ingrediente
from domain.value_objects.quantidade import Quantidade
from domain.value_objects.autor import Autor


def ingrediente_to_dict(ing: Ingrediente) -> dict:
    return {
        'id': ing.id,
        'nome': ing.nome,
        'quantidade': str(ing.quantidade)
    }


def receita_to_dict(r: Receita) -> dict:
    return {
        'id': r.id,
        'nome': r.nome,
        'tempo_preparo': r.tempo_preparo,
        'rendimento': r.rendimento,
        'modo_preparo': r.modo_preparo,
        'ingredientes': [ingrediente_to_dict(i) for i in r.ingredientes]
    }


def categoria_to_dict(c: Categoria) -> dict:
    return {
        'id': c.id,
        'nome': c.nome,
        'descricao': c.descricao,
        'receitas': [r.id for r in c.receitas]
    }


def livro_to_dict(l: LivroReceitas) -> dict:
    return {
        'id': l.id,
        'titulo': l.titulo,
        'autor': str(l.autor),
        'data_criacao': l.data_criacao.isoformat(),
        'receitas': [receita_to_dict(r) for r in l.receitas],
        'categorias': [categoria_to_dict(c) for c in l.categorias]
    }


def parse_quantidade(raw: str) -> Quantidade:
    return Quantidade.from_string(raw)
