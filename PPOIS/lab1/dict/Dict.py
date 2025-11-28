from node import Node
class Dictionary:
    """
    @brief Класс двоичного дерева поиска для англо-русского словаря.

    Поддерживает добавление, удаление, поиск слов, чтение из файла и отображение дерева.
    """
    
    def __init__(self):
        """
        @brief Конструктор словаря.
        """
        self.root = None     
        self._size = 0       

    def __find(self, node, parent, eng):
        """
        @brief Рекурсивный поиск узла по английскому слову.
        @param node Текущий узел.
        @param parent Родитель текущего узла.
        @param eng Искомое английское слово.
        @return Кортеж (найденный узел, его родитель, флаг_найдено)
        """
        if node is None:
            return None, parent, False
        if eng == node.eng:
            return node, parent, True
        if eng < node.eng and node.left:
            return self.__find(node.left, node, eng)
        if eng > node.eng and node.right:
            return self.__find(node.right, node, eng)
        return node, parent, False
    
    def append(self, word):
        """
        @brief Добавляет новый элемент в словарь.
        @param word Узел класса Node с парой (английское слово, перевод).
        @return Добавленный узел.
        """
        if self.root is None:
            self.root = word
            self._size += 1
            return word

        node, parent, fl_find = self.__find(self.root, None, word.eng)
        if not fl_find and node:
            if word.eng < node.eng:
                node.left = word
            else:
                node.right = word
            self._size += 1
        return word
    
    def __iadd__(self, other):
        """
        @brief Оператор += для добавления нового слова.
        @param other Узел класса Node.
        @return Текущий словарь с добавленным словом.
        """
        self.append(other)
        return self
    
    def show_tree(self, node):
        """
        @brief Рекурсивный симметричный обход дерева с выводом словаря.
        @param node Текущий узел дерева.
        """
        if node is None:
            return
        self.show_tree(node.left)
        print(f"{node.eng}: {node.rus}")
        self.show_tree(node.right)

    def __del_leaf(self, node, parent):
        """
        @brief Удаляет лист (узел без потомков).
        @param node Удаляемый узел.
        @param parent Родитель удаляемого узла.
        """
        if parent is None:
            self.root = None
            return
        if parent.left == node:
            parent.left = None
        elif parent.right == node:
            parent.right = None

    def __del_one_child(self, node, parent):
        """
        @brief Удаляет узел с одним потомком, сохраняя структуру дерева.
        @param node Удаляемый узел.
        @param parent Родитель удаляемого узла.
        """
        if node.left is not None and node.right is None:
            child = node.left
        elif node.right is not None and node.left is None:
            child = node.right

        if parent is None:
            self.root = child
            return

        if parent.left == node:
            if node.left is None:
                parent.left = node.right
            else:
                parent.left = node.left
        elif parent.right == node:
            if node.left is None:
                parent.right = node.right
            else:
                parent.right = node.left

    def __find_min(self, node, parent):
        """
        @brief Находит минимальный элемент в правом поддереве (для удаления узла с двумя потомками).
        @param node Корень поддерева.
        @param parent Родитель текущего узла.
        @return Кортеж (узел с минимальным ключом, его родитель)
        """
        if node.left:
            return self.__find_min(node.left, node)
        return node, parent

    def del_node(self, word):
        """
        @brief Удаляет элемент словаря по английскому слову.
        @param word Узел с английским словом для удаления.
        @return Удалённый узел или None, если слово не найдено.
        """
        node, parent, fl_find = self.__find(self.root, None, word.eng)
        if not fl_find:
            return None

        self._size -= 1

        if node.left is None and node.right is None:
            self.__del_leaf(node, parent)
        elif node.left is None or node.right is None:
            self.__del_one_child(node, parent)
        else:
            noder, parentr = self.__find_min(node.right, node)
            node.eng = noder.eng
            node.rus = noder.rus
            self.__del_one_child(noder, parentr)

        return node
    
    def __isub__(self, other):
        """
        @brief Оператор -= для удаления элемента из словаря.
        @param other Узел класса Node с ключом для удаления.
        @return Текущий словарь после удаления элемента.
        """
        self.del_node(other)
        return self
    
    def __getitem__(self, key):
        """
        @brief Поиск перевода слова по ключу.
        @param key Английское слово.
        @return Русский перевод или None, если слово не найдено.
        """
        node, parent, fl_find = self.__find(self.root, None, key)
        if fl_find:
            return node.rus
        
    def __setitem__(self, key, new_rus):
        """
        @brief Изменяет перевод слова.
        @param key Английское слово.
        @param new_rus Новый перевод.
        """
        node, parent, fl_find = self.__find(self.root, None, key)
        if fl_find:
            node.rus = new_rus
    
    def get_size(self):
        """
        @brief Возвращает количество элементов в словаре.
        @return Размер словаря.
        """
        return self._size

    def readfromfile(self, filename):
        """
        @brief Загружает данные словаря из текстового файла.
        @param filename Имя файла с парами (eng, rus), разделёнными запятой.
        @note Формат строки в файле: "eng, rus"
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        eng, rus = line.split(',', 1)
                        eng = eng.strip()
                        rus = rus.strip()
                        self.append(Node(eng, rus))
                    except ValueError:
                        print(f"Пропуск строки: некорректный формат строки '{line}'")
        except FileNotFoundError:
            print(f"Файл '{filename}' не найден")
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
