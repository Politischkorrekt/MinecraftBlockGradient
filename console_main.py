from pathlib import Path
from PIL import ImageColor
import json
import math
import numpy as np
from getData import get_average_color
from vis_grad import visualize_gradient
from hue import find_blocks_hsv, find_closest_blocks


folder = Path("blocks_highres")
folder.mkdir(parents=True, exist_ok=True)
block_dict = {}
for block in folder.iterdir():
    avg_rgb = get_average_color(block)
    block_dict.update({block.name.split(".")[0]: avg_rgb})
with open("average_colors.json", 'w') as file:
    json.dump(block_dict, file, indent=2)

print("Enter Color to match: rgb(R, G, B)")
color_string = input()
print(color_string)
rgb = np.array(ImageColor.getrgb(color_string)[:3])
print(rgb)
found_blocks = []
found_blocks = find_closest_blocks(rgb, block_dict, 5)
visualize_gradient(found_blocks, "blocks_highres")

#print("Enter First Blockname: ")
#first = input()
#print("Enter last Blockname: ")
#last = input()
#print("Enter how many steps you want to take: ")
#steps = int(input())
#gradient = find_blocks_hsv(first, last, steps, block_dict)
#visualize_gradient(gradient, "blocks_highres")
#
#TODO add top and side mode