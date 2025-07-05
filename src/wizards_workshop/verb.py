from ursina import *
import time
from .recipes import RecipeBook


class Verb3D(Entity):
    def __init__(self, position=(0, 0, 0), name="verb", game_manager=None, **kwargs):
        super().__init__(
            position=position,
            **kwargs
        )
        
        self.verb_name = name
        self.game_manager = game_manager
        self.active_cards = []
        self.is_processing = False
        self.process_start_time = None
        self.process_duration = 3.0
        self.current_recipe = None
        self.recipe_book = RecipeBook()
        
        self.setup_appearance()
        self.setup_interaction_zone()
        
    def setup_appearance(self):
        self.name_text = Text(
            text=self.verb_name.upper(),
            parent=self,
            origin=(0, 0),
            scale=10,
            color=color.white,
            position=(0, self.scale_y + 1, 0),
            billboard=True
        )
        
    def setup_interaction_zone(self):
        self.interaction_zone = Entity(
            parent=self,
            model="cube",
            color=color.green,
            scale=(self.scale_x * 1.2, 0.1, self.scale_z * 1.2),
            position=(0, self.scale_y + 0.1, 0),
            visible=False,
            collider="box"
        )
        
    def is_card_over(self, card):
        if not card:
            return False
            
        card_pos = card.world_position
        zone_pos = self.interaction_zone.world_position
        zone_scale = self.interaction_zone.world_scale
        
        return (abs(card_pos.x - zone_pos.x) < zone_scale.x / 2 and
                abs(card_pos.z - zone_pos.z) < zone_scale.z / 2)
        
    def accept_card(self, card):
        if card not in self.active_cards:
            self.active_cards.append(card)
            
            # Position cards in a circle
            angle = (len(self.active_cards) - 1) * (360 / max(len(self.active_cards), 1))
            offset_x = math.cos(math.radians(angle)) * 0.8
            offset_z = math.sin(math.radians(angle)) * 0.8
            card.position = self.position + Vec3(offset_x, self.scale_y + 0.6, offset_z)
            
            # Check for valid recipe
            self.check_recipe()
                
    def check_recipe(self):
        if self.is_processing:
            return
            
        card_titles = [card.title for card in self.active_cards]
        recipe = self.recipe_book.find_recipe(self.verb_name, card_titles)
        
        if recipe:
            self.current_recipe = recipe
            self.start_processing(recipe.time)
        else:
            # Show invalid combination feedback
            if len(self.active_cards) >= 2:
                self.interaction_zone.visible = True
                self.interaction_zone.color = color.red
                self.interaction_zone.animate_scale(
                    self.interaction_zone.scale * 1.1,
                    duration=0.2,
                    curve=curve.out_expo
                )
                invoke(lambda: setattr(self.interaction_zone, 'visible', False), delay=0.5)
            
    def start_processing(self, duration):
        if not self.active_cards:
            return
            
        self.is_processing = True
        self.process_duration = duration
        self.process_start_time = time.time()
        self.interaction_zone.visible = True
        self.interaction_zone.color = color.lime
        
        # Add processing particles
        self.create_processing_particles()
        
        def check_process():
            if self.is_processing:
                progress = (time.time() - self.process_start_time) / self.process_duration
                if progress >= 1.0:
                    self.complete_processing()
                else:
                    # Update visual progress
                    self.interaction_zone.color = color.lime * (1 - progress) + color.yellow * progress
                    invoke(check_process, delay=0.1)
                    
        invoke(check_process, delay=0.1)
        
    def complete_processing(self):
        self.is_processing = False
        self.interaction_zone.visible = False
        
        if self.current_recipe and self.game_manager:
            # Create success effect
            success_flash = Entity(
                model="sphere",
                scale=3,
                color=color.yellow,
                position=self.position + Vec3(0, self.scale_y, 0),
                alpha=0.7
            )
            success_flash.animate_scale(0, duration=0.5, curve=curve.out_expo)
            destroy(success_flash, delay=0.5)
            
            # Remove input cards
            for card in self.active_cards:
                card.animate_scale(0, duration=0.3, curve=curve.in_expo)
                destroy(card, delay=0.3)
                
            # Create output card
            output_pos = self.position + Vec3(0, 0.1, -3)
            invoke(lambda: self.game_manager.create_card(
                position=output_pos,
                card_type=self.determine_card_type(self.current_recipe.output),
                title=self.current_recipe.output,
                animate_spawn=True
            ), delay=0.4)
            
            print(f"Created {self.current_recipe.output} from {self.current_recipe.inputs}")
        else:
            # Recipe failed - return cards
            for i, card in enumerate(self.active_cards):
                card.position = self.position + Vec3(i * 1.5 - len(self.active_cards) * 0.75, 0.1, -3)
            
        self.active_cards.clear()
        self.current_recipe = None
        
    def determine_card_type(self, title):
        type_mappings = {
            "Mana": "mana",
            "Iron Ore": "ingredient",
            "Iron Ingot": "ingredient", 
            "Iron Blade": "tool",
            "Simple Wand": "tool",
            "Basic Forging": "knowledge",
            "Elemental Theory": "knowledge",
            "Spell: Ignite": "spell",
            "Flame Essence": "essence",
            "Minor Potion": "potion",
            "Potion of Fire Resistance": "potion",
            "Charged Crystal": "crystal",
            "Crystal Shard": "crystal",
            "Herb": "herb"
        }
        return type_mappings.get(title, "generic")
        
    def create_processing_particles(self):
        for i in range(5):
            particle = Entity(
                model="sphere",
                scale=0.1,
                color=self.color * 1.5,
                position=self.position + Vec3(0, self.scale_y, 0)
            )
            direction = Vec3(random.uniform(-1, 1), random.uniform(0.5, 2), random.uniform(-1, 1))
            particle.animate_position(
                particle.position + direction,
                duration=self.process_duration,
                curve=curve.linear
            )
            particle.animate_scale(0, duration=self.process_duration)
            destroy(particle, delay=self.process_duration)