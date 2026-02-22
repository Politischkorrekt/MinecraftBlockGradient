from PIL import Image
from pathlib import Path

def visualize_gradient(block_names, folder_path="block"):
    """Stitches block textures together into a single image strip."""
    images = []
    
    # 1. Load all the images from your list of names
    for name in block_names:
        # Reconstruct the file path (e.g., "block\dirt.png")
        img_path = Path(folder_path) / f"{name}.png"
        try:
            # Convert to RGBA to handle transparent blocks like glass/leaves
            img = Image.open(img_path).convert("RGBA")
            images.append(img)
        except FileNotFoundError:
            print(f"Warning: Could not find image for {name}")
            
    if not images:
        return

    # Assuming all blocks are 16x16. 
    block_size = images[0].width
    
    # 2. Create a blank canvas (Width = 16px * number of blocks)
    total_width = block_size * len(images)
    canvas = Image.new('RGBA', (total_width, block_size))
    
    # 3. Paste each image side-by-side onto the canvas
    for index, img in enumerate(images):
        # x_position moves right by 16 pixels each time
        x_position = index * block_size 
        
        # Make sure they are uniform size just in case you have HD textures
        img = img.resize((block_size, block_size), resample=Image.Resampling.NEAREST)
        canvas.paste(img, (x_position, 0))
        
    # 4. Scale the final image up so it isn't microscopic on your monitor
    # We use NEAREST to keep the crisp pixel-art look of Minecraft
    display_scale = 4 
    canvas = canvas.resize((total_width * display_scale, block_size * display_scale), resample=Image.Resampling.NEAREST)
    
    # Opens the image in your computer's default photo viewer
    canvas.show()
    
    # Optional: Save it to your disk
    # canvas.save("my_gradient.png")
