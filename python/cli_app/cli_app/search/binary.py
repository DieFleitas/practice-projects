from data_structures.binary_tree import BinaryTree
from data_structures.queue import Queue

def binary_search(target, root):
    if root:
        if root.data == target:
            return True
        
        if int(root.data) < int(target):
            if binary_search(target, root.right):
                return True
            
        if int(root.data) > int(target):
            if binary_search(target, root.left):
                return True

def search(args):
    bst = BinaryTree()

    print("Building tree...")
    bst.create_bst_from_file(args.file)
    print("Tree build!")

    print("Searching tree...")

    target = args.word

    if binary_search(target, bst.root):
        print("Word found!")
        return
    else:
        print("Word not found :(")
        return