import pygame
import random
import time
from plant import Plant, Seed

class Garden:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.plants = []
        self.soil_color = (139, 69, 19)  # Brown for soil
        self.soil_rect = pygame.Rect(0, height - 50, width, 50)
        self.last_action = None  # Keep track of the last action (water or sun)
        
        # Create soil texture
        self.soil_texture = pygame.Surface((width, 50))
        self.soil_texture.fill(self.soil_color)
        for _ in range(200):  # More soil details
            x = random.randint(0, width - 1)
            y = random.randint(0, 49)
            pygame.draw.circle(self.soil_texture, (101, 67, 33), (x, y), random.randint(1, 3))
        
        # Weather effects
        self.is_raining = False
        self.is_sunny = False
        self.effect_timer = 0
        self.effect_duration = 3  # seconds
        self.raindrops = []
        self.sun_rays = []
    
    def plant_seed(self, seed, x, y):
        """Plant a seed at the given position"""
        # Make sure the seed is planted in the soil
        if y > self.height - 60:
            plant_x = x
            plant_y = self.height - 50  # Top of soil
            self.plants.append(Plant(seed.plant_type, plant_x, plant_y))
    
    def water_plants(self):
        """Water all plants in the garden and start rain effect"""
        if self.last_action != "water":
            for plant in self.plants:
                plant.water()
            self.last_action = "water"
            
            # Start rain effect
            self.is_raining = True
            self.is_sunny = False
            self.effect_timer = time.time()
            
            # Create raindrops
            self.raindrops = []
            for _ in range(50):
                x = random.randint(0, self.width)
                y = random.randint(-50, 0)
                speed = random.randint(5, 15)
                self.raindrops.append({"x": x, "y": y, "speed": speed})
    
    def provide_sunlight(self):
        """Provide sunlight to all plants and start sun effect"""
        if self.last_action != "sun":
            for plant in self.plants:
                plant.provide_sunlight()
            self.last_action = "sun"
            
            # Start sun effect
            self.is_sunny = True
            self.is_raining = False
            self.effect_timer = time.time()
            
            # Create sun rays
            self.sun_rays = []
            sun_x = self.width - 100  # Position near the sun button
            sun_y = 100
            for i in range(8):
                angle = i * 45
                length = random.randint(50, 100)
                self.sun_rays.append({"angle": angle, "length": length, "sun_x": sun_x, "sun_y": sun_y})
    
    def check_seed_click(self, pos):
        """Check if a seed was clicked and return it if so"""
        # Increased detection radius for easier clicking
        click_tolerance = 20  # Pixels around the seed that will count as a click
        
        for plant in self.plants:
            # Check both alive and dead plants' seeds
            for seed in plant.seeds:
                # Calculate distance between click and seed center
                dx = seed.x - pos[0]
                dy = seed.y - pos[1]
                distance = (dx * dx + dy * dy) ** 0.5  # Pythagorean distance
                
                # If click is within tolerance radius, count as a click
                if distance <= click_tolerance:
                    plant.seeds.remove(seed)
                    return seed
        return None
    
    def cut_flowers(self, x, y):
        """Cut down all fully grown flowers near the given position"""
        cut_radius = 100  # Increased distance for easier cutting
        
        for plant in self.plants[:]:  # Use a copy to safely modify the list
            # Only cut mature plants (stage 5 or 6)
            if plant.growth_stage >= 5 and plant.alive:
                # Calculate horizontal distance to the scissors (ignoring vertical)
                dx = abs(plant.x - x)
                
                # If plant is within cutting radius horizontally (ignore vertical position)
                if dx <= cut_radius:
                    # Don't collect seeds automatically - let them drop to the ground
                    # Trigger plant death - seeds will fall naturally
                    plant.die()
        
        # No seeds returned - they'll stay on the ground for manual collection
        return []
    
    def update(self):
        """Update all plants in the garden and weather effects"""
        # Update plants
        for plant in self.plants[:]:  # Use a copy of the list to safely modify the original
            plant.update()
            
            # If plant is dead and has no seeds, remove it
            if not plant.alive and not plant.seeds:
                self.plants.remove(plant)
        
        # Update weather effects
        current_time = time.time()
        if (self.is_raining or self.is_sunny) and current_time - self.effect_timer > self.effect_duration:
            self.is_raining = False
            self.is_sunny = False
        
        # Update raindrops
        if self.is_raining:
            for drop in self.raindrops:
                drop["y"] += drop["speed"]
                # Reset raindrop if it goes offscreen
                if drop["y"] > self.height:
                    drop["y"] = random.randint(-50, 0)
                    drop["x"] = random.randint(0, self.width)
    
    def draw(self, surface, mouse_pos=None):
        """Draw the garden, plants, and weather effects"""
        # Draw sky (already done in main)
        
        # Draw sun effect
        if self.is_sunny:
            # Draw sun
            sun_x = self.width - 100
            sun_y = 100
            pygame.draw.circle(surface, (255, 255, 0), (sun_x, sun_y), 40)
            pygame.draw.circle(surface, (255, 200, 0), (sun_x, sun_y), 30)
            
            # Draw sun rays
            for ray in self.sun_rays:
                start_x = ray["sun_x"]
                start_y = ray["sun_y"]
                angle = ray["angle"]
                length = ray["length"]
                end_x = start_x + int(length * pygame.math.Vector2(1, 0).rotate(angle).x)
                end_y = start_y + int(length * pygame.math.Vector2(1, 0).rotate(angle).y)
                pygame.draw.line(surface, (255, 255, 0), (start_x, start_y), (end_x, end_y), 3)
        
        # Draw soil
        surface.blit(self.soil_texture, self.soil_rect)
        
        # Draw plants
        for plant in self.plants:
            plant.draw(surface)
        
        # Draw rain effect
        if self.is_raining:
            for drop in self.raindrops:
                pygame.draw.line(
                    surface, 
                    (100, 150, 255), 
                    (drop["x"], drop["y"]), 
                    (drop["x"], drop["y"] + 10), 
                    2
                )