import numpy

EARTH_RADIUS = 6378137.0
M_PI = numpy.pi


def DEG2RAD(a):
    return a / (180.0 / M_PI)


def RAD2DEG(a):
    return (a) * (180.0 / M_PI)


def y2lat_m(y):
    return RAD2DEG(2 * numpy.arctan(numpy.exp(y / EARTH_RADIUS)) - M_PI / 2)


def x2lon_m(x):
    return RAD2DEG(x / EARTH_RADIUS)


def lat2y_m(lat):
    return numpy.log(numpy.tan(DEG2RAD(lat) / 2 + M_PI / 4)) * EARTH_RADIUS


def lon2x_m(lon):
    return DEG2RAD(lon) * EARTH_RADIUS
