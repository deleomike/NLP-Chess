from stockfish import Stockfish
import json

with open("settings.json") as f:
    file = json.load(f)

    stockfish_path = file["stockfish_path"]

print(stockfish_path)

stockfish = Stockfish(parameters={"Threads": 2, "Minimum Thinking Time": 30})

stockfish.set_position(["e2e4", "e7e6"])

stockfish.make_moves_from_current_position(["g4d7", "a8b8", "f1d1"])

stockfish.set_fen_position("rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")

print(stockfish.get_best_move())