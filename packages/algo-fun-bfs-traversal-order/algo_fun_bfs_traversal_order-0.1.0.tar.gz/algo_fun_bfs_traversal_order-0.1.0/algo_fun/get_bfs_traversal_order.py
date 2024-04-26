#!/!usr/bin/env python
__program__ = "get_bfs_traversal_order.py"
__description__ = "Get the bfs traversal order of a given graph"
__date__ = "25/04/2024"
__author__ = "Christophe Lagaillarde"
__version__ = "1.0"
__license__ = "MIT License"
__copyright__ = "Copyright 2024 (c) Christophe Lagaillarde"

def get_bfs_traversal_order(graph: dict[str, list[str]]) -> list: 
	queue: list[str] = []
	traversal_order: list[str] = []
	node: str = next(iter(graph))
	queue.append(node)

	while queue:
		traversal_order.append(queue[0])
		queue.pop(0)
		queue.extend(graph.get(node, []))
		
		if queue:
			node = queue[0] 

	return traversal_order

if __name__ == '__main__':

	import sys

	user_input_graph: dict[list] = {}

	for arg in sys.argv[1:]:
		key, values = arg.split(':')
		user_input_graph[key] = values.split(',')
	
	print(get_bfs_traversal_order(user_input_graph))
