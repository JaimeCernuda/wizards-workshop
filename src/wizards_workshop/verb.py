from ursina import *
import time
import math
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
        # Enhanced station appearance based on type
        self.setup_station_details()
        
        self.name_text = Text(
            text=self.verb_name.upper(),
            parent=self,
            origin=(0, 0),
            scale=10,
            color=color.white,
            position=(0, self.scale_y + 1.5, 0),
            billboard=True
        )
        
    def setup_station_details(self):
        if self.verb_name == "forge":
            self.setup_forge_details()
        elif self.verb_name == "study":
            self.setup_study_details()
        elif self.verb_name == "ritual":
            self.setup_ritual_details()
        elif self.verb_name == "alchemy":
            self.setup_alchemy_details()
            
    def setup_forge_details(self):
        # Add anvil on top
        self.anvil = Entity(
            parent=self,
            model="cube",
            scale=(0.8, 0.3, 0.4),
            position=(0, self.scale_y + 0.3, 0),
            color=color.dark_gray
        )
        
        # Add forge fire effect
        self.fire = Entity(
            parent=self,
            model="sphere",
            scale=(0.5, 0.8, 0.5),
            position=(0.5, self.scale_y + 0.8, 0),
            color=color.orange,
            alpha=0.7
        )
        
        # Add hammers
        for i, pos in enumerate([(-0.6, self.scale_y + 0.5, 0.3), (0.6, self.scale_y + 0.5, -0.3)]):
            hammer = Entity(
                parent=self,
                model="cube",
                scale=(0.1, 0.6, 0.1),
                position=pos,
                color=color.brown,
                rotation_z=45 if i == 0 else -45
            )
            
    def setup_study_details(self):
        # Add books
        book_positions = [
            (-0.6, self.scale_y + 0.3, 0.2),
            (0, self.scale_y + 0.3, -0.4),
            (0.5, self.scale_y + 0.3, 0.3)
        ]
        
        for i, pos in enumerate(book_positions):
            book = Entity(
                parent=self,
                model="cube",
                scale=(0.3, 0.1, 0.4),
                position=pos,
                color=color.rgb(random.randint(100, 200), random.randint(50, 150), random.randint(50, 100)),
                rotation_y=random.randint(0, 360)
            )
            
        # Add quill and ink
        self.quill = Entity(
            parent=self,
            model="cube",
            scale=(0.05, 0.4, 0.05),
            position=(0.3, self.scale_y + 0.4, -0.2),
            color=color.white,
            rotation_z=15
        )
        
    def setup_ritual_details(self):
        # Add candles around the circle
        for i in range(6):
            angle = i * 60
            x = math.cos(math.radians(angle)) * 1.2
            z = math.sin(math.radians(angle)) * 1.2
            
            candle = Entity(
                parent=self,
                model="cube",
                scale=(0.1, 0.6, 0.1),
                position=(x, self.scale_y + 0.4, z),
                color=color.yellow
            )
            
            # Candle flame
            flame = Entity(
                parent=candle,
                model="sphere",
                scale=(0.3, 0.5, 0.3),
                position=(0, 0.4, 0),
                color=color.orange,
                alpha=0.8
            )
            
        # Central ritual symbol
        self.symbol = Entity(
            parent=self,
            model="sphere",
            scale=(0.8, 0.05, 0.8),
            position=(0, self.scale_y + 0.15, 0),
            color=color.violet,
            alpha=0.6
        )
        
    def setup_alchemy_details(self):
        # Add bottles and flasks
        bottle_positions = [
            (0, self.scale_y + 0.8, 0),
            (-0.5, self.scale_y + 0.6, 0.3),
            (0.4, self.scale_y + 0.5, -0.2)
        ]
        
        colors = [color.green, color.blue, color.red]
        
        for i, pos in enumerate(bottle_positions):
            bottle = Entity(
                parent=self,
                model="sphere",
                scale=(0.2, 0.4, 0.2),
                position=pos,
                color=colors[i % len(colors)],
                alpha=0.8
            )
            
        # Add bubbling effect
        self.bubbles = Entity(
            parent=self,
            model="sphere",
            scale=(0.3, 0.3, 0.3),
            position=(0, self.scale_y + 1.2, 0),
            color=color.cyan,
            alpha=0.5
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
            
    def update(self):
        # Animate station effects
        if hasattr(self, 'fire'):
            # Animate forge fire
            self.fire.scale_y = 0.8 + 0.2 * math.sin(time.time() * 3)
            self.fire.rotation_y += 50 * time.dt
            
        if hasattr(self, 'symbol'):
            # Animate ritual symbol
            self.symbol.rotation_y += 30 * time.dt
            pulse = 1 + 0.1 * math.sin(time.time() * 2)
            self.symbol.alpha = 0.6 * pulse
            
        if hasattr(self, 'bubbles'):
            # Animate alchemy bubbles
            self.bubbles.y = self.scale_y + 1.2 + 0.3 * math.sin(time.time() * 2)
            self.bubbles.rotation_x += 20 * time.dt
        
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