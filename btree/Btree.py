import math
from .QueuePy import Queue


# Btree node
class BtreeNode(object):
    # Constructor - order, keys, and pointer
    def __init__(self, order, keys=None, pointers=None):
        self._order = order
        self.keys = keys
        self.pointers = pointers

    # Getter for a boolean property to determine if the node is a leaf node
    @property
    def leaf(self):
        return self.pointers is None or len(self.pointers) == 0

    # Search:
    # Input: key to search for in current node
    # Returns:
    #       node: node that the value is in - either self if the key exists or None otherwise
    #       index: index that the value is at within node - None if it doesn't exist
    #       next_node: the pointer to look in to continue searching for the key
    #       index_pointer: index of the pointer to next node or None if there is not a node to go to
    def search(self, key):
        index = len(self.keys) - 1
        while index >= 0 and self.keys[index] >= key:
            index -= 1

        if index + 1 < len(self.keys) and self.keys[index + 1] == key:
            return self, index, None, None

        elif self.pointers is not None and index + 1 < len(self.pointers):
            return None, None, self.pointers[index + 1], index + 1

        else:
            return None, None, None, None

    # Borrow:
    # Input:
    #       left_sibling: left_sibling to borrow from if exists
    #       right_sibling: right_sibling to borrow from if exists
    #       node: node that needs to be merged to the others
    #       middle_left: parent key between node and left_sibling
    #       middle_right: parent key between node and right_sibling
    # Output:
    #       borrowed_value: value borrowed from sibling
    #       is_left: True if the sibling borrowed from is left - false otherwise
    def borrow(self, left_sibling, right_sibling, node, middle_left, middle_right):
        min_keys = int(math.ceil(self._order / 2)) - 1

        if left_sibling is not None and len(left_sibling.keys) > min_keys + 1:
            node.keys.insert(0, middle_left)
            borrowed_value = left_sibling.keys.pop(len(left_sibling.keys) - 1)
            return borrowed_value, True

        elif right_sibling is not None and len(right_sibling.keys) > min_keys + 1:
            node.keys.append(middle_right)
            borrowed_value = right_sibling.keys.pop(0)
            return borrowed_value, False

        else:
            return None, False

    # remove_key_from_leaf
    # Input: key - key to remove
    # Output: underflow: boolean if underflow error results
    def remove_key_from_leaf(self, key):
        index = 0
        while index < len(self.keys) and self.keys[index] < key:
            index += 1

        if index != len(self.keys) and self.keys[index] == key:
            self.keys.pop(index)
            min_number = int(math.ceil(self._order / 2)) - 1

            if len(self.keys) <= min_number:
                return True

            else:
                return None

        else:
            print("Key does not exist to delete")

    # replace_key_with_key
    # Input:
    #       key: key to replace
    #       new_key: new_key to replace the key with
    def replace_key_with_key(self, key, new_key):
        index = 0
        while index < len(self.keys) and self.keys[index] < key:
            index += 1

        if key == self.keys[index]:
            self.keys[index] = new_key
        else:
            print("Error: Key does not exist to replace")

    # add_key_to_leaf
    # input: key to add
    # Output:
    #       left_node: left_node after overflow - None if no overflow
    #       median: median key
    #       right_node: right_node after overflow
    def add_key_to_leaf(self, key):
        index = 0
        while index < len(self.keys) and self.keys[index] < key:
            index += 1

        if index == len(self.keys):
            self.keys.append(key)

        elif self.keys[index] == key:
            print("Warning - duplicate key - will not add")

        else:
            self.keys.insert(index, key)

        if len(self.keys) == self._order:
            median = int(math.ceil(self._order / 2.0)) - 1
            return BtreeNode(self._order, self.keys[0:median]), self.keys[median], \
                   BtreeNode(self._order, self.keys[median + 1: len(self.keys)])

        else:
            return None, None, None

    # add_key
    # Input:
    #       key: key to add
    #       left: left pointer to add
    #       right: right pointer to append
    # Output:
    #       left_node: left_node after overflow - None if no overflow
    #       median: median key
    #       right_node: right_node after overflow
    def add_key(self, key, left, right):
        index = 0
        while index < len(self.keys) and self.keys[index] < key:
            index += 1

        if index == len(self.keys):
            self.keys.append(key)
            self.pointers.append(right)
            self.pointers[index] = left

        elif self.keys[index] == key:
            print("Warning: duplicate key - will not add")

        else:
            self.keys.insert(index, key)
            self.pointers.insert(index, left)
            self.pointers[index + 1] = right

        if len(self.keys) == self._order:
            median = int(math.ceil(self._order / 2.0)) - 1
            return BtreeNode(self._order, self.keys[0:median], self.pointers[0:median + 1]), self.keys[median], \
                   BtreeNode(self._order, self.keys[median + 1: len(self.keys)],
                             self.pointers[median + 1: len(self.pointers)])

        else:
            return None, None, None


# Btree class
class Btree(object):
    # Init: with order
    def __init__(self, order):
        self._root = None
        self._order = order

    # find: public - find with input key
    # Output: return if key exists
    def find(self, key):
        return self._find(key, self._root)

    # find: private - find with input key and node to search in
    # Output: return if key exists
    def _find(self, key, node):
        search_node, index, next_node, trash = node.search(key)
        if index is not None:
            return True
        elif next_node is not None:
            return self._find(key, next_node)
        else:
            return False

    # delete: public - delete key stored in input
    def delete(self, key):
        if self._root is None:
            print("Error: There is nothing to delete")
        elif self.find(key) is False:
            print("Key does not exist to delete")
        else:
            self._delete_key(key, self._root)
            if len(self._root.keys) == 0:
                if len(self._root.pointers) == 1:
                    self._root = self._root.pointers[0]
                else:
                    print("Error in Btree: this should not happen")

    # delete_key: input - key to delete and node to delete from
    # Output:
    #       removed_key: True if removed key - none otherwise
    #       underflow_error: True if underflow_error results - False otherwise
    def _delete_key(self, key, node):
        search_node, index, next_node, index_super = node.search(key)
        if index is not None:
            if search_node.leaf is True:
                return search_node.remove_key_from_leaf(key), False
            else:
                predecessor = self._immediate_predecessor(key, search_node)
                self.delete(predecessor)
                search_node.replace_key_with_key(key, predecessor)
                return False, False

        else:
            if next_node is not None:
                underflow, handle_borrow_above = self._delete_key(key, next_node)

                if underflow:
                    self._borrow_or_combine(node, index_super, next_node)

                min_keys = (int(math.ceil(self._order / 2)) - 1)
                if underflow is None and handle_borrow_above:
                    for index in range(0, len(node.pointers)):
                        pointer = node.pointers[index]
                        if len(pointer.keys) <= min_keys:
                            self._borrow_or_combine(node, index, pointer)
                            break

                if len(node.keys) <= min_keys:
                    return None, True
                else:
                    return None, False

    # immediate_predecessor - input - key and node to search for pred in
    # output: value of immediate predecessor
    def _immediate_predecessor(self, key, node):
        index = 0
        while index < len(node.keys):
            if len(node.pointers) > index:
                if node.keys[index] == key:
                    break
            else:
                print("Error in Btree: this should not happen")
                break
            index += 1


        pointer = node.pointers[index]

        while pointer.pointers is not None:
            pointer = pointer.pointers[len(pointer.pointers) - 1]

        return pointer.keys[len(pointer.keys) - 1]

    # borrow_or_combine - either borrows value from sibling or combines two together
    # Input:
    #       node: parent of node with underflow issue
    #       index_super: index of the node within super node
    #       next_node: node with underflow issue
    def _borrow_or_combine(self, node, index_super, next_node):
        if index_super > 0 and (index_super < len(node.pointers) - 1):
            borrow_result, go_left = node.borrow(node.pointers[index_super - 1], node.pointers[index_super + 1],
                                                 next_node, node.keys[index_super - 1], node.keys[index_super])
            if borrow_result is not None:
                if go_left:
                    node.keys[index_super - 1] = borrow_result
                else:
                    node.keys[index_super] = borrow_result
            else:
                self._combine(node.pointers[index_super - 1], node.keys[index_super - 1],
                              node.pointers[index_super], node)

        elif index_super < len(node.pointers) - 1:
            borrow_result, go_left = node.borrow(None, node.pointers[index_super + 1], next_node, None,
                                                 node.keys[index_super])

            if borrow_result is not None:
                node.keys[index_super] = borrow_result
            else:
                self._combine(node.pointers[index_super + 1], node.keys[index_super],
                              node.pointers[index_super], node)

        else:
            borrow_result, go_left = node.borrow(node.pointers[index_super - 1], None, next_node,
                                                 node.keys[index_super - 1], None)

            if borrow_result is not None:
                node.keys[index_super] = borrow_result
            else:
                self._combine(node.pointers[index_super - 1], node.keys[index_super - 1],
                              node.pointers[index_super], node)

    # combine - combines two nodes
    # Input:
    #       node: node to combine with
    #       middle: middle key between combining nodes
    #       small_node: node with underflow error
    #       parent_node: parent of sibling nodes
    def _combine(self, node, middle, small_node, parent_node):
        node.add_key_to_leaf(middle)

        if small_node.pointers is not None and len(small_node.pointers) > 0:
            if node.keys[0] == middle:
                for pointer in reversed(small_node.pointers):
                    node.pointers.insert(0, pointer)
            else:
                for pointer in small_node.pointers:
                    node.pointers.append(pointer)

        for key in small_node.keys:
            node.add_key_to_leaf(key)

        for index in range(0, len(parent_node.keys)):
            if parent_node.keys[index] == middle:
                if parent_node.pointers[index] is node:
                    parent_node.keys.pop(index)
                    parent_node.pointers.pop(index + 1)
                    break
                else:
                    parent_node.keys.pop(index)
                    parent_node.pointers.pop(index)
                    break

    # insert - insert input value
    def insert(self, value):
        if self._root is None:
            self._root = BtreeNode(self._order, [value])
        else:
            left, median, right = self.insert_value(value, self._root)
            if left is not None:
                self._root = BtreeNode(self._order, [median], [left, right])

    # insert_value - input and node to insert into
    # Output:
    #       search_node: node that the value is in - either self if the key exists or None otherwise
    #       index: index that the value is at within node - None if it doesn't exist
    #       next_node: the pointer to look in to continue searching for the key
    #       index_pointer: index of the pointer to next node or None if there is not a node to go
    #           to - often put in trash
    def insert_value(self, value, node):
        if node.leaf is True:
            return node.add_key_to_leaf(value)

        else:
            search_node, index, next_node, trash = node.search(value)
            if next_node is not None:
                search_node, index, next_node_new, trash = next_node.search(value)

                if next_node_new is not None:
                    left, median, right = self.insert_value(value, next_node)

                    if left is not None:
                        return node.add_key(median, left, right)

                    else:
                        return left, median, right

                else:
                    left, median, right = self.insert_value(value, next_node)
                    if left is not None:
                        return node.add_key(median, left, right)

                    else:
                        return left, median, right
            else:
                return node.add_key_to_leaf(value)

    # print_tree
    # doesn't do anything but print using level traversal
    def print_tree(self):
        output = ""
        queue = Queue()
        queue.enqueue(self._root)

        while queue.is_empty() is False:
            node = queue.dequeue()
            for key in node.keys:
                output += str(key) + " "

            if node.pointers:
                for pointer in node.pointers:
                    queue.enqueue(pointer)

        print(output)
