from enum import Enum

WIDTH = 10
HEIGHT = 10


class TicTacToeRangeException(Exception):
    pass


class TicTacToeParseException(Exception):
    pass


class TicTacToeOccupiedException(Exception):
    pass


class TicTacToeSymbols(Enum):
    CROSS = "x"
    CIRCLE = "o"


class TicTacToe:
    should_exit: bool = False
    symbol_at_turn: TicTacToeSymbols = TicTacToeSymbols.CROSS.value
    symbols_on_board = {}
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
                print(self.get_symbol_at_coord((row, column)), end="")
            print()

    def get_coords_from_user(self) -> tuple[int, int]:
        try:
            column = int(input("select column: "))
            row = int(input("select row: "))
            return (column, row)
        except ValueError:
            raise TicTacToeParseException

    def put_symbol_to_coords(self, coords: (int, int)) -> None:
        x, y = coords
        if (x >= self.height) or (y >= self.width):
            raise TicTacToeRangeException

        symbol_on_coords = self.symbols_on_board.get(coords)

        if symbol_on_coords is not None:
            raise TicTacToeOccupiedException

        self.symbols_on_board[coords] = self.symbol_at_turn

    def get_symbol_at_coord(self, coords: (int, int)) -> TicTacToeSymbols:
        return self.symbols_on_board.get(coords, " ")

    def check_game_end(self) -> bool:
        pass

    def switch_turns(self) -> None:
        if self.symbol_at_turn == TicTacToeSymbols.CROSS.value:
            self.symbol_at_turn = TicTacToeSymbols.CIRCLE.value
        else:
            self.symbol_at_turn = TicTacToeSymbols.CROSS.value

    def game_loop(self) -> None:
        while not self.should_exit:
            if self.is_first_render:
                self.is_first_render = False
            else:
                print("----------")
            print(f"it's now {self.symbol_at_turn}'s turn")
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
            self.check_game_end()
            self.switch_turns()


if __name__ == "__main__":
    b = TicTacToe(WIDTH, HEIGHT)
    b.game_loop()
