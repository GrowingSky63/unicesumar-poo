from typing import Any


class Produto:
    """
    Classe que representa o modelo da entidade Produto
    """
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
        """
        Método para converter os atributos da entidade em um dicionário
        """
        return {
            "id": self.get_id(),
            "nome": self.get_nome(),
            "preco": self.get_preco(),
            "quantidade": self.get_quantidade(),
        }

    def __repr__(self) -> str:
        return f"Produto(id={self.get_id()}, nome='{self.get_nome()}', preco={self.get_preco():.2f}, quantidade={self.get_quantidade()})"

