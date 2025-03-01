# pokemon_battle.py - Sistema completo de Batallas entre Pokémons
import csv
import random

# Clase para representar un Pokémon
class Pokemon:
    def __init__(self, name, pokemon_type, hp, attack, defense, sp_attack, sp_defense, speed):
        self.name = name
        self.type = pokemon_type
        self.hp = hp
        self.current_hp = hp  # HP actual durante batalla
        self.attack = attack
        self.defense = defense
        self.sp_attack = sp_attack
        self.sp_defense = sp_defense
        self.speed = speed
    
    def __str__(self):
        return f"{self.name} (Tipo: {self.type}, HP: {self.hp}, Ataque: {self.attack}, Defensa: {self.defense})"
    
    # Métodos para batallas
    def attack_pokemon(self, opponent):
        damage = max(2, self.attack - opponent.defense // 2)
        opponent.current_hp = max(0, opponent.current_hp - damage)
        return damage
    
    def is_fainted(self):
        return self.current_hp <= 0
    
    def restore(self):
        self.current_hp = self.hp

# Gestiona la colección de Pokémons
class PokemonManager:
    def __init__(self):
        self.pokemons = {}
    
    def load_from_csv(self, filename):
        """Carga Pokémons desde un archivo CSV"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    pokemon = Pokemon(
                        name=row['Name'],
                        pokemon_type=row['Type'],
                        hp=int(row['HP']),
                        attack=int(row['Attack']),
                        defense=int(row['Defense']),
                        sp_attack=int(row['Sp. Atk']),
                        sp_defense=int(row['Sp. Def']),
                        speed=int(row['Speed'])
                    )
                    self.pokemons[pokemon.name] = pokemon
            return True
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            return False
    
    def add_pokemon(self, pokemon):
        """Agrega un nuevo Pokémon"""
        self.pokemons[pokemon.name] = pokemon
        return True
    
    def update_pokemon(self, name, **kwargs):
        """Actualiza las características de un Pokémon"""
        if name not in self.pokemons:
            return False
        
        pokemon = self.pokemons[name]
        for key, value in kwargs.items():
            if hasattr(pokemon, key):
                setattr(pokemon, key, value)
        return True
    
    def delete_pokemon(self, name):
        """Elimina un Pokémon por su nombre"""
        if name in self.pokemons:
            del self.pokemons[name]
            return True
        return False
    
    def get_pokemon(self, name):
        """Obtiene un Pokémon por su nombre"""
        return self.pokemons.get(name)
    
    def list_all_pokemons(self):
        """Lista todos los Pokémons disponibles"""
        return list(self.pokemons.values())

# Sistema para gestionar batallas entre Pokémons
class BattleSystem:
    def __init__(self, pokemon1, pokemon2):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        # Restaurar HP al iniciar batalla
        self.pokemon1.restore()
        self.pokemon2.restore()
        
    def start_battle(self):
        """Inicia una batalla entre dos Pokémons"""
        print(f"\n¡BATALLA POKÉMON INICIADA!")
        print(f"{self.pokemon1.name} vs {self.pokemon2.name}")
        
        # Determinar quién ataca primero basado en velocidad
        attacker, defender = self._determine_first_attacker()
        
        round_number = 1
        while True:
            print(f"\n--- Ronda {round_number} ---")
            
            # Primer Pokémon ataca
            damage = attacker.attack_pokemon(defender)
            print(f"{attacker.name} ataca a {defender.name} y causa {damage} de daño!")
            print(f"{defender.name}: HP restante = {defender.current_hp}/{defender.hp}")
            
            # Verificar si el segundo Pokémon se debilitó
            if defender.is_fainted():
                print(f"\n{defender.name} se ha debilitado!")
                print(f"{attacker.name} gana la batalla!")
                return attacker
            
            # Intercambiar roles
            attacker, defender = defender, attacker
            round_number += 1
    
    def _determine_first_attacker(self):
        """Determina qué Pokémon ataca primero basado en velocidad"""
        if self.pokemon1.speed > self.pokemon2.speed:
            return self.pokemon1, self.pokemon2
        elif self.pokemon2.speed > self.pokemon1.speed:
            return self.pokemon2, self.pokemon1
        else:
            # En caso de empate, elegir aleatoriamente
            if random.random() < 0.5:
                return self.pokemon1, self.pokemon2
            else:
                return self.pokemon2, self.pokemon1

# Función principal con menú interactivo
def main():
    manager = PokemonManager()
    loaded = manager.load_from_csv("pokemon.csv")
    
    if not loaded:
        print("Error al cargar el archivo de Pokémons. Creando base de datos vacía.")
    
    while True:
        option = display_menu()
        
        if option == "1":
            # Mostrar todos los Pokémons
            pokemons = manager.list_all_pokemons()
            if not pokemons:
                print("No hay Pokémons registrados.")
            else:
                print("\n--- LISTA DE POKÉMONS ---")
                for i, pokemon in enumerate(pokemons, 1):
                    print(f"{i}. {pokemon}")
        
        elif option == "2":
            # Agregar nuevo Pokémon
            print("\n--- AGREGAR NUEVO POKÉMON ---")
            name = input("Nombre: ")
            if manager.get_pokemon(name):
                print(f"El Pokémon {name} ya existe!")
                continue
                
            pokemon_type = input("Tipo: ")
            
            try:
                hp = int(input("HP: "))
                attack = int(input("Ataque: "))
                defense = int(input("Defensa: "))
                sp_attack = int(input("Ataque Especial: "))
                sp_defense = int(input("Defensa Especial: "))
                speed = int(input("Velocidad: "))
            except ValueError:
                print("Error: Las estadísticas deben ser valores numéricos.")
                continue
            
            pokemon = Pokemon(name, pokemon_type, hp, attack, defense, sp_attack, sp_defense, speed)
            manager.add_pokemon(pokemon)
            print(f"Pokémon {name} agregado exitosamente!")
        
        elif option == "3":
            # Modificar Pokémon existente
            print("\n--- MODIFICAR POKÉMON ---")
            name = input("Nombre del Pokémon a modificar: ")
            
            pokemon = manager.get_pokemon(name)
            if not pokemon:
                print(f"No se encontró ningún Pokémon con el nombre {name}.")
                continue
            
            print(f"Modificando a {pokemon}")
            print("Deje en blanco para mantener el valor actual")
            
            new_type = input(f"Tipo [{pokemon.type}]: ")
            new_hp = input(f"HP [{pokemon.hp}]: ")
            new_attack = input(f"Ataque [{pokemon.attack}]: ")
            new_defense = input(f"Defensa [{pokemon.defense}]: ")
            new_sp_attack = input(f"Ataque Especial [{pokemon.sp_attack}]: ")
            new_sp_defense = input(f"Defensa Especial [{pokemon.sp_defense}]: ")
            new_speed = input(f"Velocidad [{pokemon.speed}]: ")
            
            # Crear diccionario con los valores a actualizar
            updates = {}
            if new_type:
                updates['type'] = new_type
            if new_hp:
                updates['hp'] = int(new_hp)
            if new_attack:
                updates['attack'] = int(new_attack)
            if new_defense:
                updates['defense'] = int(new_defense)
            if new_sp_attack:
                updates['sp_attack'] = int(new_sp_attack)
            if new_sp_defense:
                updates['sp_defense'] = int(new_sp_defense)
            if new_speed:
                updates['speed'] = int(new_speed)
            
            if updates:
                manager.update_pokemon(name, **updates)
                print(f"Pokémon {name} actualizado exitosamente!")
            else:
                print("No se realizaron cambios.")
        
        elif option == "4":
            # Eliminar Pokémon
            print("\n--- ELIMINAR POKÉMON ---")
            name = input("Nombre del Pokémon a eliminar: ")
            
            if manager.delete_pokemon(name):
                print(f"Pokémon {name} eliminado exitosamente!")
            else:
                print(f"No se encontró ningún Pokémon con el nombre {name}.")
        
        elif option == "5":
            # Iniciar batalla
            print("\n--- INICIAR BATALLA ---")
            pokemons = manager.list_all_pokemons()
            
            if len(pokemons) < 2:
                print("Se necesitan al menos 2 Pokémons para iniciar una batalla.")
                continue
            
            print("Seleccione el primer Pokémon:")
            for i, pokemon in enumerate(pokemons, 1):
                print(f"{i}. {pokemon.name}")
            
            try:
                idx1 = int(input("Número: ")) - 1
                if idx1 < 0 or idx1 >= len(pokemons):
                    print("Selección inválida.")
                    continue
                
                pokemon1 = pokemons[idx1]
                
                print("\nSeleccione el segundo Pokémon:")
                for i, pokemon in enumerate(pokemons, 1):
                    if i - 1 != idx1:  # No mostrar el primero seleccionado
                        print(f"{i}. {pokemon.name}")
                
                idx2 = int(input("Número: ")) - 1
                if idx2 < 0 or idx2 >= len(pokemons) or idx1 == idx2:
                    print("Selección inválida.")
                    continue
                
                pokemon2 = pokemons[idx2]
                
                # Iniciar batalla
                battle = BattleSystem(pokemon1, pokemon2)
                battle.start_battle()
                
            except ValueError:
                print("Error: Debe ingresar un número.")
        
        elif option == "0":
            print("¡Gracias por jugar!")
            break
        
        else:
            print("Opción inválida. Intente nuevamente.")

def display_menu():
    print("\n===== BATALLA POKÉMON =====")
    print("1. Mostrar todos los Pokémons")
    print("2. Agregar nuevo Pokémon")
    print("3. Modificar Pokémon existente")
    print("4. Eliminar Pokémon")
    print("5. Iniciar batalla")
    print("0. Salir")
    return input("Seleccione una opción: ")

# Punto de entrada del programa
if __name__ == "__main__":
    main()