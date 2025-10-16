from labyrinth_game.constants import ROOMS
from labyrinth_game.types import Direction, GameState, Item
from labyrinth_game.utils import describe_current_room


def show_inventory(game_state: GameState):
    inventory = game_state["player_inventory"]
    if not inventory:
        print("Ваш инвентарь пуст.")
        return

    print("Ваш инвентарь:")
    for item in inventory:
        print(f"  - {item}")


def get_input(prompt="> "):
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def move_player(game_state: GameState, direction: Direction):
    current_room = game_state["current_room"]

    exits = ROOMS[current_room]["exits"]

    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return

    game_state["current_room"] = exits[direction]
    game_state["steps_taken"] += 1

    describe_current_room(game_state)


def take_item(game_state: GameState, item_name: Item):
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
