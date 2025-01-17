import sys
class Node: #nodes for future tree operations
    def __init__(self, id):
        self.id = id
        self.children = None

    def add_child(self, node, distance):
        if not self.children:
            self.children = {}
        self.children[node] = distance

def read_fna(file_name): #function to read fafsa files
    sequences = {} #dictionary to store the sequences and their information
    ids = [] #array for sequence ids
    with open(file_name) as f:
        lines = f.read().splitlines() #read every line
    curr = None #current sequence ID
    for index, line in enumerate(lines):
        if index % 2 == 0:
            curr = line[1:]
            ids.append(curr) #read every other line, pulling the ID from each sequence
        else:
            sequences[curr] = line #next line has the sequence
    return ids, sequences

def calc_dist(seq_1, seq_2):
    tot_mismatch = 0 #mismatch counter
    for i in range(len(seq_1)):
        if seq_1[i] != seq_2[i]:
            tot_mismatch += 1 #if nucleotides are not the same, increment mismatch
    return tot_mismatch / len(seq_1)  #find the mismatch %


def dist_mat(seq_id, seqs):
    dist_mat = [] #distance matrix
    for i in range(len(seq_id)):
        row = [0] * len(seq_id) #row for the squence ID
        dist_mat.append(row) #add the row
    for i in range(len(seq_id)):
        id1 = seq_id[i]  #current row ID
        for j in range(len(seq_id)):
            id2 = seq_id[j]  #current column ID
            dist_mat[i][j] = calc_dist(seqs[id1], seqs[id2]) #calculate the distance
    return dist_mat

def write_mat(seq_ids, dist_mat): #write the matrix to a file
    with open("genetic-distances.txt", 'w') as f:
        f.write("\t" + "\t".join(seq_ids) + "\n")  #header
        for i in range(len(dist_mat)):
            f.write(seq_ids[i] + '\t' + '\t'.join(map(str, dist_mat[i])) + '\n') #write the rows and distances

def neighbor_joining(orig_id, dist_mat, seq_count):
    global root #global root
    root = None #initialize root
    child_to_parent = {} #relationship dictionary
    seq_id_map = {id: str(i + 1) for i, id in enumerate(orig_id)} #map the sequence IDs to their numeric IDs

    next_neighbors(orig_id, dist_mat, seq_count, seq_id_map, child_to_parent) #recursively call next_neighbors
    bfs_root_node = Node(root)
    bfs_queue = [bfs_root_node] #queue for breadth first search
    
    edges = []  #list for edges
    
    while len(bfs_queue) > 0: #as long as the queue is not empty
        node_list = [] #current level nodes
        for node in bfs_queue: #transverse the bfs queue
            for child, (parent_node, distance) in child_to_parent.items(): #loop through the child-parent relationships
                if parent_node == node.id: #if the node is the parent of the child
                    childNode = Node(child) #child node
                    node.add_child(childNode, distance) #add to parent
                    node_list.append(childNode)
                    edges.append((node.id, child, distance))  #edge
        for node in node_list: #after you transverse, remove from the queue
            del child_to_parent[node.id]
        bfs_queue = node_list #next level

    write_edges_to_file(edges) #write edges to file
    
    return bfs_root_node #root node

def write_edges_to_file(edges): #write all of the edges to the edge file
    with open("edges.txt", 'w') as f:
        for edge in edges:
            f.write(f"{edge[0]}\t{edge[1]}\t{edge[2]}\n")


def next_neighbors(ids, dist_mat, seq_count, seq_id_map, child_to_parent):
    global root
    if len(dist_mat) <= 2: #when only 2 sequences remain
        node_1 = seq_id_map.get(ids[0], ids[0]) #ID of first sequence
        node_2 = seq_id_map.get(ids[1], ids[1]) #ID of second
        child_to_parent[node_1] = (node_2, dist_mat[0][1]) #link the child to the parent & record distance
        root = node_2 #set the root
        return
    q_mat = [[0] * len(dist_mat) for i in range(len(dist_mat))] #initialize q matrix
    min_x = 0
    min_y = 0 #indices of minimum q value
    min_mat_val = float('inf')
    for i in range(len(dist_mat)):
        for j in range(len(dist_mat)): #transverse the distance matrix
            if i == j:
                continue #make sure to ignore the diagonal elements (0)
            q_mat[i][j] = (len(dist_mat) - 2) * dist_mat[i][j] - sum(dist_mat[i]) - sum(dist_mat[j]) #calculate the qmat values
            if q_mat[i][j] < float('inf'):
                min_x = i #update minimum x index
                min_y = j #update minimum y index
                min_mat_val = q_mat[i][j]
    edge_x = 0.5 * dist_mat[min_x][min_y] + 0.5 * (sum(dist_mat[min_x]) - sum(dist_mat[min_y])) / (len(dist_mat) - 2)
    edge_y = dist_mat[min_x][min_y] - edge_x #calculate edge lenghts for internal node
    node_1 = node_2 = None
    if ids[min_x] in seq_id_map:
        node_1 = seq_id_map[ids[min_x]]
    else:
        node_1 = ids[min_x]
    if ids[min_y] in seq_id_map:
        node_2 = seq_id_map[ids[min_y]]
    else:
        node_2 = ids[min_y] #get the ID of the nodes that we will need to merge 
    
    child_to_parent[node_1] = (str(seq_count), edge_x)
    child_to_parent[node_2] = (str(seq_count), edge_y) #parent of the 2 merged nodes 

    ids = [id for id in ids if id not in (ids[min_x], ids[min_y])] + [str(seq_count)]

    seq_count -= 1
    new_dist = [[0] * (len(dist_mat) + 1) for i in range(len(dist_mat) + 1)] #update the sequence IDs, remove merged IDs, add new node
    for i in range(len(dist_mat)):
        for j in range(len(dist_mat)):
            new_dist[i][j] = dist_mat[i][j] #copy the new matrix in place of the old distance matrix
    for i in range(len(dist_mat)):
        new_dist[len(dist_mat)][i] = 0.5 * (dist_mat[min_x][i] + dist_mat[min_y][i] - dist_mat[min_x][min_y]) #new rows and columns for the merged nodes
        new_dist[i][len(dist_mat)] = new_dist[len(dist_mat)][i]

    update_dist_mat = [[0] * (len(dist_mat) - 1) for i in range(len(dist_mat) - 1)] #remove merged rows and columns
    x = y = 0
    for i in range(len(dist_mat) + 1): #loop through matrix, excluding merged rows
        if i == min_x or i == min_y:
            continue #skip merged row
        y = 0 #column for new dist mat
        for j in range(len(dist_mat) + 1): 
            if j == min_x or j == min_y:
                continue #skip merged col
            update_dist_mat[x][y] = new_dist[i][j] #assign new value to the distance matrix
            y += 1 #increment column
        x += 1 #increment row
    next_neighbors(ids, update_dist_mat, seq_count, seq_id_map, child_to_parent) #recursive call with new matrix


def main():
    input_file = sys.argv[1]

    # Read the FASTA file
    id, seqs = read_fna(input_file)
    
    # Compute the pairwise genetic distances
    distance_matrix = dist_mat(id, seqs)
    
    # Write the distance matrix to the output file
    write_mat(id, distance_matrix)

    neighbor_joining(id, distance_matrix, len(id))

if __name__ == "__main__":
    main()
