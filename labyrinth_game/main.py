#!/usr/bin/env python3


from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.types import GameState
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state: GameState, command: str):
    parts = command.split()
    if not parts:
        return
    cmd = parts[0].lower()
    args = parts[1:] if len(parts) > 1 else []

    match cmd:
        case "look":
            describe_current_room(game_state)
        case "go":
            if args:
                move_player(game_state, args[0])
            else:
                print("Укажите направление.")
        case "take":
            if args:
                take_item(game_state, " ".join(args))
            else:
                print("Укажите предмет.")
        case "use":
            if args:
                use_item(game_state, " ".join(args))
            else:
                print("Укажите предмет.")
        case "inventory":
            show_inventory(game_state)
        case "solve":
            if game_state["current_room"] == "treasure_room" and "treasure_chest" in ROOMS["treasure_room"]["items"]:
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "help":
            show_help()
        case "quit":
            game_state["game_over"] = True
        case _:
            print("Неизвестная команда. Введите 'help' для списка команд.")


def main():
    game_state: GameState = {
        "player_inventory": [],
        "current_room": "entrance",
        "game_over": False,
        "steps_taken": 0,
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state["game_over"]:
        command = get_input()
        if command.lower() == "quit":
            return
        process_command(game_state, command)

    print("Игра окончена.")
