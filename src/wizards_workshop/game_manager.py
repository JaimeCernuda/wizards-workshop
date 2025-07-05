from ursina import *
from .card import Card
from .verb import Verb3D
from .playmat import Playmat
from .card_generator import CardGenerator
from .recipes import RecipeBook
from .recipe_display import RecipeDisplay
from .environment import Environment


class GameManager(Entity):
    def __init__(self):
        super().__init__()
        self.cards = []
        self.verbs = []
        self.generators = []
        self.playmat = None
        self.held_card = None
        self.recipe_book = RecipeBook()
        self.wizard_level = 1
        self.mana_count = 0
        self.environment = None
        self.time_ui = None
        
    def setup(self):
        window.borderless = False
        window.title = "Wizard's Workshop"
        window.color = color.rgb(25, 25, 50)  # Dark blue night sky
        
        # Setup environment first
        self.environment = Environment()
        
        camera.orthographic = True
        camera.fov = 25
        camera.position = (0, 15, -12)
        camera.rotation_x = 50
        
        self.playmat = Playmat()
        
        self.create_initial_verbs()
        self.create_initial_cards()
        self.create_generators()
        
        self.setup_controls()
        self.setup_ui()
        
        # Create recipe display
        self.recipe_display = RecipeDisplay(self.recipe_book)
        
        # Setup time UI
        self.setup_time_ui()
        
    def create_initial_verbs(self):
        # Forge - for crafting tools and items
        forge = Verb3D(
            position=(5, 0, 2),
            name="forge",
            model="cube",
            color=color.orange,
            scale=(2, 1, 2),
            game_manager=self
        )
        self.verbs.append(forge)
        
        # Study table - for learning knowledge
        study_table = Verb3D(
            position=(-5, 0, 2),
            name="study",
            model="cube", 
            color=color.brown,
            scale=(2.5, 0.5, 1.5),
            game_manager=self
        )
        self.verbs.append(study_table)
        
        # Ritual circle - for advanced magic
        ritual = Verb3D(
            position=(0, 0, 5),
            name="ritual",
            model="cube",
            color=color.violet,
            scale=(3, 0.2, 3),
            game_manager=self
        )
        self.verbs.append(ritual)
        
        # Alchemy station - for potions
        alchemy = Verb3D(
            position=(0, 0, -5),
            name="alchemy",
            model="sphere",
            color=color.green,
            scale=(1.5, 1.5, 1.5),
            game_manager=self
        )
        self.verbs.append(alchemy)
        
    def create_initial_cards(self):
        starter_cards = [
            # Starting resources
            Card(position=(-4, 0.1, -2), card_type="ingredient", title="Iron Ore"),
            Card(position=(-2, 0.1, -2), card_type="ingredient", title="Coal"),
            Card(position=(0, 0.1, -2), card_type="ingredient", title="Wood"),
            
            # Starting knowledge
            Card(position=(2, 0.1, -2), card_type="knowledge", title="Mysterious Tome"),
            
            # Some initial mana
            Card(position=(4, 0.1, -2), card_type="mana", title="Mana", is_resource=True, lifetime=30),
            Card(position=(5, 0.1, -2), card_type="mana", title="Mana", is_resource=True, lifetime=30),
        ]
        self.cards.extend(starter_cards)
        
    def create_generators(self):
        # Mana Spring - generates mana every 5 seconds
        mana_spring = CardGenerator(
            position=(-8, 0.5, 0),
            card_type="mana",
            interval=5.0,
            color=color.cyan
        )
        mana_spring.game_manager = self
        self.generators.append(mana_spring)
        
        # Herb Garden - generates herbs every 10 seconds
        herb_garden = CardGenerator(
            position=(8, 0.5, 0),
            card_type="herb",
            interval=10.0,
            color=color.green
        )
        herb_garden.game_manager = self
        self.generators.append(herb_garden)
        
        # Crystal Formation - generates crystals rarely
        crystal_formation = CardGenerator(
            position=(0, 0.5, 8),
            card_type="crystal",
            interval=20.0,
            color=color.violet
        )
        crystal_formation.game_manager = self
        self.generators.append(crystal_formation)
        
    def setup_controls(self):
        def update():
            if mouse.left:
                self.handle_mouse_click()
            elif self.held_card:
                self.held_card.drag_to(mouse.world_point)
                
            # Update UI and environment
            self.update_ui()
            
            # Update environment
            if self.environment:
                self.environment.update_time_cycle()
                
        Entity(update=update)
        
        # Keyboard controls
        def input(key):
            if key == 'r':
                self.recipe_display.toggle_visibility()
            elif key == 'escape':
                if self.held_card:
                    self.held_card.drop()
                    self.held_card = None
                    
        self.input = input
        
    def handle_mouse_click(self):
        if mouse.hovered_entity:
            if isinstance(mouse.hovered_entity, Card):
                if not self.held_card:
                    self.held_card = mouse.hovered_entity
                    self.held_card.pickup()
            elif self.held_card:
                self.drop_card()
        elif self.held_card:
            self.drop_card()
            
    def drop_card(self):
        if not self.held_card:
            return
            
        for verb in self.verbs:
            if verb.is_card_over(self.held_card):
                verb.accept_card(self.held_card)
                self.held_card.drop()
                self.held_card = None
                return
                
        self.held_card.drop()
        self.held_card = None
        
    def create_card(self, position, card_type, title, animate_spawn=False, **kwargs):
        card = Card(
            position=position,
            card_type=card_type,
            title=title,
            **kwargs
        )
        
        if animate_spawn:
            card.spawn_animation()
            
        self.cards.append(card)
        return card
        
    def is_position_occupied(self, position, threshold=1.5):
        for card in self.cards:
            if distance(card.position, position) < threshold:
                return True
        return False
        
    def setup_ui(self):
        self.level_text = Text(
            text=f"Wizard Level: {self.wizard_level}",
            position=(-0.85, 0.45),
            scale=2,
            color=color.white
        )
        
        self.mana_text = Text(
            text=f"Mana: {self.mana_count}",
            position=(-0.85, 0.40),
            scale=2,
            color=color.cyan
        )
        
        # Recipe hint
        self.hint_text = Text(
            text="Experiment with combinations!\nDrag cards onto the glowing stations.\nPress 'R' for recipe book.",
            position=(0, -0.45),
            scale=1.5,
            color=color.light_gray,
            origin=(0, 0)
        )
        
    def setup_time_ui(self):
        # Time display background
        self.time_panel = Entity(
            parent=camera.ui,
            model="quad",
            color=color.rgb(20, 20, 40),
            scale=(0.25, 0.08, 1),
            position=(0, 0.42, 0),
            alpha=0.8
        )
        
        # Clock display
        self.clock_text = Text(
            text="12:00 AM",
            parent=self.time_panel,
            position=(0, 0.01, -0.01),
            scale=2.5,
            origin=(0, 0),
            color=color.white
        )
        
        # Day phase display
        self.phase_text = Text(
            text="Night",
            parent=self.time_panel,
            position=(0, -0.02, -0.01),
            scale=1.8,
            origin=(0, 0),
            color=color.cyan
        )
        
        # Sun/Moon icon
        self.time_icon = Entity(
            parent=self.time_panel,
            model="sphere",
            scale=0.02,
            position=(-0.08, 0, -0.01),
            color=color.yellow
        )
        
    def update_ui(self):
        self.mana_count = sum(1 for card in self.cards if card.title == "Mana")
        self.mana_text.text = f"Mana: {self.mana_count}"
        
        # Update time display
        if self.environment and hasattr(self, 'clock_text'):
            self.clock_text.text = self.environment.get_time_string()
            self.phase_text.text = self.environment.get_day_phase()
            
            # Update icon based on time
            phase = self.environment.get_day_phase()
            if phase in ["Morning", "Afternoon"]:
                self.time_icon.color = color.yellow  # Sun
                self.time_icon.scale = 0.025
            else:
                self.time_icon.color = color.light_gray  # Moon
                self.time_icon.scale = 0.02