import folium
import pandas as pd
import wget
from folium.plugins import MarkerCluster
from folium.plugins import MousePosition
from folium.features import DivIcon
from math import sin, cos, sqrt, atan2, radians
import time
from playwright.sync_api import sync_playwright

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# 1. Prepare Data
spacex_csv_file = wget.download('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv')
spacex_df=pd.read_csv(spacex_csv_file)
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()[['Launch Site', 'Lat', 'Long']]

nasa_coordinate = [29.559684888503615, -95.0830971930759]

# Map 1: Launch Site Markers
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)
for index, row in launch_sites_df.iterrows():
    coordinate = [row['Lat'], row['Long']]
    folium.Circle(
        coordinate, radius=1000, color='#000000', fill=True
    ).add_child(folium.Popup(row['Launch Site'])).add_to(site_map)
    folium.map.Marker(
        coordinate,
        icon=DivIcon(
            icon_size=(20,20),
            icon_anchor=(0,0),
            html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % row['Launch Site']
        )
    ).add_to(site_map)
site_map.save('map1.html')

# Map 2: Marker Clusters
def assign_marker_color(launch_outcome):
    return 'green' if launch_outcome == 1 else 'red'
spacex_df['marker_color'] = spacex_df['class'].apply(assign_marker_color)
marker_cluster = MarkerCluster()
site_map.add_child(marker_cluster)
for index, record in spacex_df.iterrows():
    marker = folium.Marker(
        location=[record['Lat'], record['Long']],
        icon=folium.Icon(color='white', icon_color=record['marker_color'])
    )
    marker_cluster.add_child(marker)
site_map.save('map2.html')

# Map 3: Distances
launch_site_lat, launch_site_lon = 28.563197, -80.576820
coastline_lat, coastline_lon = 28.56367, -80.57163
city_lat, city_lon = 28.5383, -81.3792
railway_lat, railway_lon = 28.57205, -80.58527
highway_lat, highway_lon = 28.56367, -80.57083

site_map3 = folium.Map(location=[launch_site_lat, launch_site_lon], zoom_start=15)
for lat, lon, label in zip([coastline_lat, city_lat, railway_lat, highway_lat], [coastline_lon, city_lon, railway_lon, highway_lon], ['Coast', 'City', 'Railway', 'Highway']):
    distance = calculate_distance(launch_site_lat, launch_site_lon, lat, lon)
    marker = folium.Marker(
        [lat, lon],
        icon=DivIcon(
            icon_size=(20,20),
            icon_anchor=(0,0),
            html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance),
        )
    ).add_to(site_map3)
    folium.PolyLine(locations=[[launch_site_lat, launch_site_lon], [lat, lon]], weight=1).add_to(site_map3)
site_map3.save('map3.html')

# Use playwright to take screenshots
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1200, 'height': 800})
    import os
    cbd = "file://" + os.path.abspath('.').replace(os.sep, '/')
    
    page.goto(cbd + '/map1.html')
    time.sleep(2)
    page.screenshot(path='launch_site_markers.png')

    page.goto(cbd + '/map2.html')
    time.sleep(2)
    page.screenshot(path='launch_site_marker_cluster.png')

    page.goto(cbd + '/map3.html')
    time.sleep(2)
    page.screenshot(path='launch_site_marker_distance.png')

    browser.close()

print("Maps generated and screenshots taken!")
