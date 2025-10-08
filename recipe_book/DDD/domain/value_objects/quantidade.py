from dataclasses import dataclass

COOKING_UNITS = {
    'gram', 'kilogram', 'mg', 'g', 'kg', 'milligram',
    'liter', 'milliliter', 'l', 'ml',
    'teaspoon', 'tablespoon', 'cup', 'tbsp', 'tsp',
    'oz', 'ounce', 'lb', 'pound',
    'pinch', 'dash', 'quart', 'pint', 'gal', 'gallon',
    'unit', 'count'
}

@dataclass(frozen=True)
class Quantidade:
    valor: float
    unidade: str

    def __post_init__(self):
        unit_str = self.unidade.lower()
        if not any(u == unit_str for u in COOKING_UNITS):
            raise ValueError(f"Unidade '{self.unidade}' não é uma unidade culinária válida.")

    def __str__(self):
        return f"{self.valor} {self.unidade}"

    @classmethod
    def from_string(cls, s: str):
        parts = s.strip().split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError(f"Formato de quantidade inválido: '{s}'")
        value_raw, unit = parts
        try:
            value = float(value_raw)
        except ValueError as e:
            raise ValueError(f"Valor numérico inválido em quantidade: '{value_raw}'") from e
        return cls(value, unit)
