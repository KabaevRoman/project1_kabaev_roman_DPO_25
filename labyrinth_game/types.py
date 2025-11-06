from typing import Literal, TypedDict


class GameState(TypedDict):
    player_inventory: list[str]
    current_room: str
    game_over: bool
    steps_taken: int


Direction = Literal["north", "south", "east", "west"]
Item = Literal[
    "torch",
    "sword",
    "bronze_box",
    "rusty_key",
    "ancient_book",
    "treasure_key",
    "flower",
    "crystal",
    "treasure_chest",
    "coin",
]


class Room(TypedDict):
    description: str
    exits: dict[str, str]
    items: list[Item]
    puzzle: tuple[str, str] | None
