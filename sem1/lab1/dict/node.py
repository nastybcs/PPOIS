class Node:
    """
    @brief Узел бинарного дерева для словаря.

    Содержит английское слово, его перевод и ссылки на левое и правое поддеревья.
    """

    def __init__(self, eng, rus):
        """
        @brief Конструктор узла дерева.
        @param eng Английское слово.
        @param rus Перевод на русский язык.
        """
        self.eng = eng      
        self.rus = rus      
        self.left = None    
        self.right = None  

