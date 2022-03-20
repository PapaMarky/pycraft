colorsxxx = {
     0: (  0,   0,   0,   0),
     1: (127, 178,  56, 255),
     2: (247, 233, 163, 255),
     3: (199, 199, 199, 255),
     4: (255,   0,   0, 255),
     5: (160, 160, 255, 255),
     6: (167, 167, 167, 255),
     7: (  0, 124,   0, 255),
     8: (255, 255, 255, 255),
     9: (164, 168, 184, 255),
    10: (151, 109,  77, 255),
    11: (112, 112, 112, 255),
    12: ( 64,  64, 255, 255),
    13: (143, 119,  72, 255),
    14: (255, 252, 245, 255),
    15: (216, 127,  51, 255),
    16: (178,  76, 216, 255),
    17: (102, 153, 216, 255),
    18: (229, 229,  51, 255),
    19: (127, 204,  25, 255),
    20: (242, 127, 165, 255),
    21: ( 76,  76,  76, 255),
    22: (153, 153, 153, 255),
    23: ( 76, 127, 153, 255),
    24: (127,  63, 178, 255),
    25: ( 51,  76, 178, 255),
    26: (102,  76,  51, 255),
    27: (102, 127,  51, 255),
    28: (153,  51,  51, 255),
    29: ( 25,  25,  25, 255),
    30: (250, 238,  77, 255),
    31: ( 92, 219, 213, 255),
    32: ( 74, 128, 255, 255),
    33: (  0, 217,  58, 255),
    34: (129,  86,  49, 255),
    35: (112,   2,   0, 255),
    36: (209, 177, 161, 255),
    37: (159,  82,  36, 255),
    38: (149,  87, 108, 255),
    39: (112, 108, 138, 255),
    40: (186, 133,  36, 255),
    41: (103, 117,  53, 255),
    42: (160,  77,  78, 255),
    43: ( 57,  41,  35, 255),
    44: (135, 107,  98, 255),
    45: ( 87,  92,  92, 255),
    46: (122,  73,  88, 255),
    47: ( 76,  62,  92, 255),
    48: ( 76,  50,  35, 255),
    49: ( 76,  82,  42, 255),
    50: (142,  60,  46, 255),
    51: ( 37,  22,  16, 255),
    52: (189,  48,  49, 255),
    53: (148,  63,  97, 255),
    54: ( 92,  25,  29, 255),
    55: ( 22, 126, 134, 255),
    56: ( 58, 142, 140, 255),
    57: ( 86,  44,  62, 255),
    58: ( 20, 180, 133, 255),
    59: (100, 100, 100, 255),
    60: (216, 175, 147, 255),
    61: (127, 167, 150, 255),
}
def get_color(name):
    name_map = {
        'white': 32,
        'red': 18,
        'yellow': 74,
        'gray': 84,
        'blue': 100,
        'black': 116,
        'light_gray': 88

    }
    print(f'get_color("{name}")')
    if not name in name_map:
        print(f'--- cannot find it')
        # name = 'white'
    c = colors[name_map[name]]
    print(f'--- {c}')
    return c

colors = {
  0: (0,0,0), # Not explored
  1: (0,0,0), # Not explored
  2: (0,0,0), # Not explored
  3: (0,0,0), # Not explored
  4: (89,125,39), # Grass, Slime Block
  5: (109,153,48), # Grass, Slime Block
  6: (127,178,56), # Grass, Slime Block
  7: (67,94,29), # Grass, Slime Block
  8: (174,164,115), # Sand, Sandstone, Birch plank, Glowstone, Endstone
  9: (213,201,140), # Sand, Sandstone, Birch plank, Glowstone, Endstone
  10: (247,233,163), # Sand, Sandstone, Birch plank, Glowstone, Endstone
  11: (130,123,86), # Sand, Sandstone, Birch plank, Glowstone, Endstone
  12: (138,138,138), # Bed, Cobweb
  13: (169,169,169), # Bed, Cobweb
  14: (197,197,197), # Bed, Cobweb
  15: (104,104,104), # Bed, Cobweb
  16: (180,0,0), # Lava, TNT, Redstone Block
  17: (220,0,0), # Lava, TNT, Redstone Block
  18: (255,0,0), # Lava, TNT, Redstone Block
  19: (135,0,0), # Lava, TNT, Redstone Block
  20: (112,112,180), # Ice, Packed Ice
  21: (138,138,220), # Ice, Packed Ice
  22: (160,160,255), # Ice, Packed Ice
  23: (84,84,135), # Ice, Packed Ice
  24: (117,117,117), # Iron Block, Iron items, Brewing Stand
  25: (144,144,144), # Iron Block, Iron items, Brewing Stand
  26: (167,167,167), # Iron Block, Iron items, Brewing Stand
  27: (88,88,88), # Iron Block, Iron items, Brewing Stand
  28: (0,87,0), # Leaves, Flowers, Grass
  29: (0,106,0), # Leaves, Flowers, Grass
  30: (0,124,0), # Leaves, Flowers, Grass
  31: (0,65,0), # Leaves, Flowers, Grass
  32: (180,180,180), # Wool, Snow
  33: (220,220,220), # Wool, Snow
  34: (255,255,255), # Wool, Snow
  35: (135,135,135), # Wool, Snow
  36: (115,118,129), # Clay
  37: (141,144,158), # Clay
  38: (164,168,184), # Clay
  39: (86,88,97), # Clay
  40: (129,74,33), # Dirt, Coarse Dirt, Jungle Plank, Granite
  41: (157,91,40), # Dirt, Coarse Dirt, Jungle Plank, Granite
  42: (183,106,47), # Dirt, Coarse Dirt, Jungle Plank, Granite
  43: (96,56,24), # Dirt, Coarse Dirt, Jungle Plank, Granite
  44: (79,79,79), # Stone, Cobblestone, Ores, Acacia Log, *Many others*
  45: (96,96,96), # Stone, Cobblestone, Ores, Acacia Log, *Many others*
  46: (112,112,112), # Stone, Cobblestone, Ores, Acacia Log, *Many others*
  47: (59,59,59), # Stone, Cobblestone, Ores, Acacia Log, *Many others*
  48: (101,84,51), # Oak Plank, Wooden Items, Mushroom (block), Banners, Daylight Sensor
  49: (123,103,62), # Oak Plank, Wooden Items, Mushroom (block), Banners, Daylight Sensor
  50: (143,119,72), # Oak Plank, Wooden Items, Mushroom (block), Banners, Daylight Sensor
  51: (76,63,38), # Oak Plank, Wooden Items, Mushroom (block), Banners, Daylight Sensor
  52: (45,45,180), # Water
  53: (55,55,220), # Water
  54: (64,64,255), # Water
  55: (33,33,135), # Water
  56: (180,177,172), # Quartz, Sea Lantern, Birch Log
  57: (220,217,211), # Quartz, Sea Lantern, Birch Log
  58: (255,252,245), # Quartz, Sea Lantern, Birch Log
  59: (135,133,129), # Quartz, Sea Lantern, Birch Log
  60: (152,89,36), # Orange Wool/Glass/Stained Clay, Pumpkin, Hardened Clay, Acacia Plank
  61: (186,109,44), # Orange Wool/Glass/Stained Clay, Pumpkin, Hardened Clay, Acacia Plank
  62: (216,127,51), # Orange Wool/Glass/Stained Clay, Pumpkin, Hardened Clay, Acacia Plank
  63: (114,67,27), # Orange Wool/Glass/Stained Clay, Pumpkin, Hardened Clay, Acacia Plank
  64: (125,53,152), # Magenta Wool/Glass/Stained Clay
  65: (153,65,186), # Magenta Wool/Glass/Stained Clay
  66: (178,76,216), # Magenta Wool/Glass/Stained Clay
  67: (94,40,114), # Magenta Wool/Glass/Stained Clay
  68: (72,108,152), # Light Blue Wool/Glass/Stained Clay
  69: (88,132,186), # Light Blue Wool/Glass/Stained Clay
  70: (102,153,216), # Light Blue Wool/Glass/Stained Clay
  71: (54,81,114), # Light Blue Wool/Glass/Stained Clay
  72: (161,161,36), # Yellow Wool/Glass/Stained Clay, Sponge, Hay Bale
  73: (197,197,44), # Yellow Wool/Glass/Stained Clay, Sponge, Hay Bale
  74: (229,229,51), # Yellow Wool/Glass/Stained Clay, Sponge, Hay Bale
  75: (121,121,27), # Yellow Wool/Glass/Stained Clay, Sponge, Hay Bale
  76: (89,144,17), # Lime Wool/Glass/Stained Clay, Melon
  77: (109,176,21), # Lime Wool/Glass/Stained Clay, Melon
  78: (127,204,25), # Lime Wool/Glass/Stained Clay, Melon
  79: (67,108,13), # Lime Wool/Glass/Stained Clay, Melon
  80: (170,89,116), # Pink Wool/Glass/Stained Clay
  81: (208,109,142), # Pink Wool/Glass/Stained Clay
  82: (242,127,165), # Pink Wool/Glass/Stained Clay
  83: (128,67,87), # Pink Wool/Glass/Stained Clay
  84: (53,53,53), # Grey Wool/Glass/Stained Clay
  85: (65,65,65), # Grey Wool/Glass/Stained Clay
  86: (76,76,76), # Grey Wool/Glass/Stained Clay
  87: (40,40,40), # Grey Wool/Glass/Stained Clay
  88: (108,108,108), # Light Grey Wool/Glass/Stained Clay
  89: (132,132,132), # Light Grey Wool/Glass/Stained Clay
  90: (153,153,153), # Light Grey Wool/Glass/Stained Clay
  91: (81,81,81), # Light Grey Wool/Glass/Stained Clay
  92: (53,89,108), # Cyan Wool/Glass/Stained Clay
  93: (65,109,132), # Cyan Wool/Glass/Stained Clay
  94: (76,127,153), # Cyan Wool/Glass/Stained Clay
  95: (40,67,81), # Cyan Wool/Glass/Stained Clay
  96: (89,44,125), # Purple Wool/Glass/Stained Clay, Mycelium
  97: (109,54,153), # Purple Wool/Glass/Stained Clay, Mycelium
  98: (127,63,178), # Purple Wool/Glass/Stained Clay, Mycelium
  99: (67,33,94), # Purple Wool/Glass/Stained Clay, Mycelium
  100: (36,53,125), # Blue Wool/Glass/Stained Clay
  101: (44,65,153), # Blue Wool/Glass/Stained Clay
  102: (51,76,178), # Blue Wool/Glass/Stained Clay
  103: (27,40,94), # Blue Wool/Glass/Stained Clay
  104: (72,53,36), # Brown Wool/Glass/Stained Clay, Soul Sand, Dark Oak Plank
  105: (88,65,44), # Brown Wool/Glass/Stained Clay, Soul Sand, Dark Oak Plank
  106: (102,76,51), # Brown Wool/Glass/Stained Clay, Soul Sand, Dark Oak Plank
  107: (54,40,27), # Brown Wool/Glass/Stained Clay, Soul Sand, Dark Oak Plank
  108: (72,89,36), # Green Wool/Glass/Stained Clay, End Portal Frame
  109: (88,109,44), # Green Wool/Glass/Stained Clay, End Portal Frame
  110: (102,127,51), # Green Wool/Glass/Stained Clay, End Portal Frame
  111: (54,67,27), # Green Wool/Glass/Stained Clay, End Portal Frame
  112: (108,36,36), # Red Wool/Glass/Stained Clay, Huge Red Mushroom, Brick, Enchanting Table
  113: (132,44,44), # Red Wool/Glass/Stained Clay, Huge Red Mushroom, Brick, Enchanting Table
  114: (153,51,51), # Red Wool/Glass/Stained Clay, Huge Red Mushroom, Brick, Enchanting Table
  115: (81,27,27), # Red Wool/Glass/Stained Clay, Huge Red Mushroom, Brick, Enchanting Table
  116: (17,17,17), # Black Wool/Glass/Stained Clay, Dragon Egg, Block of Coal, Obsidian
  117: (21,21,21), # Black Wool/Glass/Stained Clay, Dragon Egg, Block of Coal, Obsidian
  118: (25,25,25), # Black Wool/Glass/Stained Clay, Dragon Egg, Block of Coal, Obsidian
  119: (13,13,13), # Black Wool/Glass/Stained Clay, Dragon Egg, Block of Coal, Obsidian
  120: (176,168,54), # Block of Gold, Weighted Pressure Plate (Light)
  121: (215,205,66), # Block of Gold, Weighted Pressure Plate (Light)
  122: (250,238,77), # Block of Gold, Weighted Pressure Plate (Light)
  123: (132,126,40), # Block of Gold, Weighted Pressure Plate (Light)
  124: (64,154,150), # Block of Diamond, Prismarine, Prismarine Bricks, Dark Prismarine, Beacon
  125: (79,188,183), # Block of Diamond, Prismarine, Prismarine Bricks, Dark Prismarine, Beacon
  126: (92,219,213), # Block of Diamond, Prismarine, Prismarine Bricks, Dark Prismarine, Beacon
  127: (48,115,112), # Block of Diamond, Prismarine, Prismarine Bricks, Dark Prismarine, Beacon
  128: (52,90,180), # Lapis Lazuli Block
  129: (63,110,220), # Lapis Lazuli Block
  130: (74,128,255), # Lapis Lazuli Block
  131: (39,67,135), # Lapis Lazuli Block
  132: (0,153,40), # Block of Emerald
  133: (0,187,50), # Block of Emerald
  134: (0,217,58), # Block of Emerald
  135: (0,114,30), # Block of Emerald
  136: (90,59,34), # Podzol, Spruce Plank
  137: (110,73,41), # Podzol, Spruce Plank
  138: (127,85,48), # Podzol, Spruce Plank
  139: (67,44,25), # Podzol, Spruce Plank
  140: (79,1,0), # Netherrack, Quartz Ore, Nether Wart, Nether Brick Items
  141: (96,1,0), # Netherrack, Quartz Ore, Nether Wart, Nether Brick Items
  142: (112,2,0), # Netherrack, Quartz Ore, Nether Wart, Nether Brick Items
  143: (59,1,0) # Netherrack, Quartz Ore, Nether Wart, Nether Brick Items
}
