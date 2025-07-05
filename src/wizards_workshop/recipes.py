from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Recipe:
    verb: str
    inputs: List[str]
    output: str
    time: float = 3.0
    description: str = ""
    
    def matches(self, verb_name: str, card_titles: List[str]) -> bool:
        if verb_name != self.verb:
            return False
        return sorted(self.inputs) == sorted(card_titles)


class RecipeBook:
    def __init__(self):
        self.recipes = self._create_recipes()
        
    def _create_recipes(self) -> List[Recipe]:
        return [
            # Forge recipes
            Recipe(
                verb="forge",
                inputs=["Iron Ore", "Coal"],
                output="Iron Ingot",
                description="Smelt ore into usable metal"
            ),
            Recipe(
                verb="forge", 
                inputs=["Iron Ingot", "Basic Forging"],
                output="Iron Blade",
                description="Shape metal into a blade"
            ),
            Recipe(
                verb="forge",
                inputs=["Iron Blade", "Wood"],
                output="Simple Wand",
                description="Craft a basic magical focus"
            ),
            
            # Study recipes
            Recipe(
                verb="study",
                inputs=["Mysterious Tome"],
                output="Basic Forging",
                time=5.0,
                description="Learn the art of metalworking"
            ),
            Recipe(
                verb="study",
                inputs=["Crystal Shard", "Mana"],
                output="Elemental Theory",
                description="Understand magical energies"
            ),
            Recipe(
                verb="study",
                inputs=["Elemental Theory", "Simple Wand"],
                output="Spell: Ignite",
                description="Learn your first spell"
            ),
            
            # Ritual circle recipes
            Recipe(
                verb="ritual",
                inputs=["Mana", "Mana", "Crystal Shard"],
                output="Charged Crystal",
                time=6.0,
                description="Infuse crystal with power"
            ),
            Recipe(
                verb="ritual",
                inputs=["Spell: Ignite", "Charged Crystal"],
                output="Flame Essence",
                description="Extract elemental essence"
            ),
            
            # Alchemy recipes
            Recipe(
                verb="alchemy",
                inputs=["Herb", "Mana"],
                output="Minor Potion",
                description="Brew a simple potion"
            ),
            Recipe(
                verb="alchemy",
                inputs=["Minor Potion", "Flame Essence"],
                output="Potion of Fire Resistance",
                description="Create protective elixir"
            ),
        ]
        
    def find_recipe(self, verb_name: str, card_titles: List[str]) -> Optional[Recipe]:
        for recipe in self.recipes:
            if recipe.matches(verb_name, card_titles):
                return recipe
        return None
        
    def get_recipes_for_verb(self, verb_name: str) -> List[Recipe]:
        return [r for r in self.recipes if r.verb == verb_name]