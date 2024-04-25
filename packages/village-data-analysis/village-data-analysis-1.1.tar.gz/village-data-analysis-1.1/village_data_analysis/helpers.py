from shapely.ops import unary_union


def merge_polygons(polygons):
    return unary_union(list(polygons))


def extract_village_id(year, row) -> str:
    return row.name


def print_year_summary(id_memory_map):
    print("Counting result:")
    for _year in id_memory_map.keys():
        print(f"Year: {_year}")
        print("--------------")
        print(
            f"Provinces: {len(id_memory_map[_year]['provinces'])}, "
            f"Districts: {len(id_memory_map[_year]['districts'])}, "
            f"Sub-districts: "
            f"{len(id_memory_map[_year]['sub_districts'])}, "
            f"Total no of ids: "
            f"{len(id_memory_map[_year]['total_village_ids'])}")

        print("")
