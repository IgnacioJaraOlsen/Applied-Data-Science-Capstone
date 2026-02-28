import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

output_dir = 'Presentation_Assets'
os.makedirs(output_dir, exist_ok=True)

sns.set_context("poster")
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 20
plt.rcParams['axes.titlesize'] = 26
plt.rcParams['axes.labelsize'] = 22
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18

print("Loading data...")
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")

def save_catplot(y_col, x_col, title, x_label, y_label, filename):
    g = sns.catplot(y=y_col, x=x_col, hue="Class", data=df, aspect=1.75, height=8, s=35, jitter=0.4)
    plt.title(title, pad=20)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    # Draw horizontal dividers between categories
    plt.grid(False) # Turn off default grid
    num_categories = df[y_col].nunique()
    for i in range(num_categories - 1):
        plt.axhline(y=i + 0.5, color='gray', linestyle='-', linewidth=1.5, alpha=0.5)
    
    # Customize legend
    if g._legend:
        g._legend.remove()
    
    # Re-create a better legend
    handles, _ = plt.gca().get_legend_handles_labels()
    # catplot might create lines or collections. We just use them if available.
    if handles:
        plt.legend(handles=handles, labels=['Failure', 'Success'], title='Outcome', loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        # Fallback
        plt.legend(title='Outcome', labels=['Failure', 'Success'], loc='center left', bbox_to_anchor=(1, 0.5))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, filename), dpi=300)
    plt.close('all')

print("Generating catplots...")

# Slide 18: Scatter: Flight Number vs. Launch Site
save_catplot("LaunchSite", "FlightNumber", "Flight Number vs. Launch Site", "Flight Number", "Launch Site", 'Slide_18_Flight_vs_Site.png')

# Slide 19: Scatter: Payload vs. Launch Site
save_catplot("LaunchSite", "PayloadMass", "Payload Mass vs. Launch Site", "Payload Mass (kg)", "Launch Site", 'Slide_19_Payload_vs_Site.png')

# Slide 21: Scatter: Flight Number vs. Orbit Type
save_catplot("Orbit", "FlightNumber", "Flight Number vs. Orbit Type", "Flight Number", "Orbit Type", 'Slide_21_Flight_vs_Orbit.png')

# Slide 22: Scatter: Payload vs. Orbit Type
save_catplot("Orbit", "PayloadMass", "Payload Mass vs. Orbit Type", "Payload Mass (kg)", "Orbit Type", 'Slide_22_Payload_vs_Orbit.png')

print("Catplots generated successfully!")
