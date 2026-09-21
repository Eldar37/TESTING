"""Простая консольная игра «Крестики-нолики»."""


WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def create_board():
    """Создать пустое игровое поле из девяти клеток."""
    return [" "] * 9


def render_board(board):
    """Вернуть игровое поле в виде строки для вывода в консоль."""
    cells = [cell if cell != " " else str(index + 1) for index, cell in enumerate(board)]
    return (
        f" {cells[0]} | {cells[1]} | {cells[2]} \n"
        "---+---+---\n"
        f" {cells[3]} | {cells[4]} | {cells[5]} \n"
        "---+---+---\n"
        f" {cells[6]} | {cells[7]} | {cells[8]} "
    )


def parse_position(value):
    """Преобразовать пользовательский ввод в индекс клетки от 0 до 8."""
    try:
        position = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError("Нужно ввести целое число от 1 до 9.") from error

    if position < 1 or position > 9:
        raise ValueError("Номер клетки должен быть от 1 до 9.")
    return position - 1


def make_move(board, position, player):
    """Поставить знак игрока в клетку или сообщить о некорректном ходе."""
    if player not in ("X", "O"):
        raise ValueError("Допустимые игроки: X и O.")
    if not isinstance(position, int) or isinstance(position, bool):
        raise ValueError("Позиция должна быть целым числом.")
    if position < 0 or position >= len(board):
        raise ValueError("Позиция находится за пределами поля.")
    if board[position] != " ":
        raise ValueError("Эта клетка уже занята.")

    board[position] = player


def check_winner(board, player):
    """Проверить, собрал ли игрок три знака в ряд."""
    return any(all(board[index] == player for index in line) for line in WINNING_LINES)


def is_draw(board):
    """Проверить, заполнено ли поле без победителя."""
    return " " not in board and not check_winner(board, "X") and not check_winner(board, "O")


def play_game():
    """Запустить одну партию в консоли (не более девяти успешных ходов)."""
    board = create_board()
    player = "X"

    print("Крестики-нолики. Игрок X ходит первым.")
    print("Выберите клетку, введя число от 1 до 9.")

    for move_number in range(1, 10):
        print("\n" + render_board(board))

        while True:
            value = input(f"\nХод {move_number}/9. Игрок {player}, ваш выбор: ")
            try:
                position = parse_position(value)
                make_move(board, position, player)
                break
            except ValueError as error:
                print(f"Ошибка: {error}")

        if check_winner(board, player):
            print("\n" + render_board(board))
            print(f"\nИгрок {player} победил!")
            return player

        if is_draw(board):
            print("\n" + render_board(board))
            print("\nНичья!")
            return None

        player = "O" if player == "X" else "X"


if __name__ == "__main__":
    play_game()
