import json

notebook_path = r"c:\Users\ijara\Documentos\Codigos\python\coursera\Applied Data Science Capstone\notebooks\lab-jupyter-launch-site-location-v2.ipynb"
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        
        if "site_map = folium.Map(location=nasa_coordinate, zoom_start=5)" in source and "for index, row in launch_sites_df.iterrows():" not in source:
            new_source = """# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)
# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label
for index, row in launch_sites_df.iterrows():
    coordinate = [row['Lat'], row['Long']]
    folium.Circle(
        coordinate,
        radius=1000,
        color='#000000',
        fill=True
    ).add_child(folium.Popup(row['Launch Site'])).add_to(site_map)
    
    folium.map.Marker(
        coordinate,
        icon=DivIcon(
            icon_size=(20,20),
            icon_anchor=(0,0),
            html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % row['Launch Site']
        )
    ).add_to(site_map)

site_map"""
            cell['source'] = [line + '\n' for line in new_source.split('\n')]
            cell['source'][-1] = cell['source'][-1].strip()
            
        elif "# Create a new column in `launch_sites` dataframe called `marker_color` to store the marker colors based on the `class` value" in source:
             # Just pass, the next cell has the logic
             pass
             
        elif "for index, record in spacex_df.iterrows():\n    # TODO: Create and add a Marker cluster to the site map" in source:
            new_source = """# Add marker_cluster to current site_map
site_map.add_child(marker_cluster)

# for each row in spacex_df data frame
# create a Marker object with its coordinate
# and customize the Marker's icon property to indicate if this launch was successed or failed, 
# e.g., icon=folium.Icon(color='white', icon_color=row['marker_color']
for index, record in spacex_df.iterrows():
    # TODO: Create and add a Marker cluster to the site map
    marker = folium.Marker(
        location=[record['Lat'], record['Long']],
        icon=folium.Icon(color='white', icon_color=record['marker_color'])
    )
    marker_cluster.add_child(marker)

site_map"""
            cell['source'] = [line + '\n' for line in new_source.split('\n')]
            cell['source'][-1] = cell['source'][-1].strip()
            
        elif "# distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)" in source:
            new_source = """# find coordinate of the closest coastline
# e.g.,: Lat: 28.56367  Lon: -80.57163
launch_site_lat, launch_site_lon = 28.563197, -80.576820
coastline_lat, coastline_lon = 28.56367, -80.57163
distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)
distance_coastline"""
            cell['source'] = [line + '\n' for line in new_source.split('\n')]
            cell['source'][-1] = cell['source'][-1].strip()
            
        elif "# distance_marker = folium.Marker(" in source:
            new_source = """# Create and add a folium.Marker on your selected closest coastline point on the map
# Display the distance between coastline point and launch site using the icon property 
# for example
distance_marker = folium.Marker(
   [coastline_lat, coastline_lon],
   icon=DivIcon(
       icon_size=(20,20),
       icon_anchor=(0,0),
       html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline),
       )
   )
site_map.add_child(distance_marker)"""
            cell['source'] = [line + '\n' for line in new_source.split('\n')]
            cell['source'][-1] = cell['source'][-1].strip()
            
        elif "site_map.add_child(lines)" in source and "weight=1" in source and "lines=folium.PolyLine" in source:
            new_source = """# Create a `folium.PolyLine` object using the coastline coordinates and launch site coordinate
lines=folium.PolyLine(locations=[[launch_site_lat, launch_site_lon], [coastline_lat, coastline_lon]], weight=1)
site_map.add_child(lines)"""
            cell['source'] = [line + '\n' for line in new_source.split('\n')]
            cell['source'][-1] = cell['source'][-1].strip()
            
        elif "# Create a marker with distance to a closest city, railway, highway, etc." in source:
            new_source = """# Create a marker with distance to a closest city, railway, highway, etc.
# Draw a line between the marker to the launch site
city_lat, city_lon = 28.5383, -81.3792
railway_lat, railway_lon = 28.57205, -80.58527
highway_lat, highway_lon = 28.56367, -80.57083

for lat, lon, label in zip([city_lat, railway_lat, highway_lat], [city_lon, railway_lon, highway_lon], ['City', 'Railway', 'Highway']):
    distance = calculate_distance(launch_site_lat, launch_site_lon, lat, lon)
    marker = folium.Marker(
        [lat, lon],
        icon=DivIcon(
            icon_size=(20,20),
            icon_anchor=(0,0),
            html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance),
        )
    )
    site_map.add_child(marker)
    lines = folium.PolyLine(locations=[[launch_site_lat, launch_site_lon], [lat, lon]], weight=1)
    site_map.add_child(lines)

site_map"""
            cell['source'] = [line + '\n' for line in new_source.split('\n')]
            cell['source'][-1] = cell['source'][-1].strip()

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=4)

print("Notebook patched successfully!")
