import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

output_dir = 'Presentation_Assets'
os.makedirs(output_dir, exist_ok=True)

fig, ax = plt.subplots(figsize=(10, 12))
fig.patch.set_facecolor('#f4f6f9') # Matching PPT background
ax.set_facecolor('#f4f6f9')
ax.axis('off')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

steps = [
    "1. Request Data from SpaceX API\n(GET https://api.spacexdata.com/v4/launches)",
    "2. Receive JSON Response\n(Raw metadata of all launches)",
    "3. Normalize Data\n(pd.json_normalize to unnest JSON into Columns)",
    "4. Filter Records\n(Keep only 'Falcon 9' rocket launches)",
    "5. Handle Missing/Nested Values\n(API Calls for Core, Payload, Pad Data)",
    "6. Final Cleaned DataFrame\n(Saved as dataset_part_1.csv)"
]

n_steps = len(steps)
box_width = 0.82
box_height = 0.08
x_center = 0.5
padding = 0.025

y_centers = [0.88 - i * (0.76 / (n_steps - 1)) for i in range(n_steps)]

box_color = '#f4f8fe'     # Very light blue/white background
border_color = '#0f62fe'  # IBM/Coursera Template Blue
text_color = '#001d6c'    # Darker blue text for readability
arrow_color = '#0f62fe'   # Matching blue for arrows

for i, (step, y) in enumerate(zip(steps, y_centers)):
    
    # Draw Fancy Box (Uniform sizes)
    box = patches.FancyBboxPatch(
        (x_center - box_width/2, y - box_height/2),
        box_width, box_height,
        boxstyle=f"round,pad={padding}",
        linewidth=3, edgecolor=border_color, facecolor=box_color,
        zorder=3
    )
    ax.add_patch(box)
    
    # Add text
    ax.text(x_center, y, step, ha="center", va="center", 
            fontsize=16, color=text_color, fontweight='bold', zorder=4)
            
    # Add arrow connecting boxes
    if i < n_steps - 1:
        y_next = y_centers[i+1]
        
        arrow_start_y = y - box_height/2 - padding
        arrow_end_y = y_next + box_height/2 + padding
        
        ax.annotate('',
                    xy=(x_center, arrow_end_y),
                    xytext=(x_center, arrow_start_y),
                    arrowprops=dict(arrowstyle="-|>", color=arrow_color, lw=3,
                                    mutation_scale=25, shrinkA=0, shrinkB=0),
                    zorder=1)

plt.title("SpaceX API Data Collection Flowchart", fontsize=28, pad=20, fontweight='bold', color=border_color)
plt.savefig(os.path.join(output_dir, 'Slide_08_API_Flowchart.png'), dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()

print("Flowchart rewritten as an expert and successfully generated!")
