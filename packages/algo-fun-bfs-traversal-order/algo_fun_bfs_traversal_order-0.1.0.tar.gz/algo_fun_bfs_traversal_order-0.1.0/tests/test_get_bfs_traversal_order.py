#!/!usr/bin/env python
__program__ = "test_get_bfs_traversal_order"
__description__ = "test the get_bfs_traversal_order function" 
__date__ = "25/04/24"
__author__ = "Christophe Lagaillarde"
__version__ = "1.0"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2024 Christophe Lagaillarde"

import sys
sys.path.append('../')
from algo_fun.get_bfs_traversal_order import get_bfs_traversal_order

def test_get_bfs_traversal_order() -> None:
	graph_1: dict[str, list[str]] = {
	    'A': ['B', 'C'],
	    'B': ['D', 'E'],
	    'C': ['F', 'G'],
	    'D': [],
	    'E': [],
	    'F': [],
	    'G': []
	}
	expected_traversal_order_1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

	graph_2: dict[str, list[str]] = {
	    'A': ['B', 'C'],
	    'B': ['D', 'E'],
	    'C': ['F', 'G'],
	    'D': [],
	    'E': ['H'],
	    'F': [],
	    'G': [],
	    'H': []
	}
	expected_traversal_order_2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

	graph_3: dict[str, list[str]] = {
	    'A': ['B', 'C'],
	    'B': ['D', 'E'],
	    'C': ['F', 'G'],
	    'D': ['H', 'I'],
	    'E': [],
	    'F': [],
	    'G': [],
	    'H': [],
	    'I': []
	}
	expected_traversal_order_3 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

	graph_4: dict[str, list[str]]= {
	    'A': ['B', 'C'],
	    'B': ['D'],
	    'C': ['E'],
	    'D': ['F'],
	    'E': ['G'],
	    'F': [],
	    'G': []
	}
	expected_traversal_order_4 = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

	graph_5: dict[str, list[str]] = {
	    'A': ['B', 'C'],
	    'B': ['D', 'E'],
	    'C': ['F'],
	    'D': ['G'],
	    'E': [],
	    'F': ['H'],
	    'G': [],
	    'H': []
	}
	expected_traversal_order_5 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

	graph_6: dict[str, list[str]] = {
	    'A': ['B', 'C'],
	    'B': ['D', 'E'],
	    'C': ['F', 'G'],
	    'D': ['H'],
	    'E': ['I'],
	    'F': [],
	    'G': [],
	    'H': [],
	    'I': []
	}
	expected_traversal_order_6 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
	
	assert get_bfs_traversal_order(graph_1) == expected_traversal_order_1
	assert get_bfs_traversal_order(graph_2) == expected_traversal_order_2
	assert get_bfs_traversal_order(graph_3) == expected_traversal_order_3
	assert get_bfs_traversal_order(graph_4) == expected_traversal_order_4
	assert get_bfs_traversal_order(graph_5) == expected_traversal_order_5
	assert get_bfs_traversal_order(graph_6) == expected_traversal_order_6

	return None

if __name__ == '__main__':
	test_get_bfs_traversal_order()
