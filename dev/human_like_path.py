import numpy as np
import matplotlib.pyplot as plt
from selenium_driverless.scripts.geometry import gen_combined_path, pos_at_time


def visualize_paths(paths_list, points, trancparency=0.5):
    plt.figure(figsize=(8, 6))

    for path_points in paths_list:
        x_path, y_path = zip(*path_points)
        plt.plot(x_path, y_path, color='blue', linewidth=1, alpha=trancparency)  # Set color and alpha for transparency

    plt.plot(*zip(*points), 'go')
    plt.show(block=True)


def demo(points, n_paths=30):
    paths_list = []

    for _ in range(n_paths):
        full_pixel_path = gen_combined_path(points, n_points_soft=5, smooth_soft=10, n_points_distort=100, smooth_distort=0.4)
        paths_list.append(full_pixel_path)

    visualize_paths(paths_list, click_points)


def visualize_events(path, points, total_time, freq=60, accel=3, mid_time=0.5):
    time_interval = 1 / freq
    plt.figure(figsize=(8, 6))

    x_path, y_path = zip(*path)
    x_path = np.array(x_path)
    y_path = np.array(y_path)

    points_x, points_y = zip(*points)
    plt.plot(points_x, points_y, 'go', markersize=8, label='Target Points')
    plt.plot(x_path, y_path, color='blue', linewidth=1)

    for t in np.arange(0, total_time + time_interval, time_interval):
        coordinates = pos_at_time(path, total_time, t, accel=accel, mid_time=mid_time)

        plt.plot(coordinates[0], coordinates[1], 'ro', markersize=3)

    plt.title("Mousemove Events")
    plt.xlim(min(x_path), max(x_path))
    plt.ylim(min(y_path), max(y_path))
    plt.legend()
    plt.show(block=True)


click_points = [(10, 100),
                (150, 300),
                (200, 800)]

#demo(click_points)

path = gen_combined_path(click_points, n_points_soft=5, smooth_soft=10, n_points_distort=100, smooth_distort=0.4)

visualize_events(path, click_points, 1, accel=3, mid_time=0.4)
