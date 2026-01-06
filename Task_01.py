from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Optional, TypeVar, Callable

T = TypeVar("T")


@dataclass
class Node:
    value: T
    next: Optional["Node"] = None


class LinkedList:
    def __init__(self, values: Iterable[T] = ()) -> None:
        self.head: Optional[Node] = None
        for v in values:
            self.append(v)

    def append(self, value: T) -> None:
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            return
        cur = self.head
        while cur.next is not None:
            cur = cur.next
        cur.next = new_node

    def to_list(self) -> list[T]:
        out: list[T] = []
        cur = self.head
        while cur is not None:
            out.append(cur.value)
            cur = cur.next
        return out

    def __repr__(self) -> str:
        return f"LinkedList({self.to_list()})"


# Реверсування однозв’язного списку
def reverse_list(head: Optional[Node]) -> Optional[Node]:
    prev: Optional[Node] = None
    cur = head
    while cur is not None:
        nxt = cur.next      # зберегли "наступного"
        cur.next = prev     # розвернули посилання
        prev = cur          # посунули prev
        cur = nxt           # посунули cur
    return prev


# Розрізаємо список на 2 половини (для merge sort)
def split_middle(head: Node) -> tuple[Node, Optional[Node]]:
    slow: Node = head
    fast: Optional[Node] = head
    prev: Optional[Node] = None

    while fast is not None and fast.next is not None:
        prev = slow
        slow = slow.next         # type: ignore[assignment]
        fast = fast.next.next

    if prev is not None:
        prev.next = None       # розрізаємо
    return head, slow


# Злиття двох ВІДСОРТОВАНИХ однозв’язних списків
def merge_sorted_heads(
    a: Optional[Node],
    b: Optional[Node],
    key: Callable[[T], object] = lambda x: x,
) -> Optional[Node]:
    dummy = Node(None)  
    tail = dummy

    while a is not None and b is not None:
        if key(a.value) <= key(b.value):
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next

    tail.next = a if a is not None else b
    return dummy.next


# 2) Сортування однозв’язного списку: Merge Sort
def merge_sort(
    head: Optional[Node],
    key: Callable[[T], object] = lambda x: x,
) -> Optional[Node]:
    if head is None or head.next is None:
        return head

    left_head, right_head = split_middle(head)  
    left_sorted = merge_sort(left_head, key=key)
    right_sorted = merge_sort(right_head, key=key)
    return merge_sorted_heads(left_sorted, right_sorted, key=key)


# Зручні обгортки для роботи з LinkedList
def sort_linked_list(ll: LinkedList, key: Callable[[T], object] = lambda x: x) -> None:
    ll.head = merge_sort(ll.head, key=key)

def reverse_linked_list(ll: LinkedList) -> None:
    ll.head = reverse_list(ll.head)

def merge_two_sorted_lists(a: LinkedList, b: LinkedList, key: Callable[[T], object] = lambda x: x) -> LinkedList:
    merged = LinkedList()
    merged.head = merge_sorted_heads(a.head, b.head, key=key)
    return merged


if __name__ == "__main__":
    ll = LinkedList([4, 1, 3, 2, 5])
    print("Оригінал: ", ll)

    reverse_linked_list(ll)
    print("Реверс:   ", ll)

    sort_linked_list(ll)
    print("Сорт:     ", ll)

    a = LinkedList([1, 3, 5, 7])
    b = LinkedList([2, 3, 6, 8, 9])
    merged = merge_two_sorted_lists(a, b)
    print("Злиття:   ", merged)
