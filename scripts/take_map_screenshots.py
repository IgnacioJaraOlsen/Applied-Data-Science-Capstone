import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    map_url = f"file:///{os.path.abspath('Presentation_Assets/notebook_map.html').replace(chr(92), '/')}"
    output_dir = 'Presentation_Assets'
    os.makedirs(output_dir, exist_ok=True)

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 720})
        
        # Load the Folium Map
        await page.goto(map_url)
        # Wait for the map clusters to finish rendering
        await page.wait_for_timeout(3000)

        # Slide 35: Global View
        await page.screenshot(path=os.path.join(output_dir, 'Slide_35_Map_Global.png'))
        print("Captured Slide 35")

        # Slide 36: Zoomed into KSC LC-39A cluster
        # Emulate zoom by scroll wheel (Folium map handles mouse wheel)
        # Lat/Lon of KSC: 28.573255, -80.646895. The map centers on roughly 28, -80.
        
        # To zoom in, we can focus on a specific marker or double click
        # Double click repeatedly near the center to zoom in to Florida
        for _ in range(3):
            await page.mouse.dblclick(640, 360)
            await page.wait_for_timeout(1000)
            
        await page.screenshot(path=os.path.join(output_dir, 'Slide_36_Map_Cluster_Zoom.png'))
        print("Captured Slide 36")

        # Slide 37: Proximity to transport
        # Zoom in even closer to see the distance to railways (simulated or actual if distance lines exist)
        for _ in range(3):
            await page.mouse.dblclick(640, 360)
            await page.wait_for_timeout(1000)
            
        await page.screenshot(path=os.path.join(output_dir, 'Slide_37_Map_Proximity_Zoom.png'))
        print("Captured Slide 37")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
