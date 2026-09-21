import pytest

from game import check_winner, create_board, is_draw, make_move, parse_position, render_board


def test_create_board_returns_nine_empty_cells():
    assert create_board() == [" "] * 9


@pytest.mark.parametrize(
    ("user_value", "expected_index"),
    [("1", 0), ("5", 4), ("9", 8)],
)
def test_parse_position_accepts_numbers_from_one_to_nine(user_value, expected_index):
    assert parse_position(user_value) == expected_index


@pytest.mark.parametrize("user_value", ["abc", "", None, "3.5"])
def test_parse_position_rejects_non_integer_data(user_value):
    with pytest.raises(ValueError, match="целое число"):
        parse_position(user_value)


@pytest.mark.parametrize("user_value", ["0", "10", "-2"])
def test_parse_position_rejects_numbers_outside_board(user_value):
    with pytest.raises(ValueError, match="от 1 до 9"):
        parse_position(user_value)


def test_make_move_places_player_mark():
    board = create_board()

    make_move(board, 4, "X")

    assert board[4] == "X"


def test_make_move_rejects_occupied_cell():
    board = create_board()
    make_move(board, 4, "X")

    with pytest.raises(ValueError, match="занята"):
        make_move(board, 4, "O")


@pytest.mark.parametrize("position", [-1, 9, "1", True])
def test_make_move_rejects_invalid_position(position):
    board = create_board()

    with pytest.raises(ValueError, match="Позиция"):
        make_move(board, position, "X")


def test_make_move_rejects_unknown_player():
    board = create_board()

    with pytest.raises(ValueError, match="игроки"):
        make_move(board, 0, "A")


@pytest.mark.parametrize(
    "winning_cells",
    [(0, 1, 2), (0, 3, 6), (0, 4, 8), (2, 4, 6)],
)
def test_check_winner_finds_three_in_a_row(winning_cells):
    board = create_board()
    for cell in winning_cells:
        board[cell] = "X"

    assert check_winner(board, "X") is True


def test_check_winner_returns_false_for_unfinished_line():
    board = ["X", "X", " ", "O", "O", " ", " ", " ", " "]

    assert check_winner(board, "X") is False


def test_is_draw_returns_true_for_full_board_without_winner():
    board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]

    assert is_draw(board) is True


def test_is_draw_returns_false_when_someone_won():
    board = ["X", "X", "X", "O", "O", "X", "O", "X", "O"]

    assert is_draw(board) is False


def test_render_board_shows_numbers_for_empty_cells_and_player_marks():
    board = create_board()
    board[0] = "X"
    board[4] = "O"

    result = render_board(board)

    assert " X | 2 | 3 " in result
    assert " 4 | O | 6 " in result

