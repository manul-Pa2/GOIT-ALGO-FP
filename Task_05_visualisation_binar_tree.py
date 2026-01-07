import uuid
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt


# ---------- Базові класи з завдання 4 --------
class Node:
    def __init__(self, key, color="#B0B0B0"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
   # Рекурсія - лише для побудови схеми дерева. (я пам'ятаю примітку, але повністтю без неї - не обійдуся)
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)

        if node.left:
            graph.add_edge(node.id, node.left.id)
            lx = x - 1 / 2 ** layer
            pos[node.left.id] = (lx, y - 1)
            add_edges(graph, node.left, pos, x=lx, y=y - 1, layer=layer + 1)

        if node.right:
            graph.add_edge(node.id, node.right.id)
            rx = x + 1 / 2 ** layer
            pos[node.right.id] = (rx, y - 1)
            add_edges(graph, node.right, pos, x=rx, y=y - 1, layer=layer + 1)

    return graph


def draw_tree(tree_root, ax, title=None):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    ax.clear()
    if title:
        ax.set_title(title)
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=2500, node_color=colors, ax=ax)
    ax.axis("off")


# ---------- Допоміжні функції для HEX --------
def rgb_to_hex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"


def gradient_hex(n, start=(20, 35, 70), end=(200, 230, 255)):
    """
    n унікальних кольорів від темного (start) до світлого (end) у HEX (#RRGGBB).
    """
    if n <= 0:
        return []
    if n == 1:
        return [rgb_to_hex(*end)]

    res = []
    for i in range(n):
        t = i / (n - 1)
        r = round(start[0] + (end[0] - start[0]) * t)
        g = round(start[1] + (end[1] - start[1]) * t)
        b = round(start[2] + (end[2] - start[2]) * t)
        res.append(rgb_to_hex(r, g, b))
    return res


def reset_colors(root, default="#B0B0B0"):    # ітеративно, без рекурсії
    """Скидає кольори всіх вузлів дерева"""
    stack = [root]
    while stack:
        node = stack.pop()
        node.color = default
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)


# ---------- ітеративні обходи ----------
def dfs_iterative_preorder(root):
    """
    DFS (у глибину), порядок: Root -> Left -> Right
    Стек: кладемо right, потім left, щоб left обробився першим.
    """
    order = []
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return order


def bfs_iterative(root):
    """BFS (у ширину) через чергу."""
    order = []
    q = deque([root])
    while q:
        node = q.popleft()
        order.append(node)
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return order


# ---------- ВІЗУАЛІЗАЦІЯ ----------
def visualize_traversal(root, traversal="dfs", pause=0.9):
    """
    traversal: 'dfs' або 'bfs'
    На кожному кроці присвоює вузлу унікальний HEX-колір (темний->світлий) і перемальовує дерево.
    """
    if root is None:
        print("Дерево порожнє.")
        return

    reset_colors(root, default="#B0B0B0")

    if traversal.lower() == "dfs":
        order = dfs_iterative_preorder(root)
        name = "DFS (у глибину, stack)"
    elif traversal.lower() == "bfs":
        order = bfs_iterative(root)
        name = "BFS (у ширину, queue)"
    else:
        raise ValueError("traversal має бути 'dfs' або 'bfs'")

    colors = gradient_hex(len(order))

    plt.ion()          # анімація в одному вікні "інтерактивний режим"
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, node in enumerate(order, start=1):
        node.color = colors[i - 1]      # унікальний колір для поточного кроку
        draw_tree(
            root, ax,
            title=f"{name} — крок {i}/{len(order)} (відвідано: {node.val}, колір: {node.color})"
        )
        plt.pause(pause)

    plt.ioff()
    plt.show()


# ---------- ПРИКЛАД ДЕРЕВА ---------
if __name__ == "__main__":
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)

    visualize_traversal(root, traversal="dfs", pause=0.9)
    visualize_traversal(root, traversal="bfs", pause=0.9)
