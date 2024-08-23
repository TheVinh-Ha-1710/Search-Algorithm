import math
import time
from rtree import RTree


# Function to construct R-Tree with the dataset
def constructRTree(input_file, B):
    locations = []
    with open(input_file, "r") as input:
        for line in input.readlines():
            data = line.split()
            locations.append({"id": data[0], "x": float(data[1]), "y": float(data[2])})

    # build R-Tree
    rtree = RTree(B)

    for location in locations:
        rtree.insert(rtree.root, location)

    return rtree


# Best First algorithm
def bfs(rtree, query_point):
    H = []
    root = rtree.root
    for child in root.child_nodes:
        dist = min_distance(query_point, child.MBR)
        H.append((dist, child))

    H.sort(key=lambda x: x[0])

    best_dist = float("inf")
    nearest_neighbor = None

    while H and (nearest_neighbor == None or best_dist > H[0][0]):
        dist, node = H.pop(0)

        if node.is_leaf():
            for data_point in node.data_points:
                dist = euclidean_distance(query_point, data_point)
                if dist < best_dist:
                    best_dist = dist
                    nearest_neighbor = (data_point, query_point["id"])
        else:
            for child in node.child_nodes:
                dist = min_distance(query_point, child.MBR)
                H.append((dist, child))

        H.sort(key=lambda x: x[0])

    return nearest_neighbor


# Calculate the distance of 2 data points
def euclidean_distance(p1, p2):
    return math.sqrt((p1["x"] - p2["x"]) ** 2 + (p1["y"] - p2["y"]) ** 2)


# Calculate the minimum distance from a query point to an MBR
def min_distance(query_point, mbr):
    x = query_point["x"]
    y = query_point["y"]

    if x < mbr["x1"]:
        dx = mbr["x1"] - x
    elif x > mbr["x2"]:
        dx = x - mbr["x2"]
    else:
        dx = 0

    if y < mbr["y1"]:
        dy = mbr["y1"] - y
    elif y > mbr["y2"]:
        dy = y - mbr["y2"]
    else:
        dy = 0

    return dx * dx + dy * dy


# Main function of the query
def main(rtree, query_file, output_file):
    query_points = []
    with open(query_file, "r") as query:
        for line in query.readlines():
            data = line.split()
            query_points.append(
                {"id": data[0], "x": float(data[1]), "y": float(data[2])}
            )

    results = []
    for query_point in query_points:
        nearest_neighbor = bfs(rtree, query_point)
        results.append(nearest_neighbor)

    with open(output_file, "w") as output:
        for result in results:
            output.write(
                f"id={result[0]['id']}, x={result[0]['x']}, y={result[0]['y']} for query {result[1]}\n"
            )


input_file = "shop_dataset.txt"
query_file = "query_points.txt"
output_file = "best_first_output.txt"


B = 4
print("Constructing tree...")
rtree = constructRTree(input_file, B)
print("Tree constructed!")

print("Running search...")
start_time = time.time()
main(rtree, query_file, output_file)
end_time = time.time()
print("Search complete. Result is ready!")

## Calculate execution time
execution_time = end_time - start_time
average_query_time = execution_time / 200

with open(output_file, "a") as output:
    output.write(f"\nTotal Execution Time: {execution_time} s\n")
    output.write(f"Average Execution Time Per Query: {average_query_time} s")
