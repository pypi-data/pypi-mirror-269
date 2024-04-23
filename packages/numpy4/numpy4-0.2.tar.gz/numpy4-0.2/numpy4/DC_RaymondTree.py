# no. of nodes
n = 5

request_queue = {0: [], 1: [], 2: [], 3: [], 4: []}
holder = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1}
token = {0: 1, 1: 0, 2: 0, 3: 0, 4: 0}

adj_matrix = [[1, 0, 0, 0, 0],
              [1, 0, 0, 0, 0],
              [1, 0, 0, 0, 0],
              [0, 1, 0, 0, 0],
              [0, 1, 0, 0, 0]]

print("\nRaymond Tree Based Mutual Exclusion")
print("\nAdjacency Matrix for spanning tree:\n")

for i in adj_matrix:
    print(*i)

req_process = int(input("\nEnter the process who wants to enter CS : "))


def find_parent(req_process):

    request_queue[req_process].append(req_process)

    for i in range(n):
        if(adj_matrix[req_process][i] == 1):
            parent = i
            request_queue[parent].append(req_process)
            break

    print("\nProcess {} sending request to Parent Process {}".format(req_process, parent))
    print("Request queue: ", request_queue)

    if(token[parent] == 1):
        return parent
    else:
        parent = find_parent(parent)

    return parent


parent = find_parent(req_process)

while(token[req_process] != 1):

    child = request_queue[parent][0]
    request_queue[parent].pop(0)

    holder[parent] = child
    holder[child] = 0
    token[parent] = 0
    token[child] = 1

    print("\nParent process {} has the token and sends the token to the request process {}".format(parent, child))
    print("Request Queue: ", request_queue)
    parent = child

if(token[parent] == 1 and request_queue[parent][0] == parent):
    request_queue[parent].pop(0)
    holder[parent] = parent
    print("\nProcess {} enter the Critical Section".format(parent))
    print("Request Queue: ", request_queue)

if(len(request_queue[parent]) == 0):
    print("\nRequest Queue of process {} is empty. Therefore Release Critical Section".format(parent))

print("\nHolder: ", holder)