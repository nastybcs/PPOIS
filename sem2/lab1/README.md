# Лабораторная работа №1
## Симулятор танка

### Важные сущности
- танк
- экипаж
- двигатель
- топливный бак
- пушка
- позиция на карте
- боеприпасы

### Описание проекта
Консольная программа-симулятор танка с интерактивным меню.
Пользователь может:
- заводить/глушить двигатель
- перемещать танк по координатам
- стрелять из пушки
- управлять экипажем (добавлять/удалять членов экипажа)
- сажать/высаживать экипаж
- заправлять танк
- проверять боеготовность
- сохранять и загружать состояние между запусками (JSON-файл)
- удалять сохранение

### Основные классы и интерфейсы

#### IMovable (ABC)
**Абстрактные методы**
- `move(distance: int) -> None`

#### IShootable (ABC)
**Абстрактные методы**
- `fire() -> None`
- `reload() -> None`

#### Position
**Атрибуты**
- `__x: int` — координата X
- `__y: int` — координата Y

**Свойства**
- `x -> int`
- `y -> int`
- `coordinates -> tuple[int, int]`

**Методы**
- `distance_to(other: Position) -> float` — расстояние до другой позиции
- `to_dict() -> dict`
- `from_dict(data: dict) -> None`

#### Engine
**Атрибуты**
- `__horsepower: int` — мощность двигателя
- `__is_running: bool` — состояние двигателя

**Свойства**
- `horsepower -> int`
- `is_running -> bool`

**Методы**
- `start() -> bool` — запустить двигатель
- `stop() -> bool` — заглушить двигатель
- `to_dict() -> dict`
- `from_dict(data: dict) -> None`

#### FuelTank
**Атрибуты**
- `__capacity: int` — ёмкость бака
- `__level: int` — текущий уровень топлива

**Свойства**
- `level -> int`
- `percentage -> float`
- `is_empty -> bool`

**Методы**
- `refill(amount: int = None) -> None` — заправиться (полностью или частично)
- `consume(amount: int) -> bool` — потратить топливо
- `to_dict() -> dict`
- `from_dict(data: dict) -> None`

#### Weapon (ABC, наследуется от IShootable)
**Атрибуты**
- `_ammo: int` — количество боеприпасов
- `_caliber: int` — калибр
- `_is_loaded: bool` — заряжено ли оружие

**Свойства**
- `ammo -> int`
- `is_loaded -> bool`
- `is_empty -> bool`

**Абстрактные методы**
- `fire() -> None`

**Методы**
- `reload() -> None` — перезарядить
- `to_dict() -> dict`
- `from_dict(data: dict) -> None`

#### Cannon (наследуется от Weapon)
**Конструктор**
- `__init__(ammo: int = 30, caliber: int = 125)`

**Методы**
- `fire() -> None` — выстрел из пушки с проверкой наличия снарядов и заряженности

#### CrewMember
**Атрибуты**
- `__name: str` — имя члена экипажа

**Свойства**
- `name -> str`

**Методы**
- `to_dict() -> dict`

#### Crew
**Атрибуты**
- `__members: list[CrewMember]` — список экипажа
- `__is_ready: bool` — готовность экипажа (находятся ли в танке)

**Свойства**
- `is_ready -> bool`

**Методы**
- `board() -> bool` — экипаж в танке
- `leave() -> None` — экипаж покинул танк
- `add_member(name: str) -> None` — добавить члена экипажа
- `remove_member(name: str) -> None` — удалить члена экипажа
- `to_dict() -> dict`
- `from_dict(data: dict) -> None`

#### Tank (реализует IMovable)
**Константы**
- `FUEL_CONSUMPTION_RATE = 2.0` — расход топлива на единицу расстояния
- `SAVE_FILE = "tank_save.json"` — файл сохранения по умолчанию

**Атрибуты**
- `__position: Position`
- `__fuel_tank: FuelTank`
- `__fuel_consumption_rate: float`
- `__engine: Engine`
- `__cannon: Cannon`
- `__crew: Crew`

**Свойства**
- `fuel_level -> int`
- `crew_is_ready -> bool`
- `fuel_percentage -> float`
- `has_fuel -> bool`
- `is_combat_ready -> bool` — боеготовность (экипаж + двигатель + топливо + снаряды)
- `ammo -> int`
- `position -> Position`
- `can_move -> bool` — может ли двигаться

**Методы**
- `move_to(target_x: float, target_y: float) -> bool` — переместиться в точку (с проверкой топлива, двигателя и экипажа)
- `move(distance: int) -> bool` — переместиться на расстояние по оси X
- `shoot_cannon() -> bool` — выстрелить (с проверкой двигателя)
- `engine_is_running() -> bool`
- `start_engine() -> bool` — запустить двигатель (проверка наличия топлива)
- `stop_engine() -> bool`
- `refuel(amount: int = None) -> None` — заправить танк
- `add_member(name: str) -> None` — добавить члена экипажа
- `remove_crew_member(name: str) -> None` — удалить члена экипажа
- `show_crew() -> None` — показать экипаж
- `board_crew() -> bool` — посадить экипаж в танк
- `leave_crew() -> bool` — высадить экипаж
- `get_crew_info() -> str` — получить информацию об экипаже
- `get_status() -> None` — показать полный статус танка
- `to_dict() -> dict` — сериализация в словарь
- `from_dict(data: dict) -> None` — десериализация из словаря
- `save_state(filename: str = None) -> bool` — сохранить состояние в файл
- `load_state(filename: str = None) -> bool` — загрузить состояние из файла
- `delete_save(filename: str = None) -> bool` — удалить файл сохранения

### Пользовательский интерфейс

#### TankMenu
Класс для управления интерактивным меню.

**Атрибуты**
- `tank: Tank` — объект танка
- `running: bool` — флаг работы программы
- `commands: dict` — словарь соответствия команд и методов

**Методы меню**
- `print_menu()` — отображает главное меню
- `show_status()` — показать статус танка
- `start_engine()` — запустить двигатель
- `stop_engine()` — заглушить двигатель
- `move_tank()` — переместить танк (запрос координат)
- `shoot_cannon()` — выстрелить из пушки (с подтверждением)
- `refuel_tank()` — заправить танк (полная или частичная заправка)
- `add_crew_member()` — добавить члена экипажа
- `remove_crew_member()` — удалить члена экипажа
- `show_crew()` — показать экипаж
- `make_crew_ready()` — посадить экипаж в танк
- `save_game()` — сохранить игру
- `load_game()` — загрузить игру
- `delete_save()` — удалить сохранение
- `exit_program()` — выход из программы (с опцией сохранения)
- `run()` — главный цикл программы

### Исключения

#### exceptions.CrewMemberNotFoundError
Выбрасывается при попытке удалить несуществующего члена экипажа
