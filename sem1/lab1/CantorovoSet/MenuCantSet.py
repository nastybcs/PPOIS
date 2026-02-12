from CantorovoSet import CantorovoSet

A = CantorovoSet(input("Введите множество в {}: "))
while True:
    print("=== МЕНЮ ===")
    print("1. Показать множество")
    print("2. Добавить элемент")
    print("3. Удалить элемент")
    print("4. Мощность множества")
    print("5. Проверка принадлежности элемента")
    print("6. Объединение множеств (+)")
    print("7. Объединение с множеством (+=)")
    print("8. Пересечение множеств (*)")
    print("9. Пересечение с множеством (*=)")
    print("10. Разность множеств (-)")
    print("11. Разность с множеством (-=)")
    print("12. Булеан множества")
    print("13. Алгоритм Кантора")
    print("0. Выход")


    choice=input("Выберите пункт ")

    if choice == "1":
        A.print_set()
    elif choice == "2":
       new_elem=input("Введите элемент для добавления в {}")
       A.add_element(new_elem)
    
    elif choice == "3":
       elem_to_del=input("Введите элемент для удаления в {}")
       A.remove_element(elem_to_del)
    
    elif choice == "4":
        print("Мощность множества",A.get_size())
    
    elif choice == "5":
       elem=input("Введите элемент для проверки ")
       print(A[elem])
    
    elif choice == "6":
        B_str = input("Введите второе множество для +: ")
        B = CantorovoSet(B_str)
        C = A + B
        print("Результат A + B: ", end="")
        C.print_set()
    elif choice == "7":
        B_str = input("Введите второе множество для +=: ")
        B = CantorovoSet(B_str)
        A += B
        print("A после A += B: ", end="")
        A.print_set()

    elif choice == "8":
        B_str = input("Введите второе множество для *: ")
        B = CantorovoSet(B_str)
        C = A * B
        print("Результат A * B: ", end="")
        C.print_set()

    elif choice == "9":
        B_str = input("Введите второе множество для *=: ")
        B = CantorovoSet(B_str)
        A *= B
        print("A после A *= B: ", end="")
        A.print_set()
    elif choice == "10":
        B_str = input("Введите второе множество для -: ")
        B = CantorovoSet(B_str)
        C = A - B
        print("Результат A - B: ", end="")
        C.print_set()
    elif choice == "11":
        B_str = input("Введите второе множество для -=: ")
        B = CantorovoSet(B_str)
        A -= B
        print("A после A -= B: ", end="")
        A.print_set()
    elif choice == "12":
        print("Булеан множества:")
        A.boolean()
    elif choice == "13":
        A.elements = A.cantorovo_algorithm(A.elements)
        print("После алгоритма Кантора: ", end="")
        A.print_set()
    elif choice == "0":
        print("Выход.")
        break
    else:
        print("Неверный выбор, попробуйте снова.")