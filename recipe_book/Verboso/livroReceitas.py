from datetime import datetime

class LivroReceitas:
    def __init__(self, titulo: str, autor: str):
        self.__titulo = titulo
        self.__autor = autor
        self.__data_criacao = datetime.now()
        self.__receitas = []
        self.__categorias = []

    # Getters
    @property
    def titulo(self) -> str:
        return self.__titulo

    @property
    def autor(self) -> str:
        return self.__autor

    @property
    def data_criacao(self) -> datetime:
        return self.__data_criacao

    # Setters
    @titulo.setter
    def titulo(self, titulo: str) -> None:
        self.__titulo = titulo

    @autor.setter
    def autor(self, autor: str) -> None:
        self.__autor = autor

    # Métodos
    def adicionar_receita(self, receita) -> None:
        self.__receitas.append(receita)

    def listar_receitas(self) -> list['Receita']:
        return self.__receitas

    def buscar_receita(self, nome: str) -> 'Receita':
        for receita in self.__receitas:
            if receita.nome.lower() == nome.lower():
                return receita
        return None

    def adicionar_categoria(self, categoria) -> None:
        self.__categorias.append(categoria)

    def listar_categorias(self) -> list['Categoria']:
        return self.__categorias


class Categoria:
    def __init__(self, nome: str, descricao: str):
        self.__nome = nome
        self.__descricao = descricao

    # Getters
    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def descricao(self) -> str:
        return self.__descricao

    # Setters
    @nome.setter
    def nome(self, nome: str) -> None:
        self.__nome = nome

    @descricao.setter
    def descricao(self, descricao: str) -> None:
        self.__descricao = descricao


class Receita:
    def __init__(self, nome: str, tempo_preparo: int, rendimento: str, modo_preparo: str):
        self.__nome = nome
        self.__tempo_preparo = tempo_preparo  # em minutos
        self.__rendimento = rendimento
        self.__modo_preparo = modo_preparo
        self.__ingredientes = []

    # Getters
    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def tempo_preparo(self) -> int:
        return self.__tempo_preparo

    @property
    def rendimento(self) -> str:
        return self.__rendimento

    @property
    def modo_preparo(self) -> str:
        return self.__modo_preparo

    @property
    def ingredientes(self) -> list['Ingrediente']:
        return self.__ingredientes

    # Setters
    @nome.setter
    def nome(self, nome: str) -> None:
        self.__nome = nome

    @tempo_preparo.setter
    def tempo_preparo(self, tempo_preparo: int) -> None:
        self.__tempo_preparo = tempo_preparo

    @rendimento.setter
    def rendimento(self, rendimento: str) -> None:
        self.__rendimento = rendimento

    @modo_preparo.setter
    def modo_preparo(self, modo_preparo: str) -> None:
        self.__modo_preparo = modo_preparo

    def adicionar_ingrediente(self, ingrediente) -> None:
        self.__ingredientes.append(ingrediente)

    def listar_ingredientes(self) -> list['Ingrediente']:
        return self.__ingredientes


class Ingrediente:
    def __init__(self, nome: str, quantidade: str):
        self.__nome = nome
        self.__quantidade = quantidade

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def quantidade(self) -> str:
        return self.__quantidade

    @nome.setter
    def nome(self, nome: str) -> None:
        self.__nome = nome

    @quantidade.setter
    def quantidade(self, quantidade: str) -> None:
        self.__quantidade = quantidade

if __name__ == "__main__":
    # Criando um livro de receitas
    livro = LivroReceitas(titulo="Minhas Receitas", autor="Chef Python")
    
    sobremesa = Categoria(nome="Sobremesas", descricao="Receitas doces")
    livro.adicionar_categoria(sobremesa)
    
    farinha = Ingrediente(nome="Farinha de trigo", quantidade="2 xícaras")
    acucar = Ingrediente(nome="Açúcar", quantidade="1 xícara")
    ovos = Ingrediente(nome="Ovos", quantidade="3 unidades")
    
    bolo = Receita(
        nome="Bolo Simples",
        tempo_preparo=45,
        rendimento="8 porções",
        modo_preparo="Misture todos os ingredientes e asse por 40 minutos."
    )
    
    bolo.adicionar_ingrediente(farinha)
    bolo.adicionar_ingrediente(acucar)
    bolo.adicionar_ingrediente(ovos)
    
    livro.adicionar_receita(bolo)
    
    receita_encontrada = livro.buscar_receita("Bolo Simples")
    if receita_encontrada:
        print(f"Receita: {receita_encontrada.nome}")
        print(f"Tempo de preparo: {receita_encontrada.tempo_preparo} minutos")
        print("Ingredientes:")
        for ingrediente in receita_encontrada.listar_ingredientes():
            print(f"- {ingrediente.quantidade} de {ingrediente.nome}")