class Node:
    def __init__(self, eng, rus):
        self.eng=eng
        self.rus=rus
        self.left=None
        self.right=None
class Dictionary:
    def __init__(self):
        self.root=None
        self._size=0
    def __find(self,node,parent,eng):
        if node is None: 
            return None, parent, False
        if eng == node.eng:
            return node,parent,True
        if eng < node.eng:
            if node.left:
                return self.__find(node.left, node, eng)
        if eng > node.eng:
            if node.right:
                return self.__find(node.right, node, eng)
        return node, parent, False 
    def append(self, word):
        if self.root is None:
            self.root=word
            self._size +=1
            return word
        node, parent, fl_find=self.__find(self.root,None, word.eng)
        if not fl_find and node:
            if word.eng< node.eng:
                node.left = word
            else:
                node.right=word
            self._size+=1   
        return word
    def __iadd__(self,other):
        self.append(other)
        return self
    def show_tree(self, node):
        if node is None:
            return 
        self.show_tree(node.left)
        print(f"{node.eng}: {node.rus}")
        self.show_tree(node.right)
    def __del_leaf(self,node, parent):
        if parent is None:
            self.root=None
            return
        if parent.left==node:
            parent.left=None
        elif parent.right==node:
            parent.right=None
    def __del_one_child(self,node, parent):
        if node.left is not None and node.right is None:
            child= node.left  
        elif node.right is not None and node.left is None:
            child= node.right 
        if parent is None:
            self.root= child
            return
        if parent.left == node:
            if node.left is None:
                parent.left=node.left
            elif node.right is None:
                parent.left=node.left
        elif parent.right==node:
            if node.left is None:
                parent.right=node.right
            elif node.right is None:
                parent.right=node.left
    def __find_min(self,node, parent):
        if node.left:
            return self.__find_min(node.left,node)
        return node, parent
    def del_node(self, word):
        node, parent,fl_find=self.__find(self.root,None, word.eng)
        if not fl_find:
            return None
        self._size -=1
        if node.left is None and node.right is None:
            self.__del_leaf(node,parent)
        elif node.left is None or node.right is None:
            self.__del_one_child(node, parent)  
        else: 
            noder,parentr=self.__find_min(node.right, node)
            node.eng=noder.eng
            node.rus=noder.rus
            self.__del_one_child(noder,parentr)
        return node
    def __isub__(self,other):
        self.del_node(other)
        return self
    def __getitem__(self,key):
        node,parent,fl_find=self.__find(self.root, None, key)
        if fl_find:
           return node.rus
    def __setitem__(self, key, new_rus):
       node,parent,fl_find=self.__find(self.root,None, key)
       if fl_find:
           node.rus=new_rus
           return 
    def get_size(self):
        return self._size
    def readfromfile(self, filename):
        try:
            with open(filename,'r', encoding='utf-8') as file: 
                for line in file:
                    line=line.strip()
                    if not line:
                        continue
                    try:
                        eng, rus = line.split(',',1)
                        eng = eng.strip()
                        rus = rus.strip()
                        self.append(Node(eng, rus)) 
                    except ValueError:
                       print(f"Пропуск строки: некорректный формат строки '{line}'")
                    continue
        except FileNotFoundError:
            print (f"Файл '{filename}' не найден")
        except Exception as e:
            print (f"Ошибка при чтении файла:  {e}")
        

