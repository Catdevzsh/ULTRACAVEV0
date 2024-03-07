from ursina import *
from random import randint
from noise import pnoise2

# Define block types
BLOCK_TYPES = {
    "grass": color.green,
    "dirt": color.brown,
    "stone": color.gray,
    "wood": color.brown4,
    "leaves": color.green4,
    "water": color.blue,  # Added water block type
}

# Crafting recipes
CRAFTING_RECIPES = {
    "wood": {"grass": 4},
}

# Create a block class
class Block(Entity):
    def __init__(self, block_type, position):
        super().__init__(
            parent=scene,
            model="cube",
            color=BLOCK_TYPES[block_type],
            position=position,
        )

# Perlin noise-based world generation
def generate_world(width, height):
    # Initialize the world with Perlin noise
    noise_map = [[pnoise2(x / 10, y / 10) for x in range(width)] for y in range(height)]

    # Convert noise map to blocks
    for x in range(width):
        for y in range(height):
            if noise_map[y][x] < 0:
                block_type = "water"
            else:
                if y < height - 5:
                    block_type = "dirt"
                else:
                    block_type = "grass"
            Block(block_type, (x, y))

# Main game loop
if __name__ == "__main__":
    app = Ursina()
    window.title = "ULTRACAVE"

    # Generate a world using Perlin noise
    generate_world(40, 20)

    # Create player
    player = Entity(model="cube", color=color.orange, position=(5, 8))

    # Camera settings
    camera.orthographic = True
    camera.fov = 20

    # Inventory
    inventory = {}

    # Player movement and interaction
    def update():
        player.x += held_keys["d"] * 0.1
        player.x -= held_keys["a"] * 0.1

        # Check for block interaction
        block_hit = raycast(player.position, direction=(0, -1), distance=2)
        if block_hit.hit:
            block = block_hit.entity
            if mouse.left:
                # Break block
                block_type = block.color.name
                if block_type not in inventory:
                    inventory[block_type] = 0
                inventory[block_type] += 1
                destroy(block)
            elif mouse.right:
                # Place block
                for recipe, ingredients in CRAFTING_RECIPES.items():
                    if all(item in inventory and inventory[item] >= count for item, count in ingredients.items()):
                        # Craft the item
                        for item, count in ingredients.items():
                            inventory[item] -= count
                        new_block = Block(recipe, block.position + (0, 1))
                        break

    # Run the game
    app.run()
