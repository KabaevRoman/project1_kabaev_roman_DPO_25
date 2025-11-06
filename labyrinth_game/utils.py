import math

from labyrinth_game.constants import ROOMS
from labyrinth_game.types import GameState

# Константы для генератора случайных событий
RANDOM_EVENT_PROBABILITY = 10  # Вероятность случайного события (1 из 10)
EVENT_TYPES_COUNT = 3  # Количество типов событий
TRAP_DAMAGE_THRESHOLD = 3  # Порог урона от ловушки


def pseudo_random(seed: int, modulo: int) -> int:
    """
    Генерирует псевдослучайное число на основе seed.

    Args:
        seed: Значение для генерации (обычно количество шагов)
        modulo: Модуль для ограничения диапазона результата

    Returns:
        Псевдослучайное число в диапазоне [0, modulo)
    """
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional_part = x - math.floor(x)
    result = fractional_part * modulo
    return int(result)


def trigger_trap(game_state: GameState):
    """
    Активирует ловушку, которая может забрать предмет или завершить игру.

    Args:
        game_state: Текущее состояние игры
    """
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state["player_inventory"]
    steps = game_state["steps_taken"]

    if inventory:
        random_index = pseudo_random(steps, len(inventory))
        lost_item = inventory.pop(random_index)
        print(f"Вы потеряли предмет: {lost_item}")
    else:
        damage_roll = pseudo_random(steps, RANDOM_EVENT_PROBABILITY)
        if damage_roll < TRAP_DAMAGE_THRESHOLD:
            print("Вы не смогли избежать опасности... Игра окончена.")
            game_state["game_over"] = True
        else:
            print("Вам удалось уцелеть, но это было опасно!")


def random_event(game_state: GameState):
    """
    Генерирует случайные события во время перемещения игрока.

    Args:
        game_state: Текущее состояние игры
    """
    steps = game_state["steps_taken"]
    current_room = game_state["current_room"]
    inventory = game_state["player_inventory"]

    if pseudo_random(steps, RANDOM_EVENT_PROBABILITY) != 0:
        return

    event_type = pseudo_random(steps + 1, EVENT_TYPES_COUNT)

    if event_type == 0:
        print("\nВы заметили на полу что-то блестящее...")
        ROOMS[current_room]["items"].append("coin")
        print("Это монетка! Она теперь лежит здесь.")
    elif event_type == 1:
        print("\nВы слышите странный шорох в темноте...")
        if "sword" in inventory:
            print("Вы взмахиваете мечом, отпугивая существо!")
        else:
            print("Вам становится не по себе.")
    else:
        if current_room == "trap_room" and "torch" not in inventory:
            print("\nВы не видите опасности в темноте!")
            trigger_trap(game_state)


def describe_current_room(game_state: GameState):
    """
    Выводит описание текущей комнаты, предметы в ней и доступные выходы.

    Args:
        game_state: Текущее состояние игры
    """
    current_room = game_state["current_room"]

    room = ROOMS[current_room]
    print(f"\n== {current_room.upper()} ==")
    print(room["description"])
    if room["items"]:
        print("Заметные предметы:")
        for item in room["items"]:
            print(f"  - {item}")
    print("Выходы:")
    for direction, room_name in room["exits"].items():
        print(f"  - {direction}: {room_name}")
    if room["puzzle"]:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state: GameState):
    """
    Обрабатывает попытку решить загадку в текущей комнате.

    Args:
        game_state: Текущее состояние игры
    """
    current_room = game_state["current_room"]

    room = ROOMS[current_room]
    if not room["puzzle"]:
        print("Загадок здесь нет.")
        return

    question, answer = room["puzzle"]
    print(question)
    user_answer = input("Ваш ответ: ").strip()

    alternatives = {
        "10": ["10", "десять"],
        "7": ["7", "семь"],
        "шаг шаг шаг": ["шаг шаг шаг"],
        "резонанс": ["резонанс"],
        "эхо": ["эхо"],
    }

    correct_answers = alternatives.get(answer.lower(), [answer.lower()])

    if user_answer.lower() in correct_answers:
        print("Правильно! Загадка решена.")
        room["puzzle"] = None

        if current_room == "hall":
            print("Пьедестал раскрывается, внутри находится древний артефакт!")
            room["items"].append("ancient_book")
        elif current_room == "library":
            print("Появляется секретный отсек с сокровищем!")
            room["items"].append("crystal")
        elif current_room == "garden":
            print("Фонтан начинает светиться, и появляется волшебный цветок!")
            if "flower" not in room["items"]:
                room["items"].append("flower")
        elif current_room == "cave":
            print("Эхо усиливается и открывает спрятанный проход!")
    else:
        print("Неверно. Попробуйте снова.")
        if current_room == "trap_room":
            print("Вы услышали щелчок под ногами...")
            trigger_trap(game_state)


def attempt_open_treasure(game_state: GameState):
    """
    Обрабатывает попытку открыть сундук с сокровищами.

    Args:
        game_state: Текущее состояние игры
    """
    current_room = game_state["current_room"]

    room = ROOMS[current_room]
    inventory = game_state["player_inventory"]
    if "treasure_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room["items"].remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return
    choice = input("Сундук заперт. Ввести код? (да/нет): ").strip().lower()
    if choice == "да":
        code = input("Введите код: ").strip()
        if room["puzzle"] and code.lower() == room["puzzle"][1].lower():
            print("Код верный! Сундук открыт!")
            room["items"].remove("treasure_chest")
            print("В сундуке сокровище! Вы победили!")
            game_state["game_over"] = True
        else:
            print("Неверный код.")
        return
    print("Вы отступаете от сундука.")


def show_help(commands: dict[str, str]):
    """
    Выводит список доступных команд с их описанием.

    Args:
        commands: Словарь с командами и их описаниями
    """
    print("\nДоступные команды:")
    for command, description in commands.items():
        print(f"  {command:<16} - {description}")
