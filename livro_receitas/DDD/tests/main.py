from domain.value_objects.quantidade import Quantidade
from domain.entities.livro_receitas import LivroReceitas
from domain.value_objects.autor import Autor
from datetime import datetime
from domain.entities.receita import Receita
from domain.entities.ingrediente import Ingrediente
from domain.entities.categoria import Categoria
from infraestructure.repositories.livro_repository import LivroReceitasRepository
from infraestructure.database import init_db
from infraestructure.repositories.livro_sqlite_repository import LivroReceitasSQLiteRepository

if __name__ == "__main__":
    try:
        autor_valido = Autor('Maria Silva')
        print(f"Autor válido criado: {autor_valido}")
    except Exception as e:
        print(f"Erro ao criar autor válido: {e}")

    try:
        autor_invalido = Autor('Maria')
        print(f"Autor inválido criado (não deveria): {autor_invalido}")
    except Exception as e:
        print(f"Corretamente rejeitou autor inválido: {e}")
    try:
        q1 = Quantidade(100, 'gram')
        q2 = Quantidade(2, 'cup')
        q3 = Quantidade(1, 'liter')
        print('Instanciou Quantidade com unidades válidas.')
    except Exception as e:
        print('Erro ao instanciar Quantidade:', e)

    try:
        q4 = Quantidade(5, 'meter')
    except Exception as e:
        print('Corretamente rejeitou unidade inválida:', e)

    ingrediente1 = Ingrediente('Farinha', Quantidade(200, 'gram'))
    ingrediente2 = Ingrediente('Açúcar', Quantidade(100, 'gram'))
    ingrediente3 = Ingrediente('Leite', Quantidade(300, 'ml'))
    ingrediente4 = Ingrediente('Ovo', Quantidade(2, 'count'))

    receita1 = Receita(
        nome='Bolo',
        tempo_preparo=60.0,
        rendimento='8 porções',
        modo_preparo='Misture tudo e asse por 40 minutos.',
        ingredientes=[ingrediente1, ingrediente2, ingrediente3, ingrediente4]
    )
    receita2 = Receita(
        nome='Panqueca',
        tempo_preparo=30.0,
        rendimento='6 porções',
        modo_preparo='Misture, frite em frigideira.',
        ingredientes=[ingrediente1, ingrediente3, ingrediente4]
    )
    receita3 = Receita(
        nome='Pudim',
        tempo_preparo=90.0,
        rendimento='10 porções',
        modo_preparo='Bata, asse em banho-maria.',
        ingredientes=[ingrediente2, ingrediente3]
    )

    categoria_doces = Categoria(
        nome='Doces',
        descricao='Receitas doces',
        receitas=[receita1, receita3]
    )
    categoria_salgados = Categoria(
        nome='Salgados',
        descricao='Receitas salgadas',
        receitas=[receita2]
    )

    autor = Autor('Eric Verschoor')

    livro = LivroReceitas(
        titulo='Livro de Teste',
        autor=autor,
        data_criacao=datetime.now(),
        receitas_avulsas=[receita2],
        categorias=[categoria_doces, categoria_salgados]
    )

    # Repositório em memória
    repo = LivroReceitasRepository()
    repo.add(livro)
    print(f"Livro persistido em memória. Total armazenado: {len(repo.list())}")
    recuperado = repo.get(livro.id)
    print('Recuperado pelo ID igual?', recuperado is livro)

    # Repositório SQLite
    init_db()
    sqlite_repo = LivroReceitasSQLiteRepository()
    sqlite_repo.add(livro)
    print('Livro salvo em SQLite.')
    mesmo = sqlite_repo.get(livro.id)
    print('Carregado do SQLite título:', mesmo.titulo if mesmo else 'N/A')

    print('Livro de receitas criado com:', len(livro.receitas), 'receitas')
    for r in livro.receitas:
        print(f'Receita: {r.nome}, Ingredientes: {[i.nome for i in r.ingredientes]}')

    print('\nCategorias e suas receitas:')
    for cat in livro.categorias:
        print(f'Categoria: {cat.nome}, Receitas: {[r.nome for r in cat.receitas]}')