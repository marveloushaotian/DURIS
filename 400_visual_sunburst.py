import matplotlib.pyplot as plt
import numpy as np

def sunburst(nodes, total=np.pi * 2, offset=0, level=0, ax=None, text_rotation=True, color_map=None, path=""):
    ax = ax or plt.subplot(111, projection='polar')

    if level == 0 and len(nodes) == 1:
        label, value, subnodes = nodes[0]
        ax.bar([0], [0.5], [np.pi * 2], color='#E0E0E0')
        ax.text(0, 0, label, ha='center', va='center', fontsize=14, fontweight='bold')
        sunburst(subnodes, total=value, level=level + 1, ax=ax, color_map=color_map, path=label)
    elif nodes:
        d = np.pi * 2 / total

        # Define width factors for each layer
        width_factors = [1/4, 1/2, 1/2, 1/2]

        for i, (label, value, subnodes) in enumerate(nodes):
            if level < len(width_factors):
                inner = sum(width_factors[:level])
                outer = inner + width_factors[level]
            else:
                inner = level * width_factors[-1]
                outer = (level + 1) * width_factors[-1]

            # Generate a unique key for the color map using the path
            current_path = f"{path}-{label}" if path else label
            color = color_map.get(current_path, "#d6ecc1") if color_map else "#d6ecc1"
            angle = (offset + value * d / 2) * 180 / np.pi
            rotation = angle if text_rotation else 0

            ax.bar([offset + value * d / 2], [outer - inner], [value * d],
                   bottom=[inner], color=color, edgecolor='w', lw=0)

            # Calculate and format percentage
            percentage = (value / total) * 100
            text = f"{label}\n{percentage:.2f}%"

            ax.text(offset + value * d / 2, (inner + outer) / 2, text,
                    ha='center', va='center', fontsize=18,
                    fontweight='bold', rotation=0, rotation_mode='anchor')

            sunburst(subnodes, total=total, offset=offset, level=level + 1, ax=ax, color_map=color_map, path=current_path)
            offset += value * d

    if level == 0:
        ax.set_axis_off()

# Define color mapping, assigning unique colors for each path
color_map = {
    "All Contigs": "#ffffff",
    "All Contigs-Metagenome": "#e3dce4",
    "All Contigs-Plasmidome": "#e1f0d6",
    "All Contigs-Metagenome-Circular": "#dcd0dd",
    "All Contigs-Metagenome-Linear P": "#ceb7ce",
    "All Contigs-Metagenome-Linear G": "#be9bbc",
    "All Contigs-Metagenome-Circular-Defense": "#a673a3",
    "All Contigs-Metagenome-Circular-None": "#af82ac",
    "All Contigs-Metagenome-Linear P-Defense": "#a673a3",
    "All Contigs-Metagenome-Linear P-None": "#af82ac",
    "All Contigs-Metagenome-Linear G-Defense": "#a673a3",
    "All Contigs-Metagenome-Linear G-None": "#af82ac",
    "All Contigs-Plasmidome-Circular": "#d1eab6",
    "All Contigs-Plasmidome-Linear P": "#bfe292",
    "All Contigs-Plasmidome-Linear G": "#a6d579",
    "All Contigs-Plasmidome-Circular-Defense": "#7cbd85",
    "All Contigs-Plasmidome-Circular-None": "#92ca77",
    "All Contigs-Plasmidome-Linear P-Defense": "#7cbd85",
    "All Contigs-Plasmidome-Linear P-None": "#92ca77",
    "All Contigs-Plasmidome-Linear G-Defense": "#7cbd85",
    "All Contigs-Plasmidome-Linear G-None": "#92ca77"
}

# Data structure
data = [("All Contigs", 287424, [
    ("Metagenome", 206581, [
        ("Circular", 3361, [
            ("Defense", 311, []),
            ("None", 3050, [])
        ]),
        ("Linear P", 89568, [
            ("Defense", 3040, []),
            ("None", 86528, [])
        ]),
        ("Linear G", 113652, [
            ("Defense", 8962, []),
            ("None", 104690, [])
        ])
    ]),
    ("Plasmidome", 80843, [
        ("Circular", 6395, [
            ("Defense", 338, []),
            ("None", 6057, [])
        ]),
        ("Linear P", 47153, [
            ("Defense", 1234, []),
            ("None", 45919, [])
        ]),
        ("Linear G", 27315, [
            ("Defense", 997, []),
            ("None", 26318, [])
        ])
    ])
])]

# Create the chart
plt.figure(figsize=(12, 12))
sunburst(data, color_map=color_map)
plt.tight_layout()

# Save the chart as a PDF file
plt.savefig('sunburst_chart_defense.pdf', dpi=300, bbox_inches='tight')
print("Sunburst chart has been saved as sunburst_chart_defense.pdf")

# Display the chart (for debugging)
plt.show()
