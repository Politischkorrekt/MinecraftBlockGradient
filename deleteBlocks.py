import json
import os
from pathlib import Path


with open("blocks_default_top.json", "r") as file:
    blocks = json.load(file)
exclude = []
for block in blocks:
    blockname = Path('blocks_highres_top').joinpath(block + ".png") 
    exclude.append(str(blockname))

print(exclude)
folder = Path("blocks_highres_top")
for block in folder.iterdir():
    if str(block) in exclude: # only name not path
        print("not "+ str(block))
    else:
        os.remove(block)
        print(block)