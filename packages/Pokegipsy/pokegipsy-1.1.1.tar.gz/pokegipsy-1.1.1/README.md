# Pokegipsy
Es una libreria para generar un pokemon aleatorio
 
## Instalacion 
Para instalar la libreria tienes que usar `pip install Pokegipsy`

## Uso
Aquí hay un ejemplo de como puedes usar la biblioteca para obtener informacion sobre Pokemón aleatorios:

```python
from Pokegipsy import RandomPokemon

# Crear una instancia de RandomPokemon
pokemon = RandomPokemon()

# Generar un Pokemón aleatorio
pokemon.generate_random()

# Obtener el nombre del Pokemón generado
pokemon_name = pokemon.getName()

# Imprimir el nombre del Pokemón 
print("Nombre del Pokemón: ", pokemon_name)

```
## Archivo CSV de Pokemón
La biblioteca utiliza un archivo CSV llamado pokemon.csv que contiene datos de Pokemón. Este archivo incluye en el paquete y se utiliza para generar Pokemón aleatorios. Si necesitas acceder al archivo pokemon.csv directamente, puedes encontrarlo en el directorio Pokegipsy.

## Autor
Fernando Gonzalez

