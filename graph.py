import math
from model import Linear
from collections import deque


def create_graph(train_specs):
    num_labels = train_specs["num_labels"]
    layers = math.floor(math.log2(num_labels)) + 1
    num_nodes = layers*2+2
    adjList = [list() for i in range(num_nodes+1)]
    adjList[1].append(1)
    adjList[1].append(2)
    for i in range(2, layers+1):
        j = 2 * i + 1
        adjList[j-3].append(j)
        adjList[j-3].append(j-1)
        adjList[j-2].append(j)
        adjList[j-2].append(j-1)
    temp = num_labels
    ctr = 1
    while temp > 0:
        if temp % 2 == 1:
            adjList[ctr*2].append(num_nodes)
        ctr += 1
        temp //= 2

    edges = list()
    edge_map = dict()
    cnt = 0
    for i in range(1, num_nodes+1):
        for a in adjList[i]:
            edges.append([i, a])
            edge_map[str(i)+":"+str(a)] = cnt
            cnt += 1

    graph_params = {"num_layers": layers,
                    "num_nodes": num_nodes, "adj_list": adjList, "edges": edges, "edge_map": edge_map}
    # print(num_nodes)
    # for i in range(1, num_nodes+1):
    #     for a in adjList[i]:
    #         print(a, end=" ")
    #     print()
    return graph_params


def assign_edges(graph_params, train_specs):
    edges = graph_params["edges"]
    num_edges = len(edges)
    model = Linear(num_edges, train_specs["num_features"])
    graph_params["model":model]


def get_top_k(graph_params, num, x_single_row):

    num_nodes = graph_params["num_nodes"]
    adjList = graph_params["adj_list"]
    edges = graph_params["edges"]
    num_edges = len(edges)
    model = graph_params["model"]
    weights = model.get_predictions(x_single_row)
    edge_map = graph_params["edge_map"]

    indeg = [0 for i in range(num_nodes+2)]
    for i in range(1, num_nodes+1):
        for a in adjList[i]:
            indeg[a] += 1

    bestk = [list() for i in range(num_nodes+2)]
    bestk[1].append([0, -1])

    q = deque()
    q.append(1)
    while len(q) > 0:
        ver = q.popleft()
        for a in adjList[ver]:
            ##
            for val in bestk[ver]:
                new_val = val + weights[edge_map[str(ver)+":"+str(a)]]
                for i in range(bestk[a]):
                    if bestk[a][i][0] > new_val:
                        break
                # if
            ##
            indeg[a] -= 1
            if indeg[a] == 0:
                q.append(a)


if __name__ == "__main__":
    create_graph({"num_labels": 31})
