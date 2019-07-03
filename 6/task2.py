"""
E - dict(<V> : [<V>, <V>, ...])
Ключ - строка, идентифицирующая вершину графа
значение - список вершин, достижимых из данной

Сделать так, чтобы по графу можно было итерироваться(обходом в ширину)

"""


class Graph:
    def __init__(self, E):
        self.E = E

    def __iter__(self):
        self.visited = {}
        self.que = [list(self.E.keys())[0]]
        return self

    def __next__(self):
        while self.que:
            v = self.que.pop(0)
            self.visited[v] = True
            for elem in self.E[v]:
                if elem not in self.que:
                    try:
                        if not self.visited[elem]:
                            self.que.append(elem)
                    except KeyError:
                        self.que.append(elem)
            return v
        raise StopIteration


E = {'A': ['B', 'C', 'D'], 'B': ['C'], 'C': [], 'D': ['A']}
graph = Graph(E)

for vertice in graph:
    print(vertice)
