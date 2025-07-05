from ursina import *
import time
import math


class CardGenerator(Entity):
    def __init__(self, position=(0, 0, 0), card_type="mana", interval=5.0, **kwargs):
        super().__init__(
            model="sphere",
            scale=1,
            position=position,
            collider="box",
            **kwargs
        )
        
        self.card_type = card_type
        self.interval = interval
        self.last_generation = time.time()
        self.game_manager = None
        self.is_active = True
        
        self.setup_appearance()
        self.setup_particles()
        
    def setup_appearance(self):
        generator_configs = {
            "mana": {
                "color": color.cyan,
                "title": "Mana Spring",
                "card_title": "Mana"
            },
            "herb": {
                "color": color.green,
                "title": "Herb Garden", 
                "card_title": "Herb"
            },
            "crystal": {
                "color": color.violet,
                "title": "Crystal Formation",
                "card_title": "Crystal Shard"
            }
        }
        
        config = generator_configs.get(self.card_type, {
            "color": color.white,
            "title": "Generator",
            "card_title": "Resource"
        })
        
        self.color = config["color"]
        self.generator_title = config["title"]
        self.card_title = config["card_title"]
        
        self.title_text = Text(
            text=self.generator_title,
            parent=self,
            origin=(0, 0),
            scale=8,
            color=color.white,
            position=(0, 1.5, 0),
            billboard=True
        )
        
        self.inner_sphere = Entity(
            parent=self,
            model="sphere",
            scale=0.6,
            color=self.color * 2
        )
        
    def setup_particles(self):
        self.particles = []
        for i in range(3):
            particle = Entity(
                parent=self,
                model="cube",
                scale=0.1,
                color=self.color * 1.5,
                position=(0, 0, 0)
            )
            self.particles.append(particle)
            
    def update(self):
        if not self.is_active or not self.game_manager:
            return
            
        # Animate
        self.inner_sphere.rotation_y += 50 * time.dt
        
        # Animate particles
        for i, particle in enumerate(self.particles):
            angle = time.time() * 2 + i * 120
            particle.x = math.cos(angle) * 0.8
            particle.z = math.sin(angle) * 0.8
            particle.y = math.sin(time.time() * 3 + i) * 0.3
            
        # Check if should generate
        current_time = time.time()
        if current_time - self.last_generation >= self.interval:
            self.generate_card()
            self.last_generation = current_time
            
    def generate_card(self):
        if not self.game_manager:
            return
            
        # Find empty spot near generator
        offset_positions = [
            Vec3(2, 0.1, 0),
            Vec3(-2, 0.1, 0),
            Vec3(0, 0.1, 2),
            Vec3(0, 0.1, -2),
            Vec3(1.5, 0.1, 1.5),
            Vec3(-1.5, 0.1, 1.5),
        ]
        
        spawn_pos = None
        for offset in offset_positions:
            test_pos = self.position + offset
            if not self.game_manager.is_position_occupied(test_pos):
                spawn_pos = test_pos
                break
                
        if spawn_pos:
            # Add lifetime for resource cards like mana
            kwargs = {"animate_spawn": True}
            if self.card_type == "mana":
                kwargs["lifetime"] = 30.0
                kwargs["is_resource"] = True
                
            self.game_manager.create_card(
                position=spawn_pos,
                card_type=self.card_type,
                title=self.card_title,
                **kwargs
            )
            
            # Visual feedback
            flash = Entity(
                model="sphere",
                scale=2,
                color=self.color,
                position=self.position,
                alpha=0.5
            )
            flash.animate_scale(0, duration=0.5, curve=curve.out_expo)
            destroy(flash, delay=0.5)