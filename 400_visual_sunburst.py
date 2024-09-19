import matplotlib.pyplot as plt
import numpy as np

def sunburst(nodes, total=np.pi * 2, offset=0, level=0, ax=None, text_rotation=True, color_map=None, path=""):
    ax = ax or plt.subplot(111, projection='polar')

    if level == 0 and len(nodes) == 1:
        label, value, subnodes = nodes[0]
        # Adjust the size of the central circle
        central_circle_size = 0.2  # Decreased from 0.3 to 0.2
        ax.bar([0], [central_circle_size], [np.pi * 2], color='#E0E0E0')
        ax.text(0, 0, label, ha='center', va='center', fontsize=18, fontweight='bold')  # Slightly reduced font size
        sunburst(subnodes, total=value, level=level + 1, ax=ax, color_map=color_map, path=label)
    elif nodes:
        d = np.pi * 2 / total

        # Define width factors for each layer
        width_factors = [0.20, 0.19, 0.18]  # Adjusted to account for smaller central circle

        for i, (label, value, subnodes) in enumerate(nodes):
            if level < len(width_factors):
                inner = sum(width_factors[:level])
                outer = inner + width_factors[level]
            else:
                inner = sum(width_factors[:-1]) + (level - len(width_factors) + 1) * width_factors[-1]
                outer = inner + width_factors[-1]

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

            # Adjust font size based on level
            font_size = 18 - level * 2  # Decrease font size for inner rings
            font_size = max(font_size, 10)  # Ensure font size doesn't go below 10

            ax.text(offset + value * d / 2, (inner + outer) / 2, text,
                    ha='center', va='center', fontsize=font_size,
                    fontweight='bold', rotation=0, rotation_mode='anchor')

            sunburst(subnodes, total=total, offset=offset, level=level + 1, ax=ax, color_map=color_map, path=current_path)
            offset += value * d

    if level == 0:
        ax.set_axis_off()

# Define color mapping, assigning unique colors for each path
color_map = {
    "All Contigs": "#eaeeea",
    "All Contigs-Metagenome": "#dcd0dd",
    "All Contigs-Plasmidome": "#c0cfbd",
    "All Contigs-Metagenome-Defense": "#a775a4",
    "All Contigs-Metagenome-None": "#c6a4c5",
    "All Contigs-Plasmidome-Defense": "#7b9b64",
    "All Contigs-Plasmidome-None": "#9bb88a"
}

# Data structure
data = [("All Contigs", 287424, [
    ("Metagenome", 206581, [
        ("Defense", 12313, []),
        ("None", 194268, [])
    ]),
    ("Plasmidome", 80843, [
        ("Defense", 2569, []),
        ("None", 78274, [])
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
