import math
import time


def sequential_scan_base(input_file, query_file, output_file):
    ## Function to calculate the distance of 2 points
    def euclidean_distance(query_point, neighbor):
        return math.sqrt(
            (query_point[1] - neighbor[1]) ** 2 + (query_point[2] - neighbor[2]) ** 2
        )

    ## Read and extract data from location list
    locations = []
    with open(input_file, "r") as input:
        for line in input.readlines():
            data = line.split()
            location = (data[0], float(data[1]), float(data[2]))
            locations.append(location)

    ## Read and extract data from query list
    query_points = []
    with open(query_file, "r") as query:
        for line in query.readlines():
            data = line.split()
            query_point = (data[0], float(data[1]), float(data[2]))
            query_points.append(query_point)

    ## Finding the nearest neighbor for each query points
    results = []
    for query_point in query_points:
        nearest_neighbor = None
        min_distance = float("inf")
        for location in locations:
            distance = euclidean_distance(query_point, location)
            if distance < min_distance:
                min_distance = distance
                nearest_neighbor = location
        results.append((nearest_neighbor, query_point[0]))

    ## Write the result into the text file
    with open(output_file, "w") as output:
        for nearest_neighbor, queryID in results:
            output.write(
                f"id={nearest_neighbor[0]}, x={nearest_neighbor[1]}, y={nearest_neighbor[2]} for query {queryID}\n"
            )


input_file = "shop_dataset.txt"
query_file = "query_points.txt"
output_file = "sequential_scan_output.txt"

print("Running Search...")
start_time = time.time()
sequential_scan_base(input_file, query_file, output_file)
end_time = time.time()
print("Search Completed. Result is ready!")

## Calculate execution time
execution_time = end_time - start_time
average_query_time = execution_time / 200

with open(output_file, "a") as output:
    output.write(f"\nTotal Execution Time: {execution_time} seconds\n")
    output.write(f"Average Execution Time Per Query: {average_query_time} seconds")
