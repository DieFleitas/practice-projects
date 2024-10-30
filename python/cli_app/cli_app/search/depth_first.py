from data_structures.binary_tree import BinaryTree
from data_structures.queue import Queue

def pre_order_search(target, root):
    if root:
        if root.data == target:
                return True
        
        if pre_order_search(target, root.left):
            return True
        
        if pre_order_search(target, root.right):
            return True
        
    return False
            
            

def search(args):
    bt = BinaryTree()

    print("Building tree...")
    bt.create_from_file(args.file)
    print("Tree Built!")

    if args.order == "pre-order":
        print("Searching tree...")
        target = args.word

        if pre_order_search(target, bt.root):
            print("Word found!")
        else:
            print("Word not found :(")
    
    # print("depth-first-search can only be used with --order 'pre-order'")