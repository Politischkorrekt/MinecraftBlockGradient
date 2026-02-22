from pyscript import document, window
from pyodide.ffi import create_proxy
import json
import numpy as np
from PIL import ImageColor
from hue import find_closest_blocks, find_blocks_hsv

# 1. Load dictionary (Assuming both folders have the same blocks and colors)

current_folder = document.getElementById("folderSelect").value
with open(current_folder+".json", "r") as f:
    block_dict = json.load(f)

selected_blocks = []

def change_folder(event):
    """Triggered when the dropdown menu is changed."""
    global current_folder
    # Update the global variable to whatever the dropdown is set to
    current_folder = event.target.value 
    global block_dict
    with open(current_folder+".json", "r") as f:
        block_dict = json.load(f)

    # Re-render the grid to load the new images
    show_all_blocks() 
    
    # Clear the generated gradient so it doesn't show the old folder's images
    container = document.querySelector("#gradient-result-container")
    container.innerHTML = '<span class="text-muted">Folder changed. Please generate a new gradient.</span>'


def update_selection_ui():
    """Safely updates the images and borders."""
    container = document.querySelector("#blocks-container")
    for i in range(container.children.length):
        img = container.children.item(i)
        if img.tagName == "IMG":
            img.style.borderColor = "transparent"
            img.style.borderWidth = "2px"

    sel1_div = document.querySelector("#selection-1")
    sel1_div.innerHTML = "" 
    
    if len(selected_blocks) >= 1:
        img1 = document.createElement("img")
        # <-- UPDATED: Use the variable instead of hardcoded folder
        img1.src = f"{current_folder}/{selected_blocks[0]}.png" 
        img1.style.width = "64px"
        img1.style.height = "64px"
        img1.style.borderRadius = "4px"
        img1.title = selected_blocks[0]
        sel1_div.appendChild(img1)
        
        el1 = document.getElementById(selected_blocks[0])
        if el1: 
            el1.style.borderColor = "#198754" 
            el1.style.borderWidth = "4px"
    else:
        sel1_div.innerHTML = '<span class="text-muted small">None</span>'

    sel2_div = document.querySelector("#selection-2")
    sel2_div.innerHTML = "" 
    
    if len(selected_blocks) == 2:
        img2 = document.createElement("img")
        # <-- UPDATED
        img2.src = f"{current_folder}/{selected_blocks[1]}.png"
        img2.style.width = "64px"
        img2.style.height = "64px"
        img2.style.borderRadius = "4px"
        img2.title = selected_blocks[1]
        sel2_div.appendChild(img2)
        
        el2 = document.getElementById(selected_blocks[1])
        if el2:
            el2.style.borderColor = "#0d6efd" 
            el2.style.borderWidth = "4px"
    else:
        sel2_div.innerHTML = '<span class="text-muted small">None</span>'

def handle_image_click(event):
    global selected_blocks
    clicked_block_name = event.target.id
    
    if clicked_block_name in selected_blocks:
        selected_blocks.remove(clicked_block_name)
    else:
        if len(selected_blocks) >= 2:
            selected_blocks.pop(0) 
        selected_blocks.append(clicked_block_name)
    
    update_selection_ui()

click_proxy = create_proxy(handle_image_click)

def render_grid(block_names):
    container = document.querySelector("#blocks-container")
    container.innerHTML = "" 
    
    for block_name in block_names:
        img = document.createElement("img")
        # <-- UPDATED
        img.src = f"{current_folder}/{block_name}.png"
        img.className = "block-img rounded shadow-sm"
        img.id = block_name 
        img.title = block_name 
        
        img.addEventListener("click", click_proxy)
        container.appendChild(img)
        
    update_selection_ui()

def search_colors(event):
    hex_color = document.querySelector("#colorPicker").value
    rgb = np.array(ImageColor.getrgb(hex_color)[:3])
    found_block_names = find_closest_blocks(rgb, block_dict, 15)
    render_grid(found_block_names)

def show_all_blocks(event=None):
    all_block_names = sorted(list(block_dict.keys()))
    render_grid(all_block_names)

def generate_gradient(event):
    if len(selected_blocks) < 2:
        window.alert("Please select exactly two blocks from the library first!")
        return
        
    first = selected_blocks[0]
    last = selected_blocks[1]
    steps = int(document.querySelector("#stepCount").value)
    
    gradient_blocks = find_blocks_hsv(first, last, steps, block_dict)
    
    container = document.querySelector("#gradient-result-container")
    container.innerHTML = "" 
    
    for block_name in gradient_blocks:
        img = document.createElement("img")
        # <-- UPDATED
        img.src = f"{current_folder}/{block_name}.png"
        img.className = "block-result m-0 p-0" 
        img.title = block_name
        container.appendChild(img)

# Initialize the grid
show_all_blocks()