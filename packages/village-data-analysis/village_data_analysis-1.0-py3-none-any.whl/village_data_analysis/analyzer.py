import math
import pickle
from tqdm import tqdm
import time
from typing import List, Tuple
from .coord_converter import (
    convert_shape_wsg84_sinu)
from .data_create import create_grid
from .helpers import merge_polygons
import shapely
import numpy as np
import pandas as pd
import geopandas as gpd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


loaded_shape_data = []
row_count: int = 0
image_data = None
tif = None


def poly_intersection_merge(a_polygon, b_polygon):
    try:
        intersection_poly = a_polygon.intersection(b_polygon)
        intersecting_area = shapely.area(intersection_poly)
        return int(intersecting_area / shapely.area(a_polygon) * 100)
    except:
        return 0


def poly_intersection_split(a_polygon, b_polygon):
    try:
        intersection_poly = a_polygon.intersection(b_polygon)
        intersecting_area = shapely.area(intersection_poly)
        return int(intersecting_area / shapely.area(b_polygon) * 100)
    except:
        return 0


def create_report(
        shapefile_paths: List[Tuple[str, str]],
        baseline_year: int = 2000,
        col_num: int = 5,
        grid_size: int = 0) -> None:

    # SHAPEFILES READ -------------------------------------------------------------------------------------------------------------------------------
    tt = time.time()
    global image_data
    global tif
    previous_year_map = dict()
    grid_dict = dict()
    first_year_village_count = 0
    for i, p in enumerate(tqdm(shapefile_paths, "Preparing shapefiles: ", len(shapefile_paths))):
        gdf = gpd.read_file(p[1])
        # This is specific for JT's data
        for ID_variant in [f"ID{p[0]}_d", f"ID{p[0]}", "iddesa", "IDDESA"]:
            if ID_variant in gdf.columns:
                break
        gdf = gdf[[ID_variant, 'geometry']]
        gdf.rename(columns={ID_variant: 'village_id'}, inplace=True)

        gdf = gdf.groupby("village_id").agg({'geometry': merge_polygons})
        if i == 0:
            first_year_village_count = gdf.shape[0]
            previous_year_map[int(p[0])] = int(p[0])
        else:
            previous_year_map[int(p[0])] = int(shapefile_paths[i - 1][0])

        gdf['year'] = p[0]
        gdf['year'] = gdf['year'].apply(lambda x: int(x))

        gdf['geometry_sinu'] = gdf['geometry'].apply(
            lambda x: convert_shape_wsg84_sinu(x))
        grid_size = 5 * round(math.sqrt(first_year_village_count)
                              ) if grid_size == 0 else grid_size
        grid_gdf, grid_id_locations, invalid_villages = create_grid(
            gdf, p[0], grid_size)
        grid_dict[int(p[0])] = (grid_gdf, grid_id_locations)
        gdf.drop(invalid_villages, inplace=True)
        gdf.reset_index(inplace=True)
        loaded_shape_data.append(gdf)
        gdf = None
    gdf = pd.concat(loaded_shape_data)
    # SHAPEFILES READ END ----------------------------------------------------------------------------------------------------------------------------------------

    # Border and area computations -------------------------------------------------------------------------------------------------------------------------------
    fst = time.time()
    gdf['border_length'] = gdf['geometry_sinu'].length
    gdf['border_length'] = gdf.apply(lambda x: x['border_length'] if x['geometry'].geom_type == 'Polygon' else sum(
        [shapely.length(subpoly) for subpoly in x['geometry_sinu'].geoms]), axis=1)
    gdf['border_length'] = gdf['border_length'].apply(lambda x: round(x, 0))
    gdf['area'] = gdf['geometry_sinu'].area
    gdf['area'] = gdf.apply(lambda x: x['area'] if x['geometry'].geom_type == 'Polygon' else sum(
        [shapely.area(subpoly) for subpoly in x['geometry_sinu'].geoms]), axis=1)
    gdf['area'] = gdf['area'].apply(lambda x: round(x, 0))
    gdf.set_index(['village_id', 'year'], inplace=True)
    gdf['baseline_border_length'] = gdf.apply(
        lambda x: gdf.loc[(x.name[0], baseline_year), 'border_length'] if (x.name[0], baseline_year) in gdf.index else 'N/A', axis=1)
    gdf['border_length_change_compared_to_baseline'] = gdf.apply(
        lambda x: -1 * round((x['baseline_border_length'] - x['border_length']) / x['baseline_border_length'] * 100, 2) if x['baseline_border_length'] != 'N/A' else 'N/A', axis=1)
    gdf['previous_border_length'] = gdf.apply(
        lambda x: gdf.loc[(x.name[0], previous_year_map[x.name[1]]), 'border_length'] if (x.name[0], previous_year_map[x.name[1]]) in gdf.index else 'N/A', axis=1)
    gdf['border_length_change_compared_to_prev_year'] = gdf.apply(
        lambda x: -1 * round((x['previous_border_length'] - x['border_length']) / x['previous_border_length'] * 100, 2) if x['previous_border_length'] != 'N/A' else 'N/A', axis=1)
    gdf['baseline_area'] = gdf.apply(lambda x: gdf.loc[(x.name[0], baseline_year), 'area'] if (
        x.name[0], baseline_year) in gdf.index else 'N/A', axis=1)
    gdf['area_change_compared_to_baseline'] = gdf.apply(
        lambda x: -1 * round((x['baseline_area'] - x['area']) / x['baseline_area'] * 100, 2) if x['baseline_area'] != 'N/A' else 'N/A', axis=1)
    gdf['previous_area'] = gdf.apply(
        lambda x: gdf.loc[(x.name[0], previous_year_map[x.name[1]]), 'area'] if (x.name[0], previous_year_map[x.name[1]]) in gdf.index else 'N/A', axis=1)
    gdf['area_change_compared_to_prev_year'] = gdf.apply(
        lambda x: -1 * round((x['previous_area'] - x['area']) / x['previous_area'] * 100, 2) if x['previous_area'] != 'N/A' else 'N/A', axis=1)
    print(f'Border and area computations took {int(time.time()-fst)} seconds')
    # Border and area computations END ----------------------------------------------------------------------------------------------------------------------------

    # SPLIT/MERGE CALCULATIONS ------------------------------------------------------------------------------------------------------------------------------------
    ID_change_to_dict = dict()
    ID_change_from_dict = dict()
    split_from_dict_IDs = dict()
    split_from_dict_Ps = dict()
    split_to_dict_IDs = dict()
    split_to_dict_Ps = dict()
    merge_from_dict_IDs = dict()
    merge_from_dict_Ps = dict()
    merge_to_dict_IDs = dict()
    merge_to_dict_Ps = dict()

    vectorized_intersection_merge = np.vectorize(poly_intersection_merge)
    vectorized_intersection_split = np.vectorize(poly_intersection_split)

    for k, v in previous_year_map.items():
        if k == v:
            continue
        else:
            split_from_dict_IDs[k] = dict()
            split_from_dict_Ps[k] = dict()
            split_to_dict_IDs[v] = dict()
            split_to_dict_Ps[v] = dict()

            ID_change_from_dict[k] = dict()
            ID_change_to_dict[v] = dict()

            merge_from_dict_IDs[k] = dict()
            merge_from_dict_Ps[k] = dict()
            merge_to_dict_IDs[v] = dict()
            merge_to_dict_Ps[v] = dict()

            previous_village_ids = list(
                list(zip(*(gdf.loc[pd.IndexSlice[:, v], :].index.values)))[0])
            actual_village_ids = list(
                list(zip(*(gdf.loc[pd.IndexSlice[:, k], :].index.values)))[0])
            splits = set(actual_village_ids).difference(
                set(previous_village_ids))
            merges = set(previous_village_ids).difference(
                set(actual_village_ids))

            if splits:
                for split in tqdm(list(splits), f'Computing village splitting for {k}: ', len(splits)):
                    try:
                        grid_cells = grid_dict[k][1][split]
                    except:
                        grid_cells = []
                        print(f'Side location conflict error for', split)
                    candidate_village_ids = []
                    for grid_cell in grid_cells:
                        candidate_village_ids.extend(
                            grid_dict[v][0][grid_cell[0]][grid_cell[1]])
                    candidate_village_ids = list(
                        set(candidate_village_ids).difference(merges))
                    # Note: it happens when the new village is not a result of a split but a merge
                    if len(candidate_village_ids) == 0:
                        continue
                    geo_polygons_A = gdf.loc[(split, k), 'geometry_sinu']
                    geo_polygons_B = pd.DataFrame(
                        {'single_column': gdf.loc[(candidate_village_ids, v), 'geometry_sinu']}).single_column.values

                    percentages = vectorized_intersection_split(
                        geo_polygons_A, geo_polygons_B)
                    actual_splits = np.nonzero(percentages > 0)

                    if len(actual_splits[0]) > 0:
                        split_from_IDs = np.array(candidate_village_ids)[
                            actual_splits[0]]
                        split_from_Ps = np.array(percentages)[actual_splits[0]]
                        split_from_dict_IDs[k][split] = split_from_IDs
                        split_from_dict_Ps[k][split] = split_from_Ps
                        for ID, P in zip(split_from_IDs, split_from_Ps):
                            if ID in split_to_dict_IDs[v]:
                                split_to_dict_IDs[v][ID].append(split)
                                split_to_dict_Ps[v][ID].append(P)
                            else:
                                split_to_dict_IDs[v][ID] = [split]
                                split_to_dict_Ps[v][ID] = [P]
            else:
                print(f'There are no village splitting in {k}')

            if merges:
                for merge in tqdm(list(merges), f'Computing village merging for {k}: ', len(merges)):
                    try:
                        grid_cells = grid_dict[v][1][merge]
                    except:
                        grid_cells = []
                        print(f'Side location conflict error for', merge)
                    candidate_village_ids = []
                    for grid_cell in grid_cells:
                        candidate_village_ids.extend(
                            grid_dict[k][0][grid_cell[0]][grid_cell[1]])
                    candidate_village_ids = list(set(candidate_village_ids))
                    if len(candidate_village_ids) == 0:  # NOTE: this should never happen!
                        continue
                    geo_polygons_A = gdf.loc[(merge, v), 'geometry_sinu']
                    geo_polygons_B = pd.DataFrame(
                        {'single_column': gdf.loc[(candidate_village_ids, k), 'geometry_sinu']}).single_column.values

                    percentages = vectorized_intersection_merge(
                        geo_polygons_A, geo_polygons_B)
                    actual_merges = np.nonzero(percentages > 0)
                    # actual_ID_changes = np.nonzero((percentages >= 90)) # TODO: merges VS splits intersection

                    if len(actual_merges[0]) > 0:
                        merge_to_IDs = np.array(candidate_village_ids)[
                            actual_merges[0]]
                        merge_to_Ps = np.array(percentages)[actual_merges[0]]
                        merge_to_dict_IDs[v][merge] = merge_to_IDs
                        merge_to_dict_Ps[v][merge] = merge_to_Ps
                        for ID, P in zip(merge_to_IDs, merge_to_Ps):
                            if ID in merge_from_dict_IDs[k]:
                                merge_from_dict_IDs[k][ID].append(merge)
                                merge_from_dict_Ps[k][ID].append(P)
                            else:
                                merge_from_dict_IDs[k][ID] = [merge]
                                merge_from_dict_Ps[k][ID] = [P]
            else:
                print(f'There are no village merging in {k}')
    # SPLIT/MERGE CALCULATIONS END ----------------------------------------------------------------------------------------------------------------------------
    
    st = time.time()
    print(f'Exporting output...', end='', flush=True)

    for t in ['split_from', 'split_to', 'merge_from', 'merge_to']:
        gdf[f'{t}'] = 0
        for i in range(1, col_num+1):
            gdf[f'{t}_village_id_{i}'] = 'N/A'
            gdf[f'{t}_village_percentage_{i}'] = 'N/A'
    gdf['ID_change_from'] = 'N/A'
    gdf['ID_change_to'] = 'N/A'

    for dict_IDs, dict_Ps, t in zip([split_from_dict_IDs, split_to_dict_IDs, merge_from_dict_IDs, merge_to_dict_IDs],
                                    [split_from_dict_Ps, split_to_dict_Ps,
                                        merge_from_dict_Ps, merge_to_dict_Ps],
                                    ['split_from', 'split_to', 'merge_from', 'merge_to']):
        for (k, IDs), (_, Ps) in zip(dict_IDs.items(), dict_Ps.items()):
            sorting_indices = dict()
            for row_ID, col_Ps in Ps.items():
                flag_setter = False
                sorting_indices[row_ID] = np.argsort(col_Ps)[::-1]
                for i, col_P in enumerate(np.array(col_Ps)[sorting_indices[row_ID]][:col_num]):
                    if not flag_setter:
                        flag_setter = True
                        gdf.loc[(row_ID, k), f'{t}'] = 1
                    gdf.loc[(row_ID, k),
                            f'{t}_village_percentage_{i+1}'] = f'{col_P}%'
            for row_ID, col_IDs in IDs.items():
                for i, col_ID in enumerate(np.array(col_IDs)[sorting_indices[row_ID]][:col_num]):
                    gdf.loc[(row_ID, k), f'{t}_village_id_{i+1}'] = str(col_ID)

    gdf.drop(['baseline_border_length', 'baseline_area', 'previous_border_length',
             'previous_area', 'geometry', 'geometry_sinu'], axis=1, inplace=True)
    gdf['border_length_change_compared_to_baseline'] = gdf['border_length_change_compared_to_baseline'].apply(
        lambda x: f'{x}%' if x != 'N/A' else '0%' if x == -0.0 else x)
    gdf['border_length_change_compared_to_prev_year'] = gdf['border_length_change_compared_to_prev_year'].apply(
        lambda x: f'{x}%' if x != 'N/A' else '0%' if x == -0.0 else x)
    gdf['area_change_compared_to_baseline'] = gdf['area_change_compared_to_baseline'].apply(
        lambda x: f'{x}%' if x != 'N/A' else '0%' if x == -0.0 else x)
    gdf['area_change_compared_to_prev_year'] = gdf['area_change_compared_to_prev_year'].apply(
        lambda x: f'{x}%' if x != 'N/A' else '0%' if x == -0.0 else x)

    gdf.sort_values(['year', 'village_id'], inplace=True)
    gdf.reset_index(inplace=True)
    gdf['village_id'] = gdf['village_id'].apply(lambda x: str(x))
    gdf['year'] = gdf['year'].apply(lambda x: str(x))
    gdf.to_csv('output.csv')
    gdf.to_excel('output.xlsx')
    print(f' took {int(time.time()-st)} seconds')

    print(f'\nTotal execution time: {int(time.time()-tt)} seconds')
