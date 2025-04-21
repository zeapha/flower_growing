import pygame
import random
import time

class Seed:
    def __init__(self, plant_type, x=0, y=0):
        self.plant_type = plant_type
        self.x = x
        self.y = y
        self.size = 12
        self.rect = pygame.Rect(x - self.size/2, y - self.size/2, self.size, self.size)
        
        # Set seed color and shape based on plant type
        if plant_type == "rose":
            self.color = (180, 50, 50)  # Reddish-brown
            self.highlight_color = (220, 100, 100)
            self.shape = "oval"
        elif plant_type == "sunflower":
            self.color = (50, 50, 30)  # Dark brown
            self.highlight_color = (80, 80, 60)
            self.shape = "teardrop"
        elif plant_type == "daisy":
            self.color = (200, 180, 140)  # Light tan
            self.highlight_color = (230, 210, 170)
            self.shape = "round"
        else:
            self.color = (150, 100, 50)  # Brown (default)
            self.highlight_color = (180, 130, 80)
            self.shape = "oval"
        
        # Add a random rotation to make seeds look more natural
        self.rotation = random.randint(0, 360)
    
    def draw_at_position(self, surface, x, y):
        """Draw the seed at a specific position"""
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x - self.size/2, y - self.size/2, self.size, self.size)
        
        if self.shape == "oval":
            # Draw oval-shaped seed
            seed_rect = pygame.Rect(x - self.size/2, y - self.size/4, self.size, self.size/2)
            pygame.draw.ellipse(surface, self.color, seed_rect)
            # Add seed details - line down middle
            seed_line_color = (max(0, self.color[0]-20), max(0, self.color[1]-20), max(0, self.color[2]-20))
            pygame.draw.line(surface, seed_line_color,
                           (x, y - self.size/4), (x, y + self.size/4), 1)
            # Add highlight
            pygame.draw.ellipse(surface, self.highlight_color, 
                             pygame.Rect(x - self.size/4, y - self.size/6, self.size/3, self.size/6))
            
        elif self.shape == "teardrop":
            # Draw teardrop-shaped sunflower seed
            # Main body
            pygame.draw.ellipse(surface, self.color, 
                             pygame.Rect(x - self.size/3, y - self.size/2, self.size/1.5, self.size))
            # Pointed end
            points = [
                (x, y + self.size/2),
                (x - self.size/4, y + self.size/3),
                (x + self.size/4, y + self.size/3)
            ]
            pygame.draw.polygon(surface, self.color, points)
            # Stripe
            pygame.draw.line(surface, self.highlight_color, 
                           (x, y - self.size/2), (x, y + self.size/2), 1)
            
        elif self.shape == "round":
            # Draw round seed with details
            pygame.draw.circle(surface, self.color, (x, y), self.size/2)
            # Add seed texture - little dots
            for _ in range(3):
                dot_x = x + random.randint(-int(self.size/3), int(self.size/3))
                dot_y = y + random.randint(-int(self.size/3), int(self.size/3))
                pygame.draw.circle(surface, self.highlight_color, (dot_x, dot_y), 1)
        
        else:
            # Fallback to simple seed shape
            pygame.draw.circle(surface, self.color, (x, y), self.size/2)
            pygame.draw.circle(surface, (0, 0, 0), (x, y), self.size/2, 1)  # Black outline

class Plant:
    def __init__(self, plant_type, x, y):
        self.plant_type = plant_type
        self.x = x
        self.y = y
        self.growth_stage = 0  # 0: seed, 1: small stalk, 2: stalk with few leaves, etc.
        self.growth_timer = time.time()
        self.water_level = 0
        self.sun_level = 0
        self.growth_speed = 10  # Seconds between natural growth
        self.seeds = []
        self.alive = True
        self.lifetime = random.randint(30, 60)  # Seconds plant will live after maturity
        self.maturity_time = 0  # When the plant reached maturity
        
        # Random variation to make plants look unique
        self.variation = random.uniform(0.9, 1.1)
        self.lean_direction = random.choice([-1, 1]) * random.uniform(0.8, 1.2)
        
        # Set plant colors based on type
        if plant_type == "rose":
            self.stem_color = (0, 100, 0)  # Dark green
            self.leaf_color = (0, 150, 0)  # Medium green
            self.flower_color = (255, 50, 50)  # Red
            self.flower_highlight = (255, 150, 150)  # Light red
            self.center_color = (150, 0, 0)  # Dark red
        elif plant_type == "sunflower":
            self.stem_color = (0, 120, 0)  # Green
            self.leaf_color = (50, 150, 50)  # Light green
            self.flower_color = (255, 200, 0)  # Golden yellow
            self.flower_highlight = (255, 255, 100)  # Light yellow
            self.center_color = (100, 50, 0)  # Brown
        elif plant_type == "daisy":
            self.stem_color = (0, 150, 0)  # Green
            self.leaf_color = (100, 200, 100)  # Light green
            self.flower_color = (255, 255, 255)  # White
            self.flower_highlight = (255, 255, 230)  # Cream
            self.center_color = (255, 255, 0)  # Yellow
        else:
            # Default colors
            self.stem_color = (0, 128, 0)  # Green
            self.leaf_color = (50, 150, 50)  # Light green
            self.flower_color = (255, 100, 100)  # Pink
            self.flower_highlight = (255, 200, 200)  # Light pink
            self.center_color = (255, 255, 0)  # Yellow
    
    def water(self):
        """Water the plant to help it grow"""
        self.water_level += 1
        self.check_growth_boost()
    
    def provide_sunlight(self):
        """Give the plant sunlight to help it grow"""
        self.sun_level += 1
        self.check_growth_boost()
    
    def check_growth_boost(self):
        """Check if the plant should get a growth boost from water and sun"""
        if self.water_level >= 1 and self.sun_level >= 1:
            self.grow()
            self.water_level = 0
            self.sun_level = 0
    
    def grow(self):
        """Advance the plant to the next growth stage"""
        if self.growth_stage < 6:  # Max stage is 6 (fully grown with seeds)
            self.growth_stage += 1
            
            # If reaching maturity (stage 6), create seeds
            if self.growth_stage == 6:
                self.create_seeds()
    
    def create_seeds(self):
        """Create seeds for a fully grown plant"""
        seed_count = random.randint(2, 4)
        for i in range(seed_count):
            seed_x = self.x + random.randint(-30, 30)
            seed_y = self.y - random.randint(80, 120)  # Seeds at top of plant
            self.seeds.append(Seed(self.plant_type, seed_x, seed_y))
    
    def update(self):
        """Update the plant's growth over time"""
        current_time = time.time()
        
        # Only update if plant is alive
        if self.alive:
            # Natural slow growth
            if current_time - self.growth_timer > self.growth_speed:
                if self.growth_stage < 6:
                    self.growth_stage += 1
                    
                    # If reaching maturity (stage 6), create seeds and set maturity time
                    if self.growth_stage == 6:
                        self.create_seeds()
                        self.maturity_time = current_time
                    
                    self.growth_timer = current_time
            
            # Check if plant should die (after seeds are produced and lifetime elapsed)
            if self.growth_stage == 6 and self.maturity_time > 0:
                if current_time - self.maturity_time > self.lifetime:
                    self.die()
    
    def die(self):
        """Plant dies and drops seeds to the ground"""
        self.alive = False
        
        # Drop all seeds to the ground
        soil_y = self.y  # Soil level is at plant's base
        for seed in self.seeds:
            # Randomize falling position
            seed.x = self.x + random.randint(-50, 50)
            seed.y = soil_y - random.randint(10, 30)  # Slightly above the soil
    
    def draw(self, surface):
        """Draw the plant based on its current growth stage"""
        # Draw seeds for both alive and dead plants
        for seed in self.seeds:
            seed.draw_at_position(surface, seed.x, seed.y)
            
        # If plant is dead, don't draw the plant itself
        if not self.alive:
            return
            
        # Draw the plant only if it's alive
        if self.growth_stage >= 1:
            # Draw stem with a slightly curved look for more natural appearance
            stem_height = 30 + (self.growth_stage * 20)
            stem_width = 2 + self.growth_stage // 2
            
            # Instead of a straight line, draw a slightly curved stem
            if self.growth_stage >= 2:
                # Curved stem for more mature plants
                curve_amount = 10 * self.lean_direction
                control_point_x = self.x + curve_amount
                
                # Draw stem as a bezier curve
                points = []
                steps = 20
                for i in range(steps + 1):
                    t = i / steps
                    # Quadratic bezier curve
                    bx = (1-t)**2 * self.x + 2*(1-t)*t * control_point_x + t**2 * self.x
                    by = (1-t)**2 * self.y + 2*(1-t)*t * (self.y - stem_height/2) + t**2 * (self.y - stem_height)
                    points.append((bx, by))
                
                # Draw stem segments
                for i in range(len(points) - 1):
                    pygame.draw.line(surface, self.stem_color, points[i], points[i+1], stem_width)
                
                # Store the top point for attaching flower
                stem_top_x, stem_top_y = self.x, self.y - stem_height
            else:
                # Simple straight stem for young plants
                pygame.draw.line(surface, self.stem_color, 
                               (self.x, self.y), 
                               (self.x, self.y - stem_height), 
                               stem_width)
                stem_top_x, stem_top_y = self.x, self.y - stem_height
        
        if self.growth_stage >= 2:
            # Draw first set of small leaves
            leaf_size = 7 + (self.growth_stage * 3)
            # Left leaf
            leaf_angle = random.randint(-20, -10)
            leaf_points = [
                (self.x, self.y - stem_height * 0.3),
                (self.x - leaf_size, self.y - stem_height * 0.3 - leaf_size/2),
                (self.x - leaf_size/2, self.y - stem_height * 0.3 - leaf_size/4),
                (self.x, self.y - stem_height * 0.3)
            ]
            pygame.draw.polygon(surface, self.leaf_color, leaf_points)
            # Add leaf vein
            leaf_vein_color = (max(0, self.leaf_color[0]-30), max(0, self.leaf_color[1]-30), max(0, self.leaf_color[2]-30))
            pygame.draw.line(surface, leaf_vein_color,
                           (self.x, self.y - stem_height * 0.3),
                           (self.x - leaf_size/2, self.y - stem_height * 0.3 - leaf_size/3), 1)
            
            # Right leaf
            leaf_points = [
                (self.x, self.y - stem_height * 0.3),
                (self.x + leaf_size, self.y - stem_height * 0.3 - leaf_size/2),
                (self.x + leaf_size/2, self.y - stem_height * 0.3 - leaf_size/4),
                (self.x, self.y - stem_height * 0.3)
            ]
            pygame.draw.polygon(surface, self.leaf_color, leaf_points)
            # Add leaf vein
            leaf_vein_color = (max(0, self.leaf_color[0]-30), max(0, self.leaf_color[1]-30), max(0, self.leaf_color[2]-30))
            pygame.draw.line(surface, leaf_vein_color,
                           (self.x, self.y - stem_height * 0.3),
                           (self.x + leaf_size/2, self.y - stem_height * 0.3 - leaf_size/3), 1)
        
        if self.growth_stage >= 3:
            # Draw second set of leaves
            leaf_size = 10 + (self.growth_stage * 3)
            # Left leaf
            leaf_points = [
                (self.x, self.y - stem_height * 0.6),
                (self.x - leaf_size, self.y - stem_height * 0.6 - leaf_size/2),
                (self.x - leaf_size/2, self.y - stem_height * 0.6 - leaf_size/4),
                (self.x, self.y - stem_height * 0.6)
            ]
            pygame.draw.polygon(surface, self.leaf_color, leaf_points)
            # Add leaf vein
            leaf_vein_color = (max(0, self.leaf_color[0]-30), max(0, self.leaf_color[1]-30), max(0, self.leaf_color[2]-30))
            pygame.draw.line(surface, leaf_vein_color,
                           (self.x, self.y - stem_height * 0.6),
                           (self.x - leaf_size/2, self.y - stem_height * 0.6 - leaf_size/3), 1)
            
            # Right leaf
            leaf_points = [
                (self.x, self.y - stem_height * 0.6),
                (self.x + leaf_size, self.y - stem_height * 0.6 - leaf_size/2),
                (self.x + leaf_size/2, self.y - stem_height * 0.6 - leaf_size/4),
                (self.x, self.y - stem_height * 0.6)
            ]
            pygame.draw.polygon(surface, self.leaf_color, leaf_points)
            # Add leaf vein
            leaf_vein_color = (max(0, self.leaf_color[0]-30), max(0, self.leaf_color[1]-30), max(0, self.leaf_color[2]-30))
            pygame.draw.line(surface, leaf_vein_color,
                           (self.x, self.y - stem_height * 0.6),
                           (self.x + leaf_size/2, self.y - stem_height * 0.6 - leaf_size/3), 1)
        
        if self.growth_stage >= 4:
            # Draw larger leaves
            leaf_size = 15 + (self.growth_stage * 3)
            # Left leaf - more detailed with slight serration
            leaf_points = [
                (self.x, self.y - stem_height * 0.8),
                (self.x - leaf_size * 0.3, self.y - stem_height * 0.8 - leaf_size * 0.2),
                (self.x - leaf_size * 0.6, self.y - stem_height * 0.8 - leaf_size * 0.3),
                (self.x - leaf_size, self.y - stem_height * 0.8 - leaf_size * 0.5),
                (self.x - leaf_size * 0.8, self.y - stem_height * 0.8 - leaf_size * 0.7),
                (self.x - leaf_size * 0.4, self.y - stem_height * 0.8 - leaf_size * 0.6),
                (self.x, self.y - stem_height * 0.8 - leaf_size * 0.2),
            ]
            pygame.draw.polygon(surface, self.leaf_color, leaf_points)
            # Add leaf veins
            leaf_vein_color = (max(0, self.leaf_color[0]-30), max(0, self.leaf_color[1]-30), max(0, self.leaf_color[2]-30))
            pygame.draw.line(surface, leaf_vein_color,
                           (self.x, self.y - stem_height * 0.8),
                           (self.x - leaf_size * 0.6, self.y - stem_height * 0.8 - leaf_size * 0.4), 1)
            
            # Right leaf - with slight serration
            leaf_points = [
                (self.x, self.y - stem_height * 0.8),
                (self.x + leaf_size * 0.3, self.y - stem_height * 0.8 - leaf_size * 0.2),
                (self.x + leaf_size * 0.6, self.y - stem_height * 0.8 - leaf_size * 0.3),
                (self.x + leaf_size, self.y - stem_height * 0.8 - leaf_size * 0.5),
                (self.x + leaf_size * 0.8, self.y - stem_height * 0.8 - leaf_size * 0.7),
                (self.x + leaf_size * 0.4, self.y - stem_height * 0.8 - leaf_size * 0.6),
                (self.x, self.y - stem_height * 0.8 - leaf_size * 0.2),
            ]
            pygame.draw.polygon(surface, self.leaf_color, leaf_points)
            # Add leaf veins
            leaf_vein_color = (max(0, self.leaf_color[0]-30), max(0, self.leaf_color[1]-30), max(0, self.leaf_color[2]-30))
            pygame.draw.line(surface, leaf_vein_color,
                           (self.x, self.y - stem_height * 0.8),
                           (self.x + leaf_size * 0.6, self.y - stem_height * 0.8 - leaf_size * 0.4), 1)
        
        if self.growth_stage >= 5:
            # Draw flower bud or flower
            if self.growth_stage == 5:
                # Draw bud - more detailed with color transition
                bud_size = 10
                
                # Outer green sepals
                for i in range(4):
                    angle = i * 90
                    offset_x = int(bud_size * 0.7 * pygame.math.Vector2(1, 0).rotate(angle).x)
                    offset_y = int(bud_size * 0.7 * pygame.math.Vector2(1, 0).rotate(angle).y)
                    sepal_points = [
                        (stem_top_x, stem_top_y),
                        (stem_top_x + offset_x - 3, stem_top_y + offset_y - 3),
                        (stem_top_x + offset_x, stem_top_y + offset_y),
                        (stem_top_x + offset_x + 3, stem_top_y + offset_y + 3),
                    ]
                    pygame.draw.polygon(surface, self.stem_color, sepal_points)
                
                # Inner bud showing flower color
                pygame.draw.circle(surface, self.flower_color, 
                                  (stem_top_x, stem_top_y), 
                                  bud_size * 0.5)
                
            else:  # stage 6 (fully grown flower)
                # Draw full flower - much more detailed and specific to plant type
                flower_radius = 20
                
                if self.plant_type == "rose":
                    # Draw rose with multiple layers of petals
                    # Outer petals
                    for i in range(16):
                        angle = i * (360 / 16)
                        offset_x = int(flower_radius * 0.9 * pygame.math.Vector2(1, 0).rotate(angle).x)
                        offset_y = int(flower_radius * 0.9 * pygame.math.Vector2(1, 0).rotate(angle).y)
                        
                        # Petal base color
                        pygame.draw.ellipse(surface, self.flower_color, 
                                          (stem_top_x + offset_x * 0.5 - flower_radius * 0.4,
                                           stem_top_y + offset_y * 0.5 - flower_radius * 0.4,
                                           flower_radius * 0.8, flower_radius * 0.8))
                        
                        # Petal highlight
                        pygame.draw.ellipse(surface, self.flower_highlight, 
                                          (stem_top_x + offset_x * 0.5 - flower_radius * 0.2,
                                           stem_top_y + offset_y * 0.5 - flower_radius * 0.2,
                                           flower_radius * 0.4, flower_radius * 0.4))
                    
                    # Inner petals
                    for i in range(8):
                        angle = i * (360 / 8) + 22.5
                        offset_x = int(flower_radius * 0.4 * pygame.math.Vector2(1, 0).rotate(angle).x)
                        offset_y = int(flower_radius * 0.4 * pygame.math.Vector2(1, 0).rotate(angle).y)
                        
                        pygame.draw.ellipse(surface, self.flower_color, 
                                          (stem_top_x + offset_x * 0.5 - flower_radius * 0.3,
                                           stem_top_y + offset_y * 0.5 - flower_radius * 0.3,
                                           flower_radius * 0.6, flower_radius * 0.6))
                    
                    # Flower center
                    pygame.draw.circle(surface, self.center_color, 
                                      (stem_top_x, stem_top_y), 
                                      flower_radius * 0.2)
                
                elif self.plant_type == "sunflower":
                    # Draw sunflower with detailed petals and textured center
                    # Draw petals - more elongated and pointed
                    for i in range(20):
                        angle = i * (360 / 20)
                        
                        # Create petal shape with bezier curves
                        petal_length = flower_radius * 1.5
                        
                        start_x = stem_top_x + int(flower_radius * 0.4 * pygame.math.Vector2(1, 0).rotate(angle).x)
                        start_y = stem_top_y + int(flower_radius * 0.4 * pygame.math.Vector2(1, 0).rotate(angle).y)
                        
                        end_x = stem_top_x + int(petal_length * pygame.math.Vector2(1, 0).rotate(angle).x)
                        end_y = stem_top_y + int(petal_length * pygame.math.Vector2(1, 0).rotate(angle).y)
                        
                        control1_x = stem_top_x + int(petal_length * 0.5 * pygame.math.Vector2(1, 0).rotate(angle-15).x)
                        control1_y = stem_top_y + int(petal_length * 0.5 * pygame.math.Vector2(1, 0).rotate(angle-15).y)
                        
                        control2_x = stem_top_x + int(petal_length * 0.5 * pygame.math.Vector2(1, 0).rotate(angle+15).x)
                        control2_y = stem_top_y + int(petal_length * 0.5 * pygame.math.Vector2(1, 0).rotate(angle+15).y)
                        
                        # Create polygon for petal
                        petal_points = [
                            (start_x, start_y),
                            (control1_x, control1_y),
                            (end_x, end_y),
                            (control2_x, control2_y)
                        ]
                        pygame.draw.polygon(surface, self.flower_color, petal_points)
                        
                        # Add highlight to petal
                        pygame.draw.line(surface, self.flower_highlight,
                                       (start_x, start_y),
                                       (end_x, end_y), 1)
                    
                    # Draw textured center
                    pygame.draw.circle(surface, self.center_color, 
                                      (stem_top_x, stem_top_y), 
                                      flower_radius * 0.5)
                    
                    # Add seed texture to center
                    for _ in range(40):
                        seed_angle = random.uniform(0, 360)
                        seed_distance = random.uniform(0, flower_radius * 0.4)
                        seed_x = stem_top_x + int(seed_distance * pygame.math.Vector2(1, 0).rotate(seed_angle).x)
                        seed_y = stem_top_y + int(seed_distance * pygame.math.Vector2(1, 0).rotate(seed_angle).y)
                        
                        pygame.draw.circle(surface, (30, 30, 10), 
                                         (seed_x, seed_y), 
                                         2)
                
                else:  # daisy or default
                    # Draw daisy with pointed petals and detailed center
                    # Draw white petals
                    for i in range(16):
                        angle = i * (360 / 16)
                        
                        # Create elongated oval petals
                        petal_length = flower_radius * 1.2
                        petal_width = flower_radius * 0.3
                        
                        # Calculate petal points
                        center_x = stem_top_x + int((flower_radius * 0.5) * pygame.math.Vector2(1, 0).rotate(angle).x)
                        center_y = stem_top_y + int((flower_radius * 0.5) * pygame.math.Vector2(1, 0).rotate(angle).y)
                        
                        # Create a rotated rect for the petal
                        petal_points = []
                        for corner in [(petal_width/2, -petal_length/2), 
                                      (petal_width/2, petal_length/2),
                                      (-petal_width/2, petal_length/2),
                                      (-petal_width/2, -petal_length/2)]:
                            # Rotate corner and add to center position
                            rotated_x = corner[0] * pygame.math.Vector2(1, 0).rotate(angle).x - corner[1] * pygame.math.Vector2(1, 0).rotate(angle).y
                            rotated_y = corner[0] * pygame.math.Vector2(1, 0).rotate(angle).y + corner[1] * pygame.math.Vector2(1, 0).rotate(angle).x
                            petal_points.append((center_x + rotated_x, center_y + rotated_y))
                        
                        pygame.draw.polygon(surface, self.flower_color, petal_points)
                        
                        # Add subtle highlight to petal
                        pygame.draw.line(surface, self.flower_highlight,
                                       (center_x, center_y),
                                       (center_x + int(petal_length * pygame.math.Vector2(1, 0).rotate(angle).x),
                                        center_y + int(petal_length * pygame.math.Vector2(1, 0).rotate(angle).y)), 
                                       1)
                    
                    # Draw yellow center
                    pygame.draw.circle(surface, self.center_color, 
                                      (stem_top_x, stem_top_y), 
                                      flower_radius * 0.4)
                    
                    # Add texture to center
                    for _ in range(20):
                        dot_angle = random.uniform(0, 360)
                        dot_distance = random.uniform(0, flower_radius * 0.3)
                        dot_x = stem_top_x + int(dot_distance * pygame.math.Vector2(1, 0).rotate(dot_angle).x)
                        dot_y = stem_top_y + int(dot_distance * pygame.math.Vector2(1, 0).rotate(dot_angle).y)
                        
                        pygame.draw.circle(surface, (220, 180, 0), 
                                         (dot_x, dot_y), 
                                         1)
        
        # Draw seeds if the plant is fully grown
        for seed in self.seeds:
            seed.draw_at_position(surface, seed.x, seed.y)