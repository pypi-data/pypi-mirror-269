from shapely.geometry import Polygon, MultiPolygon
from pyproj import Proj, Transformer


# WSG84 coord system
in_proj = Proj(init='epsg:4326')  # WGS 84

# Sinusoidal system
out_proj = Proj(proj='sinu', R='6371007.181000', units='m')
transformer = Transformer.from_proj(in_proj, out_proj, always_xy=True)
transformer_rev = Transformer.from_proj(out_proj, in_proj, always_xy=True)


def convert_poly_wsg84_sinu(polygon: Polygon):
    transformed_coords = []
    for c_data in polygon.exterior.coords:
        new_coord = transformer.transform(c_data[0], c_data[1])
        transformed_coords.append(new_coord)

    return Polygon(transformed_coords)


def convert_multipoly_wsg84_sinu(multipolygon: MultiPolygon):
    polygons = []
    for subpoly in multipolygon.geoms:
        polygon = convert_poly_wsg84_sinu(subpoly)
        polygons.append(polygon)

    return MultiPolygon(polygons)


def convert_shape_wsg84_sinu(shape):
    if shape.geom_type == "Polygon":
        return convert_poly_wsg84_sinu(shape)
    elif shape.geom_type == "MultiPolygon":
        return convert_multipoly_wsg84_sinu(shape)
