import numpy as np


def polygon_perimeter_random_point(polygon):
    idx = np.random.randint(0, len(polygon))
    alpha = np.random.uniform(0.0, 1.0)
    return alpha * np.array(polygon[idx]) + (1.0 - alpha) * np.array(polygon[(idx + 1) % len(polygon)])


def polygon_random_point(polygon):
    point_1 = polygon_perimeter_random_point(polygon)
    point_2 = polygon_perimeter_random_point(polygon)
    alpha = np.random.uniform(0.0, 1.0)
    return alpha * point_1 + (1.0 - alpha) * point_2
