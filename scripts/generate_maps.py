import folium
import pandas as pd
from folium.plugins import MarkerCluster
import os
import time
from playwright.sync_api import sync_playwright

# Ensure output directory exists
out_dir = "Presentation_Assets"
os.makedirs(out_dir, exist_ok=True)

# Load data
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv")

def save_map_screenshot(m, filename):
    html_file = os.path.abspath(os.path.join(out_dir, "temp_map.html"))
    m.save(html_file)
    file_url = "file:///" + html_file.replace("\\", "/")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1200, "height": 800})
        page.goto(file_url)
        time.sleep(2) # let map tiles load
        page.screenshot(path=os.path.join(out_dir, filename))
        browser.close()
        
    os.remove(html_file)

# NASA Johnson Space Center coords
nasa_coordinate = [29.559684888503615, -95.0830971930759]

# --- 1. Global Launch Site Distribution (Slide 35) ---
print("Generating Slide 35 Global Map...")
site_map_1 = folium.Map(location=nasa_coordinate, zoom_start=4)
launch_sites = spacex_df[['Launch Site', 'Lat', 'Long']].drop_duplicates()

for index, site in launch_sites.iterrows():
    folium.Marker(
        [site['Lat'], site['Long']],
        popup=site['Launch Site'],
        icon=folium.Icon(color='blue')
    ).add_to(site_map_1)
    
save_map_screenshot(site_map_1, 'Slide_35_Global_Map.png')

# --- 2. Color-Labeled Launch Outcomes (Slide 36) ---
print("Generating Slide 36 Color-Labeled Map...")
site_map_2 = folium.Map(location=nasa_coordinate, zoom_start=5)
marker_cluster = MarkerCluster().add_to(site_map_2)

def assign_marker_color(launch_outcome):
    if launch_outcome == 1:
        return 'green'
    else:
        return 'red'
    
spacex_df['marker_color'] = spacex_df['class'].apply(assign_marker_color)

for index, record in spacex_df.iterrows():
    marker = folium.Marker(
        location=[record['Lat'], record['Long']],
        icon=folium.Icon(color='white', icon_color=record['marker_color']),
        popup=record['Launch Site']
    )
    marker_cluster.add_child(marker)

save_map_screenshot(site_map_2, 'Slide_36_Color_Labeled_Map.png')

# --- 3. Proximity to Transport/Coastline (Slide 37) ---
print("Generating Slide 37 Proximity Map...")
ksc_coordinates = [28.573255, -80.646895]
site_map_3 = folium.Map(location=ksc_coordinates, zoom_start=14)

# Add LC-39A marker
folium.Marker(ksc_coordinates, popup='KSC LC-39A', icon=folium.Icon(color='blue')).add_to(site_map_3)

# Add nearby railway (FEC Railway)
railway_coords = [28.573255, -80.65411]
# Add nearby coastline
coastline_coords = [28.573255, -80.60660]

lines=folium.PolyLine(locations=[ksc_coordinates, railway_coords], weight=2, color='red')
site_map_3.add_child(lines)

lines_coast=folium.PolyLine(locations=[ksc_coordinates, coastline_coords], weight=2, color='green')
site_map_3.add_child(lines_coast)

save_map_screenshot(site_map_3, 'Slide_37_Proximity_Map.png')

print("Map screenshots generated successfully.")
