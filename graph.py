import math

def create_graph(train_specs):
    num_labels = train_specs["num_labels"]
    layers = math.floor(math.log2(num_labels)) + 1
    num_nodes = layers*2+2
    adjList = [list() for i in range(num_nodes)]
    adjList[0].append(1)
    adjList[0].append(2)
    for i in range(2,layers+1):
        j = 2 * i +1
        adjList[j-3].append(j)
        adjList[j-3].append(j-1)
        adjList[j-2].append(j)
        adjList[j-2].append(j-1)
    


if __name__=="__main__":
    create_graph({"num_labels":32})