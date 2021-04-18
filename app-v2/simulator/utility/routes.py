import numpy as np
import shapely.geometry as shp
from shapely.geometry import CAP_STYLE, JOIN_STYLE

def generate_default_route():
    path = np.array([[10.0, 50.0], [600.0, 50.0], [600.0, 600.0], [310.0, 310.0], [10.0, 600.0]])

    route = shp.Polygon(path)
    margin = route.buffer(-80, join_style=JOIN_STYLE.round)

    walls1_points = np.array(route.exterior)
    walls2_points = np.array(margin.exterior)

