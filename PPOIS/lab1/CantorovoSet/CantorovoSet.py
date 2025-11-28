class CantorovoSet:
    """
    @brief Класс для работы с множествами Кантора.

    Предоставляет методы для парсинга строкового представления множества, 
    выполнения операций объединения, пересечения, разности, построения булеана множества
    и применения канторова алгоритма.
    """

    def __init__(self, input_str):
        """
        @brief Конструктор множества Кантора.
        @param input_str Строка, представляющая множество, например: "{{1},{2,{3}}}"
        """
        self.elements = self._parse_string(input_str)
   
    def _nesting_check(self, depth, i, input_str, temp_element):
        """
        @brief Проверяет корректность вложенности фигурных скобок при парсинге множества.
        @param depth Список с текущей глубиной вложенности.
        @param i Текущий индекс символа в строке.
        @param input_str Входная строка множества.
        @param temp_element Временный буфер для накопления элементов.
        @return Новый индекс после обработки вложенных скобок.
        """
        if input_str[i] == '{':
            depth[0] += 1
            i += 1
            while not (input_str[i] == '}' and depth[0] <= 2):
                if input_str[i] == '{':
                    depth[0] += 1
                elif input_str[i] == '}':
                    depth[0] -= 1
                temp_element.append(input_str[i]) 
                i += 1
            depth[0] -= 1
        else:
            temp_element.append(input_str[i])
        return i 
    
    def _parse_string(self, input_str):
        """
        @brief Разбирает строковое представление множества в структуру данных Python.
        @param input_str Строка с множеством, например: "{{1},{2,{3}}}"
        @return Список элементов множества в виде вложенных списков.
        """
        input_str = input_str.replace(" ", "") 
        cleaned = []

        # Убираем лишние запятые и пробелы
        for i, ch in enumerate(input_str):
            if i > 0 and ((ch == ',' and input_str[i-1] == ',') or (ch == ',' and input_str[i-1] == '{')):
                continue
            cleaned.append(ch)
        input_str = "".join(cleaned)

        result = []
        temp_element = []
        depth = [1]
        i = 1

        while i < len(input_str):
            if input_str[i] == "," or (input_str[i] == '}' and depth[0] == 1):
                result.append(["".join(temp_element)])
                temp_element = []
                i += 1
                continue
            i = self._nesting_check(depth, i, input_str, temp_element)
            i += 1

        if temp_element != []:  
            result.append(["".join(temp_element)])
        return result
    
    def print_set(self):
        """
        @brief Печатает множество в формате Кантора.
        """
        print("{", end="")  
        for i, element in enumerate(self.elements):
            print("{", end="") 
            print("".join(element), end="")
            print("}", end="")  
            if i < len(self.elements) - 1:
                print(",", end="")
        print("}")  

    def add_element(self, new_element):
        """
        @brief Добавляет новый элемент во множество.
        @param new_element Строка, представляющая элемент множества.
        """
        elems_to_add = self._parse_string(new_element)
        for el in elems_to_add:
            if el == "{}" and el not in self.elements:
                self.elements.append("")
            elif el not in self.elements:
                self.elements.append(el)

    def remove_element(self, target_element):
        """
        @brief Удаляет элемент из множества.
        @param target_element Строка, представляющая удаляемый элемент.
        """
        elem_to_del = self._parse_string(target_element)
        new_elements = [el for el in self.elements if el not in elem_to_del]
        self.elements = new_elements

    def cantorovo_algorithm(self, elements):
        """
        @brief Реализует алгоритм Кантора для построения канторова множества.
        @param elements Список элементов для обработки.
        @return Отфильтрованный список элементов.
        """
        if len(elements) <= 2:
            return elements
        count = len(elements) // 3
        left_third = elements[:count]
        right_third = elements[-count:]

        left_result = self.cantorovo_algorithm(left_third)
        right_result = self.cantorovo_algorithm(right_third)
        return left_result + right_result
    
    def get_size(self):
        """
        @brief Возвращает количество элементов множества.
        @return Размер множества.
        """
        return len(self.elements)
    
    def __getitem__(self, item):
        """
        @brief Проверяет наличие элемента в множестве.
        @param item Строка, представляющая элемент.
        @return True, если элемент присутствует, иначе False.
        """
        if item == "{}":
            item_list = [""]
        else:
            item_list = self._parse_string(item)[0]
        return item_list in self.elements

    def __add__(self, other):
        """
        @brief Объединение двух множеств.
        @param other Второе множество Кантора.
        @return Новое множество с объединёнными элементами.
        """
        new_set = CantorovoSet("{}")
        new_set.elements = [el for el in self.elements]

        for el in other.elements:
            if el not in self.elements:
                new_set.elements.append(el)
        return new_set

    def __iadd__(self, other):
        """
        @brief Оператор += для объединения с другим множеством.
        @param other Второе множество Кантора.
        @return Текущее множество с добавленными элементами.
        """
        for el in other.elements:
            if el not in self.elements:
                self.elements.append(el)
        return self
    
    def __mul__(self, other):
        """
        @brief Пересечение двух множеств.
        @param other Второе множество Кантора.
        @return Новое множество с общими элементами.
        """
        new_set = CantorovoSet("{}")
        new_set.elements = [el for el in self.elements if el in other.elements and el != [""]]
        return new_set

    def __imul__(self, other):
        """
        @brief Оператор *= для пересечения множеств.
        @param other Второе множество Кантора.
        @return Текущее множество, содержащее только общие элементы.
        """
        self.elements = [el for el in self.elements if el in other.elements]
        return self

    def __sub__(self, other):
        """
        @brief Разность двух множеств.
        @param other Второе множество Кантора.
        @return Новое множество без элементов второго.
        """
        new_set = CantorovoSet("{}")
        new_set.elements = [el for el in self.elements if el not in other.elements]
        return new_set

    def __isub__(self, other):
        """
        @brief Оператор -= для разности множеств.
        @param other Второе множество Кантора.
        @return Текущее множество после удаления элементов второго.
        """
        self.elements = [el for el in self.elements if el not in other.elements]
        return self

    def boolean(self):
        """
        @brief Выводит булеан множества (множество всех подмножеств).
        """
        result = [[]]

        for el in self.elements:
            new_subsets = []
            for subset in result:
                new_subsets.append(subset + [el])
            result.extend(new_subsets)

        print(f"Булеан множества (всего {len(result)} подмножеств):")
        for subset in result:
            print("{", end="")
            for elem in subset:
                print("{", end="")
                print("".join(elem), end="")
                print("}", end="")
            print("}")
