import random
import numpy as np
import bezier
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def main():
    result_folder = 'results/'
    avg_methods = [default_roll, shift_default_roll]

    # get points
    points = generate_points()
    
    # calculate points of geometric rolling average
    avgs = []
    for method in avg_methods:
        avgs.append(method(points))

    # plot
    plt.scatter(points[0], points[1], c=range(len(points[0])), label='points', cmap='viridis', marker='o')
    for i, avg in enumerate(avgs):
        plt.scatter(avg[0], avg[1], label=avg_methods[i].__name__, marker='o')
    title = ""
    for method in avg_methods:
        title += method.__name__ + ', '
    plt.title(title)
    plt.legend()
    plt.savefig(result_folder + 'scatter_plot.png')

def generate_points(node_amount=32):
    nodes = [[],[]]
    for _ in range(node_amount):
        nodes[0].append(random.randint(0, 100))
        nodes[1].append(random.randint(0, 100))
    curve = bezier.Curve.from_nodes(nodes)
    s_vals = np.linspace(0.0, 1.0, 100)
    points = curve.evaluate_multi(s_vals)
    return points

def unwrap(points):
    return list(zip(points[0], points[1]))

def wrap(points):
    wrapped = [[],[]]
    for point in points:
        wrapped[0].append(point[0])
        wrapped[1].append(point[1])
    return wrapped

def normalize(direction):
    return direction / (direction[0]**2 + direction[1]**2)**0.5

# doesn't work (yet)
def last_dir_roll(points, roll_amount=16):
    points = unwrap(points)
    last_points = []
    result = None
    last_direction = None
    for point in points:
        # todo: take last point, add direction*distance to it, add to result
        # last point is the last point in result
        # direction determined by taking the average of the last points and then shifting it by the last direction*factor
        last_points.append(point)
        if len(last_points) > roll_amount:
            last_points.pop(0)
        if result is None:
            result = [point]
            continue
        if last_direction is None:
            last_direction = (last_points[-1][0] - last_points[-2][0], last_points[-1][1] - last_points[-2][1])
        direction = np.average(last_points, axis=0) + last_direction*1
        direction = normalize(direction)
        distance = (last_direction[0]**2 + last_direction[1]**2)**0.5
        result.append(result[-1] + direction*distance)
    return wrap(result)

def shift_default_roll(points, roll_amount=16, shift_factor=2):
    points = unwrap(points)
    last_points = []
    result = []
    for point in points:
        last_points.append(point)
        if len(last_points) >= 2:
            local_factor = shift_factor * (len(last_points) - 1) / (roll_amount - 1)
            result.append((np.average(last_points, axis=0)[0] + (last_points[-1][0] - last_points[-2][0]) * local_factor, np.average(last_points, axis=0)[1] + (last_points[-1][1] - last_points[-2][1]) * local_factor))
        if len(last_points) > roll_amount:
            last_points.pop(0)
    return wrap(result)        

def default_roll(points, roll_amount=16):
    points = unwrap(points)
    last_points = []
    result = []
    for point in points:
        last_points.append(point)
        result.append(np.average(last_points, axis=0))
        if len(last_points) > roll_amount:
            last_points.pop(0)
    return wrap(result)
        

if __name__ == "__main__":
    main()
