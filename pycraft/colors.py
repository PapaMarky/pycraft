def get_sheep_color(value:int):
    sheep_colors = {
        0: 'white',
        1: 'orange',
        2: 'magenta',
        3: 'light blue',
        4: 'yellow',
        5: 'lime',
        6: 'pink',
        7: 'gray',
        8: 'light gray',
        9: 'cyan',
        10: 'purple',
        11: 'blue',
        12: 'brown',
        13: 'green',
        14: 'red',
        15: 'black'
    }
    return sheep_colors[value] if value in sheep_colors else None

def get_dye_color(name:str):
    '''
    Look up a color in the "dye_colors" dict

    Source of data: https://minecraft.fandom.com/wiki/Dye#Dyeing_wool_and_mobs
    '''
    return dye_colors[name]

def get_map_color(color_index:int):
    '''
    These are the colors for the 'colors' data in map files. With
    Minecraft 1.18.2 I have to make a manual adjustment for "water"
    colors. Either the wiki (ref below) is outdated or I'm not
    understanding something.

    Source of data: https://minecraft.fandom.com/wiki/Map_item_format
    '''
    if color_index < 0:
        # colors are unsigned bytes, but nbt returns signed bytes. Adjust accordingly.
        color_index = 256 + color_index
    if color_index >= len(colors):
        # if value out of range return an ugly color instead of crashing
        print(f'BAD MAP COLOR VALUE: {color_index}')
        color_index = 75
    if color_index >= 48 and color_index <= 51:
        # for some reason when I use this on minecraft 1.18.2 data,
        # the color for water are in the wrong place. This fixes that.
        color_index += 4

    return colors[color_index]

dye_colors = {
    'black': '#1D1D21',
    'red': '#B02E26',
    'green': '#5E7C16',
    'brown': '#835432',
    'blue': '#3C44AA',
    'purple': '#8932B8',
    'cyan': '#169C9C',
    'light_gray': '#9D9D97',
    'gray': '#474F52',
    'pink': '#F38BAA',
    'lime': '#80C71F',
    'yellow': '#FED83D',
    'light_blue': '#3AB3DA',
    'magenta': '#C74EBD',
    'orange': '#F9801D',
    'white': '#F9FFFE'
}

colors = {
  0: (0,0,0,0), # Not explored
  1: (0,0,0,0), # Not explored
  2: (0,0,0,0), # Not explored
  3: (0,0,0,0), # Not explored
  4: (89,125,39,255), # Grass, Slime Block
  5: (109,153,48,255), # Grass, Slime Block
  6: (127,178,56,255), # Grass, Slime Block
  7: (67,94,29,255), # Grass, Slime Block
  8: (174,164,115,255), # Sand, Sandstone, Birch plank, Glowstone, Endstone
  9: (213,201,140,255), # Sand, Sandstone, Birch plank, Glowstone, Endstone
  10: (247,233,163,255), # Sand, Sandstone, Birch plank, Glowstone, Endstone
  11: (130,123,86,255), # Sand, Sandstone, Birch plank, Glowstone, Endstone
  12: (138,138,138,255), # Bed, Cobweb
  13: (169,169,169,255), # Bed, Cobweb
  14: (197,197,197,255), # Bed, Cobweb
  15: (104,104,104,255), # Bed, Cobweb
  16: (180,0,0,255), # Lava, TNT, Redstone Block
  17: (220,0,0,255), # Lava, TNT, Redstone Block
  18: (255,0,0,255), # Lava, TNT, Redstone Block
  19: (135,0,0,255), # Lava, TNT, Redstone Block
  20: (112,112,180,255), # Ice, Packed Ice
  21: (138,138,220,255), # Ice, Packed Ice
  22: (160,160,255,255), # Ice, Packed Ice
  23: (84,84,135,255), # Ice, Packed Ice
  24: (117,117,117,255), # Iron Block, Iron items, Brewing Stand
  25: (144,144,144,255), # Iron Block, Iron items, Brewing Stand
  26: (167,167,167,255), # Iron Block, Iron items, Brewing Stand
  27: (88,88,88,255), # Iron Block, Iron items, Brewing Stand
  28: (0,87,0,255), # Leaves, Flowers, Grass
  29: (0,106,0,255), # Leaves, Flowers, Grass
  30: (0,124,0,255), # Leaves, Flowers, Grass
  31: (0,65,0,255), # Leaves, Flowers, Grass
  32: (180,180,180,255), # Wool, Snow
  33: (220,220,220,255), # Wool, Snow
  34: (255,255,255,255), # Wool, Snow
  35: (135,135,135,255), # Wool, Snow
  36: (115,118,129,255), # Clay
  37: (141,144,158,255), # Clay
  38: (164,168,184,255), # Clay
  39: (86,88,97,255), # Clay
  40: (129,74,33,255), # Dirt, Coarse Dirt, Jungle Plank, Granite
  41: (157,91,40,255), # Dirt, Coarse Dirt, Jungle Plank, Granite
  42: (183,106,47,255), # Dirt, Coarse Dirt, Jungle Plank, Granite
  43: (96,56,24,255), # Dirt, Coarse Dirt, Jungle Plank, Granite
  44: (79,79,79,255), # Stone, Cobblestone, Ores, Acacia Log, *Many others*
  45: (96,96,96,255), # Stone, Cobblestone, Ores, Acacia Log, *Many others*
  46: (112,112,112,255), # Stone, Cobblestone, Ores, Acacia Log, *Many others*
  47: (59,59,59,255), # Stone, Cobblestone, Ores, Acacia Log, *Many others*
  48: (101,84,51,255), # Oak Plank, Wooden Items, Mushroom (block), Banners, Daylight Sensor
  49: (123,103,62,255), # Oak Plank, Wooden Items, Mushroom (block), Banners, Daylight Sensor
  50: (143,119,72,255), # Oak Plank, Wooden Items, Mushroom (block), Banners, Daylight Sensor
  51: (76,63,38,255), # Oak Plank, Wooden Items, Mushroom (block), Banners, Daylight Sensor
  52: (45,45,180,255), # Water
  53: (55,55,220,255), # Water
  54: (64,64,255,255), # Water
  55: (33,33,135,255), # Water
  56: (180,177,172,255), # Quartz, Sea Lantern, Birch Log
  57: (220,217,211,255), # Quartz, Sea Lantern, Birch Log
  58: (255,252,245,255), # Quartz, Sea Lantern, Birch Log
  59: (135,133,129,255), # Quartz, Sea Lantern, Birch Log
  60: (152,89,36,255), # Orange Wool/Glass/Stained Clay, Pumpkin, Hardened Clay, Acacia Plank
  61: (186,109,44,255), # Orange Wool/Glass/Stained Clay, Pumpkin, Hardened Clay, Acacia Plank
  62: (216,127,51,255), # Orange Wool/Glass/Stained Clay, Pumpkin, Hardened Clay, Acacia Plank
  63: (114,67,27,255), # Orange Wool/Glass/Stained Clay, Pumpkin, Hardened Clay, Acacia Plank
  64: (125,53,152,255), # Magenta Wool/Glass/Stained Clay
  65: (153,65,186,255), # Magenta Wool/Glass/Stained Clay
  66: (178,76,216,255), # Magenta Wool/Glass/Stained Clay
  67: (94,40,114,255), # Magenta Wool/Glass/Stained Clay
  68: (72,108,152,255), # Light Blue Wool/Glass/Stained Clay
  69: (88,132,186,255), # Light Blue Wool/Glass/Stained Clay
  70: (102,153,216,255), # Light Blue Wool/Glass/Stained Clay
  71: (54,81,114,255), # Light Blue Wool/Glass/Stained Clay
  72: (161,161,36,255), # Yellow Wool/Glass/Stained Clay, Sponge, Hay Bale
  73: (197,197,44,255), # Yellow Wool/Glass/Stained Clay, Sponge, Hay Bale
  74: (229,229,51,255), # Yellow Wool/Glass/Stained Clay, Sponge, Hay Bale
  75: (121,121,27,255), # Yellow Wool/Glass/Stained Clay, Sponge, Hay Bale
  76: (89,144,17,255), # Lime Wool/Glass/Stained Clay, Melon
  77: (109,176,21,255), # Lime Wool/Glass/Stained Clay, Melon
  78: (127,204,25,255), # Lime Wool/Glass/Stained Clay, Melon
  79: (67,108,13,255), # Lime Wool/Glass/Stained Clay, Melon
  80: (170,89,116,255), # Pink Wool/Glass/Stained Clay
  81: (208,109,142,255), # Pink Wool/Glass/Stained Clay
  82: (242,127,165,255), # Pink Wool/Glass/Stained Clay
  83: (128,67,87,255), # Pink Wool/Glass/Stained Clay
  84: (53,53,53,255), # Grey Wool/Glass/Stained Clay
  85: (65,65,65,255), # Grey Wool/Glass/Stained Clay
  86: (76,76,76,255), # Grey Wool/Glass/Stained Clay
  87: (40,40,40,255), # Grey Wool/Glass/Stained Clay
  88: (108,108,108,255), # Light Grey Wool/Glass/Stained Clay
  89: (132,132,132,255), # Light Grey Wool/Glass/Stained Clay
  90: (153,153,153,255), # Light Grey Wool/Glass/Stained Clay
  91: (81,81,81,255), # Light Grey Wool/Glass/Stained Clay
  92: (53,89,108,255), # Cyan Wool/Glass/Stained Clay
  93: (65,109,132,255), # Cyan Wool/Glass/Stained Clay
  94: (76,127,153,255), # Cyan Wool/Glass/Stained Clay
  95: (40,67,81,255), # Cyan Wool/Glass/Stained Clay
  96: (89,44,125,255), # Purple Wool/Glass/Stained Clay, Mycelium
  97: (109,54,153,255), # Purple Wool/Glass/Stained Clay, Mycelium
  98: (127,63,178,255), # Purple Wool/Glass/Stained Clay, Mycelium
  99: (67,33,94,255), # Purple Wool/Glass/Stained Clay, Mycelium
  100: (36,53,125,255), # Blue Wool/Glass/Stained Clay
  101: (44,65,153,255), # Blue Wool/Glass/Stained Clay
  102: (51,76,178,255), # Blue Wool/Glass/Stained Clay
  103: (27,40,94,255), # Blue Wool/Glass/Stained Clay
  104: (72,53,36,255), # Brown Wool/Glass/Stained Clay, Soul Sand, Dark Oak Plank
  105: (88,65,44,255), # Brown Wool/Glass/Stained Clay, Soul Sand, Dark Oak Plank
  106: (102,76,51,255), # Brown Wool/Glass/Stained Clay, Soul Sand, Dark Oak Plank
  107: (54,40,27,255), # Brown Wool/Glass/Stained Clay, Soul Sand, Dark Oak Plank
  108: (72,89,36,255), # Green Wool/Glass/Stained Clay, End Portal Frame
  109: (88,109,44,255), # Green Wool/Glass/Stained Clay, End Portal Frame
  110: (102,127,51,255), # Green Wool/Glass/Stained Clay, End Portal Frame
  111: (54,67,27,255), # Green Wool/Glass/Stained Clay, End Portal Frame
  112: (108,36,36,255), # Red Wool/Glass/Stained Clay, Huge Red Mushroom, Brick, Enchanting Table
  113: (132,44,44,255), # Red Wool/Glass/Stained Clay, Huge Red Mushroom, Brick, Enchanting Table
  114: (153,51,51,255), # Red Wool/Glass/Stained Clay, Huge Red Mushroom, Brick, Enchanting Table
  115: (81,27,27,255), # Red Wool/Glass/Stained Clay, Huge Red Mushroom, Brick, Enchanting Table
  116: (17,17,17,255), # Black Wool/Glass/Stained Clay, Dragon Egg, Block of Coal, Obsidian
  117: (21,21,21,255), # Black Wool/Glass/Stained Clay, Dragon Egg, Block of Coal, Obsidian
  118: (25,25,25,255), # Black Wool/Glass/Stained Clay, Dragon Egg, Block of Coal, Obsidian
  119: (13,13,13,255), # Black Wool/Glass/Stained Clay, Dragon Egg, Block of Coal, Obsidian
  120: (176,168,54,255), # Block of Gold, Weighted Pressure Plate (Light)
  121: (215,205,66,255), # Block of Gold, Weighted Pressure Plate (Light)
  122: (250,238,77,255), # Block of Gold, Weighted Pressure Plate (Light)
  123: (132,126,40,255), # Block of Gold, Weighted Pressure Plate (Light)
  124: (64,154,150,255), # Block of Diamond, Prismarine, Prismarine Bricks, Dark Prismarine, Beacon
  125: (79,188,183,255), # Block of Diamond, Prismarine, Prismarine Bricks, Dark Prismarine, Beacon
  126: (92,219,213,255), # Block of Diamond, Prismarine, Prismarine Bricks, Dark Prismarine, Beacon
  127: (48,115,112,255), # Block of Diamond, Prismarine, Prismarine Bricks, Dark Prismarine, Beacon
  128: (52,90,180,255), # Lapis Lazuli Block
  129: (63,110,220,255), # Lapis Lazuli Block
  130: (74,128,255,255), # Lapis Lazuli Block
  131: (39,67,135,255), # Lapis Lazuli Block
  132: (0,153,40,255), # Block of Emerald
  133: (0,187,50,255), # Block of Emerald
  134: (0,217,58,255), # Block of Emerald
  135: (0,114,30,255), # Block of Emerald
  136: (90,59,34,255), # Podzol, Spruce Plank
  137: (110,73,41,255), # Podzol, Spruce Plank
  138: (127,85,48,255), # Podzol, Spruce Plank
  139: (67,44,25,255), # Podzol, Spruce Plank
  140: (79,1,0,255), # Netherrack, Quartz Ore, Nether Wart, Nether Brick Items
  141: (96,1,0,255), # Netherrack, Quartz Ore, Nether Wart, Nether Brick Items
  142: (112,2,0,255), # Netherrack, Quartz Ore, Nether Wart, Nether Brick Items
  143: (59,1,0,255) # Netherrack, Quartz Ore, Nether Wart, Nether Brick Items
}
