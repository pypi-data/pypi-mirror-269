from typing import Optional, Any

from ofnodes.nodes.singlynode import SinglyNode
from ofnodes.components.structures.descriptors import Head, Tail, Target
from ofnodes.components.structures.mixins import SearchMixin, RemoveMixin, InsertHeadMixin, InsertTailMixin, InsertAfterTargetMixin, InsertBeforeTargetMixin, PrintMixin

class SinglyLinkedList(SearchMixin, RemoveMixin, InsertHeadMixin, InsertTailMixin, InsertAfterTargetMixin, InsertBeforeTargetMixin, PrintMixin):
    """A class representing a singly linked list.

    This class provides functionality to create and manipulate a singly linked list
    data structure. Each node in the linked list contains a reference to the next
    node in the sequence.

    Attributes:
        _head (Optional[SinglyNode]): The head of the linked list.
        _tail (Optional[SinglyNode]): The tail of the linked list.
        _target (Optional[Any]): The target data or node instance.

    Examples:
        >>> linked_list = SinglyLinkedList()
        >>> linked_list
        SinglyLinkedList(head=None, tail=None, target=None)
    """

    __slots__ = ('_head', '_tail', '_target',)
    head = Head()
    tail = Tail()
    target = Target()
    def __init__(self, values=None) -> None:
        self._head: Optional[SinglyNode] = None
        self._tail: Optional[SinglyNode] = None
        self._target: Optional[Any|SinglyNode] = None
        if values:
            for value in values:
                self.tail = value

    def __add__(self, other):
        self.tail = other  # tail attr will validate


    def __repr__(self) -> str:
        #return f"{type(self).__name__}(head={type(self.head).__name__}, tail={self.tail})"
        if not self._head:
            return "SinglyLinkedList()"
        node = self._head
        nodes = []
        while node:
            nodes.append(repr(node.data))
            node = node.next
        return f"{type(self).__name__}([" + ', '.join(nodes) + "])"

    def __str__(self) -> str:
        if not self._head:
            return "Empty Singly Linked List"
        node = self._head
        nodes = []
        while node:
            nodes.append(str(node.data))
            node = node.next
        return ' -> '.join(nodes)
            
    def __dir__(self) -> list[str]:
        # Get the list of attributes and methods from the parent classes
        parent_dir = set(super().__dir__())
        # Filter out private attributes and methods
        parent_dir = {attr for attr in parent_dir if attr not in {'_head', '_tail', '_target'}}
        # Return a sorted list of all attributes and methods
        return sorted(parent_dir)
