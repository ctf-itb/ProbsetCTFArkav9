import chess
import chess.engine
import random
import socket

STOCKFISH_PATH = "/stockfish/stockfish-ubuntu-x86-64-avx2"
HOST = "127.0.0.1"
PORT = 3000

def print_board(board):
    return str(board)

def get_user_move(board, conn):
    while True:
        try:
            move = conn.recv(1024).decode().strip()
            if chess.Move.from_uci(move) in board.legal_moves:
                return chess.Move.from_uci(move)
            else:
                conn.send("Invalid move!\n".encode())
        except Exception as e:
            conn.send("Invalid input format.\n".encode())

def get_stockfish_move(board, engine):
    result = engine.play(board, chess.engine.Limit(time=2.0))
    return result.move

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server started on {HOST}:{PORT}. Waiting for connections...")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            board = chess.Board()

            with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
                engine.configure({"Skill Level": 17})

                conn.send("Welcome to Chess! You are playing as White. Beat our Frendy!\n".encode())
                
                while not board.is_game_over():
                    board_str = print_board(board)
                    conn.send(f"\nBoard:\n{board_str}\n".encode())

                    if board.turn == chess.WHITE:
                        conn.send("Your move (e.g., e2e4): ".encode())
                        move = get_user_move(board, conn)
                        board.push(move)
                    
                    else:
                        conn.send("Frendy is thinking...\n".encode())
                        move = get_stockfish_move(board, engine)
                        conn.send(f"Frendy plays: {move}\n".encode())
                        board.push(move)

                board_str = print_board(board)
                conn.send(f"Game Over!\n{board_str}\n".encode())

                if board.is_checkmate():
                    if board.turn == chess.WHITE:
                        conn.send("Frendy wins!\n".encode())
                    else:
                        conn.send("You win!\nHere's the reward: ARKAV{ampun_sepuh_catur_👑}\n".encode())
                elif board.is_stalemate():
                    conn.send("It's a stalemate!\n".encode())
                elif board.is_insufficient_material():
                    conn.send("Insufficient material for checkmate!\n".encode())
                elif board.is_variant_draw():
                    conn.send("Draw!\n".encode())
                else:
                    conn.send(board.outcome().result().upper() + "\n".encode())

if __name__ == "__main__":
    start_server()
