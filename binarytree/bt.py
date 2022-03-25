import pickle
import os
import random


class BinaryTree(object):
    def __init__(self, name=None):
        '''Class to create, search, store and load binary trees.'''
        self.__structure = None
        self.__name = name

    def add_nodes(*nodes):
        '''Add a finite number of nodes to the binary tree.'''
        if len(nodes) < 2:
            raise Exception("No node was passed to the function.")
        self = nodes[0]
        nodes = nodes[1:]
        for node in nodes:
            if not self.__check_node(node):
                raise Exception("Can't recognized the value inside the node.")
            try:
                self.__add_node(node)
            except:
                raise Exception("There was an error while adding the node.")

    def __check_node(self, node):
        return isinstance(node, (int, str,))

    def __add_node(self, node):
        if not self.__structure:
            self.__structure = [[node, -1, -1]]
            return
        chosenNode = self.__structure[0]
        p = -1
        while True:
            if node < chosenNode[0]:
                p = 1
            else:
                p = 2
            if chosenNode[p] == -1:
                chosenNode[p] = len(self.__structure)
                break
            chosenNode = self.__structure[chosenNode[p]]
        self.__structure.append([node, -1, -1])

    def find_nodes(*nodes):
        '''Find a finite number of nodes inside the binary tree.

        Returns an array with the result(s) of the research for each node.'''
        if len(nodes) < 2:
            raise Exception("No node was passed to the function.")
        self = nodes[0]
        nodes = nodes[1:]
        results = []
        for node in nodes:
            if not self.__check_node(node):
                raise Exception("Can't recognized the value inside the node.")
            try:
                results.append(self.__find_node(node))
            except:
                raise Exception("Error while exploring the tree.")
        return results if len(results) != 1 else results[0]

    def __find_node(self, node):
        chosenNode = self.__structure[0]
        while chosenNode[0] != node:
            if node < chosenNode[0]:
                chosenNode = self.__structure[chosenNode[1]
                                              ] if chosenNode[1] != -1 else None
            else:
                chosenNode = self.__structure[chosenNode[2]
                                              ] if chosenNode[2] != -1 else None
            if not chosenNode:
                return False
        return True

    def store(self, name=None):
        '''Stores the binary tree inside a specified file.'''
        if not name:
            name = self.__name if self.__name else "".join(
                [chr(random.randint(97, 122)) for _ in range(10)])
        with open(os.path.join("storage", "{}.bt".format(name)), "wb") as f:
            pickle.dump(self.__structure, f)

    def load(self, name=None):
        '''Loads a binary tree from a specified file.'''
        self.__check_file(name)
        with open(os.path.join("storage", "{}.bt".format(name)), "rb") as f:
            self.__structure = pickle.load(f)

    def delete(self, name=None):
        '''Deletes a binary tree from the storage.'''
        self.__check_file(name)
        os.remove(os.path.join("storage", "{}.bt".format(name)))

    def __check_file(self, name):
        if not name:
            raise Exception("File name needed.")
        if "{}.bt".format(name) not in os.listdir("storage"):
            raise Exception("Binary tree file not found.")


bn = BinaryTree()
