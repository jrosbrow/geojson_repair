def repair_duplicates(geom):
    """Repair duplicate consecutive coordinates and return the fixed geometry"""
    all_coords = geom.get('geometry').get('coordinates')
    geom_type = geom.get('geometry').get('type')
    if geom_type == 'MultiPolygon':
        coords_list = [coords[0] for coords in all_coords]
    elif geom_type == 'Polygon':
        coords_list = [coords for coords in all_coords]
    for i, coord_set in enumerate(coords_list):
        fixed_coord_set = [c for n, c in enumerate(coord_set) if n == 0 or c != coord_set[n - 1]]
        if geom_type == 'MultiPolygon':
            all_coords[i][0] = fixed_coord_set
        elif geom_type == 'Polygon':
            all_coords[i] = fixed_coord_set
    geom['geometry']['coordinates'] = all_coords
    return geom
