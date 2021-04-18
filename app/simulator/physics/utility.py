import numpy as np


# https://stackoverflow.com/questions/61341712/calculate-projected-point-location-x-y-on-given-line-startx-y-endx-y
def point_projection_on_segment(segment_start, segment_end, point):
    segment = segment_end - segment_start
    seg_point = point - segment_start
    t = np.dot(segment, seg_point) / np.dot(segment, segment)
    t = max(0, min(1, t))
    return segment_start + t * segment


def route_completion(car_route, point):
    segments = [(car_route[i], car_route[i + 1]) for i in range(len(car_route) - 1)]
    total_distance = np.sum([np.linalg.norm(car_route[i + 1] - car_route[i]) for i in range(len(car_route) - 1)])
    proj_points = []
    for segment in segments:
        proj_points.append(point_projection_on_segment(segment[0], segment[1], point))
    distances = []
    for proj_point in proj_points:
        distances.append(np.linalg.norm(proj_point - point))

    segment_location_index: int = np.argmin(distances)
    point_location = proj_points[segment_location_index]

    traveled_distance = 0
    for idx in range(segment_location_index):
        (start, end) = segments[idx]
        traveled_distance += np.linalg.norm(end - start)

    traveled_distance += np.linalg.norm(segments[segment_location_index][0] - point_location)

    # print(traveled_distance)

    return traveled_distance / total_distance


if __name__ == '__main__':
    route = np.array([[10.0, 50.0], [600.0, 50.0], [600.0, 600.0], [310.0, 310.0], [10.0, 600.0], [10.0, 50.0]])
    print(route_completion(route, np.array([30, 100])))
