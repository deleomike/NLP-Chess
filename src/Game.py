from stockfish import Stockfish
from tqdm import tqdm

import numpy as np

import os
import time

import argparse

REPO_DIR = os.path.realpath(os.path.join(os.path.realpath(__file__), "..", ".."))

STOCKFISH_BINARY_PATH = os.path.join(REPO_DIR,
                                     "stockfish_build",
                                     "stockfish",
                                     "src",
                                     "stockfish")

STOCKFISH_BINARY_PATH = os.path.realpath(STOCKFISH_BINARY_PATH)

parser = argparse.ArgumentParser()

parser.add_argument("--games", default=3000000, type=int)
parser.add_argument("--threads", default=1, type=int)
parser.add_argument("--thinking_time", default=100, type=int)




class Game:

    def __init__(self, threads=2, ELO=3900, thinking_time=50):

        self.ELO = ELO
        self.threads = threads
        self.thinking_time = thinking_time

        # print(STOCKFISH_BINARY_PATH)
        # self.stockfish.set_depth(20)
        # self.stockfish.set_elo_rating(ELO)
        # self.ELO = ELO

    def run(self):

        self.stockfish = Stockfish(path=STOCKFISH_BINARY_PATH,
                                   parameters={"Threads": self.threads,
                                               "Minimum Thinking Time": self.thinking_time,
                                               "MultiPV": 1,
                                               "Use NNUE": True})

        self.stockfish.set_elo_rating(self.ELO)
        self.stockfish.set_depth(5)

        # print(self.stockfish.get_parameters())


        num_moves = 0
        moves = []
        FEN_positions = []
        while True:
            num_moves = num_moves + 1
            # Average moves per game is 40, so 60 is a deviation above that
            # There should be a better way to detect stalemates

            FEN_positions.append(self.stockfish.get_fen_position())
            move = self.stockfish.get_best_move()

            if num_moves > 200:
                eval = self.stockfish.get_evaluation()
                if eval["type"] == "cp" and eval["value"] == 0:
                    FEN_positions.pop()
                    # print("stalemate")
                    # print(self.stockfish.get_board_visual())
                    break

            # stalemate or endgame
            if move is None:
                eval = self.stockfish.get_evaluation()
                FEN_positions.pop()
                # if eval["type"] == "cp":
                #     print(num_moves)
                #     print(self.stockfish.get_board_visual())
                # else:
                #     print(eval)
                break

            moves.append(move)

            # print(move)
            # print("==================")
            # print(self.stockfish.get_board_visual())

            self.stockfish.get_board_visual()

            self.stockfish.make_moves_from_current_position([move])

        return moves, FEN_positions


if __name__=="__main__":

    args = parser.parse_args()

    game = Game(threads=args.threads, thinking_time=args.thinking_time)

    dataset_1 = []
    dataset_2 = []
    all_fen_positions = []
    all_players_encoded = []
    all_moves = []
    times = []
    for _ in tqdm(range(args.games)):
        start = time.time()
        moves, fen_positions = game.run()
        stop = time.time()

        times.append(stop - start)

        dataset_1.append(" <MOVE_SEP> ".join(moves))

        tmp = fen_positions
        tmp = np.array(tmp, dtype=str)
        tmp[::2] = "White"
        tmp[1::2] = "Black"

        all_moves.extend(moves)
        all_fen_positions.extend(fen_positions)
        all_players_encoded.extend(list(tmp))

        # for fen, move in zip(np.array(fen_positions), np.array(moves)):
        #     dataset_2.append(fen + " <MOVE_SEP> " + move)

    with open("dataset_1.txt", 'w') as f:
        f.write("\n<SEP>\n".join(dataset_1))

    with open("dataset_2.txt", 'w') as f:
        dataset_2 = map(" <MOVE_SEP> ".join, zip(all_fen_positions, all_moves))
        f.write("\n<SEP>\n".join(dataset_2))

    with open("dataset_3.txt", 'w') as f:
        all_fen_encoded = map(" ".join, zip(all_fen_positions, all_players_encoded))
        dataset_3 = map(" <MOVE_SEP> ".join, zip(all_fen_encoded, all_moves))
        f.write("\n<SEP>\n".join(dataset_3))

    print(np.average(times))
