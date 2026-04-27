import datetime

class Animal:
    def __init__(self, age, sex, species, color, weight, origin, season):
        self.species = species
        self.sex = sex
        self.color = color
        self.weight = weight
        self.origin = origin
        self.arrival_date = datetime.date.today().isoformat()

        # Unique Logic: Calculate attributes during initialization
        self.animal_id = self._generate_id()
        self.birth_date = self._calculate_birthday(age, season)
        self.name = "Unnamed"

    def _calculate_birthday(self, age, season):
        """Custom birth year calculation logic."""
        year = datetime.date.today().year - int(age)
        dates = {"spring": "03-21", "summer": "06-21", "fall": "09-21", "winter": "12-21"}
        return f"{year}-{dates.get(season.lower(), '01-01')}"

    def _generate_id(self):
        """Creates unique ID using species prefix and count tracker."""
        if not hasattr(Animal, 'registry'):
            Animal.registry = {}

        Animal.registry[self.species] = Animal.registry.get(self.species, 0) + 1
        return f"{self.species[:2].upper()}{Animal.registry[self.species]:02}"

    def to_report_string(self):
        """Formats the output exactly as requested in the instructions."""
        return (f"{self.animal_id}; {self.name}; birth date: {self.birth_date}; "
                f"{self.color}; {self.sex}; {self.weight}; from {self.origin}; "
                f"arrived {self.arrival_date}")

def load_names():
    """Custom parser for animalNames.txt."""
    name_map = {}
    try:
        with open('animalNames.txt', 'r') as f:
            for line in f:
                if ':' in line:
                    species, names = line.split(':')
                    name_map[species.strip().lower()] = [n.strip() for n in names.split(',')]
    except FileNotFoundError:
        print("Warning: animalNames.txt not found. Using generic names.")
    return name_map

def main():
    names_bank = load_names()
    habitats = {}

    try:
        with open('arrivingAnimals.txt', 'r') as f:
            for line in f:
                if not line.strip(): continue

                # Parsing logic specific to your example format
                data = [item.strip() for item in line.split(',')]
                # '4 year old female hyena' -> extract components
                bio_info = data[0].split()

                # Dynamic extraction: last word is species, second to last is sex, first is age
                new_animal = Animal(
                    age=bio_info[0],
                    sex=bio_info[3],
                    species=bio_info[4],
                    color=data[2],
                    weight=data[3],
                    origin=f"{data[4]}, {data[5]}",
                    season=data[1].replace("born in ", "")
                )

                # Assign name from the bank
                species_key = new_animal.species.lower()
                if species_key in names_bank and names_bank[species_key]:
                    new_animal.name = names_bank[species_key].pop(0)

                # Sort into habitats
                h_key = f"{new_animal.species.capitalize()} Habitat"
                habitats.setdefault(h_key, []).append(new_animal)

        # Write output
        with open('zooPopulation.txt', 'w') as out:
            for habitat, occupants in habitats.items():
                out.write(f"{habitat}:\n\n")
                for animal in occupants:
                    out.write(f"{animal.to_report_string()}\n")
                out.write("\n" + "="*30 + "\n\n")

        print("Report generated: zooPopulation.txt")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()