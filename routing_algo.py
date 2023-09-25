import math

# Hyperparameters for the routing algorithm
# because water consumption and distance are on different scales
# each might have different levels of importance depending on situation
# can be set accordingly
DIST_SCALE_FACTOR = 0.2
CONSUMPTION_SCALE_FACTOR = 0.05

def find_optimal_route(start, graph, predicted_water_consumption, maxDepth = 1):
    best_path = None
    best_path_dist = math.inf

    def find_optimal_route_helper(start, maxDepth, path, path_dist):
        nonlocal best_path, best_path_dist, graph, predicted_water_consumption

        if len(path) - 1 > maxDepth:
            return
        else:
            if len(path) == 1:
                pass
            else:
                if predicted_water_consumption[path[-1] - 1] > predicted_water_consumption[path[0] - 1]:
                    # Cant request water from a node that needs it more
                    pass
                else:
                    # include the water demand of last node
                    final_dist = path_dist + CONSUMPTION_SCALE_FACTOR * predicted_water_consumption[path[-1] - 1]
                    if final_dist < best_path_dist:
                        best_path = path.copy()
                        best_path_dist = final_dist

        # Find all nodes from start at most maxDepth away
        # with minimum distance to start
        for node in graph[start]:
            neighbour = node[0]
            if neighbour not in path:
                node_dist = DIST_SCALE_FACTOR * node[1]

                # add node to current path
                path.append(neighbour)
                path_dist += node_dist

                # recurse
                find_optimal_route_helper(neighbour, maxDepth, path, path_dist)

                # remove node from current path
                path.pop()
                path_dist -= node_dist
    
    find_optimal_route_helper(start, maxDepth, [start], 0)
    return best_path

def main():
    nodes = [1, 2, 3, 4]
    node_names = ["bungalow", "hospital", "school", "supermarket"]
    predicted_water_consumption = [40, 100, 30, 5]

    graph = {
        #[dest, weight]
        1: [[2, 5], [4, 3]],
        2: [[1, 5], [3, 10]],
        3: [[2, 10], [4, 2]],
        4: [[1, 3], [3, 2]]
    }

    print("Situation 1: Request from Hospital")
    start = 2
    maxDepth = 2 # Maximum number of edges away from requesting node
    optimal_route = find_optimal_route(start, graph, predicted_water_consumption, maxDepth)
    if optimal_route is None:
        print("No route found")
        return
    optimal_route.reverse() # The water flow direction
    print(optimal_route)
    print("Routing path:" , [node_names[i-1] for i in optimal_route])

    print()
    print("Situation 2: Request from bungalow")
    predicted_water_consumption = [40, 100, 60, 50]
    start = 1
    optimal_route = find_optimal_route(start, graph, predicted_water_consumption, maxDepth)
    if optimal_route is None:
        print("No route found")
        return
    optimal_route.reverse() # The water flow direction
    print(optimal_route)
    print("Routing path:" , [node_names[i-1] for i in optimal_route])

main()