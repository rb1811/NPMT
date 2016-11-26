import json

import mercator as m


def get_xy_for(nodes):
    return [{'x': m.lon2x_m(node['lng']), 'y': m.lat2y_m(node['lat'])} for node in nodes]


def get_lat_lng_for(nodes):
    return [{'lat': m.y2lat_m(node['y']), 'lng': m.x2lon_m(node['x'])} for node in nodes]