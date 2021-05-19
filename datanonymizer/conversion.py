import h3 as _h3

string = str
integer = int


def coords_to_h3(value, resolution=8):
    lat, lng = [float(x) for x in value[1:-1].split(",")]
    return _h3.geo_to_h3(lat, lng, resolution)


def has_value(value):
    return bool(value)
