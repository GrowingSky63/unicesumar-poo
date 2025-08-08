
from pint import UnitRegistry, Unit

ureg = UnitRegistry()

# Lista de unidades culinárias permitidas
COOKING_UNITS = {
	'gram', 'kilogram', 'mg', 'g', 'kg', 'milligram',
	'liter', 'milliliter', 'l', 'ml',
	'teaspoon', 'tablespoon', 'cup', 'tbsp', 'tsp',
	'oz', 'ounce', 'lb', 'pound',
	'pinch', 'dash', 'quart', 'pint', 'gal', 'gallon',
	'unit', 'count',
}

class Quantidade(Unit):
	def __new__(cls, value, units):
		# Normaliza unidade para comparação
		unit_str = str(units).lower()
		# Verifica se a unidade está entre as permitidas
		if not any(u in unit_str for u in COOKING_UNITS):
			raise ValueError(f"Unidade '{units}' não é uma unidade culinária válida.")
		# Cria a unidade usando o UnitRegistry
		obj = ureg.Quantity(value, units).to_base_units()._units
		# Instancia como Unit
		return super().__new__(cls, obj)

	def __init__(self, value, units):
		# Não faz nada, pois Unit é imutável
		pass
