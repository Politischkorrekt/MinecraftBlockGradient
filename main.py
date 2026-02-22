from pyscript import document, window
from pyodide.ffi import create_proxy
import json
import numpy as np
from PIL import ImageColor
from hue import find_closest_blocks, find_blocks_hsv

current_folder = document.getElementById("folderSelect").value
with open(current_folder+".json", "r") as f:
    block_dict = json.load(f)

selected_blocks = []
excluded_blocks = []

def change_folder(event):
    """Triggered when the dropdown menu is changed."""
    global current_folder
    current_folder = event.target.value 
    global block_dict
    with open(current_folder+".json", "r") as f:
        block_dict = json.load(f)

    show_all_blocks() 
    
    container = document.querySelector("#gradient-result-container")
    container.innerHTML = '<span class="text-muted">Folder changed. Please generate a new gradient.</span>'


def change_click_mode(event):
    global click_mode
    click_mode = event.target.value

def clear_exclusions(event):
    global excluded_blocks
    excluded_blocks = []
    update_selection_ui()

def handle_exclude_click(event):
    global excluded_blocks
    block_name = event.target.title
    if block_name in excluded_blocks:
        excluded_blocks.remove(block_name)
        update_selection_ui()

exclude_proxy = create_proxy(handle_exclude_click)

def update_selection_ui():
    container = document.querySelector("#blocks-container")
    
    # 1. Reset everything to normal
    for i in range(container.children.length):
        img = container.children.item(i)
        if img.tagName == "IMG":
            img.style.borderColor = "transparent"
            img.style.borderWidth = "2px"
            img.style.opacity = "1.0"

    # 2. Highlight Excluded Blocks (Red & Faded)
    for ex_block in excluded_blocks:
        el = document.getElementById(ex_block)
        if el:
            el.style.borderColor = "#dc3545" 
            el.style.borderWidth = "4px"
            el.style.opacity = "0.3"

    # 3. Handle Selection 1 (Green)
    sel1_div = document.querySelector("#selection-1")
    sel1_div.innerHTML = "" 
    if len(selected_blocks) >= 1:
        img1 = document.createElement("img")
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
            el1.style.opacity = "1.0"
    else:
        sel1_div.innerHTML = '<span class="text-muted small">None</span>'

    # 4. Handle Selection 2 (Blue)
    sel2_div = document.querySelector("#selection-2")
    sel2_div.innerHTML = "" 
    if len(selected_blocks) == 2:
        img2 = document.createElement("img")
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
            el2.style.opacity = "1.0"
    else:
        sel2_div.innerHTML = '<span class="text-muted small">None</span>'

    # 5. Populate Excluded Bin UI
    ex_container = document.querySelector("#excluded-container")
    ex_container.innerHTML = ""
    if len(excluded_blocks) == 0:
        ex_container.innerHTML = '<span class="text-muted small align-self-center">No blocks excluded.</span>'
    else:
        for ex_block in excluded_blocks:
            img = document.createElement("img")
            img.src = f"{current_folder}/{ex_block}.png"
            img.style.width = "32px" # Make them cute and small
            img.style.height = "32px"
            img.style.borderRadius = "4px"
            img.title = ex_block
            img.style.cursor = "pointer"
            
            # Clicking them in the bin removes the exclusion!
            img.addEventListener("click", exclude_proxy)
            ex_container.appendChild(img)

def handle_image_click(event):
    global selected_blocks, excluded_blocks
    clicked_block_name = event.target.id
    
    if click_mode == "select":
        # Block selecting an excluded block
        if clicked_block_name in excluded_blocks:
            return 
            
        if clicked_block_name in selected_blocks:
            selected_blocks.remove(clicked_block_name)
        else:
            if len(selected_blocks) >= 2:
                selected_blocks.pop(0) 
            selected_blocks.append(clicked_block_name)
            
    elif click_mode == "exclude":
        if clicked_block_name in excluded_blocks:
            excluded_blocks.remove(clicked_block_name)
        else:
            # If a block that is currently selected is excluded, remove it from the selection!
            if clicked_block_name in selected_blocks:
                selected_blocks.remove(clicked_block_name)
            excluded_blocks.append(clicked_block_name)
    
    update_selection_ui()

click_proxy = create_proxy(handle_image_click)

def render_grid(block_names):
    container = document.querySelector("#blocks-container")
    container.innerHTML = "" 
    
    for block_name in block_names:
        img = document.createElement("img")
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
    
    filtered_dict = {k: v for k, v in block_dict.items() if k not in excluded_blocks}
    
    # Pass the filtered dictionary to to the gradiant generator
    gradient_blocks = find_blocks_hsv(first, last, steps, filtered_dict)
    
    container = document.querySelector("#gradient-result-container")
    container.innerHTML = "" 
    
    for block_name in gradient_blocks:
        img = document.createElement("img")
        img.src = f"{current_folder}/{block_name}.png"
        img.className = "block-result m-0 p-0" 
        img.title = block_name
        container.appendChild(img)

show_all_blocks()
