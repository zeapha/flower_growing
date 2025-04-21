import pygame
from plant import Seed

class ToolBar:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = (200, 200, 200)  # Light gray background
        
        # Create water button (blue)
        self.water_button = pygame.Rect(20, y + 10, 60, height - 20)
        self.water_color = (0, 0, 255)  # Blue
        
        # Create sun button (yellow)
        self.sun_button = pygame.Rect(width - 80, y + 10, 60, height - 20)
        self.sun_color = (255, 255, 0)  # Yellow
        
        # Create scissors button (metal/gray)
        self.scissors_button = pygame.Rect(width - 160, y + 10, 60, height - 20)
        self.scissors_color = (160, 160, 180)  # Metal gray
        
        # Create seed storage slots
        self.seed_slots = []
        self.seed_counts = {"rose": 0, "sunflower": 0, "daisy": 0}  # Count by seed type
        
        slot_width = 40
        slot_spacing = 10
        start_x = 100
        for i in range(3):  # Only need 3 slots (one for each type)
            slot_x = start_x + i * (slot_width + slot_spacing)
            slot_rect = pygame.Rect(slot_x, y + 10, slot_width, height - 20)
            self.seed_slots.append({"rect": slot_rect, "type": ["rose", "sunflower", "daisy"][i]})
        
        # Font for counting seeds
        self.font = pygame.font.SysFont(None, 20)  # Default font, size 20
    
    def check_click(self, pos):
        """Check if any tool was clicked and return which one"""
        if self.water_button.collidepoint(pos):
            return "water"
        elif self.sun_button.collidepoint(pos):
            return "sun"
        elif self.scissors_button.collidepoint(pos):
            return "scissors"
        
        # Check seed slots - ANY click in the slot returns the seed type
        for slot in self.seed_slots:
            if slot["rect"].collidepoint(pos):
                return f"seed_{slot['type']}"
        
        return None
        
    def add_seed(self, seed_type):
        """Add a seed to the count"""
        self.seed_counts[seed_type] += 1
        
    def remove_seed(self, seed_type):
        """Remove a seed from the count if available"""
        if self.seed_counts[seed_type] > 0:
            self.seed_counts[seed_type] -= 1
            return True
        return False
    
    def draw(self, surface, collected_seeds):
        """Draw the toolbar and all tools"""
        # Draw toolbar background
        pygame.draw.rect(surface, self.bg_color, self.rect)
        
        # Draw water button
        pygame.draw.rect(surface, self.water_color, self.water_button)
        # Add water drop icon
        drop_points = [
            (self.water_button.centerx, self.water_button.top + 10),
            (self.water_button.centerx - 10, self.water_button.centery),
            (self.water_button.centerx + 10, self.water_button.centery)
        ]
        pygame.draw.polygon(surface, (100, 100, 255), drop_points)
        pygame.draw.circle(surface, (100, 100, 255), 
                          (self.water_button.centerx, self.water_button.centery + 5), 
                          10)
        
        # Draw sun button
        pygame.draw.rect(surface, self.sun_color, self.sun_button)
        # Add sun icon (circle with rays)
        pygame.draw.circle(surface, (255, 200, 0), 
                          (self.sun_button.centerx, self.sun_button.centery), 
                          15)
        
        # Draw scissors button
        pygame.draw.rect(surface, self.scissors_color, self.scissors_button)
        # Add scissors icon (simple X shape)
        scissors_color = (80, 80, 100)
        line_length = 12
        center_x = self.scissors_button.centerx
        center_y = self.scissors_button.centery
        # Draw the X shape
        pygame.draw.line(surface, scissors_color, 
                        (center_x - line_length, center_y - line_length),
                        (center_x + line_length, center_y + line_length), 4)
        pygame.draw.line(surface, scissors_color, 
                        (center_x + line_length, center_y - line_length),
                        (center_x - line_length, center_y + line_length), 4)
        # Draw handles
        pygame.draw.circle(surface, scissors_color, 
                          (center_x - line_length - 3, center_y - line_length - 3), 5)
        pygame.draw.circle(surface, scissors_color, 
                          (center_x + line_length + 3, center_y - line_length - 3), 5)
        
        # Draw seed slots
        for slot in self.seed_slots:
            pygame.draw.rect(surface, (100, 80, 60), slot["rect"])  # Brown slot
            
            seed_type = slot["type"]
            if self.seed_counts[seed_type] > 0:
                # Create a temporary seed for display
                temp_seed = Seed(seed_type)
                
                # Draw seed in the slot
                temp_seed.draw_at_position(surface, slot["rect"].centerx, slot["rect"].centery)
                
                # Draw seed count
                count_text = self.font.render(str(self.seed_counts[seed_type]), True, (255, 255, 255))
                count_rect = count_text.get_rect(topright=(slot["rect"].right - 2, slot["rect"].top + 2))
                surface.blit(count_text, count_rect)