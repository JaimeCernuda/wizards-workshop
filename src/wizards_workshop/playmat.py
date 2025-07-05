from ursina import *


class Playmat(Entity):
    def __init__(self):
        super().__init__(
            model="cube",
            scale=(20, 0.1, 20),
            position=(0, 0, 0),
            color=color.dark_gray,
            texture="white_cube"
        )
        
        self.grid_lines = []
        self.create_grid()
        
    def create_grid(self):
        grid_size = 10
        grid_spacing = 2
        
        for i in range(-grid_size, grid_size + 1):
            line_x = Entity(
                model="cube",
                scale=(0.05, 0.02, grid_size * 2),
                position=(i * grid_spacing, 0.06, 0),
                color=color.gray,
                parent=self
            )
            self.grid_lines.append(line_x)
            
            line_z = Entity(
                model="cube", 
                scale=(grid_size * 2, 0.02, 0.05),
                position=(0, 0.06, i * grid_spacing),
                color=color.gray,
                parent=self
            )
            self.grid_lines.append(line_z)