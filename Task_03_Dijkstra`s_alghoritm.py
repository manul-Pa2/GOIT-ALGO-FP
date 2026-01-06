from __future__ import annotations

import heapq
from typing import Dict, List, Tuple, Optional

Vertex = str
Graph = Dict[Vertex, List[Tuple[Vertex, float]]]  


def add_edge(graph: Graph, u: Vertex, v: Vertex, w: float, undirected: bool = True) -> None:
    """Додає ребро u->v з вагою w."""
    if w < 0:
        raise ValueError("Алгоритм Дейкстри не підтримує від’ємні ваги ребер.")    # <-головна властивість, яку я запам'ятав про нього з лекцій))

    graph.setdefault(u, []).append((v, w))
    graph.setdefault(v, [])  # щоб вершина існувала навіть без вихідних ребер

    if undirected:
        graph[v].append((u, w))


def dijkstra_heap(graph: Graph, start: Vertex) -> tuple[Dict[Vertex, float], Dict[Vertex, Optional[Vertex]]]:
    """
    Дейкстра з бінарною купою
    Повертає:
      - dist: найкороткі відстані від start до кожної вершини
      - prev: попередник у найкоротшому шляху
    """
    if start not in graph:
        raise KeyError(f"Стартова вершина '{start}' відсутня в графі.")

    dist: Dict[Vertex, float] = {v: float("inf") for v in graph}
    prev: Dict[Vertex, Optional[Vertex]] = {v: None for v in graph}
    dist[start] = 0.0

    # distance, vertex
    heap: List[Tuple[float, Vertex]] = [(0.0, start)]

    while heap:
        cur_dist, u = heapq.heappop(heap)

        # “Ліниве” видалення застарілих записів у купі
        if cur_dist != dist[u]:
            continue

        for v, w in graph[u]:
            cand = cur_dist + w
            if cand < dist[v]:
                dist[v] = cand
                prev[v] = u
                heapq.heappush(heap, (cand, v))

    return dist, prev


def reconstruct_path(prev: Dict[Vertex, Optional[Vertex]], start: Vertex, target: Vertex) -> List[Vertex]:
    """Відновлює шлях start -> target за словником prev."""
    path: List[Vertex] = []
    cur: Optional[Vertex] = target

    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cur = prev[cur]

    path.reverse()               # шляху не існує
    if not path or path[0] != start:
        return []         
    return path


if __name__ == "__main__":
    # Створення графа
    G: Graph = {}
    add_edge(G, "A", "B", 5)
    add_edge(G, "A", "C", 10)
    add_edge(G, "B", "D", 3)
    add_edge(G, "C", "D", 2)
    add_edge(G, "D", "E", 4)

    # Запуск Дейкстри
    dist, prev = dijkstra_heap(G, "A")

    # Результати: відстані до всіх вершин
    print("Найкоротші відстані від A:")
    for v in sorted(dist):
        print(f"  A -> {v}: {dist[v]}")

    # Вибір найкоротшого шляху
    target = "E"
    path = reconstruct_path(prev, "A", target)
    print(f"\nШлях A -> {target}: {path} (довжина {dist[target]})")
