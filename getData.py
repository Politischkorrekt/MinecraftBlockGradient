from PIL import Image
def get_average_color(image_path):
    with Image.open(image_path) as img:
        # Resize image to 1x1 pixel using a high-quality resampling filter
        # This effectively averages all pixels
        img = img.convert("RGB")
        img_1pixel = img.resize((1, 1), resample=Image.Resampling.BOX)
        
        # Get the color of that single pixel
        color = img_1pixel.getpixel((0, 0))
        
        # If the image is RGBA (transparent), ignore alpha
        return color[:3] 