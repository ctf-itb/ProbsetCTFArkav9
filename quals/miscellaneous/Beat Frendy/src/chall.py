import chess
import chess.engine
import signal
import sys

STOCKFISH_PATH = "/stockfish/stockfish-ubuntu-x86-64-avx2"

class TimeoutException(Exception):
    pass

def handler(signum, frame):
    raise TimeoutException

def start_timer(timeout_seconds):
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_seconds)


def print_board(board):
    return str(board)

def get_user_move(board, is_first_move):
    while True:
        timeout_seconds = 5
        start_timer(timeout_seconds)

        try:
            move = input("Your move (e.g., e2e4): ").strip()

            if is_first_move and move != "g2g4":
                print("Your first move must be g2g4!\n")
                continue

            if chess.Move.from_uci(move) in board.legal_moves:
                return chess.Move.from_uci(move)
            else:
                print("Invalid move!\n")
        except TimeoutException:
            print("\nDon't think too long.. bang..")
            sys.exit(1)
        except Exception as e:
            print("Invalid input format.\n")
        finally:
            signal.alarm(0)

def get_stockfish_move(board, engine):
    result = engine.play(board, chess.engine.Limit(time=2.0))
    return result.move

def play_game():
    board = chess.Board()
    is_first_move = True


    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        engine.configure({"Skill Level": 15})

        print("Welcome to Chess! You are playing as White. Beat our Frendy!")
        
        while not board.is_game_over():
            board_str = print_board(board)
            print(f"\nBoard:\n{board_str}\n")

            if board.turn == chess.WHITE:
                move = get_user_move(board, is_first_move)
                is_first_move = False
                board.push(move)
            
            else:
                print("Frendy is thinking...\n")
                move = get_stockfish_move(board, engine)
                print(f"Frendy plays: {move}\n")
                board.push(move)

        board_str = print_board(board)
        print(f"Game Over!\n{board_str}\n")

        if board.is_checkmate():
            if board.turn == chess.WHITE:
                print("Frendy wins!\n")
            else:
                print("You win!\nHere's the reward: ARKAV{hanya_sepuh_yang_berani_make_opening_g2-g4}\n")
        elif board.is_stalemate():
            print("It's a stalemate!\n")
        elif board.is_insufficient_material():
            print("Insufficient material for checkmate!\n")
        elif board.is_variant_draw():
            print("Draw!\n")
        else:
            print(board.outcome().result().upper() + "\n")

if __name__ == "__main__":
    play_game()
