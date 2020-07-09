import math
from model import Linear
from collections import deque


def create_graph(train_specs):
    """
    Creates graph structure and various utilities
     - layers
     - num_nodes
     - adjList (directed assumed, zero indexed)
     - edges (list stores pairs)
     - edge_map (dict maps pair to edge number)
    """
    num_labels = train_specs["num_labels"]

    layers = math.floor(math.log2(num_labels)) + 1
    num_nodes = layers * 2
    adjList = [list() for i in range(num_nodes+1)]
    adjList[0].append(1)
    adjList[0].append(2)
    for i in range(2, layers+1):
        j = 2 * i
        if j != num_nodes:
            adjList[j-2].append(j)
            adjList[j-3].append(j)
        adjList[j-2].append(j-1)
        adjList[j-3].append(j-1)
    temp = num_labels
    ctr = 1
    while temp > 0:
        if temp % 2 == 1:
            adjList[ctr*2-1].append(num_nodes)
        ctr += 1
        temp //= 2

    edges = list()
    edge_map = dict()
    cnt = 0
    for i in range(0, num_nodes+1):
        for a in adjList[i]:
            edges.append([i, a])
            edge_map[str(i)+":"+str(a)] = cnt
            cnt += 1

    graph_params = {"num_layers": layers,
                    "num_nodes": num_nodes, "adj_list": adjList, "edges": edges, "edge_map": edge_map}
    print(num_nodes)
    for i in range(0, num_nodes+1):
        print(i, end=' : ')
        for a in adjList[i]:
            print(a, end=" ")
        print()
    return graph_params


def assign_edges(graph_params, train_specs):
    """
    Calls the model constructor and adds to graph_params (seperate fn not needed probably)
    """
    edges = graph_params["edges"]
    num_edges = len(edges)
    model = Linear(num_edges, train_specs["num_features"])
    return model


def get_top_k(graph_params, num, x_single_row, weights):
    """
    Performs Viterbi once and returns top 'num' paths for a single training example
    TODO - needs testing
    """
    num_nodes = graph_params["num_nodes"]
    adjList = graph_params["adj_list"]
    edges = graph_params["edges"]
    num_edges = len(edges)
    edge_map = graph_params["edge_map"]

    # compute indegrees for toposort
    indeg = [0 for i in range(num_nodes+1)]
    for i in range(0, num_nodes):
        for a in adjList[i]:
            indeg[a] += 1

    # bestk is the dp here, stores [value, [parent_vertex, xth highest path reaching parent vertex]]
    bestk = [list() for i in range(num_nodes+1)]
    bestk[1].append([0, [-1, -1]])

    q = deque()
    q.append(0)
    while len(q) > 0:
        ver = q.popleft()
        print(ver)
        for neighbour in adjList[ver]:
            ##################
            # Main Viterbi code here
            cnt = 0
            for val in bestk[ver]:
                # Calculate new weight of path
                new_val = val[0] + \
                    weights[edge_map[str(ver)+":"+str(neighbour)]]
                counter = 0
                temp = [new_val, [ver, cnt]]
                # Loop till the number of paths here (shouldnt exceed k(num))
                while counter < len(bestk[neighbour]):
                    if bestk[neighbour][counter][0] < new_val:
                        # Push back values till the end if a better path found
                        temp = bestk[neighbour][counter]
                        # print(temp)
                        bestk[neighbour][counter] = [new_val, [ver, cnt]]
                        while counter < len(bestk[neighbour])-1 and counter < num-1:
                            # print(temp)
                            # Swap temp, bestk[neighbour][counter+1]
                            temp2 = bestk[neighbour][counter+1]
                            bestk[neighbour][counter+1] = temp
                            temp = temp2
                            ##
                            counter += 1
                        break
                    counter += 1
                # If there were less elements than k then add
                if len(bestk[neighbour]) < num:
                    bestk[neighbour].append(temp)
                cnt += 1
            ##################
            indeg[neighbour] -= 1
            if indeg[neighbour] == 0:
                q.append(neighbour)

    # print("Here", num_nodes)
    # Retrieve paths (in vertices form)
    paths = []
    for i in range(len(bestk[num_nodes])):
        path = [num_nodes]
        curr = bestk[num_nodes][i]
        print(curr)
        while curr[1][1] != -1:
            path.append(curr[1][0])
            curr = bestk[curr[1][0]][curr[1][1]]
        paths.append(path)

    # print(paths)
    # Convert to edge index form
    indexed_paths = []
    for path in paths:
        indexed_path = []
        for i in range(len(path)-1):
            indexed_path.append(edge_map[str(path[i+1])+':'+str(path[i])])
        indexed_paths.append(indexed_path)

    # print(paths)
    return indexed_paths


if __name__ == "__main__":
    create_graph({"num_labels": int(input())})
