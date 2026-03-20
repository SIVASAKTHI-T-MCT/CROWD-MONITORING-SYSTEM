import numpy as np

def polar_to_xy(angles_deg, dists_cm, max_range_m=50.0):
    """
    Convert polar coordinates (angle in degrees, distance in cm) to Cartesian XY (meters).
    Filters out distances beyond max_range_m.
    """
    # Convert cm to m, treat None as a large value
    r = np.array([d/100.0 if d is not None else 999.0 for d in dists_cm])
    angles_rad = np.deg2rad(angles_deg)
    
    x = r * np.cos(angles_rad)
    y = r * np.sin(angles_rad)
    
    # Filter points within sensor range
    mask = r < max_range_m
    return np.vstack([x[mask], y[mask]]).T
