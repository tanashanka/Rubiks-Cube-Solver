##### Build move/pruning tables in one place #####
import os
import pickle
from collections import namedtuple

from moves import(
    twist_table as build_twist_table,
    flip_table as build_flip_table,
    slice_table as build_slice_table,
    corners_table as build_corners_table,
    ud_edges_table as build_ud_edges_table,
    slice_sorted_table as build_slice_sorted_table
)
from pruning import(
    build_twist_slice_table,
    build_flip_slice_table,
    build_corners_slice_p2_table,
    build_ud_edges_slice_p2_table
)

Tables = namedtuple('Tables', [
    'twist_table','flip_table', 'slice_table',
    'corners_table', 'ud_edges_table', 'slice_sorted_table',
    'twist_slice_table', 'flip_slice_table',
    'corners_slice_table', 'ud_edges_slice_table'
])

CACHE_VERSION = 1 # Bump for changes to coord, move, or pruning code

def cache_path():
    """
    A fixed per-user location, so the cache is found however the program is launched.
    """
    base = os.environ.get('LOCALAPPDATA') or os.path.expanduser('~')
    folder = os.path.join(base, 'CubeSolver')
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, 'tables_cache.pkl')

def load_cache(path):
    """
    Return Tables from the cache file, or None if there is no usable cache
    """
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'rb') as f:
            data = pickle.load(f)
        if data['version'] != CACHE_VERSION or len(data['tables']) != len(Tables._fields):
            return None
        return Tables(*data['tables'])
    except Exception:
        return None # Corrupt, truncated, or from an older build; just rebuild

def save_cache(path, tables):
    """
    Write to a temporary file first, so closing the program mid-write can't leave a broken cache
    """
    temp = path + '.tmp'
    with open(temp, 'wb') as f:
        pickle.dump({'version': CACHE_VERSION, 'tables': tuple(tables)}, f)
    os.replace(temp, path)


def build_all_tables(verbose=True, use_cache=True):
    """
    Build every move/pruning table needed by solve()
    Returns a Tables namedtuple
    """
    path = cache_path()
    if use_cache:
        tables = load_cache(path)
        if tables is not None:
            if verbose:
                print(f"Loaded tables from {path}")
            return tables

    if verbose:
        print("Building move tables...")

    twist_table = build_twist_table()
    flip_table = build_flip_table()
    slice_table = build_slice_table()
    corners_table = build_corners_table()
    ud_edges_table = build_ud_edges_table()
    slice_sorted_table = build_slice_sorted_table()

    if verbose:
        print("Building pruning tables...")
    
    twist_slice_table = build_twist_slice_table(twist_table, slice_table)
    flip_slice_table = build_flip_slice_table(flip_table, slice_table)
    corners_slice_table = build_corners_slice_p2_table(corners_table, slice_sorted_table)
    ud_edges_slice_table = build_ud_edges_slice_p2_table(ud_edges_table, slice_sorted_table)

    tables = Tables(
        twist_table=twist_table,
        flip_table=flip_table,
        slice_table=slice_table,
        corners_table=corners_table,
        ud_edges_table=ud_edges_table,
        slice_sorted_table=slice_sorted_table,
        twist_slice_table=twist_slice_table,
        flip_slice_table=flip_slice_table,
        corners_slice_table=corners_slice_table,
        ud_edges_slice_table=ud_edges_slice_table
    )

    if use_cache:
        try:
            save_cache(path, tables)
        except OSError:
            pass # Read-only disk should not stop the program; it rebuilds next time
    return tables