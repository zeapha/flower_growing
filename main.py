import pygame
import sys
import random
from garden import Garden
from tools import ToolBar
from plant import Plant, Seed

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GARDEN_HEIGHT = int(SCREEN_HEIGHT * 7/8)
TOOLBAR_HEIGHT = SCREEN_HEIGHT - GARDEN_HEIGHT
BG_COLOR = (135, 206, 235)  # Sky blue background

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flower Growing Game")

# Create game objects
garden = Garden(SCREEN_WIDTH, GARDEN_HEIGHT)
toolbar = ToolBar(SCREEN_WIDTH, TOOLBAR_HEIGHT, 0, GARDEN_HEIGHT)

# Game variables
clock = pygame.time.Clock()
FPS = 60
selected_seed = None
selected_tool = None

# Initialize with starting seeds
toolbar.seed_counts["rose"] = 3
toolbar.seed_counts["sunflower"] = 3
toolbar.seed_counts["daisy"] = 3

# Empty list for backwards compatibility
collected_seeds = []  # This is no longer used actively

# Main game loop
def main():
    global selected_seed, selected_tool
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Left click
                if event.button == 1:
                    # Check if clicked in garden area
                    if mouse_pos[1] < GARDEN_HEIGHT:
                        # If scissors are selected
                        if selected_tool == "scissors":
                            # Cut flowers but don't collect seeds automatically
                            garden.cut_flowers(mouse_pos[0], mouse_pos[1])
                            # Seeds will drop to the ground and player can collect them manually
                        # If we have a selected seed, plant it
                        elif selected_seed is not None:
                            garden.plant_seed(selected_seed, mouse_pos[0], mouse_pos[1])
                            selected_seed = None
                        else:
                            # Check if clicked near a seed from a plant
                            seed = garden.check_seed_click(mouse_pos)
                            if seed:
                                # Add seed directly to toolbar storage
                                toolbar.add_seed(seed.plant_type)
                                # No need to select the seed as it goes directly to storage
                
                # Right click - auto plant feature
                elif event.button == 3:
                    # Only handle right-clicks in toolbar area
                    if mouse_pos[1] >= GARDEN_HEIGHT:
                        tool_clicked = toolbar.check_click(mouse_pos)
                        if tool_clicked and tool_clicked.startswith("seed_"):
                            # Get the seed type
                            seed_type = tool_clicked.split("_")[1]
                            
                            # Check if we have seeds of this type
                            if toolbar.seed_counts[seed_type] > 0:
                                # Remove a seed from storage
                                toolbar.remove_seed(seed_type)
                                
                                # Create the seed 
                                auto_seed = Seed(seed_type)
                                
                                # Pick a random horizontal position in soil
                                random_x = random.randint(50, SCREEN_WIDTH - 50)
                                
                                # Plant the seed
                                garden.plant_seed(auto_seed, random_x, GARDEN_HEIGHT - 10)
                
                # Regular left click handling for toolbar
                if event.button == 1 and mouse_pos[1] >= GARDEN_HEIGHT:
                    tool_clicked = toolbar.check_click(mouse_pos)
                    if tool_clicked is None:
                        # Clicked in toolbar area but not on any tool
                        if selected_seed:
                            # Store seed based on its type
                            toolbar.add_seed(selected_seed.plant_type)
                            selected_seed = None
                        # Deselect scissors if they were selected
                        if selected_tool == "scissors":
                            selected_tool = None
                    elif tool_clicked == "water":
                        garden.water_plants()
                        # Deselect any tools
                        selected_tool = None
                    elif tool_clicked == "sun":
                        garden.provide_sunlight()
                        # Deselect any tools
                        selected_tool = None
                    elif tool_clicked == "scissors":
                        # Select scissors tool
                        selected_tool = "scissors"
                        # Deselect seed if one was selected
                        if selected_seed:
                            toolbar.add_seed(selected_seed.plant_type)
                            selected_seed = None
                    elif tool_clicked.startswith("seed_"):
                        # Deselect any tools first
                        selected_tool = None
                        
                        # Get the seed type
                        seed_type = tool_clicked.split("_")[1]
                        
                        if selected_seed is None:
                            # No seed selected, try to take one from storage
                            if toolbar.remove_seed(seed_type):
                                selected_seed = Seed(seed_type)
                        else:
                            # Already have a seed selected, put it in storage
                            toolbar.add_seed(selected_seed.plant_type)
                            selected_seed = None
        
        # Update
        garden.update()
        
        # Get mouse position for highlighting seeds
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw everything
        screen.fill(BG_COLOR)
        garden.draw(screen)  # Remove mouse_pos parameter since we're not using it anymore
        toolbar.draw(screen, collected_seeds)
        
        # Draw selected seed following the mouse if there is one
        if selected_seed is not None:
            mouse_pos = pygame.mouse.get_pos()
            selected_seed.draw_at_position(screen, mouse_pos[0], mouse_pos[1])
            
        # Draw scissors following the mouse if selected
        if selected_tool == "scissors":
            mouse_pos = pygame.mouse.get_pos()
            # Draw a simple scissors icon at mouse position
            scissors_color = (80, 80, 100)
            line_length = 12
            # Draw the X shape
            pygame.draw.line(screen, scissors_color, 
                           (mouse_pos[0] - line_length, mouse_pos[1] - line_length),
                           (mouse_pos[0] + line_length, mouse_pos[1] + line_length), 4)
            pygame.draw.line(screen, scissors_color, 
                           (mouse_pos[0] + line_length, mouse_pos[1] - line_length),
                           (mouse_pos[0] - line_length, mouse_pos[1] + line_length), 4)
            # Draw handles
            pygame.draw.circle(screen, scissors_color, 
                             (mouse_pos[0] - line_length - 3, mouse_pos[1] - line_length - 3), 5)
            pygame.draw.circle(screen, scissors_color, 
                             (mouse_pos[0] + line_length + 3, mouse_pos[1] - line_length - 3), 5)
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()