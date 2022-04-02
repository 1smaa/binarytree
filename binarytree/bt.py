import pickle
import os
import random
import numpy as np
import functools

from telegram import ChosenInlineResult


def arithmetic_error_catcher(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        if not isinstance(args[1], (binarytree.AtomicBinaryTree,)) or args[0].type != args[1].type:
            raise Exception("Binary trees not compatible.")
        try:
            return f(*args, **kwargs)
        except:
            raise Exception("Impossible arithmetic operation.")
    return func


def obj_arithmetic_error_catcher(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        if not isinstance(args[1], (binarytree.ObjectBinaryTree,)) or args[0].type != args[1].type:
            raise Exception("Binary trees not compatible.")
        try:
            return f(*args, **kwargs)
        except:
            raise Exception("Impossible arithmetic operation.")
    return func


def conversion_error_catcher(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            raise Exception("Conversion failed.")
    return func


class binarytree(object):
    def delete(name):
        '''Deletes a binary tree from the storage.'''
        if "storage" not in os.listdir():
            raise Exception("Storage directory non-existent.")
        if "{}.bt".format(name) in os.listdir("storage"):
            os.remove(os.path.join("storage", "{}.bt".format(name)))
        else:
            raise Exception("File not found.")

    class __binarytree(object):
        def __init__(self):
            pass

        def __repr__(self):
            return "{name}\n{structure}".format(name=self.name if self.name else "No Name", structure=str(self._structure))

        def __bool__(self):
            return not self._structure.shape[0] == 0

        def __len__(self):
            return self._structure.shape[0]

        @conversion_error_catcher
        def __list__(self):
            return [node[0] for node in self._structure]

        def store(self, name=None):
            '''Stores the binary tree inside a specified file.'''
            if not name:
                name = self.name if self.name else "".join(
                    [chr(random.randint(97, 122)) for _ in range(10)])
            if "storage" not in os.listdir():
                os.mkdir("storage")
            with open(os.path.join("storage", "{}.bt".format(name)), "wb") as f:
                pickle.dump(self._structure, f)

        def load(self, name=None):
            '''Loads a binary tree from a specified file.'''
            self.__check_file(name)
            with open(os.path.join("storage", "{}.bt".format(name)), "rb") as f:
                self._structure = pickle.load(f)
            if not self.name:
                self.name = name

        def getObject(self):
            '''Returns the tree structure using a matrix.
            The first column is the value of the node, the second is the first child node,
            the third one the second child node.'''
            return self._structure

        def __check_file(self, name=None):
            if not name:
                if self.name:
                    name = self.name
                else:
                    raise Exception("File name needed.")
            if "{}.bt".format(name) not in os.listdir("storage"):
                raise Exception("Binary tree file not found.")

        def _check_node(self, node):
            return isinstance(node, (self.type,)) and (True if self.type is not dict else "key" in node.keys())

    class AtomicBinaryTree(__binarytree):
        def __init__(self, name=None, key_type=int):
            '''Class to create, search, store and load binary trees.
            Specifically created to handle atomic data, such as strings or numbers.'''
            if name:
                self.name = name
            self._structure = np.ndarray((0, 3), key_type)
            self.type = key_type

        @arithmetic_error_catcher
        def __add__(self, bt):
            new = [node[0] for node in bt.getObject()]
            for node in new:
                self.__add_node(np.asscalar(node))
            return self

        @arithmetic_error_catcher
        def __lt__(self, bt):
            return self._structure.shape(0) > bt.getObject().shape[0]

        @arithmetic_error_catcher
        def __gt__(self, bt):
            return self._structure.shape[0] < bt.getObject().shape[0]

        @arithmetic_error_catcher
        def __le__(self, bt):
            return self._structure.shape[0] <= bt.getObject().shape[0]

        @arithmetic_error_catcher
        def __ge__(self, bt):
            return self._structure.shape[0] >= bt.getObject().shape[0]

        @arithmetic_error_catcher
        def __eq__(self, bt):
            new = [node[0] for node in bt.getObject()]
            old = [node[0] for node in self._structure]
            return set(new) == set(old)

        @arithmetic_error_catcher
        def __ne__(self, bt):
            new = [node[0] for node in bt.getObject()]
            old = [node[0] for node in self._structure]
            return set(new) != set(old)

        def add_nodes(*nodes):
            '''Add a finite number of nodes to the binary tree.'''
            if len(nodes) < 2:
                raise Exception("No node was passed to the function.")
            self = nodes[0]
            nodes = nodes[1:]
            for node in nodes:
                if not self._check_node(node):
                    raise Exception(
                        "Can't recognize the value inside the node.")
                try:
                    self.__add_node(node)
                except:
                    raise Exception(
                        "There was an error while adding the node.")

        def __add_node(self, node):
            if self._structure.shape[0] == 0:
                self._structure = np.append(
                    self._structure, [[node, -1, -1]], axis=0)
                return
            chosenNode = 0
            p = -1
            while True:
                if node < self._structure[chosenNode][0]:
                    p = 1
                else:
                    p = 2
                if self._structure[chosenNode][p] == -1:
                    self._structure[chosenNode][p] = self._structure.shape[0]
                    break
                chosenNode = self._structure[chosenNode][p]
            self._structure = np.append(
                self._structure, [[node, -1, -1]], axis=0)

        def find_nodes(*nodes):
            '''Find a finite number of nodes inside the binary tree.

            Returns an array with the result(s) of the research for each node.'''
            if len(nodes) < 2:
                raise Exception("No node was passed to the function.")
            self = nodes[0]
            nodes = nodes[1:]
            results = []
            for node in nodes:
                if not self._check_node(node):
                    raise Exception(
                        "Can't recognized the value inside the node.")
                try:
                    results.append(self.__find_node(node))
                except:
                    raise Exception("Error while exploring the tree.")
            return results if len(results) != 1 else results[0]

        def __find_node(self, node):
            chosenNode = self._structure[0]
            while chosenNode[0] != node:
                if node < chosenNode[0]:
                    chosenNode = self._structure[chosenNode[1]
                                                 ] if chosenNode[1] != -1 else None
                else:
                    chosenNode = self._structure[chosenNode[2]
                                                 ] if chosenNode[2] != -1 else None
                if chosenNode is None:
                    return False
            return True

        def empty(self):
            '''Empty the binary tree.'''
            self._structure = np.ndarray((0, 3), self.type)

        def eliminate(self, node):
            '''Eliminates a specified node from the tree and its subtree.'''
            chosenNode = self._structure[0]
            father, index, pos = 0, 0, 1
            while chosenNode[0] != node:
                father = index
                pos = 1 if node < chosenNode[0] else 2
                index = chosenNode[pos]
                chosenNode = self._structure[chosenNode[pos]
                                             ] if chosenNode[pos] != -1 else None
                if chosenNode is None:
                    raise Exception("Node not found.")
            self._structure[father][pos] = -1
            self._structure = np.delete(self._structure, index, axis=0)

        def subtree(self, node):
            chosenNode = self._structure[0]
            pos = 0
            while node != chosenNode[0]:
                pos = 1 if node < chosenNode[0] else 2
                chosenNode = self._structure[chosenNode[pos]
                                             ] if chosenNode[pos] != -1 else None
                if chosenNode is None:
                    raise Exception("Node not found.")
            new = binarytree.AtomicBinaryTree(
                name="sub_{}".format(self.name), key_type=self.type)
            self.__build(new, chosenNode)
            return new

        def __build(self, new, chosenNode):
            new.add_nodes(chosenNode[0].item())
            if chosenNode[1] != -1:
                self.__build(new, self._structure[chosenNode[1]])
            if chosenNode[2] != -1:
                self.__build(new, self._structure[chosenNode[2]])

    class ObjectBinaryTree(__binarytree):
        def __init__(self, name=None):
            '''Class to create, search, store and load binary trees.
            Nodes must be dictionaries and include a 'key' key.'''
            if name:
                self.name = name
            self._structure = np.ndarray((0, 3), dict)
            self.type = dict

        @obj_arithmetic_error_catcher
        def __add__(self, bt):
            if not isinstance(bt, (binarytree.ObjectBinaryTree,)) or self.type != bt.type:
                raise
            new = [node[0] for node in bt.getObject()]
            for node in new:
                self.__add_node(node)
            return self

        @obj_arithmetic_error_catcher
        def __lt__(self, bt):
            return self._structure.shape[0] > bt.getObject().shape[0]

        @obj_arithmetic_error_catcher
        def __gt__(self, bt):
            return self._structure.shape[0] < bt.getObject().shape[0]

        @obj_arithmetic_error_catcher
        def __le__(self, bt):
            return self._structure.shape[0] <= bt.getObject().shape[0]

        @obj_arithmetic_error_catcher
        def __ge__(self, bt):
            return self._structure.shape[0] >= bt.getObject().shape[0]

        @obj_arithmetic_error_catcher
        def __eq__(self, bt):
            new = [node[0] for node in bt.getObject()]
            old = [node[0] for node in self._structure]
            return set(new) == set(old)

        @obj_arithmetic_error_catcher
        def __ne__(self, bt):
            new = [node[0] for node in bt.getObject()]
            old = [node[0] for node in self._structure]
            return set(new) != set(old)

        def add_nodes(*nodes):
            '''Add a finite number of nodes to the binary tree.'''
            if len(nodes) < 2:
                raise Exception("No node was passed to the function.")
            self = nodes[0]
            nodes = nodes[1:]
            for node in nodes:
                if not self._check_node(node):
                    raise Exception(
                        "Can't recognize the value inside the node.")
                try:
                    self.__add_node(node)
                except:
                    raise Exception(
                        "There was an error while adding the node.")

        def __add_node(self, node):
            if self._structure.shape[0] == 0:
                self._structure = np.append(
                    self._structure, [[node, -1, -1]], axis=0)
                return
            chosenNode = self._structure[0]
            p = -1
            while True:
                if node["key"] < chosenNode[0]["key"]:
                    p = 1
                else:
                    p = 2
                if chosenNode[p] == -1:
                    chosenNode[p] = self._structure.shape[0]
                    break
                chosenNode = self._structure[chosenNode[p]]
            self._structure = np.append(
                self._structure, [[node, -1, -1]], axis=0)

        def find_nodes(*keys):
            '''Find a finite number of nodes inside the binary tree.

            Returns an array with the result(s) of the research for each node.'''
            if len(keys) < 2:
                raise Exception("No node was passed to the function.")
            self = keys[0]
            keys = keys[1:]
            results = []
            for key in keys:
                if not isinstance(key, (int, float, str,)):
                    raise Exception(
                        "Can't recognized the value inside the node.")
                try:
                    results.append(self.__find_node(key))
                except:
                    raise Exception("Error while exploring the tree.")
            return results if len(results) != 1 else results[0]

        def __find_node(self, key):
            chosenNode = self._structure[0]
            while chosenNode[0]["key"] != key:
                if key < chosenNode[0]["key"]:
                    chosenNode = self._structure[chosenNode[1]
                                                 ] if chosenNode[1] != -1 else None
                else:
                    chosenNode = self._structure[chosenNode[2]
                                                 ] if chosenNode[2] != -1 else None
                if chosenNode is None:
                    break
            return chosenNode[0] if chosenNode else None

        def empty(self):
            '''Empty the binary tree.'''
            self._structure = np.ndarray((0, 3), dict)

        def eliminate(self, node):
            '''Eliminates a specified node from the tree and its subtree.'''
            chosenNode = self._structure[0]
            father, index, pos = 0, 0, 1
            while chosenNode[0]["key"] != node:
                if node < chosenNode[0]["key"]:
                    father = index
                    pos = 1
                else:
                    father = index
                    pos = 2
                index = chosenNode[pos]
                chosenNode = self._structure[chosenNode[pos]
                                             ] if chosenNode[pos] != -1 else None
                if chosenNode is None:
                    raise Exception("Node not found.")
            self._structure[father][pos] = -1
            self._structure = np.delete(self._structure, index, axis=0)

        def subtree(self, node):
            chosenNode = self._structure[0]
            pos = 0
            while node != chosenNode[0]["key"]:
                pos = 1 if node < chosenNode[0]["key"] else 2
                chosenNode = self._structure[chosenNode[pos]
                                             ] if chosenNode[pos] != -1 else None
                if chosenNode is None:
                    raise Exception("Node not found.")
            new = binarytree.ObjectBinaryTree(
                name="sub_{}".format(self.name))
            self.__build(new, chosenNode)
            return new

        def __build(self, new, chosenNode):
            new.add_nodes(chosenNode[0])
            if chosenNode[1] != -1:
                self.__build(new, self._structure[chosenNode[1]])
            if chosenNode[2] != -1:
                self.__build(new, self._structure[chosenNode[2]])
