import argparse
from search import breadth_first, depth_first, binary

def main():
    parser = argparse.ArgumentParser(description="Search for word in file")

    parser.add_argument("-w", "--word", required=True, help="Word to be search for")

    parser.add_argument("-f", "--file", required=True, help="Path to file that is to be searched")

    parser.add_argument("-sa", "--search-algorithm", choices=["binary-search", "depth-first-search", "breadth-first-search"], required=True, help="The algorithm to be used to search the file")

    parser.add_argument("-o", "--order", choices=["pre-order", "post-order", "in-order", "level-order"], required=True, help="Order in wich to traverse the tree")

    args = parser.parse_args()

    if args.search_algorithm == "depth-first-search":
        depth_first.search(args)
        return
    
    if args.search_algorithm == "breadth-first-search":
        breadth_first.search(args)
        return
    
    if args.search_algorithm == "binary-search":
        binary.search(args)
        return

if __name__ == "__main__":
    main()