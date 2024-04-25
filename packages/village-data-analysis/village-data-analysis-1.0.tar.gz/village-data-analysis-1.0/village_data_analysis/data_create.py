from shapely.geometry import Polygon


def get_cell_by_coordinates(x_cord: float, y_cord: float, average_box_size_x: float, average_box_size_y: float, minx: float, miny: float):
    # calculates the matrix index of a point.
    return (int(abs(minx - x_cord) / average_box_size_x), int(abs(miny - y_cord) / average_box_size_y))


def convert_cell_index_to_rectangle(a: int, b: int, average_box_size_x: float, average_box_size_y: float, minx: float, miny: float):
    # calculates rectangle poligon of a cell index.
    x_cord = minx + (a * average_box_size_x)
    y_cord = miny + (b * average_box_size_y)
    return Polygon([
        (x_cord, y_cord),  # left  bottom
        (x_cord + average_box_size_x, y_cord),  # right bottom
        (x_cord + average_box_size_x, y_cord + average_box_size_y),  # right top
        (x_cord, y_cord + average_box_size_y)  # left  top
    ])


def create_grid(gdf: any, year, matrix_size):

    invalid_villages = list()
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # I.
    #   Iterate trough data to get an average grid size.
    #   And get the min, max coords of the provinces.
    map_minx, map_miny, map_maxx, map_maxy = [None, None, None, None]
    is_first_row = True
    province_counter = 0
    for _, row in gdf.iterrows():
        current_poligon = row['geometry_sinu']  # convert_poligon(row.geometry)
        # Get base min-max values
        if is_first_row:
            map_minx, map_miny, map_maxx, map_maxy = current_poligon.bounds
            is_first_row = False
        else:
            minx, miny, maxx, maxy = current_poligon.bounds
            map_minx = sorted([map_minx, minx])[0]
            map_miny = sorted([map_miny, miny])[0]
            map_maxx = sorted([map_maxx, maxx])[1]
            map_maxy = sorted([map_maxy, maxy])[1]
        province_counter += 1

    # Box size
    average_box_size_x = abs(map_maxx - map_minx)/matrix_size
    average_box_size_y = abs(map_maxy - map_miny)/matrix_size

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # II
    #   Iterate trough the data, again.
    #   Get what id goes where on grid

    # Generate matrix
    result_matrix = [[[] for _ in range(matrix_size)]]*matrix_size

    # map to find what id is where
    id_locations = {}

    for _, row in gdf.iterrows():
        village_id: str = row.name
        current_poligon = row['geometry_sinu']
        minx, miny, maxx, maxy = current_poligon.bounds

        start_x_index, start_y_index = get_cell_by_coordinates(
            minx, miny, average_box_size_x, average_box_size_y, map_minx, map_miny)
        end_x_index, end_y_index = get_cell_by_coordinates(
            maxx, maxy, average_box_size_x, average_box_size_y, map_minx, map_miny)

        # Solve outindexing.
        end_x_index = end_x_index - 1 if end_x_index == matrix_size else end_x_index
        end_y_index = end_y_index - 1 if end_y_index == matrix_size else end_y_index

        # Iterate trough all grids that CAN contain the poligon, check if it contains, then add it two ways!
        for x_index in range(start_x_index, end_x_index+1):
            for y_index in range(start_y_index, end_y_index+1):
                current_rectangle = convert_cell_index_to_rectangle(
                    x_index, y_index, average_box_size_x, average_box_size_y, map_minx, map_miny)

                try:
                    if (current_rectangle.touches(current_poligon) or current_rectangle.intersects(current_poligon)):
                        result_matrix[x_index][y_index].append(village_id)
                        # append to village_id key
                        if village_id in id_locations:
                            id_locations[village_id].append((x_index, y_index))
                        # create a base list if village_id isn't in id_locations
                        else:
                            id_locations[village_id] = [(x_index, y_index)]
                except:
                    invalid_villages.append(village_id)

    return result_matrix, id_locations, invalid_villages
