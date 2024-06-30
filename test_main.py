import pytest

from main import (
    TicTacToe,
    TicTacToeOccupiedException,
    TicTacToeParseException,
    TicTacToeRangeException,
    TicTacToeSymbols,
)


def test_raises_range_exception():
    with pytest.raises(TicTacToeRangeException):
        b = TicTacToe(10, 10, 5, TicTacToeSymbols.CROSS)
        b.put_symbol_to_coords((11, 5))


def test_raises_parse_exception(monkeypatch):
    with pytest.raises(TicTacToeParseException):
        monkeypatch.setattr("builtins.input", lambda _: "hello")
        b = TicTacToe(10, 10, 5, TicTacToeSymbols.CROSS)
        b.get_coords_from_user()


def test_raises_occupied_exception():
    with pytest.raises(TicTacToeOccupiedException):
        b = TicTacToe(10, 10, 5, TicTacToeSymbols.CROSS)
        b.put_symbol_to_coords((1, 1))
        b.put_symbol_to_coords((1, 1))


def test_get_symbol_at_coord():
    b = TicTacToe(10, 10, 5, TicTacToeSymbols.CROSS)
    b.put_symbol_to_coords((1, 1))
    symbol = b.get_symbol_at_coord((1, 1))
    assert symbol == TicTacToeSymbols.CROSS


def test_find_winning_set():
    # winning case
    winning = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    b = TicTacToe(10, 10, 5, TicTacToeSymbols.CROSS)
    b.put_symbol_to_coords(winning[0])
    for coord in winning[1:]:
        b.put_symbol_to_coords((coord[0], coord[1] + 1))
        b.put_symbol_to_coords(coord)
    assert b.find_winning_set() == set(winning)

    # not yet winning case
    b = TicTacToe(10, 10, 5, TicTacToeSymbols.CROSS)
    b.put_symbol_to_coords(winning[0])
    for coord in winning[1:-1]:
        b.put_symbol_to_coords((coord[0], coord[1] + 1))
        b.put_symbol_to_coords(coord)
    assert b.find_winning_set() == set()
