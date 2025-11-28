from Dict import Dictionary
from node import Node
d=Dictionary()

while True:
    print("\n=== МЕНЮ СЛОВАРЯ ===")
    print("1. Добавить слово")
    print("2. Удалить слово")
    print("3. Найти перевод")
    print("4. Изменить перевод")
    print("5. Показать весь словарь")
    print("6. Загрузить из файла")
    print("7. Размер словаря")
    print("0. Выход")

    choice=input("Выберите пункт ")

    if choice == "1":
        eng=input("").strip()
        rus=input("").strip()
        d+=Node(eng,rus)
        print("Добавлено")
    elif choice == "2":
        eng = input("Введите слово для удаления: ").strip()
        d -= Node(eng, "")
        print("Удалено.")
    
    elif choice == "3":
        eng = input("Введите слово для поиска: ").strip()
        rus = d[eng]
        if rus:
            print(f"Перевод: {rus}")
        else:
            print("Слово не найдено.")
    
    elif choice == "4":
        eng = input("Введите слово для изменения: ").strip()
        new_rus = input("Введите новый перевод: ").strip()
        if d[eng]:
            d[eng] = new_rus
            print(" Перевод обновлён.")
        else:
            print("Слово не найдено.")
    
    elif choice == "5":
        print("\n Словарь:")
        d.show_tree(d.root)
    
    elif choice == "6":
        fname = input("Введите имя файла: ").strip()
        d.readfromfile(fname)
        print("Загрузка завершена.")
    
    elif choice == "7":
        
        print(f"В словаре {d.get_size()} слов.")
    
    elif choice == "0":
        print("Выход.")
        break
    else:
        print("Неверный выбор, попробуйте снова.")

