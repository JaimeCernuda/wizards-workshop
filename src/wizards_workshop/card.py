from ursina import *
import time


class Card(Entity):
    def __init__(self, position=(0, 0, 0), card_type="generic", title="Card", 
                 lifetime=None, is_resource=False, **kwargs):
        super().__init__(
            model="quad",
            scale=(1.5, 2, 1),
            position=position,
            collider="box",
            **kwargs
        )
        
        self.card_type = card_type
        self.title = title
        self.is_held = False
        self.original_y = position[1]
        self.lifetime = lifetime
        self.is_resource = is_resource
        self.creation_time = time.time()
        self.is_decaying = False
        
        self.setup_appearance()
        
    def setup_appearance(self):
        card_configs = {
            "ingredient": {"color": color.light_gray, "border": color.dark_gray},
            "knowledge": {"color": color.azure, "border": color.blue},
            "tool": {"color": color.brown, "border": color.dark_gray},
            "mana": {"color": color.cyan, "border": color.blue},
            "spell": {"color": color.violet, "border": color.magenta},
            "essence": {"color": color.orange, "border": color.red},
            "potion": {"color": color.lime, "border": color.green},
            "crystal": {"color": color.magenta, "border": color.violet},
            "herb": {"color": color.green, "border": color.dark_green},
            "generic": {"color": color.white, "border": color.gray}
        }
        
        config = card_configs.get(self.card_type, card_configs["generic"])
        self.color = config["color"]
        
        # Add border
        self.border = Entity(
            parent=self,
            model="wireframe_quad",
            scale=(1.05, 1.05, 1),
            color=config["border"],
            position=(0, 0, -0.005)
        )
        
        self.title_text = Text(
            text=self.title,
            parent=self,
            origin=(0, 0),
            scale=7 if len(self.title) > 12 else 8,
            color=color.black,
            position=(0, 0.3, -0.01)
        )
        
        self.type_text = Text(
            text=self.card_type.capitalize(),
            parent=self,
            origin=(0, 0),
            scale=5,
            color=color.dark_gray,
            position=(0, -0.3, -0.01)
        )
        
        # Add symbol for resource cards
        if self.is_resource:
            self.resource_symbol = Entity(
                parent=self,
                model="sphere",
                scale=0.2,
                color=self.color * 1.5,
                position=(0.5, 0.7, -0.02)
            )
            
        # Setup lifetime indicator if temporary
        if self.lifetime:
            self.lifetime_bar = Entity(
                parent=self,
                model="cube",
                scale=(1.4, 0.1, 1),
                color=color.red,
                position=(0, -0.9, -0.01)
            )
        
    def pickup(self):
        self.is_held = True
        self.y = self.original_y + 0.5
        self.rotation_x = 0
        
    def drop(self):
        self.is_held = False
        self.y = self.original_y
        
    def drag_to(self, position):
        if self.is_held and position:
            self.position = Vec3(position.x, self.y, position.z)
            
    def update(self):
        # Update lifetime
        if self.lifetime and not self.is_decaying:
            elapsed = time.time() - self.creation_time
            remaining = max(0, 1 - (elapsed / self.lifetime))
            
            if hasattr(self, 'lifetime_bar'):
                self.lifetime_bar.scale_x = 1.4 * remaining
                
            if remaining <= 0:
                self.start_decay()
                
        # Animate resource symbol
        if hasattr(self, 'resource_symbol'):
            self.resource_symbol.rotation_y += 50 * time.dt
            
    def start_decay(self):
        self.is_decaying = True
        self.animate_color(color.dark_gray, duration=0.5)
        self.animate_scale(0, duration=0.5, curve=curve.in_expo)
        destroy(self, delay=0.5)
        
    def spawn_animation(self):
        original_scale = self.scale
        self.scale = 0
        self.animate_scale(original_scale, duration=0.3, curve=curve.out_back)