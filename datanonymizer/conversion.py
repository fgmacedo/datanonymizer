import h3


def coords_to_h3(value, resolution=8):
    lat, lng = [float(x) for x in value[1:-1].split(",")]
    return h3.geo_to_h3(lat, lng, resolution)


def has_value(value):
    return str(value).strip() != ""
