"""Constants for the flower growing game"""

# Available plant types
PLANT_TYPES = [
    "rose",
    "sunflower",
    "daisy",
]

# Growth stages
GROWTH_STAGES = [
    "seed",
    "small stalk",
    "stalk with few leaves",
    "stalk with more leaves",
    "stalk with large leaves",
    "flower bud",
    "full flower with seeds"
]

# Colors
COLORS = {
    "sky": (135, 206, 235),
    "soil": (139, 69, 19),
    "toolbar": (200, 200, 200),
    "water": (0, 0, 255),
    "sun": (255, 255, 0),
}

# Game settings
NATURAL_GROWTH_TIME = 10  # Seconds between natural growth stages