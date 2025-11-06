from labyrinth_game.constants import ROOMS
from labyrinth_game.types import Direction, GameState, Item
from labyrinth_game.utils import describe_current_room, random_event


def show_inventory(game_state: GameState):
    """
    Выводит содержимое инвентаря игрока.

    Args:
        game_state: Текущее состояние игры
    """
    inventory = game_state["player_inventory"]
    if not inventory:
        print("Ваш инвентарь пуст.")
        return

    print("Ваш инвентарь:")
    for item in inventory:
        print(f"  - {item}")


def get_input(prompt: str = "> ") -> str:
    """
    Получает ввод от пользователя с обработкой прерываний.

    Args:
        prompt: Строка приглашения для ввода

    Returns:
        Введенная пользователем строка (очищенная от пробелов)
    """
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state: GameState, direction: Direction):
    """
    Перемещает игрока в указанном направлении.

    Args:
        game_state: Текущее состояние игры
        direction: Направление перемещения (north/south/east/west)
    """
    current_room = game_state["current_room"]

    exits = ROOMS[current_room]["exits"]

    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return

    next_room = exits[direction]
    
    if next_room == "treasure_room":
        if "rusty_key" not in game_state["player_inventory"]:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return
        else:
            print(
                "Вы используете найденный ключ, чтобы открыть "
                "путь в комнату сокровищ."
            )
    
    game_state["current_room"] = next_room
    game_state["steps_taken"] += 1

    describe_current_room(game_state)
    
    random_event(game_state)


def take_item(game_state: GameState, item_name: Item):
    """
    Поднимает предмет из текущей комнаты и добавляет в инвентарь.

    Args:
        game_state: Текущее состояние игры
        item_name: Название предмета для поднятия
    """
    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    current_room = game_state["current_room"]

    room_items = ROOMS[current_room]["items"]
    if item_name in room_items:
        game_state["player_inventory"].append(item_name)
        room_items.remove(item_name)
        print(f"Вы подняли: {item_name}")
        return

    print("Такого предмета здесь нет.")


def use_item(game_state: GameState, item_name: Item):
    """
    Использует предмет из инвентаря игрока.

    Args:
        game_state: Текущее состояние игры
        item_name: Название предмета для использования
    """
    inventory = game_state["player_inventory"]
    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    match item_name:
        case "torch":
            print("Вы зажгли факел. Стало светлее.")
        case "sword":
            print("Вы взяли меч. Теперь вы чувствуете себя увереннее.")
        case "bronze_box":
            if "rusty_key" not in inventory:
                inventory.append("rusty_key")
                print("Вы открыли бронзовую шкатулку. Внутри был ржавый ключ!")
                return
            print("Вы открыли бронзовую шкатулку, но она пуста.")
