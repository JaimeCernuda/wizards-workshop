from ursina import *
import math
import time


class Playmat(Entity):
    def __init__(self):
        super().__init__()
        self.create_magical_workshop_floor()
        
    def create_magical_workshop_floor(self):
        # Main stone workshop floor
        self.main_floor = Entity(
            model="cube",
            scale=(25, 0.1, 25),
            position=(0, 0, 0),
            color=color.rgb(105, 105, 105)  # Dim gray stone
        )
        
        # Add stone tile pattern
        self.create_stone_tiles()
        
        # Magical circle in center
        self.create_magical_circle()
        
        # Workshop boundaries with decorative stones
        self.create_workshop_boundary()
        
    def create_stone_tiles(self):
        # Create individual stone tiles
        tile_size = 2
        for x in range(-10, 11, tile_size):
            for z in range(-10, 11, tile_size):
                if abs(x) <= 10 and abs(z) <= 10:
                    tile = Entity(
                        model="cube",
                        scale=(tile_size * 0.9, 0.02, tile_size * 0.9),
                        position=(x, 0.06, z),
                        color=color.rgb(
                            random.randint(85, 125),
                            random.randint(85, 125), 
                            random.randint(85, 125)
                        ),
                        parent=self.main_floor
                    )
                    
    def create_magical_circle(self):
        # Central runic circle
        self.magic_circle = Entity(
            model="sphere",
            scale=(3, 0.05, 3),
            position=(0, 0.08, 0),
            color=color.rgb(138, 43, 226),  # Blue violet
            alpha=0.7,
            parent=self.main_floor
        )
        
        # Inner circle detail
        self.inner_circle = Entity(
            model="sphere",
            scale=(1.5, 0.06, 1.5),
            position=(0, 0.09, 0),
            color=color.cyan,
            alpha=0.5,
            parent=self.main_floor
        )
        
        # Runic symbols around circle
        for i in range(8):
            angle = i * 45
            x = math.cos(math.radians(angle)) * 2.5
            z = math.sin(math.radians(angle)) * 2.5
            
            rune = Entity(
                model="cube",
                scale=(0.2, 0.1, 0.2),
                position=(x, 0.1, z),
                color=color.gold,
                parent=self.main_floor
            )
            
    def create_workshop_boundary(self):
        # Decorative boundary stones
        boundary_positions = [
            (-12, 0, 0), (12, 0, 0),  # Left and right
            (0, 0, -12), (0, 0, 12),  # Front and back
            (-8, 0, -8), (8, 0, -8),  # Corners
            (-8, 0, 8), (8, 0, 8)
        ]
        
        for pos in boundary_positions:
            stone = Entity(
                model="sphere",
                scale=(0.8, 1.2, 0.8),
                position=pos,
                color=color.rgb(70, 70, 70),
                parent=self
            )
            
            # Add glowing crystal on top
            crystal = Entity(
                model="sphere",
                scale=(0.3, 0.6, 0.3),
                position=(pos[0], pos[1] + 1, pos[2]),
                color=color.rgb(random.randint(100, 255), random.randint(100, 255), 255),
                parent=self
            )
        
    def update(self):
        # Animate magical elements
        if hasattr(self, 'magic_circle'):
            self.magic_circle.rotation_y += 10 * time.dt
            
        if hasattr(self, 'inner_circle'):
            self.inner_circle.rotation_y -= 15 * time.dt
            
        # Animate boundary crystals
        for child in self.children:
            if hasattr(child, 'children'):
                for crystal in child.children:
                    if crystal.scale_y > 0.5:  # It's a crystal
                        crystal.rotation_y += 30 * time.dt
                        # Gentle pulsing
                        pulse = 1 + 0.1 * math.sin(time.time() * 2)
                        crystal.scale = (crystal.scale_x, crystal.scale_y * pulse, crystal.scale_z)