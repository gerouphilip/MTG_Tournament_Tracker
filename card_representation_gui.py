import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

DATA_DIR = "data"

def load_card_data(format_name):
    file_path = os.path.join(DATA_DIR, format_name, f"cardcount_{format_name}.json")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Card count file not found for format '{format_name}'")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_card_details(format_name):
    file_path = os.path.join(DATA_DIR, format_name, f"processed_{format_name}.json")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Processed data file not found for format '{format_name}'")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_and_display():
    format_name = format_var.get()
    card_name = card_entry.get().strip()

    if not format_name or not card_name:
        messagebox.showerror("Input Error", "Please select a format and enter a card name.")
        return

    try:
        card_counts = load_card_data(format_name)
        processed_data = load_card_details(format_name)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    total_count = sum(card_counts.values())
    count = card_counts.get(card_name, 0)

    if count == 0:
        messagebox.showinfo("Not Found", f"'{card_name}' not found in {format_name}.")
        result_var.set("")
        card_image_label.config(image="", text="No image")
        return

    percent = (count / total_count) * 100
    result_text = (
        f"Card: {card_name}\n"
        f"Format: {format_name}\n"
        f"Count: {count}\n"
        f"Total Cards: {total_count}\n"
        f"Representation: {percent:.2f}%"
    )
    result_var.set(result_text)

    # Find image_uris in processed data (case-insensitive match)
    image_url = None
    for card_key, card in processed_data.items():
        if isinstance(card, dict) and "name" in card:
            if card["name"].lower() == card_name.lower():
                image_data = card.get("image_uris")
                if isinstance(image_data, str):
                    image_url = image_data
                elif isinstance(image_data, dict):
                    image_url = image_data.get("normal")
                break

    if image_url:
        try:
            response = requests.get(image_url)
            img_data = BytesIO(response.content)
            img = Image.open(img_data).resize((223, 310))  # resize for display
            photo = ImageTk.PhotoImage(img)
            card_image_label.image = photo
            card_image_label.config(image=photo)
        except Exception as e:
            card_image_label.config(text="Image load error", image="")
            print("Image error:", e)
    else:
        card_image_label.config(text="No image found", image="")



# GUI Setup
root = tk.Tk()
root.title("MTG Card Representation Checker")
root.geometry("500x600")

# Format selector
ttk.Label(root, text="Select Format:").pack(pady=5)
format_var = tk.StringVar()
format_box = ttk.Combobox(root, textvariable=format_var)
format_box['values'] = sorted(os.listdir(DATA_DIR))
format_box.pack(pady=5)

# Card name entry
ttk.Label(root, text="Enter Card Name:").pack(pady=5)
card_entry = ttk.Entry(root, width=40)
card_entry.pack(pady=5)

# Submit button
ttk.Button(root, text="Check Representation", command=calculate_and_display).pack(pady=10)

# Result text
result_var = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_var, justify="left")
result_label.pack(pady=10)

# Card image
card_image_label = tk.Label(root, text="Card image will appear here")
card_image_label.pack(pady=10)

root.mainloop()
