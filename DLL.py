class Node:
    # class of the items in the DLL
    def __init__(self, next=None, prev=None, data=None):
        self.next = next
        self.prev = prev
        self.data = data

    # string representation used for debugging
    def __str__(self) -> str:
        return self.data


class DoubleLinkedList:
    head = None
    tail = None

    # string representation for easier debugging
    def __str__(self) -> str:
        current_node = self.head
        output = "DLL: {"
        len_list = 0

        while current_node is not None:
            string_to_add = current_node.data.__str__()
            output += string_to_add + ", "
            len_list += 1
            current_node = current_node.next

        return "len: " + str(len_list) + "  " + output[:len(output)-2] + "}"

    # return iterable object of DLL
    def __iter__(self):
        self.current_node = self.head
        return self

    # return next in iteration
    def __next__(self):
        if self.current_node == self.tail:
            current_data = self.current_node.data
            self.current_node = Node(None,None,"stop")
            return  current_data
        if self.current_node.next is not None:
            current_data = self.current_node.data
            self.current_node = self.current_node.next
            return current_data
        else:
            raise StopIteration

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
        # if old_node is not an instance of node try finding it as data in the DLL
        if not isinstance(old_node, Node):
            old_node = self.find(old_node)

        new_node = Node(None, None, data)

        if old_node is not None:
            new_node.next = old_node.next
            new_node.prev = old_node

            old_node.next = new_node

            new_node.next.prev = new_node

            return new_node
        else:
            return "ERROR: could not find the item old_node in list"


    """ add an element before old_node """

    def add_before(self, data, old_node):
        # if old_node is not an instance of node try finding it as data in the DLL
        if not isinstance(old_node, Node):
            old_node = self.find(old_node)

        new_node = Node(None, None, data)

        if old_node is not None:
            new_node.next = old_node
            new_node.prev = old_node.prev

            old_node.prev = new_node

            new_node.prev.next = new_node

            return new_node
        else:
            return "ERROR: could not find the item old_node in list"

    """ remove an element from the list """

    def remove(self, removable_node):
        # if removable_node is not an instance of node try finding it as data in the DLL
        if not isinstance(removable_node, Node):
            removable_node = self.find(removable_node)

        if removable_node is not None:
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
        else:
            return "ERROR: could not find the item removable_node in list"

    def find(self, data):
        current_node = self.head

        while current_node is not None:
            if current_node.data == data:
                return current_node
            current_node = current_node.next

        return None

