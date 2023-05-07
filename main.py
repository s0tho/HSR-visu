from itertools import combinations
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import numpy as np
import json
import pandas as pd

ELEMENTS = ["Fire", "Ice", "Lightning", "Wind", "Physical", "Imaginary", "Quantum"]


def get_mobs(mob_file, zones_file, mob_type, planets):
    mobs = {}
    zones = []

    with open(zones_file, "r") as f:
        tmp_zones = json.load(f)

    for planet in planets:
        zones.extend(tmp_zones[planet])
    
    with open(mob_file, "r") as f:
        tmp_mobs = json.load(f)

    for mob in tmp_mobs.keys():
        if any(item in tmp_mobs[mob]["Type"] for item in mob_type) and any(item in tmp_mobs[mob]["Zones"] for item in zones):
            mobs[mob] = tmp_mobs[mob]["Weaknesses"]

    return mobs


def describe(mobs, mob_type, planet):
    print('======================================')
    print(f"{planet:20} --- {mob_type} mobs\n")
    print(f"Number of mobs: {len(mobs)}")
    count = sum(1 for mob in mobs if len(mobs[mob]) == 2)
    print(f"Number of mobs with 2 weaknesses:{count}")
    count = sum(1 for mob in mobs if len(mobs[mob]) == 3)
    print(f"Number of mobs with 3 weaknesses:{count}")
    print("\n")


def overlap_images(img1_path, img2_path, offset=(50, 150), new_width=600):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    img1_w, img1_h = img1.size
    img2_w, img2_h = img2.size
    # resize asset
    new_height = int(new_width * img2_h / img2_w)
    img2 = img2.resize((new_width, new_height))

    img2_w, img2_h = img2.size
    new_img = Image.new('RGBA', (img1_w, img1_h), (255, 255, 255, 255))
    new_img.paste(img1, (0, 0))
    x_offset, y_offset = offset # pixels from the right and bottom edge
    new_img.paste(img2, (img1_w - img2_w - x_offset, img1_h - img2_h - y_offset), mask=img2)
    new_img.save(img1_path)


def plot_count_mobs_per_weaknesses_combination(mobs, mob_type, planet, min_weaknesses, max_weaknesses):
    weaknesses = ELEMENTS
    results = []

    for i in range(min_weaknesses, min(len(weaknesses), max_weaknesses) + 1):
        for weakness_combination in combinations(weaknesses, i):
            count = 0
            for mob_weaknesses in mobs.values():
                if any(weakness in mob_weaknesses for weakness in weakness_combination):
                    count += 1
            results.append((weakness_combination, count))

    results.sort(key=lambda x: x[1])

    weaknesses = [result[0] for result in results]
    counts = [result[1] for result in results]

    # configuration
    plt.style.use('style.mplstyle')
    palette = sns.dark_palette('Blue', n_colors=len(counts))
    fig, ax = plt.subplots(figsize=(12, 8))
    for i in range(len(weaknesses)):
        ax.barh(i, counts[i], color=palette[i])

    # Add images on axis
    for i, weakness_list in enumerate(weaknesses):
        x = 0
        for weakness in weakness_list:
            image = "assets/"+ weakness + ".webp"
            img = Image.open(image)
            img = img.resize((26, 26))
            im = OffsetImage(img, zoom=0.5)
            ab = AnnotationBbox(im, (-1-x, i), xycoords='data', frameon=False)
            ax.add_artist(ab)
            size = img.size
            x += size[0] * 0.04

    # Remove labels
    plt.yticks(range(len(weaknesses)), ['' for weakness in weaknesses])
    plt.xlabel('Number of mobs')
    plt.ylabel('Weakness')
    plt.xlim(-4, 60)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.xticks(np.arange(0, max(counts)+2, 2))
    plt.title(f'How many ({mob_type}) mobs from {planet} have at least one weakness from this weaknesses combination?')
    fig_path = f"charts/mobs_per_weakness_{max_weaknesses}-{mob_type}_from_{planet}.png"
    plt.savefig(fig_path, dpi=200)
    plt.close()
    
    # Overlap planet's logo on bottom right
    width=400
    overlap_images(fig_path, f"assets/{planet}.webp", (25, 150), new_width=width)


def plot_weaknesses_overlap(data, mob_type, planet):
    weaknesses = ELEMENTS
    df = pd.DataFrame(0, index=weaknesses, columns=weaknesses)

    for mob, mob_weaknesses in data.items():
        for i in range(len(mob_weaknesses)):
            for j in range(len(mob_weaknesses)):
                df.loc[mob_weaknesses[i], mob_weaknesses[j]] += 1

    # configuration
    plt.style.use('style.mplstyle')
    fig, ax = plt.subplots(figsize=(12, 8))
    palette = sns.dark_palette('Blue')
    sns.heatmap(df, cmap=palette, annot=True, cbar=False)
    plt.subplots_adjust(right=0.85, bottom=.1)

    # Add images on axis
    for i, weakness in enumerate(weaknesses):
            image = "assets/"+ weakness + ".webp"
            img = Image.open(image)
            img = img.resize((48, 48))
            im = OffsetImage(img, zoom=0.5)
            ab = AnnotationBbox(im, (0, i+.5), xycoords='data', frameon=False)
            ax.add_artist(ab)
            ab = AnnotationBbox(im, (i+.5, 0), xycoords='data', frameon=False)
            ax.add_artist(ab)
    
    # Remove labels
    plt.yticks(range(len(weaknesses)), ['' for weakness in weaknesses])
    plt.xticks(range(len(weaknesses)), ['' for weakness in weaknesses])

    fig_path = f"charts/weaknesses_overlap-{mob_type}_from_{planet}.png"

    plt.title(f'How many ({mob_type}) mobs from {planet} have these two weaknesses?', y=1.05)
    plt.savefig(fig_path, dpi=200)
    plt.close()

    # Overlap planet's logo on bottom right
    width=400
    overlap_images(fig_path, f"assets/{planet}.webp", (25, 25), new_width=width)

planet_modes = {
    "every planets": ["Herta Space Station", "Jarilo-VI", "The Xianzhou Luofu", "Simulated Universe"],
    "Herta Space Station": ["Herta Space Station"],
    "Jarilo-VI": ["Jarilo-VI"], 
    "The Xianzhou Luofu": ["The Xianzhou Luofu"]
}

mob_type_modes = {
    "all": ["Normal","Elite","Boss", "Boss' Invocation"],
    "normal": ["Normal"],
    "elite": ["Elite","Boss", "Boss' Invocation"]
}

if __name__ == "__main__":
    for mob_type_mode in mob_type_modes.keys():
        for planet_mode in planet_modes.keys():
            mobs = get_mobs("mobs.json", "zones.json", mob_type_modes[mob_type_mode], planet_modes[planet_mode])
            for quantity in range(2,4):
                weaknesses_quantity = quantity
                plot_count_mobs_per_weaknesses_combination(mobs, mob_type_mode, planet_mode, weaknesses_quantity, weaknesses_quantity)
            plot_weaknesses_overlap(mobs, mob_type_mode, planet_mode)
            describe(mobs, mob_type_mode, planet_mode)