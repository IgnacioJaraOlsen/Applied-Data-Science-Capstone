import pandas as pd
import plotly.express as px
import os

output_dir = 'Presentation_Assets'

print("Loading dash data...")
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Slide 39: Pie chart for all sites
print("Generating Pie Chart All Sites...")
fig_pie_all = px.pie(spacex_df, values='class', 
                     names='Launch Site', 
                     title='Total Success Launches By Site')
fig_pie_all.write_image(os.path.join(output_dir, 'Slide_39_Dash_Pie_All.png'), scale=2)

# Slide 40: Pie chart for one site (KSC LC-39A)
print("Generating Pie Chart Specific Site...")
site_data = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
site_counts = site_data['class'].value_counts().reset_index()
site_counts.columns = ['class', 'count']
fig_pie_site = px.pie(site_counts, values='count', 
                     names='class', 
                     title='Total Success Launches for site KSC LC-39A')
fig_pie_site.write_image(os.path.join(output_dir, 'Slide_40_Dash_Pie_Site.png'), scale=2)

# Slide 41: Scatter plot
print("Generating Scatter Plot...")
fig_scatter = px.scatter(spacex_df, x="Payload Mass (kg)", y="class", 
                         color="Booster Version Category",
                         title="Correlation between Payload and Success for all Sites")
fig_scatter.write_image(os.path.join(output_dir, 'Slide_41_Dash_Scatter.png'), scale=2)

print("Dash charts generated successfully.")
