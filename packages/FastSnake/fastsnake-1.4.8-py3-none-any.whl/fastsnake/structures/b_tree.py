from typing import Any, Optional, Tuple


class BTreeNode:
	def __init__(self, leaf = False):
		self.leaf = leaf
		self.keys = []
		self.child = []
		

class BTree:
	"""
	Example:
	
	B = BTree(3)
	
	for i in range(10):
		B.insert((i, 2*i))  # Insert (key, value [any data type])
		
	B.print_tree(B.root, "\n")
	
	B.delete((3,), B.root)
	
	result = B.search(5)

	if result is not None:
		parent_node, index = result
		print("Found!")
	else:
		print("Not found!")

	B.print_tree("\n", B.root)
	"""
	def __init__(self, minimum_degree: int):
		"""
		:param minimum_degree: Order of B Tree (must be greater than or equal to 2)
		"""
		self.root = BTreeNode(True)
		self.t = max(2, minimum_degree)

	def print_tree(self, node: Optional[BTreeNode] = None, l = 0) -> None:
		"""
		Print each level of the tree.
		"""
		if node is None:
			node = self.root

		x = node

		print("Level ", l, " ", len(x.keys), end = ":")
		
		for i in x.keys:
			print(i, end=" ")
			
		print()
		l += 1
		
		if len(x.child) > 0:
			for i in x.child:
				self.print_tree(i, l)
	

	def search(self, key: int, position: Optional[BTreeNode] = None) -> Optional[Tuple[BTreeNode, int]]:
		"""
		Search for a key at a position.
        
		:param key: Key to be searched
		:param position: Node to search from
		
		If 'position' is not specified, then search occurs from root.

		Returns 'None' if 'key' is not found.
		Otherwise returns a tuple of node and index at which the key was found.
		"""
		k = key
		x = position
		
		if x != None:
			i = 0
			while i < len(x.keys) and k > x.keys[i][0]:
				i += 1
			if i < len(x.keys) and k == x.keys[i][0]:
				return (x, i)
			elif x.leaf or i >= len(x.child):
				return None
			else:
				#Search in children
				return self.search(k, x.child[i])
		else:
			#Search entire tree as node not provided
			return self.search(k, self.root)

	def insert(self, key: Tuple[int, Any]) -> None:
		"""
		Calls helper functions to insert a key in the B-Tree.
		
		:param key: Key to be inserted. It must be a tuple (key, value)
		"""
		k = key
		root = self.root
		
		#Keys are full, hence we must split child
		if len(root.keys) == (2 * self.t) - 1:
			temp = BTreeNode()
			self.root = temp
			
			#Former root becomes 0th child of new root 'temp'
			temp.child.insert(0, root)
			self._split_child(temp, 0)
			self._insert_nonfull(temp, k)
		else:
			self._insert_nonfull(root, k)

	def _insert_nonfull(self, x, k):
		"""
		Insert key 'k' at position 'x' in a non-full node

		Arguments:
			x -- Position of node
			k -- key to be inserted
		"""
		
		i = len(x.keys) - 1
		
		if x.leaf:
			x.keys.append((None, None))
			
			while i >= 0 and k[0] < x.keys[i][0]:
				x.keys[i + 1] = x.keys[i]
				i -= 1
			x.keys[i + 1] = k
		else:
			while i >= 0 and k[0] < x.keys[i][0]:
				i -= 1
			i += 1
			
			if len(x.child[i].keys) == (2 * self.t) - 1:
				self._split_child(x, i)
				
				if k[0] > x.keys[i][0]:
					i += 1
			self._insert_nonfull(x.child[i], k)

	def _split_child(self, x, i):
		"""
		Splits the child of node at 'x' from index 'i'

		Arguments:
			x -- parent node of the node to be split
			i -- index value of the child
		"""
		t = self.t
		y = x.child[i]
		
		z = BTreeNode(y.leaf)
		x.child.insert(i + 1, z)
		x.keys.insert(i, y.keys[t - 1])
		
		z.keys = y.keys[t : (2 * t) - 1]
		y.keys = y.keys[0 : t - 1]
		
		if not y.leaf:
			z.child = y.child[t : 2 * t]
			y.child = y.child[0 : t - 1]

	def delete(self, key: Tuple[int, Any], position: Optional[BTreeNode] = None) -> None:
		"""
		Calls helper functions to delete the key after searching from node 'position'

		:param key: Key to be deleted
		:param position: Node, according to whose relative position, helper functions are called
		"""
		if position is None:
			position = self.root

		k = key
		x = position
		
		t = self.t
		i = 0
		
		while i < len(x.keys) and k[0] > x.keys[i][0]:
			i += 1
			
		#Deleting the key if the node is a leaf
		if x.leaf:
			if i < len(x.keys) and x.keys[i][0] == k[0]:
				x.keys.pop(i)
				return
			return
		
		#Calling '_delete_internal_node' when x is an internal node and contains the key 'k'
		if i < len(x.keys) and x.keys[i][0] == k[0] :
			return self._delete_internal_node(x, k, i)
		
		#Recursively calling 'delete' on x's child
		elif len(x.child[i].keys) >= t:
			self.delete(k, x.child[i])	
					
		#Ensuring that a child always has atleast 't' keys
		else:
			if i != 0 and i+2 < len(x.child):
				if len(x.child[i-1].keys) >= t:
					self._delete_sibling(x, i, i-1)
				elif len(x.child[i+1].keys) >= t:
					self._delete_sibling(x, i, i+1)
				else:
					self._del_merge(x, i, i+1)
			elif i == 0: 
				if len(x.child[i+1].keys) >= t:
					self._delete_sibling(x, i, i+1)
				else:
					self._del_merge(x, i, i+1)
			elif i+1 == len(x.child):
				if len(x.child[i-1].keys) >= t:
					self._delete_sibling(x, i, i-1)
				else:
					self._del_merge(x, i, i-1)
			self.delete(k, x.child[i])
	
	def _delete_internal_node(self, x, k, i):
		"""
		Deletes internal node

		Arguments:
			x -- internal node in which key 'k' is present
			k -- key to be deleted
			i -- index position of key in the list
		"""
		t = self.t
		
		#Deleting the key if the node is a leaf
		if x.leaf:
			if x.keys[i][0] == k[0]:
				x.keys.pop(i)
				return
			return

		#Replacing the key with its predecessor and deleting predecessor
		if len(x.child[i].keys) >= t :
			x.keys[i] = self._delete_predecessor(x.child[i])
			return
		
		#Replacing the key with its successor and deleting successor
		elif len(x.child[i+1].keys) >= t:
			x.keys[i] = self._delete_successor(x.child[i+1])
			return
		
		#Merging the child, its left sibling and the key 'k'
		else:
			self._del_merge(x, i, i+1)
			self._delete_internal_node(x.child[i], k, self.t - 1)

	def _delete_predecessor(self, x):
		"""
		Returns and deletes predecessor of key 'k' which is to be deleted

		Arguments:
			x -- node
		"""
		if x.leaf:
			return x.pop()
		
		n = len(x.keys) - 1
		
		if len(x.child[n].keys) >= self.t:
			self._delete_sibling(x, n+1, n)
		else:
			self._del_merge(x, n, n+1)
			
		self._delete_predecessor(x.child[n])

	def _delete_successor(self, x):
		"""
		Returns and deletes successor of key 'k' which is to be deleted

		Arguments:
			x -- node
		"""
		if x.leaf:
			return x.keys.pop(0)
		
		if len(x.child[1].keys) >= self.t:
			self._delete_sibling(x, 0, 1)
		else:
			self._del_merge(x, 0, 1)
			
		self._delete_successor(x.child[0])

	def _del_merge(self, x, i, j):
		"""
		Merges the children of x and one of its own keys

		Arguments:
			x -- parent node
			i -- index of one of the children
			j -- index of one of the children
		"""
		cnode = x.child[i]

		#Merging the x.child[i], x.child[j] and x.keys[i]
		if j > i:			
			rsnode = x.child[j]
			cnode.keys.append(x.keys[i])
			
			#Assigning keys of right sibling node to child node
			for k in range(len(rsnode.keys)):
				cnode.keys.append(rsnode.keys[k])
				
				if len(rsnode.child) > 0:
					cnode.child.append(rsnode.child[k])
					
			if len(rsnode.child) > 0:
				cnode.child.append(rsnode.child.pop())
				
			new = cnode
			
			x.keys.pop(i)
			x.child.pop(j)
			
		#Merging the x.child[i], x.child[j] and x.keys[i]
		else :
			lsnode = x.child[j]
			lsnode.keys.append(x.keys[j])
			
			#Assigning keys of left sibling node to child node
			for i in range(len(cnode.keys)):
				lsnode.keys.append(cnode.keys[i])
				
				if len(lsnode.child) > 0:
					lsnode.child.append(cnode.child[i])
					
			if len(lsnode.child) > 0:
				lsnode.child.append(cnode.child.pop())
				
			new = lsnode
			
			x.keys.pop(j)
			x.child.pop(i)
		
		#If x is root and is empty, then re-assign root
		if x == self.root and len(x.keys) == 0:
			self.root = new

	def _delete_sibling(self, x, i, j):
		"""
		Borrows a key from jth child of x and appends it to ith child of x

		Arguments:
			x -- parent node
			i -- index of one of the children
			j -- index of one of the children
		"""
		cnode = x.child[i]
		
		if i < j:
			#Borrowing key from right sibling of the child
			rsnode = x.child[j]
			cnode.keys.append(x.keys[i])
			
			x.keys[i] = rsnode.keys[0]
			
			if len(rsnode.child)>0:
				cnode.child.append(rsnode.child[0])
				rsnode.child.pop(0)
			rsnode.keys.pop(0)
		else :
			#Borrowing key from left sibling of the child
			lsnode = x.child[j]
			cnode.keys.insert(0,x.keys[i-1])
			
			x.keys[i-1] = lsnode.keys.pop()
			
			if len(lsnode.child)>0:
				cnode.child.insert(0,lsnode.child.pop())
