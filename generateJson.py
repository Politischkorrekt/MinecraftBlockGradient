from pathlib import Path
import json
from getData import get_average_color

folders = [Path("blocks_highres_top"), Path("blocks_highres_side"), Path("blocks_default_top"), Path("blocks_default_side")]
for folder in folders:
    folder.mkdir(parents=True, exist_ok=True)

    block_dict = {}
    print(f"Scanning images in {folder}...")

    for block in folder.iterdir():
        if block.is_file() and block.suffix in ['.png', '.jpg']:
            avg_rgb = get_average_color(block)
            block_dict.update({block.name.split(".")[0]: avg_rgb})

    with open(f"{folder}.json", 'w') as file:
        json.dump(block_dict, file, indent=2)

    print(f"Successfully created {folder}.json!")