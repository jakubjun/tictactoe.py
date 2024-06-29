from enum import Enum
from typing import Set

WIDTH = 10
HEIGHT = 10
N_TO_WIN = 2


class TicTacToeRangeException(Exception):
    pass


class TicTacToeParseException(Exception):
    pass


class TicTacToeOccupiedException(Exception):
    pass


class TicTacToeSymbols(Enum):
    CROSS = "x"
    CIRCLE = "o"
    EMPTY = " "


class TicTacToe:
    should_exit: bool = False
    symbol_at_turn: TicTacToeSymbols = TicTacToeSymbols.CROSS
    symbols_on_board: dict[tuple[int, int], TicTacToeSymbols] = {}
    is_first_render = True

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def print_board(self) -> None:
        print("  ", end="")
        for column in range(self.width):
            print(column, end="")
        print()
        for row in range(self.height):
            print(f"{row}|", end="")
            for column in range(self.width):
                print(self.get_symbol_at_coord((row, column)).value, end="")
            print()

    def print_winning_set(self, winning_set):
        print("  ", end="")
        for column in range(self.width):
            print(column, end="")
        print()
        for row in range(self.height):
            print(f"{row}|", end="")
            for column in range(self.width):
                print(
                    self.symbol_at_turn.value if (row, column) in winning_set else " ",
                    end="",
                )
            print()

    def get_coords_from_user(self) -> tuple[int, int]:
        try:
            column = int(input("select column: "))
            row = int(input("select row: "))
            return (column, row)
        except ValueError:
            raise TicTacToeParseException

    def put_symbol_to_coords(self, coords: tuple[int, int]) -> None:
        x, y = coords
        if (x >= self.height) or (y >= self.width):
            raise TicTacToeRangeException

        symbol_on_coords = self.symbols_on_board.get(coords)

        if symbol_on_coords is not None:
            raise TicTacToeOccupiedException

        self.symbols_on_board[coords] = self.symbol_at_turn

    def get_symbol_at_coord(self, coords: tuple[int, int]) -> TicTacToeSymbols:
        return self.symbols_on_board.get(coords, TicTacToeSymbols.EMPTY)

    def find_winning_set(self) -> Set[tuple[int, int]]:
        found: Set[tuple[int, int]] = set()
        for coords, first_symbol in self.symbols_on_board.items():
            # check only to right, to lower right and to bottom
            found.add(coords)
            for _ in range(N_TO_WIN):
                next_coords = (coords[0], coords[1] + 1)
                symbol = self.get_symbol_at_coord(next_coords)
                found.add(next_coords)
                if symbol != first_symbol:
                    found.clear()
                    break

            if len(found) != 0:
                return found

            found.add(coords)
            for _ in range(N_TO_WIN):
                next_coords = (coords[0] + 1, coords[1] + 1)
                symbol = self.get_symbol_at_coord(next_coords)
                found.add(next_coords)
                if symbol != first_symbol:
                    found.clear()
                    break

            if len(found) != 0:
                return found

            found.add(coords)
            for _ in range(N_TO_WIN):
                next_coords = (coords[0] + 1, coords[1])
                symbol = self.get_symbol_at_coord(next_coords)
                found.add(next_coords)
                if symbol != first_symbol:
                    found.clear()
                    break

            if len(found) != 0:
                return found

        return found

    def switch_turns(self) -> None:
        if self.symbol_at_turn == TicTacToeSymbols.CROSS:
            self.symbol_at_turn = TicTacToeSymbols.CIRCLE
        else:
            self.symbol_at_turn = TicTacToeSymbols.CROSS

    def game_loop(self) -> None:
        while not self.should_exit:
            if self.is_first_render:
                self.is_first_render = False
            else:
                print("----------")
            print(f"it's now {self.symbol_at_turn.value}'s turn")
            self.print_board()
            try:
                coords = self.get_coords_from_user()
                self.put_symbol_to_coords(coords)
            except TicTacToeParseException:
                print("wrong input format! please input a whole number")
                continue
            except TicTacToeRangeException:
                print(
                    f"you picked a field out of the bounds. pick between 0 - {self.height-1} and 0 - {self.width-1}"
                )
                continue
            except TicTacToeOccupiedException:
                print("the field is occupied! select a different one")
                continue

            winning_dict = self.find_winning_set()
            if len(winning_dict) > 0:
                self.should_exit = True
                print("----------")
                print(f"game over, {self.symbol_at_turn.value} is a winner!")
                self.print_winning_set(winning_dict)
            self.switch_turns()


if __name__ == "__main__":
    b = TicTacToe(WIDTH, HEIGHT)
    b.game_loop()
