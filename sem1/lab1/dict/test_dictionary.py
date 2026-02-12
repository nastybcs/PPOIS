import unittest
from Dict import Node, Dictionary

class TestDictionary(unittest.TestCase):
    def setUp(self):
        self.d=Dictionary()
        self.d.append(Node("apple","яблоко"))
        self.d.append(Node("banana","банан"))
        self.d.append(Node("cherry","вишня"))
    def test_iadd_operator_direct(self):
        d = Dictionary()
        d += Node("kiwi", "киви")
        self.assertEqual(d.get_size(), 1)
        self.assertEqual(d["kiwi"], "киви")
    def test_append_to_empty(self):
        d = Dictionary()
        node = Node("first", "первый")
        d.append(node)
        self.assertEqual(d.root.eng, "first")
        self.assertEqual(d.get_size(), 1)


    def test_append_and_size(self):
        self.assertEqual(self.d.get_size(),3)
        self.d.append(Node("orange","апельсин"))
        self.assertEqual(self.d.get_size(), 4)
    def test_find_and_append(self):
        d = Dictionary()
        node = Node("apple", "яблоко")
        d.append(node)
        self.assertEqual(d.get_size(), 1)
        node_found, parent, found = d._Dictionary__find(d.root, None, "apple")
        self.assertTrue(found)
        self.assertEqual(node_found.eng, "apple")

    def test_getitem_and_setitem(self):
        self.assertEqual(self.d["banana"], "банан")
        self.d["banana"]="бананчик"
        self.assertEqual(self.d["banana"], "бананчик")
    
    def test_getitem_not_found(self):
        self.assertIsNone(self.d["lemon"])
    
    def test_setitem_not_found(self):
        result=self.d.__setitem__("lemon",None)
        self.assertIsNone(result)
    
    def test_iadd_operator(self):
        self.d +=Node("village","деревня")
        self.assertEqual(self.d.get_size(), 4)
    
    def test_isub_operator(self):
        self.d-=Node("banana","банан")
        self.assertEqual(self.d.get_size(),2)
        self.assertIsNone(self.d["banana"])
    
    def test_del_leaf(self):
        self.d.del_node(Node("banana","банан"))
        self.assertEqual(self.d.get_size(), 2)
        self.assertIsNone(self.d["banana"])

    def test_del_one_child(self):
        d= Dictionary()
        d+=(Node("mango","манго"))
        d+=(Node("kiwi","киви"))
        d.del_node(Node("mango","манго"))
        self.assertEqual(d.get_size(),1)
        self.assertEqual(d["kiwi"],"киви")
    def test_del_two_children(self):
        self.d.del_node(Node("apple","яблоко"))
        self.assertEqual(self.d.get_size(),2)
        self.assertIsNone(self.d["apple"])
        self.assertIn(self.d["banana"],["банан","вишня"])
        self.assertIn(self.d["cherry"],["банан","вишня"])
    def test_del_not_found(self):
        result=self.d.del_node(Node("ggg","&&&"))
        self.assertIsNone(result)
        self.assertEqual(self.d.get_size(),3)
    
    def test_del_one_child_right_none(self):
        d = Dictionary()
        root = Node("root", "корень")
        child = Node("child", "ребенок")   
        left = Node("left", "левый")
        child.left = left
        root.right = child                  
        d.root = root

        d._Dictionary__del_one_child(child, root)

   
        self.assertEqual(root.right.eng, "left")
        self.assertIsNone(left.left)

    def test_del_leaf_root(self):
        d = Dictionary()
        node = Node("root", "корень")
        d.root = node
        d._Dictionary__del_leaf(node, None)
        self.assertIsNone(d.root)
    def test_del_node_leaf(self):
        d = Dictionary()
        node = Node("x", "икс")
        d.append(node)
        removed = d.del_node(Node("x", "икс"))
        self.assertEqual(removed.eng, "x")
        self.assertIsNone(d["x"])
        self.assertEqual(d.get_size(), 0)
    def test_find_min(self):
        d = Dictionary()
        d.append(Node("m", "м"))
        d.append(Node("a", "а"))
        d.append(Node("z", "з"))

        min_node, min_parent = d._Dictionary__find_min(d.root, None)
        self.assertEqual(min_node.eng, "a")    
        self.assertEqual(min_parent.eng, "m")   

   
        d2 = Dictionary()
        d2.append(Node("only", "только"))

        min_node2, min_parent2 = d2._Dictionary__find_min(d2.root, None)
        self.assertEqual(min_node2.eng, "only")
        self.assertIsNone(min_parent2)
    def test_del_leaf_and_one_child(self):
        d = Dictionary()
        root = Node("root", "корень")
        leaf = Node("leaf", "лист")
        root.left = leaf
        d.root = root
        d._Dictionary__del_leaf(leaf, root)
        self.assertIsNone(root.left)
        child = Node("child", "ребенок")
        root.right = child
        d._Dictionary__del_one_child(child, root)
        self.assertIsNone(root.right)
    

    def test_readfromfile(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as f:
            f.write("dog, собака\ncat, кошка\n\nwrong_line\n")
            fname = f.name
        d = Dictionary()
        d.readfromfile(fname)
        os.remove(fname)
        self.assertEqual(d.get_size(), 2)
        self.assertEqual(d["dog"], "собака")
        self.assertEqual(d["cat"], "кошка")

    def test_readfromfile_not_found(self):
        d = Dictionary()
        d.readfromfile("файла_нет.txt")
    def test_readfromfile_empty(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as f:
            fname = f.name
        d = Dictionary()
        d.readfromfile(fname)
        os.remove(fname)
        self.assertEqual(d.get_size(), 0)


    def test_del_one_child_root_left(self):
        d = Dictionary()
        root = Node("root", "корень")
        child = Node("child", "ребенок")
        root.left = child
        d.root = root
        d._Dictionary__del_one_child(root, None)
        self.assertEqual(d.root.eng, "child")

    def test_del_one_child_root_right(self):
        d = Dictionary()
        root = Node("root", "корень")
        child = Node("child", "ребенок")
        root.right = child
        d.root = root
        d._Dictionary__del_one_child(root, None)
        self.assertEqual(d.root.eng, "child")

  

    

    

        


    

    