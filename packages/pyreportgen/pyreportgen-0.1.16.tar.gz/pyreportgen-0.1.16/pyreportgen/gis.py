from pyreportgen.base import Component, _DATA_DIR
import pyreportgen.helpers as helpers
from PIL import Image, ImageDraw
import math
from io import BytesIO
import requests
import os.path as path
import contextily as cx
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import shape
import time

def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 1 << zoom
  xtile = (lon_deg + 180.0) / 360.0 * n
  ytile = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n
  return xtile, ytile

def num2deg(xtile, ytile, zoom):
    n = 1 << zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg

def translate(value, leftMin, leftMax, rightMin, rightMax):
    value *= 100000
    leftMin *= 100000
    leftMax *= 100000

    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)



def translate_coord(value, leftMin, leftMax, rightMin, rightMax):
    return (translate(value[0], leftMin[0], leftMax[0], rightMin[0], rightMax[0]), translate(value[1], leftMin[1], leftMax[1],  rightMin[1], rightMax[1]))

def open_image_from_url(url):
    try:
        response = requests.get(url, headers={"user-agent":"pyreportgen-library"})
        response.raise_for_status()  # Raise an HTTPError for bad responses
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        return img
    except Exception as e:
        print(f"Error: {e}")
        # Return a black image with size 1x1 in case of failure
        return Image.new("RGB", (1, 1), color="black")

class Map(Component):
    ## bbox: ((latitude, longditude), (latitude, longditude))
    def __init__(self, bbox: tuple[tuple[float, float], tuple[float, float]], zoom=18, tile_host="https://tile.openstreetmap.org/{z}/{x}/{y}.png"):
        super().__init__()
        print("This component is still not done.")
        self.bottom_left: tuple[float, float] = (min(bbox[0][0], bbox[1][0]), min(bbox[0][1], bbox[1][1]))
        self.upper_right: tuple[float, float] = (max(bbox[0][0], bbox[1][0]), max(bbox[0][1], bbox[1][1]))
        self.zoom = zoom
        self.tile_host = tile_host
        self.image: Image.Image = None        
    
    def make_image(self) -> Image.Image:
        # Get the corners as tile numbers.
        

        return None
    
   

class MapGeoJson():
    def __init__(self, geojson, tile_host="https://tile.openstreetmap.org/{z}/{x}/{y}.png"):
        self.tile_host = tile_host
        self.geojson = geojson
  

    def make_image(self):
        # Set up the matplotlib figure and axis
        fig, ax = plt.subplots(figsize=(20, 20))

        for feature in self.geojson["features"]:
            if feature["type"] != "Feature":
                continue
            geom = feature["geometry"]
            
            gdf = gpd.GeoDataFrame({'geometry': [shape(geom)]}, crs='EPSG:4326')
            gdf.plot(facecolor='none', edgecolor='red', linewidth=2, ax=ax)

        ax.set_box_aspect(1)
        plt.axis('off')
        cx.add_basemap(ax=ax, crs='EPSG:4326', source=self.tile_host, zoom=18)
        plt.savefig(path.join(_DATA_DIR, "tmp.png"), bbox_inches="tight")
        return Image.open(path.join(_DATA_DIR, "tmp.png"))

    
    def render(self) -> str:
        self.image = self.make_image()
        name = helpers.random_filename("png")
        self.image.save(path.join(_DATA_DIR, name))
        return helpers.tagwrap("", "img", "Map", f"src='{name}'", False)