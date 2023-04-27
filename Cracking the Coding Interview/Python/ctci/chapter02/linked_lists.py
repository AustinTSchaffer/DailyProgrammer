class SinglyLinkedNode(object):
    """
    Implementation of a node to hold a single value within a singly linked list.
    """

    def __init__(self, data):
        self.data = data
        self.next = None  # type: SinglyLinkedNode

    def append(self, data):
        """
        Appends a new node to the tail of the list that contains this node.
        """

        last = self

        while last.next is not None:
            last = last.next

        last.next = (
            data
            if type(data) is SinglyLinkedNode else
            SinglyLinkedNode(data)
        )

    def __contains__(self, data):
        return data == self.data or ((self.next is not None) and (data in self.next))

    def __str__(self) -> str:
        return str(self.data)

    def __repr__(self) -> str:
        return "SinglyLinkedNode({})".format(str(self.data))


class SinglyLinkedList(object):
    """

    Implementation of a singly linked list

    """
    def __init__(self, *data):
        """
        Initializes an instance of a linked list, optionally accepting
        a list of values that it should use to populate the list.
        """
        self.head = None  # type: SinglyLinkedNode

        for d in data:
            self.append(d)

    def append(self, data):
        """
        Appends a new node to the tail of this linked list.
        """

        if self.head is None:
            self.head = (
                data
                if type(data) is SinglyLinkedNode else
                SinglyLinkedNode(data)
            )
        else:
            self.head.append(data)

    def delete(self, data) -> bool:
        """
        Removes a node from this linked list if the specified data exists
        anywhere in the list.

        Returns true if the list is altered, false otherwise.
        """

        if self.head is None:
            return False

        if self.head.data == data:
            self.head = self.head.next
            return True

        current = self.head

        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next
                return True
            current = current.next

        return False

    def remove(self, node) -> bool:
        """
        Removes a node from this linked list if the specified node exists
        anywhere in the list. This is not the same as the `delete` function as
        it removes the node based on the node's reference, instead of the node's
        data.

        Returns true if the list is altered, false otherwise.
        """

        if self.head is None:
            return False

        if self.head == node:
            self.head = self.head.next
            return True

        current = self.head

        while current.next is not None:
            if current.next == node:
                current.next = current.next.next
                return True
            current = current.next

        return False



    def pop(self) -> SinglyLinkedNode:
        """
        Removes the head element from the linked list and returns its data.
        Returns None if the head of this linked list is None.
        """

        old_head = self.head

        if self.head is not None:
            self.head = self.head.next

        return None if old_head is None else old_head.data

    def __contains__(self, data) -> bool:
        return (self.head is not None) and (data in self.head)

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current
            current = current.next

    def __str__(self) -> str:
        return "[{}]".format(" -> ".join(str(node) for node in self))

    def __repr__(self) -> str:
        return "SinglyLinkedList({})".format(", ".join(str(node) for node in self))
