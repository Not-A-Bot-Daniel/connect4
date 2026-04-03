# <editor-fold desc="'imports'">
import math
import os
import random as r
import sys
import time as t

import pygame as pg


# </editor-fold>

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# <editor-fold desc="'colors'">
red = "\033[91m"
yellow = "\033[93m"
black = "\033[90m"
blue = "\033[34m"
green = "\033[32m"
purple = "\033[35m"
orange = "\033[38;5;208m"
pink = "\033[38;5;205m"
resetC = "\033[0m"
# </editor-fold>

# הגדרת שחקנים
empty = f" {black}O {resetC}"
p1 = f" {red}O {resetC}"
p2 = f" {yellow}O {resetC}"

# <editor-fold desc="Board Logic">
# הגדרת לוח
board = [[empty] * 7 for i in range(6)]
user_index = [" 1 ", " 2 ", " 3 ", " 4 ", " 5 ", " 6 ", " 7 "]


# איפוס לוח
def reset_board():
    for c in range(7):
        for r in range(6):
            board[r][c] = empty


# יצירת לוח (תוקן הסדר של הארגומנטים)
def makeboard(n1, s1, n2, s2):
    side_text = [
        "      🏆 SCOREBOARD 🏆",
        f"      {n1} : {s1}",
        f"      {n2} : {s2}",
        "",  # שורה ריקה
        "",  # שורה ריקה
        ""  # שורה ריקה
    ]

    print("|" + "|".join(user_index) + "|")
    print("_____________________________")
    for i in range(6):
        row_string = "|" + "|".join(board[i]) + "|"
        print(row_string + side_text[i])


def turn(token, player_name, n1, s1, n2, s2, opponent_token, bot_iq):
    while True:
        if "b1p" in player_name.lower():
            start = t.time()
            found = False
            i = 0
            colum = -1

            while True:
                dots = "." * (i % 4)
                print(f"\rB1P is thinking{dots}   ", end="")
                t.sleep(0.5)
                i += 1
                if not found:
                    colum, ignored_score = minmax(board, bot_iq, -math.inf, math.inf, True, token, opponent_token,
                                                  empty)
                    found = True

                passed = t.time() - start
                if found and passed >= 2:
                    print()
                    break
        else:
            try:
                colum = int(input(f"Enter a column number for {player_name}: ")) - 1
            except ValueError:
                print("Please enter a valid column number")
                continue

            if colum < 0 or colum > 6:
                print("Please enter a valid column number")
                continue
            if board[0][colum] != empty:
                print("no space in that colum, try a different one")
                continue

        # --- אנימציית נפילה ---
        target_row = -1
        for k in range(5, -1, -1):
            if board[k][colum] == empty:
                target_row = k
                break

        for current_row in range(target_row + 1):
            board[current_row][colum] = token

            clear_screen()
            makeboard(n1, s1, n2, s2)

            if current_row < target_row:
                t.sleep(0.08)
                board[current_row][colum] = empty

        break

    clear_screen()
    makeboard(n1, s1, n2, s2)


# </editor-fold>


# <editor-fold desc="'winning checks'">
def check4h(b=board):
    for r in range(6):
        for c in range(4):
            if b[r][c] != empty and b[r][c] == b[r][c + 1] == b[r][c + 2] == b[r][c + 3]:
                return True
    return False


def check4v(b=board):
    for c in range(7):
        for r in range(5, 2, -1):
            if b[r][c] != empty and b[r][c] == b[r - 1][c] == b[r - 2][c] == b[r - 3][c]:
                return True
    return False


def check4dd(b=board):
    for r in range(3):
        for c in range(4):
            if b[r][c] != empty and b[r][c] == b[r + 1][c + 1] == b[r + 2][c + 2] == b[r + 3][c + 3]:
                return True
    return False


def check4du(b=board):
    for r in range(5, 2, -1):
        for c in range(4):
            if b[r][c] != empty and b[r][c] == b[r - 1][c + 1] == b[r - 2][c + 2] == b[r - 3][c + 3]:
                return True
    return False


def win(b=board):
    return check4v(b) or check4h(b) or check4dd(b) or check4du(b)


# </editor-fold>

# <editor-fold desc="'UX/UI'">
def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def show_instructions():
    clear_screen()
    print("=========================================================")
    print("                WELCOME TO CONNECT 4: B1P EDITION        ")
    print("=========================================================")
    print("\nHOW TO PLAY:")
    print("1. The game board has 7 columns (1 to 7).")
    print("2. Players take turns dropping tokens into a column.")
    print("3. Tokens fall to the lowest available space.")

    print("\nWINNING:")
    print("4. Get 4 tokens in a row (Horizontal, Vertical, or Diagonal).")

    print("\nB1P - THE EVOLVING AI:")
    print("- B1P learns from you. Win 2 in a row, and it gets SMARTER.")
    print("- Lose 2 in a row, and B1P will back off to let you breathe.")

    print("\n💀 THE POINT OF NO RETURN:")
    print("- If you dare to defeat B1P while it's already at Level 6,")
    print("  you will trigger 'GOD MODE'.")
    print("- In GOD MODE (Level 10), B1P stops playing games.")
    print("  It will calculate every move to ensure your total defeat.")

    print("\nCONTROLS (FOR TERMINAL BEGINNERS):")
    print("- Type a number (1-7) and press 'ENTER' to confirm.")
    print("- The board clears and redraws after every move.")

    print("\n=========================================================")
    input("\n   Are you brave enough to provoke the machine? Press ENTER... ")
    clear_screen()


# </editor-fold>

def setup():
    name1 = getname(1)
    c1, nope = getcolor(name1, 0)
    t.sleep(1)
    clear_screen()
    name2 = getname(2)
    c2 = getcolor(name2, nope)[0]
    t.sleep(1)
    clear_screen()
    return name1, c1, name2, c2


# <editor-fold desc="'inputs'">
def getname(player_num):
    while True:
        name = input(f"player {player_num}, enter your name: ").strip()
        if not name:
            print("you must enter a name")
            continue
        return name


def getcolor(name, forbidden):
    color_options = [
        (red, "Red"),
        (yellow, "Yellow"),
        (blue, "Blue"),
        (green, "Green"),
        (purple, "Purple"),
        (orange, "Orange"),
        (pink, "Pink"),
    ]

    while True:
        num = 1
        for color_code, color_name in color_options:
            print(f"{num}. {color_code}{color_name}{resetC}", end="  ")
            if num % 3 == 0:
                print()
            num += 1
        print()
        try:
            color = int(input(f"{name}, choose your color: "))
        except ValueError:
            print("Please enter a valid color number, 1-7")
            t.sleep(2)
            continue
        if color < 1 or color > 7:
            print("Please enter a valid color number, 1-7")
            t.sleep(2)
            continue
        if color == forbidden:
            print("you cant have the same color as your opponent")
            t.sleep(2)
            continue
        break
    choice = color_options[color - 1]
    print(f"you chose {choice[0]}{choice[1]}{resetC}")
    t.sleep(1)
    return choice[0], color


# </editor-fold>


def setgame():
    pg.init()
    try:
        pg.mixer.init()
        pg.mixer.music.load(resource_path("c4_music.mp3"))
        pg.mixer.music.play(-1)
    except Exception as e:
        print(f"Could not load music: {e}")


def colors(n1, C1, n2, C2):
    t1 = f" {C1}O {resetC}"
    t2 = f" {C2}O {resetC}"
    colored_n1 = f"{C1}{n1}{resetC}"
    colored_n2 = f"{C2}{n2}{resetC}"
    return t1, t2, colored_n1, colored_n2


# <editor-fold desc="Game Logic">
def rungame(name1, name2, token1, token2, s1, s2, bot_iq):
    reset_board()
    makeboard(name1, s1, name2, s2)
    current_player = token1
    current_opponent = token2
    playersname = name1
    while True:
        turn(current_player, playersname, name1, s1, name2, s2, current_opponent, bot_iq)

        if win():
            print(f"\n🎉{playersname} won! 🎉")
            if current_player == token1:
                return 1
            else:
                return 2
        elif empty not in board[0]:
            print("its a tie!")
            return 0

        if current_player == token1:
            current_player = token2
            current_opponent = token1
            playersname = name2
        else:
            current_player = token1
            current_opponent = token2
            playersname = name1


def game_session(colored_n1, colored_n2, t1, t2):
    score1 = 0
    score2 = 0

    player_streak = 0
    bot_streak = 0
    bot_iq = 3

    while True:
        clear_screen()
        winner = rungame(colored_n1, colored_n2, t1, t2, score1, score2, bot_iq)

        print()
        if winner == 1:
            score1 += 1
            player_streak += 1
            bot_streak = 0
        elif winner == 2:
            score2 += 1
            bot_streak += 1
            player_streak = 0

        print(f"the score is\n{colored_n1} - {score1}\n{colored_n2} - {score2}")
        print()

        # --- שינוי רמת הקושי בהתאם לתוצאות ---
        if player_streak >= 4 and bot_iq == 6:
            bot_iq = 10
            print("think you are tough? GOD MODE ACTIVATED!")
            player_streak = 0
            try:
                pg.mixer.music.load(resource_path("god_mode_music.mp3"))
                pg.mixer.music.play(-1)
            except:
                pass

        elif player_streak >= 2:
            bot_iq = min(6, bot_iq + 1)
            print("B1P is learning your strategy... It just got SMARTER!")
            player_streak = 0

        elif bot_streak >= 2:
            if bot_iq == 10:
                bot_iq = 5
                try:
                    pg.mixer.music.load(resource_path("c4_music.mp3"))
                    pg.mixer.music.play(-1)
                except Exception as e:
                    pass
            else:
                bot_iq = max(1, bot_iq - 1)

            print("B1P's circuits are cooling down... It just got EASIER.")
            bot_streak = 0

        # --- מצב הובלה ---
        if score1 > score2:
            print(f"{colored_n1} is in the lead")
        elif score1 < score2:
            print(f"{colored_n2} is in the lead")
        elif score1 == score2:
            print("its a tie, you must play a tie braker")

        t.sleep(3)
        clear_screen()
        print(f"the score is\n{colored_n1} - {score1}\n{colored_n2} - {score2}")

        while True:
            answer = input("want to play again?[y/n]").lower().strip()
            if answer not in ["y", "n"]:
                print("Please enter a valid answer, y for yes or n for no")
                continue
            break

        if answer == "y":
            t.sleep(1)
            continue
        else:
            clear_screen()
            print("Thank you for playing")
            t.sleep(2)
            clear_screen()
            print("goodbye")
            t.sleep(2)
            break


def game_mode():
    while True:
        print("do you want to play with a friend\nor against the computer?")
        try:
            aws = int(input("type 1 to playing against the computer\ntype 2 to play with a friend"))
        except ValueError:
            print("Please enter a valid answer, 1 for playing against the computer, 2 for playing with a friend")
            continue
        if aws == 1:
            return 1
        elif aws == 2:
            return 2
        else:
            print("Please enter a valid answer, 1 for playing against the computer, 2 for playing with a friend")


def game_mode_1():
    name1 = getname(1)
    c1, nope = getcolor(name1, 0)
    t.sleep(1)
    clear_screen()
    name2 = "B1P"
    bot_color_num = nope + 1 if nope < 7 else 1

    color_options = [red, yellow, blue, green, purple, orange, pink]
    c2 = color_options[bot_color_num - 1]
    t1, t2, colored_n1, colored_n2 = colors(name1, c1, name2, c2)
    print(f"the bot name is {c2}B1P{resetC} ")
    t.sleep(2)

    game_session(colored_n1, colored_n2, t1, t2)


def game_mode_2():
    name1 = getname(1)
    c1, nope1 = getcolor(name1, 0)
    name2 = getname(2)
    c2, nope2 = getcolor(name2, nope1)
    t1, t2, colored_n1, colored_n2 = colors(name1, c1, name2, c2)

    game_session(colored_n1, colored_n2, t1, t2)
    # נמחק כאן קוד מת שלא היה יכול לרוץ לעולם


# </editor-fold>

# בוט
def evaluate_window(window, bot_token, player_token, empty_token):
    score = 0

    bot_count = window.count(bot_token)
    players_count = window.count(player_token)
    empty_count = window.count(empty_token)

    # הניקוד תוקן כדי לא להוריד פעמיים על אותו איום
    if bot_count == 4:
        score += 100
    elif bot_count == 3 and empty_count == 1:
        score += 5
    elif bot_count == 2 and empty_count == 2:
        score += 2

    if players_count == 4:
        score -= 200
    elif players_count == 3 and empty_count == 1:
        score -= 80
    elif players_count == 2 and empty_count == 2:
        score -= 2

    return score


def score_position(board, bot_token, player_token, empty_token):
    total_score = 0

    # בדיקת ניקוד שורות
    for r in range(6):
        row_array = board[r]
        for c in range(4):
            window = row_array[c:c + 4]
            total_score += evaluate_window(window, bot_token, player_token, empty_token)

    # בדיקת ניקוד עמודות
    for c in range(7):
        colum_array = [board[i][c] for i in range(6)]
        for r in range(3):
            window = colum_array[r:r + 4]
            total_score += evaluate_window(window, bot_token, player_token, empty_token)

    # בדיקת אלכסון יורד
    for r in range(3):
        for c in range(4):
            window = []
            for i in range(4):
                window.append(board[r + i][c + i])
            total_score += evaluate_window(window, bot_token, player_token, empty_token)

    # בדיקת אלכסון עולה
    for r in range(5, 2, -1):
        for c in range(4):
            window = []
            for i in range(4):
                window.append(board[r - i][c + i])
            total_score += evaluate_window(window, bot_token, player_token, empty_token)

    return total_score


def move_picker(board, bot_token, player_token, empty_token):
    valid_location = []
    for col in range(7):
        if board[0][col] == empty_token:
            valid_location.append(col)

    best_score = -100000
    best_cols = []
    center_col = 3

    for col in valid_location:
        temp_board = [row[:] for row in board]

        for row_idx in range(5, -1, -1):
            if temp_board[row_idx][col] == empty_token:
                temp_board[row_idx][col] = bot_token
                break

        current_score = score_position(temp_board, bot_token, player_token, empty_token)
        if current_score > best_score:
            best_score = current_score
            best_cols = [col]
        elif current_score == best_score:
            best_cols.append(col)

    closest_to_center = min(abs(col - center_col) for col in best_cols)
    center_priority_cols = [col for col in best_cols if abs(col - center_col) == closest_to_center]

    return r.choice(center_priority_cols)


def get_valid_colums(board, empty_token):
    valid_colums = []

    for c in range(7):
        if board[0][c] == empty_token:
            valid_colums.append(c)
    return valid_colums


def get_bottom_space(board, col, empty_token):
    for row in range(5, -1, -1):
        if board[row][col] == empty_token:
            return row
    return None


def get_valid_location(board, empty_token):
    valid_columns = get_valid_colums(board, empty_token)
    center_preference = [3, 2, 4, 1, 5, 0, 6]
    valid_columns.sort(key=lambda col: center_preference.index(col) if col in center_preference else 10)

    playable_locations = []
    for col in valid_columns:
        row = get_bottom_space(board, col, empty_token)
        playable_locations.append((row, col))
    return playable_locations


def minmax(board, depth, alpha, beta, minmaxPlayer, bot_token, player_token, empty_token):
    valid_locations = get_valid_location(board, empty_token)
    is_win = win(board)
    is_tie = len(valid_locations) == 0

    if depth == 0 or is_win or is_tie:
        if is_win:
            if not minmaxPlayer:
                return (None, 100000000000000)
            else:
                return (None, -100000000000000)
        elif is_tie:
            return (None, 0)
        else:
            return (None, score_position(board, bot_token, player_token, empty_token))

    if minmaxPlayer:
        value = -math.inf
        best_col = valid_locations[0][1]
        for row, col in valid_locations:
            board[row][col] = bot_token
            ignored_col, new_score = minmax(board, depth - 1, alpha, beta, False, bot_token, player_token, empty_token)
            board[row][col] = empty_token
            if new_score > value:
                value = new_score
                best_col = col

            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value

    else:
        value = math.inf
        best_col = valid_locations[0][1]
        for row, col in valid_locations:
            board[row][col] = player_token
            ignored_col, new_score = minmax(board, depth - 1, alpha, beta, True, bot_token, player_token, empty_token)
            board[row][col] = empty_token
            if new_score < value:
                value = new_score
                best_col = col

            beta = min(beta, value)
            if alpha >= beta:
                break

        return best_col, value


if __name__ == "__main__":
    setgame()
    show_instructions()
    mode = game_mode()
    if mode == 2:
        game_mode_2()
    elif mode == 1:
        game_mode_1()
