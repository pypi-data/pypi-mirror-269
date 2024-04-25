# PokeCorky
Es una libreria para generar un pokemon aleatorio
## Instalacion
Para instalar la libreria tienes que usar  `pip install PokeCorky`
## Uso 
Aqui hay un ejemplo de como puedes usar la biblioteca para obtener informacion sobre pokemon aleatorios.
``` python
from Pokecorky import RandomPokemon
#crear una instancia de RandomPokemon
pokemon= RandomPokemon()
#generar un pokemon aleatorio
pokemon.generate_random()
#obtener el nombre del pokemon generado
pokemon_name=pokemon.getName()
#imprimir el nombre del pokemon
print("Nombre del pokemon:", pokemon_name)
``` 
### Archivo CSV de pokemon
La biblioteca utiliza un archivo CSV llamado pokemon.csv que contiene datos de Pokemon. Este archivo se incluye en el paquete y se utiliza para generar pokemon aleatorios. Si necesitas acceder al archivo pokemon.csv directamente, puedes encontrarlo en el directorio PokeCorky
### Autor
Victor Diaz
