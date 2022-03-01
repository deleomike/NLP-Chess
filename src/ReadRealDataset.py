from chess import pgn
import io

with open("./data/train.pgn", 'r') as f:
    text = f.read()

games = text.split("\n")

pgn.read_game(io.StringIO(games[0]))
