import folium
from folium import plugins
import pandas as pd
import os

output_dir = 'Presentation_Assets'
os.makedirs(output_dir, exist_ok=True)

# 1. Load the dataset (We'll use dataset_part_2.csv which should have LaunchSite coords)
# If coords are not in part_2, we will use spacex_launch_geo.csv directly from Coursera URL
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv"
spacex_df = pd.read_csv(url)

# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]

# 2. Create Map
nasa_coordinate = [28.562302, -80.577356]
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

# 3. Add Launch Sites
for index, row in launch_sites_df.iterrows():
    folium.Circle(
        [row['Lat'], row['Long']],
        radius=1000, color='#d35400', fill=True
    ).add_child(folium.Popup(row['Launch Site'])).add_to(site_map)
    
    folium.Marker(
        [row['Lat'], row['Long']],
        icon=folium.DivIcon(html=f'<div style="font-size: 12; color:#d35400;"><b>{row["Launch Site"]}</b></div>')
    ).add_to(site_map)

# 4. Add Success/Failure Markers (green/red)
marker_cluster = folium.plugins.MarkerCluster()
site_map.add_child(marker_cluster)

def assign_marker_color(launch_outcome):
    if launch_outcome == 1:
        return 'green'
    else:
        return 'red'
    
spacex_df['marker_color'] = spacex_df['class'].apply(assign_marker_color)

for index, row in spacex_df.iterrows():
    folium.Marker(
        location=[row['Lat'], row['Long']],
        icon=folium.Icon(color='white', icon_color=row['marker_color']),
        popup=row['Launch Site']
    ).add_to(marker_cluster)

# Save the map HTML
map_path = os.path.join(output_dir, "map.html")
site_map.save(map_path)
print(f"Map successfully generated and saved to {map_path}")
