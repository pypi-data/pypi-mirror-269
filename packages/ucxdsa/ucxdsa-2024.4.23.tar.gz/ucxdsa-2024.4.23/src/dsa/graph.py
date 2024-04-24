class AdjacencyMatrixGraph:
    """ 
    An unweighted adjacency matrix graph implementation in Python
    (allows either directed or undirected representation)
    """
    def __init__(self, labels: list[str]):
        """ 
        Args:
            labels: list of labels for each vertex
        """
        self.labels = labels
        self.label_index = { label: index for index, label  in enumerate(labels) }

        node_count = len(self.labels)
        self.array = [[None for i in range(node_count)] for j in range(node_count)]

    def add_edge(self, a_label: str, b_label: str):
        """ 
        Add an undirected edge between one vertex to another (same as add_edge())

        Args:
            a_label: starting vertex label
            b_label: ending vertex label
        """
        self.add_adjacent_vertex(a_label, b_label)
        
    def add_adjacent_vertex(self, a_label: str, b_label: str):
        """ 
        Add an undirected edge between one vertex to another (same as add_adjacent_vertex())

        Args:
            a_label: starting vertex label
            b_label: ending vertex label
        """
        a = self.label_index[a_label]
        b = self.label_index[b_label]
        self.array[a][b] = True
        self.array[a][a] = True

        self.array[b][a] = True
        self.array[b][b] = True

    def add_directed_edge(self, a_label: str, b_label: str):
        """ 
        Add a directed edge between one vertex to another (same as add_directed_adjacent_vertex() and add_adjacent_directed_vertex())

        Args:
            a_label: starting vertex label
            b_label: ending vertex label
        """
        self.add_adjacent_directed_vertex(a_label, b_label)

    def add_directed_adjacent_vertex(self, a_label: str, b_label: str):
        """ 
        Add a directed edge between one vertex to another (same as add_adjacent_directed_vertex()  and add_directed_edge())
 
        Args:
            a_label: starting vertex label
            b_label: ending vertex label
        """
        self.add_adjacent_directed_vertex(a_label, b_label)
        
    def add_adjacent_directed_vertex(self, a_label: str, b_label: str):
        """ 
        Add a directed edge between one vertex to another (same as add_directed_adjacent_vertex() and add_directed_edge())
 
        Args:
            a_label: starting vertex label
            b_label: ending vertex label
        """
        a = self.label_index[a_label]
        b = self.label_index[b_label]
        self.array[a][b] = True
        self.array[a][a] = True
        self.array[b][b] = True

    def df_traverse(self, start_label: str):
        """ 
        Perform depth first traversal in an adjacency matrix
 
        Args:
            start_label: starting vertex label
        """
        return self._df_rec_traverse(start_label, dict())
        
    def _df_rec_traverse(self, start_label: str, visited):
        """ 
        Helper method for depth first recursive traversal
        """
        start_index = self.label_index[start_label]
        visited[start_index] = True
        print(self.labels[start_index])
        
        for i in range(len(self.array)):
            if i not in visited and self.array[start_index][i]:
                self.df_rec_traverse(self.labels[i], visited)

    def bf_traverse(self, start_label: str):
        """ 
        Perform breadth first traversal in an adjacency matrix
 
        Args:
            start_label: starting vertex label
        """
        q = []
        visited={}
        start_index = self.label_index[start_label]
        q.append(start_index)

        while len(q) > 0:
            current = q.pop(0) # equivalent of dequeue

            if current not in visited: 
                visited[current] = True
                print(self.labels[current])

                for i in range(len(self.array)):
                    if self.array[current][i]:
                        q.append(i)

    def print_graph(self):
        """ 
        Print the contents of the graph
        """
        print("   |", end="")
        for label in self.labels:
            print(f"{label:^3}", end=" ")
        print()
        print("----" * (len(self.array) + 1))
        for r, row in enumerate(self.array):
            label = self.labels[r]
            print(f"{label:^3}|", end="");
            for col in row:
                b = " T " if col else "   "
                print(b, end=" ")
            print()
            
class AdjacencyMatrixWeightedGraph:
    """ 
    A weighted adjacency matrix graph implementation in Python
    (allows either directed or undirected representation)
    """
    def __init__(self, labels):
        """ 
        Args:
            labels: list of labels for each vertex
        """
        self.labels = labels
        self.label_index = { label: index for index, label  in enumerate(labels) }

        node_count = len(self.labels)
        self.array = [[None for i in range(node_count)] for j in range(node_count)]

    def add_edge(self, a_label: str, b_label: str, weight):
        """ 
        Add an undirected edge between one vertex to another (same as add_edge())

        Args:
            a_label: starting vertex label
            b_label: ending vertex label
            weight: weight of the vertex
        """
        self.add_adjacent_vertex(a_label, b_label, weight)

    def add_adjacent_vertex(self, a_label: str, b_label: str, weight):
        """ 
        Add an undirected edge between one vertex to another (same as add_edge())

        Args:
            a_label: starting vertex label
            b_label: ending vertex label
            weight: weight of the vertex
        """
        a = self.label_index[a_label]
        b = self.label_index[b_label]

        self.array[a][b] = weight
        self.array[a][a] = 0

        self.array[b][a] = weight
        self.array[b][b] = 0

    def add_directed_edge(self, a_label: str, b_label: str, weight):
        """ 
        Add a weighted directed edge between one vertex to another (same as add_adjacent_directed_vertex(), add_directed_adjacent_vertex())

        Args:
            a_label: starting vertex label
            b_label: ending vertex label
            weight: weight of the vertex
        """
        self.add_adjacent_directed_vertex(a_label, b_label, weight)

    def add_directed_adjacent_vertex(self, a_label: str, b_label: str, weight):
        """ 
        Add a weighted directed edge between one vertex to another (same as add_directed_edge(), add_adjacent_directed_vertex())

        Args:
            a_label: starting vertex label
            b_label: ending vertex label
            weight: weight of the vertex
        """
        self.add_adjacent_directed_vertex(a_label, b_label, weight)

    def add_adjacent_directed_vertex(self, a_label: str, b_label: str, weight):
        """ 
        Add a weighted directed edge between one vertex to another (same as add_directed_edge(), add_directed_adjacent_vertex())

        Args:
            a_label: starting vertex label
            b_label: ending vertex label
            weight: weight of the vertex
        """
        a = self.label_index[a_label]
        b = self.label_index[b_label]

        self.array[a][b] = weight
        self.array[a][a] = 0
        self.array[b][b] = 0
        
    def print_graph(self):
        """ 
        Print the contents of the graph.
        """
        print("   |", end="")
        for label in self.labels:
            print(f"{label:>3}", end=" ")
        print()
        print("----" * (len(self.array) + 1))
        for r, row in enumerate(self.array):
            label = self.labels[r]
            print(f"{label:^3}|", end="");
            for col in row:
                w = f"{col:3}" if col is not None else "   "
                print(w, end=" ")
            print()
            
            
class Vertex:
    pass

class Vertex:
    """ 
    A unweighted adjacency list vertex implementation in Python
    (allows either directed or undirected representation)
    """
    def __init__(self, value):
        """ 
        Args:
            value: value of the vertex
        """
        #: value of the vertex
        self.value = value
        #: list of adjacent vertices
        self.adjacents = []
        
    def add_adjacent_vertex(self, vertex: type[Vertex]):
        """ 
        Add an undirected vertex to the adjacency list (same as add_edge()).

        Args:
            vertex: vertex to add
        """
        if vertex not in self.adjacents:
            self.adjacents.append(vertex)
        if self not in vertex.adjacents:
            vertex.add_adjacent_vertex(self)
        
    def add_edge(self, vertex: type[Vertex]):
        """ 
        Add an undirected vertex to the adjacency list (same as add_adjacent_vertex()).

        Args:
            vertex: vertex to add
        """
        self.add_adjacent_vertex(vertex)

    def add_directed_edge(self, vertex: type[Vertex]):
        """ 
        Add a directed vertex to the adjacency list (same as add_directed_adjacent_vertex()).

        Args:
            vertex: vertex to add
        """
        self.add_directed_adjacent_vertex(vertex)
        
    def add_directed_adjacent_vertex(self, vertex: type[Vertex]):
        """ 
        Add a directed vertex to the adjacency list (same as add_directed_edge()).

        Args:
            vertex: vertex to add
        """
        if vertex not in self.adjacents:
            self.adjacents.append(vertex)

    def df_traverse(self):
        """
        Perform depth first traversal.
        """
        self._df_traverse_rec(self, dict())

    def _df_traverse_rec(self, vertex: type[Vertex], visited={}):
        """
        helper depth first traversal recursive function
        """
        visited[vertex] = True
        print(vertex.value)
        
        for v in vertex.adjacents:
            if not visited.get(v, False):
                v._df_traverse_rec(v, visited)
            
    def bf_traverse(self):
        """
        Perform breadth first traversal.
        """
        start = self
        visited = {}
        queue = []
        
        queue.append(start)

        while len(queue) > 0:
            current = queue[0]
            del queue[0]
            
            if not visited.get(current, False):               
                visited[current] = True
                print(current.value)
        
                for v in current.adjacents:
                    queue.append(v)
        
    def dfs(self, end):
        """ 
        Recursive depth first search.

        Args:
            end: vertex to search for
        Returns:
        Vertex in the graph
        None if not found.
        """
        return self.dfs_rec(self, end, dict())
        
    def dfs_rec(self, current, end, visited=None):
        """
        helper depth first search recursive function

        Returns:
        Vertex in the graph
        None if not found.
        """
        if current.value == end.value:
            print("Found: ", end.value)
            return current

        visited[current] = True
        print(current.value)
        
        for v in current.adjacents:
            if not visited.get(v, False):
                return v.dfs_rec(v, end, visited)
        return None
    
    def bfs(self, end):
        """ 
        Recursive breadth first search.

        Args:
            end: vertex to search for
        Returns:
        Vertex in the graph
        None if not found.
        """
        visited = {}
        queue = []
        start = self
        
        visited[start] = True
        queue.append(start)

        while len(queue) > 0:
            current = queue[0]
            del queue[0]
            print(current.value)
            # print("Visited: ", visited)
            # print("Queue: ", queue)
            
            if current.value == end.value:
                return current
            
            for v in current.adjacents:
                if not visited.get(v, False):               
                    visited[v] = True
                    queue.append(v)
        
        return None

    def __repr__(self):
        return self.value

class WeightedVertex:
    pass
class WeightedVertex:
    """ 
    A weighted adjacency list vertex implementation in Python
    (allows either directed or undirected representation)
    """
    def __init__(self, value):
        """ 
        Args:
            value: value of the vertex
        """
        self.value = value
        self.adjacents = {}
        
    # same as add_adjacent_vertex
    def add_edge(self, vertex: type[WeightedVertex], weight):
        """ 
        Add a weighted directed edge to the adjacency list (same as add_adjacent_vertex()).

        Args:
            vertex: vertex to add
            weight: weight of the vertex
        """
        self.add_adjacent_vertex(vertex, weight)

    # same as add_directed_adjacent_vertex
    def add_directed_edge(self, vertex: type[WeightedVertex], weight):
        """ 
        Add a weighted directed edge to the adjacency list (same as add_directed_adjacent_vertex()).

        Args:
            vertex: vertex to add
            weight: weight of the vertex
        """
        self.add_directed_adjacent_vertex(vertex, weight)

    def add_directed_adjacent_vertex(self, vertex: type[WeightedVertex], weight):
        """ 
        Add a weighted directed edge to the adjacency list (same as add_directed_edge()).

        Args:
            vertex: vertex to add
            weight: weight of the vertex
        """
        if vertex not in self.adjacents:
            self.adjacents[vertex] = weight

    def add_adjacent_vertex(self, vertex: type[WeightedVertex], weight):
        """ 
        Add a weighted edge to the adjacency list (same as add_directed_edge()).

        Args:
            vertex: vertex to add
            weight: weight of the vertex
        """
        if vertex not in self.adjacents:
            self.adjacents[vertex] = weight
        if self not in vertex.adjacents:
            vertex.adjacents[self] = weight
        
    def df_traverse(self, vertex: type[WeightedVertex], visited={}):
        """ 
        depth first traversal 

        Args:
            vertex: starting vertex
            visited: dictionary of visited vertices
        """
        visited[vertex] = True
        print(vertex.value)
        
        for v in vertex.adjacents:
            if not visited.get(v, False):
                v.df_traverse(v, visited)
            
    def bf_traverse(self, vertex: type[WeightedVertex]):
        """ 
        breadth first traversal 
        
        Args:
            vertex: starting vertex
        """
        visited = {}
        queue = []
        
        queue.append(vertex)

        while len(queue) > 0:
            current = queue[0]
            del queue[0]
            
            if not visited.get(current, False):               
                visited[current] = True
                print(current.value)
        
                for v in current.adjacents:
                    queue.append(v)
                    
    def dfs(self, target: type[WeightedVertex]):
        """ 
        depth first search 

        Args:
            target: target value to search for
        """
        return self._dfs_rec(self, target, dict())
        
    def _dfs_rec(self, current, end, visited={}):
        """ 
        recursive depth first search healper function

        Args:
            current: starting vertex
            end: target vertex to search for
            visited: dictionary of visited values
        """

        print(current.value, visited.keys())
        if current.value == end.value:
            return current

        visited[current] = True
        print("Current: ", current.value)
        
        for v in current.adjacents:
            if not visited.get(v, False):
                v.dfs_rec(v, end, visited)
        return None

    
    def bfs(self, vertex: type[WeightedVertex], target):
        """ 
        breadth first search 

        Args:
            vertex: startering vertex
            target: target value to search for
        """
        visited = {}
        queue = []
        
        queue.append(vertex)

        while len(queue) > 0:
            current = queue[0]
            del queue[0]
            
            if current.value == target:
                return current
            
            if not visited.get(current, False):               
                visited[current] = True
                print(current.value)
        
                for v in current.adjacents:
                    queue.append(v)
        return None
    
    def __repr__(self):
        return self.value

    def __lt__(self, vertex):
        return self.value < vertex.value

    
#### Dijkstra's Algorithm Functions
def shortest_path(start, end):
    """ 
    Helper function that returns a weight table and a previous vertex table using Dijkstra's Algorithm.

    Args:
        start: starting vertex
        end: ending vertex
    
    Returns:
    a tuple of a weight table dictionary and a previous path dictionary
    """
    weight_table = {}
    previous = {}
    visited = {}
    queue = [] # ideally, a min heap
    
    current = start
    queue.append(current)
    weight_table[current.value] = 0
    previous[current.value] = current
    
    while len(queue) > 0:
        current_weight = weight_table.get(current.value, None)
        visited[current.value] = True

# for non-weighted version, use:
# for adjacent in current.adjacents:
#   weight = 1

        for adjacent, weight in current.adjacents.items():
            if not visited.get(adjacent.value, False):
                queue.append(adjacent)

            wt = weight_table.get(adjacent.value, None)
            if not wt or wt > weight + current_weight:
                print(weight_table)
                weight_table[adjacent.value] = weight + current_weight
                previous[adjacent.value] = current

        current = queue[0]
        del queue[0]
            
    return weight_table, previous

def find_path(start, end):
    """ 
    Return the shortest path of two vertices using Dijkstra's Algorithm.

    Args:
        start: starting vertex
        end: ending vertex

    Returns:
    A list of vertices that form a shortest path
    """
    weight_table, previous = shortest_path(start, end)
    path = []

    current = end
    path.append(current.value)
    while current != start:
        current = previous[current.value]
        path.append(current.value)
        
    path.reverse()
    print("weight table")
    print(weight_table)
    print("price ", weight_table[end.value])
    return path

