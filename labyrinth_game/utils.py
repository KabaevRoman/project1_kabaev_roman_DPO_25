from labyrinth_game.constants import ROOMS


def describe_current_room(game_state):
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


def solve_puzzle(game_state):
    current_room = game_state["current_room"]

    room = ROOMS[current_room]
    if not room["puzzle"]:
        print("Загадок здесь нет.")
        return
    question, answer = room["puzzle"]
    print(question)
    user_answer = input("Ваш ответ: ").strip()
    if user_answer.lower() == answer.lower():
        print("Правильно! Загадка решена.")
        room["puzzle"] = None  # Remove puzzle
    else:
        print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state):
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


def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
