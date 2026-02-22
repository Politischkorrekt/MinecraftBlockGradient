import numpy as np
import colorsys
import math
from pathlib import Path
from PIL import Image

# ... [Keep your get_average_color function exactly as it is] ...

def rgb_to_hsv(rgb):
    """Converts RGB (0-255) to HSV (0.0-1.0)"""
    return colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)

def hsv_to_rgb(hsv):
    """Converts HSV (0.0-1.0) back to RGB (0-255)"""
    r, g, b = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
    return np.array([r*255, g*255, b*255])

def get_ideal_color(rgb1, rgb2, fraction):
    """Finds the perfect midpoint color using the HSV color wheel"""
    h1, s1, v1 = rgb_to_hsv(rgb1)
    h2, s2, v2 = rgb_to_hsv(rgb2)

    # Calculate shortest path around the circular hue wheel
    dh = h2 - h1
    if dh > 0.5:
        dh -= 1.0
    elif dh < -0.5:
        dh += 1.0

    # Lerp the values
    h_ideal = (h1 + dh * fraction) % 1.0
    s_ideal = s1 + (s2 - s1) * fraction
    v_ideal = v1 + (v2 - v1) * fraction

    return hsv_to_rgb((h_ideal, s_ideal, v_ideal))

def perceptual_distance(rgb1, rgb2):
    """
    Calculates distance based on human eye perception (Redmean formula).
    Prevents the algorithm from mistaking dark greens for browns.
    """
    rmean = (rgb1[0] + rgb2[0]) / 2
    r_diff = rgb1[0] - rgb2[0]
    g_diff = rgb1[1] - rgb2[1]
    b_diff = rgb1[2] - rgb2[2]
    
    # The human eye is more sensitive to Green, and Red/Blue sensitivity changes based on brightness
    weight_r = 2 + rmean / 256
    weight_g = 4.0
    weight_b = 2 + (255 - rmean) / 256
    
    return math.sqrt(weight_r * r_diff**2 + weight_g * g_diff**2 + weight_b * b_diff**2)

def find_blocks_hsv(first, last, steps, block_dict):
    """
    Generates a smooth gradient using HSV interpolation and perceptual block matching.
    """
    orig_first_arr = np.array(block_dict[first])
    orig_last_arr = np.array(block_dict[last])
    
    block_selection = [first]
    used_blocks = {first, last} 
    
    for step in range(1, steps + 1):
        fraction = step / (steps + 1)
        
        # 1. Get the vibrant, mathematically perfect color on the color wheel
        ideal_color = get_ideal_color(orig_first_arr, orig_last_arr, fraction)
        
        best_distance = float('inf') 
        best_block = ""
        
        # 2. Find the Minecraft block that visually looks the closest to it
        for current_block, color in block_dict.items():
            if current_block in used_blocks:
                continue
                
            current_arr = np.array(color)
            
            # Use Human Vision distance instead of flat 3D math
            distance = perceptual_distance(current_arr, ideal_color)
            
            if distance < best_distance:
                best_distance = distance
                best_block = current_block   
                
        if best_block: 
            block_selection.append(best_block)
            used_blocks.add(best_block)

    block_selection.append(last) 
    return block_selection


def find_closest_blocks(target_color, block_dict, n=5):
    """
    Finds the top 'n' closest blocks to a target color.
    Returns a list of block names.
    """
    target_arr = np.array(target_color) 
    
    # We will store tuples of (distance, block_name) here
    all_distances = []
    
    for current_block, block_color in block_dict.items():
        current_arr = np.array(block_color)
        
        # Calculate distance
        distance = perceptual_distance(current_arr, target_arr)
        
        # Add it to our list
        all_distances.append((distance, current_block))
        
    # Sort the list. Python automatically sorts tuples by their first item (distance),
    # so the lowest distances (closest colors) will move to the front of the list.
    all_distances.sort()
    
    # Slice the list to get only the top 'n' results
    top_n_tuples = all_distances[:n]
    
    # Extract just the block names from those tuples
    best_blocks = [block_name for dist, block_name in top_n_tuples]

    return best_blocks