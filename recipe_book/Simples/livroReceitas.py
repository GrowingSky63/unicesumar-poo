from datetime import datetime

class LivroReceitas:
    """
    Classe para representar uma coleção de Receitas
    """
    def __init__(self, titulo: str, autor: str):
        self.titulo: str = titulo
        self.autor: str = autor
        self.data_criacao: datetime = datetime.now()
        self.receitas: list['Receita'] = []
        self.categorias: list['Categoria'] = []
    
    def buscar_receita(self, nome: str) -> 'Receita':
        """
        Método para buscar uma Receita através de seu nome.
        """
        for receita in self.receitas:
            if receita.nome.lower() == nome.lower():
                return receita
        return None

class Categoria:
    """
    Classe para representar uma categoria de receita
    """
    def __init__(self, nome: str, descricao: str):
        self.nome: str = nome
        self.descricao: str = descricao

class Receita:
    """
    Classe `main`, representando a entidade mais importante do projeto, a Receita.
    """
    def __init__(self, nome: str, tempo_preparo: int, rendimento: str, modo_preparo: str):
        self.nome: str = nome
        self.tempo_preparo: int = tempo_preparo
        self.rendimento: str = rendimento
        self.modo_preparo: str = modo_preparo
        self.ingredientes: list['Ingrediente'] = []


class Ingrediente:
    """
    Classe para representar um ingrediente para receitas
    """
    def __init__(self, nome: str, quantidade: str):
        self.nome: str = nome
        self.quantidade: str = quantidade

if __name__ == "__main__":
    livro = LivroReceitas(
        titulo="Minhas Receitas",
        autor="Chef Python"
    )
    
    sobremesa = Categoria(
        nome="Sobremesas",
        descricao="Receitas doces"
    )

    livro.categorias.append(sobremesa)
    
    farinha = Ingrediente(
        nome="Farinha de trigo",
        quantidade="2 xícaras"
    )

    acucar = Ingrediente(
        nome="Açúcar",
        quantidade="1 xícara"
    )

    ovos = Ingrediente(
        nome="Ovos",
        quantidade="3 unidades"
    )
    
    bolo = Receita(
        nome="Bolo Simples",
        tempo_preparo=45,
        rendimento="8 porções",
        modo_preparo="Misture todos os ingredientes e asse por 40 minutos."
    )
    
    bolo.ingredientes.append(farinha)
    bolo.ingredientes.append(acucar)
    bolo.ingredientes.append(ovos)
    
    livro.receitas.append(bolo)
    
    receita_encontrada = livro.buscar_receita("Bolo Simples")
    if receita_encontrada:
        print(f"Receita: {receita_encontrada.nome}")
        print(f"Tempo de preparo: {receita_encontrada.tempo_preparo} minutos")
        print("Ingredientes:")
        for ingrediente in receita_encontrada.ingredientes:
            print(f"- {ingrediente.quantidade} de {ingrediente.nome}")