class Node:
    # class of the items in
    def __init__(self, next=None, prev=None, data=None):
        self.next = next
        self.prev = prev
        self.data = data

    def __str__(self) -> str:
        return self.data


class DLL:
    head = None
    tail = None

    def __str__(self) -> str:
        current_node = self.head
        output = "DLL {"

        while current_node is not None:
            output += current_node.data + ", "
            current_node = current_node.next

        return output[:len(output)-2] + "}"

    # add element to the end of the double linked list
    def append(self, data):
        new_node = Node(None, None, data)

        # check whether DLL has a head if yes add new_node as tail if no make new node head and tail
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            new_node.next = None
            self.tail.next = new_node
            self.tail = new_node

        return new_node

    """ add element to the start of the DLL """

    def add_begin(self, data):
        new_node = Node(None, None, data)

        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node = Node(self.head, None, data)
            self.head.prev = new_node
            self.head = new_node

        return new_node

    """ add an element after old_node (if this is a Node """
    def add_after(self, data, old_node):
        if not isinstance(old_node, Node):
            old_node = self.find(old_node)

        new_node = Node(None, None, data)

        new_node.next = old_node.next
        new_node.prev = old_node

        old_node.next = new_node

        new_node.next.prev = new_node

        return new_node

    """ add an element before old_node """

    def add_before(self, data, old_node):
        if not isinstance(old_node, Node):
            old_node = self.find(old_node)
        new_node = Node(None, None, data)

        new_node.next = old_node
        new_node.prev = old_node.prev

        old_node.prev = new_node

        new_node.prev.next = new_node

        return new_node

    """ remove an element from the list """

    def remove(self, removable_node):
        if not isinstance(removable_node, Node):
            removable_node = self.find(removable_node)

        if removable_node.prev is None:
            self.head = removable_node.next
            removable_node.next.prev = None
        if removable_node.prev is not None:
            removable_node.prev.next = removable_node.next
        if removable_node.next is None:
            self.tail = removable_node.prev
            removable_node.prev.next = None
        else:
            removable_node.next.prev = removable_node.prev

    def find(self, data):
        current_node = self.head

        while current_node is not None:
            if current_node.data == data:
                return current_node
            current_node = current_node.next

        return None
