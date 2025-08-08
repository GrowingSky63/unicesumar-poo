from nameparser import HumanName

class Autor(str):
    """
    Value object para nome de autor, com verificação simples de nome próprio.
    """
    def __new__(cls, value):
        # Verificação simples usando nameparser
        name = HumanName(value)
        if not name.first or not name.last:
            raise ValueError(f"Nome '{value}' não parece ser um nome próprio válido.")
        return str.__new__(cls, value)
