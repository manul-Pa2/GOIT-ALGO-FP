import uuid
import math
import networkx as nx
import matplotlib.pyplot as plt
import heapq


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)

        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)

        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)

    return graph


def draw_tree(tree_root, title=None):
    if tree_root is None:
        print("Дерево порожнє.")
        return

    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    if title:
        plt.title(title)
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()


def heap_to_tree(heap_list):
    """
    Створює бінарне дерево з масиву купи:
    heap_list[0] — корінь
    heap_list[2*i+1] — лівий нащадок
    heap_list[2*i+2] — правий нащадок
    """
    if not heap_list:
        return None

    # Палітра для фарбування
    palette = ["skyblue", "lightgreen", "khaki", "plum", "lightsalmon", "lightgray"]

    nodes = []
    for i, value in enumerate(heap_list):
        level = int(math.log2(i + 1))         # рівень вузла в бінарному дереві
        color = palette[level % len(palette)]
        nodes.append(Node(value, color=color))

    for i in range(len(nodes)):
        left_i = 2 * i + 1
        right_i = 2 * i + 2
        if left_i < len(nodes):
            nodes[i].left = nodes[left_i]
        if right_i < len(nodes):
            nodes[i].right = nodes[right_i]

    return nodes[0]


def visualize_heap(heap_list, title="Binary Heap Visualization"):
    root = heap_to_tree(heap_list)
    draw_tree(root, title=title)


# ====== test =====
if __name__ == "__main__":
    data = [5, 3, 8, 4, 1, 7, 9, 2]
    heapq.heapify(data)       # робимо min-heap 
    print("Масив купи (після heapify):", data)

    visualize_heap(data, title="Min-Heap (heapq.heapify)")

    # Якщо хочеш max-heap через heapq:
    data2 = [5, 3, 8, 4, 1, 7, 9, 2]
    max_heap = [-x for x in data2]
    heapq.heapify(max_heap)
    # Для відображення значень інвертуємо назад:
    visualize_heap([-x for x in max_heap], title="Max-Heap")
