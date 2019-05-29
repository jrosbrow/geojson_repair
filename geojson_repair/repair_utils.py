import numpy as np


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


def pldist(point, start, end):
    if np.all(np.equal(start, end)):
        return np.linalg.norm(point - start)
    return np.divide(
            np.abs(np.linalg.norm(np.cross(end - start, start - point))),
            np.linalg.norm(end - start))


def rdp_recursive(coords, epsilon):
    dmax = 0.0
    index = -1
    for i in range(1, coords.shape[0]):
        d = pldist(coords[i], coords[0], coords[-1])
        if d > dmax:
            index = i
            dmax = d
    if dmax > epsilon:
        r1 = rdp_recursive(coords[:index + 1], epsilon)
        r2 = rdp_recursive(coords[index:], epsilon)
        return np.vstack((r1[:-1], r2))
    else:
        return np.vstack((coords[0], coords[-1]))


def simplify_rdp(geom, epsilon):
    """Simplifies Polygons and MultiPolygons based on the Ramer–Douglas–Peucker algorithm"""
    all_coords = geom.get('geometry').get('coordinates')
    geom_type = geom.get('geometry').get('type')
    if geom_type == 'MultiPolygon':
        coords_list = [coords[0] for coords in all_coords]
    elif geom_type == 'Polygon':
        coords_list = [coords for coords in all_coords]
    for i, coord_set in enumerate(coords_list):
        simplified_coord_set = rdp_recursive(np.array(coord_set), epsilon)
        if geom_type == 'MultiPolygon':
            all_coords[i][0] = simplified_coord_set.tolist()
        elif geom_type == 'Polygon':
            all_coords[i][0] = simplified_coord_set.tolist()
    geom['geometry']['coordinates'] = all_coords
    return geom