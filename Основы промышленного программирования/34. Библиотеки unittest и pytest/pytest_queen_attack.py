import pytest
from yandex_testing_lesson import is_under_queen_attack


def test_position_out_of_board():
    with pytest.raises(ValueError):
        is_under_queen_attack("e1", "e9")


def test_position_wrong_format():
    with pytest.raises(ValueError):
        is_under_queen_attack("abc", "h8")


def test_position_wrong_format2():
    with pytest.raises(ValueError):
        is_under_queen_attack('c3', 'd4d')


def test_position_wrong_type():
    with pytest.raises(TypeError):
        is_under_queen_attack(None, 42)


def test_queen_position_wrong_type():
    with pytest.raises(TypeError):
        is_under_queen_attack("h8", (8, 8))
        is_under_queen_attack("h8", 64)


def test_queen_can_beat_same_cell():
    assert is_under_queen_attack("a1", "a1")


def test_queen_can_beat_same_row():
    assert is_under_queen_attack("a1", "e1")


def test_queen_can_beat_same_column():
    assert is_under_queen_attack("a1", "a8")


def test_queen_can_beat_same_diagonal():
    assert is_under_queen_attack("b3", "e6")


def test_queen_can_not_beat():
    assert not is_under_queen_attack("a1", "g8")
