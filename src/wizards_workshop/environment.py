from ursina import *
import time
import math


class Environment(Entity):
    def __init__(self):
        super().__init__()
        self.current_time = 0  # 0-24 hours
        self.time_speed = 1.0  # Speed multiplier for time
        self.day_length = 120  # 2 minutes = 1 day
        
        self.setup_sky()
        self.setup_lighting()
        self.setup_ground()
        
    def setup_sky(self):
        # Create sky dome
        self.sky = Entity(
            model="sphere",
            scale=100,
            double_sided=True,
            position=(0, 0, 0)
        )
        
        # Sky gradient colors for different times
        self.sky_colors = {
            "dawn": color.rgb(255, 200, 150),      # Orange dawn
            "day": color.rgb(135, 206, 235),       # Sky blue
            "dusk": color.rgb(255, 140, 100),      # Orange sunset
            "night": color.rgb(25, 25, 112)        # Midnight blue
        }
        
    def setup_lighting(self):
        # Main directional light (sun)
        self.sun = DirectionalLight(
            position=(10, 10, 10),
            rotation=(45, 45, 0)
        )
        
        # Ambient lighting
        self.ambient = AmbientLight(color=color.white, intensity=0.3)
        
    def setup_ground(self):
        # Create grass texture
        self.grass_plane = Entity(
            model="plane",
            scale=(50, 1, 50),
            position=(0, -0.05, 0),
            color=color.rgb(34, 139, 34)  # Forest green
        )
        
        # Add grass pattern
        for i in range(-20, 21, 4):
            for j in range(-20, 21, 4):
                grass_patch = Entity(
                    model="cube",
                    scale=(0.1, 0.2, 0.1),
                    position=(i + random.uniform(-1, 1), 0, j + random.uniform(-1, 1)),
                    color=color.rgb(random.randint(30, 60), random.randint(120, 160), random.randint(30, 60)),
                    parent=self.grass_plane
                )
                
    def update_time_cycle(self):
        # Update time (0-24 hours)
        self.current_time += time.dt * self.time_speed * (24 / self.day_length)
        if self.current_time >= 24:
            self.current_time -= 24
            
        # Update sky color based on time
        hour = self.current_time
        
        if 6 <= hour < 8:  # Dawn
            progress = (hour - 6) / 2
            self.sky.color = lerp(self.sky_colors["night"], self.sky_colors["dawn"], progress)
        elif 8 <= hour < 18:  # Day
            progress = (hour - 8) / 10
            self.sky.color = lerp(self.sky_colors["dawn"], self.sky_colors["day"], min(progress * 2, 1))
        elif 18 <= hour < 20:  # Dusk
            progress = (hour - 18) / 2
            self.sky.color = lerp(self.sky_colors["day"], self.sky_colors["dusk"], progress)
        else:  # Night
            if hour >= 20:
                progress = (hour - 20) / 4
            else:  # Early morning (0-6)
                progress = (hour + 4) / 4
            self.sky.color = lerp(self.sky_colors["dusk"], self.sky_colors["night"], min(progress, 1))
            
        # Update lighting intensity
        if 6 <= hour <= 18:  # Daytime
            intensity = 0.8 + 0.2 * math.sin((hour - 6) * math.pi / 12)
        else:  # Nighttime
            intensity = 0.2 + 0.1 * math.sin(hour * math.pi / 12)
            
        if hasattr(self.sun, 'intensity'):
            self.sun.intensity = intensity
            
        # Update ambient light
        self.ambient.intensity = 0.2 + intensity * 0.3
        
        # Update sun position
        sun_angle = (hour - 6) * 15 - 90  # Sun moves across sky
        sun_height = max(0, math.sin(math.radians(sun_angle + 90)) * 20)
        
        self.sun.position = (
            math.cos(math.radians(sun_angle)) * 30,
            sun_height,
            math.sin(math.radians(sun_angle)) * 30
        )
        
    def get_time_string(self):
        hour = int(self.current_time)
        minute = int((self.current_time - hour) * 60)
        period = "AM" if hour < 12 else "PM"
        display_hour = hour if hour <= 12 else hour - 12
        if display_hour == 0:
            display_hour = 12
        return f"{display_hour:02d}:{minute:02d} {period}"
        
    def get_day_phase(self):
        hour = self.current_time
        if 6 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 18:
            return "Afternoon"
        elif 18 <= hour < 22:
            return "Evening"
        else:
            return "Night"