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



class Game:

    def __init__(self, threads=2, ELO=1350):

        print(STOCKFISH_BINARY_PATH)

        self.stockfish = Stockfish(path=STOCKFISH_BINARY_PATH,
                                   parameters={"Threads": threads,
                                               "Minimum Thinking Time": 30,
                                               "MultiPV": 1,
                                               "Use NNUE": True})

        self.stockfish.set_skill_level(10)
        self.stockfish.set_depth(20)
        # self.stockfish.set_elo_rating(ELO)
        # self.ELO = ELO

    def run(self):


        num_moves = 0
        moves = []
        while True:
            num_moves = num_moves + 1
            # Average moves per game is 40, so 60 is a deviation above that
            # There should be a better way to detect stalemates
            move = self.stockfish.get_best_move()

            if num_moves > 200:
                eval = self.stockfish.get_evaluation()
                if eval["type"] == "cp" and eval["value"] == 0:
                    print("stalemate")
                    print(self.stockfish.get_board_visual())
                    break

            # stalemate or endgame
            if move is None:
                eval = self.stockfish.get_evaluation()
                if eval["type"] == "cp":
                    print(num_moves)
                    print(self.stockfish.get_board_visual())
                else:
                    print(eval)
                break

            moves.append(move)

            print(move)
            # print("==================")
            # print(self.stockfish.get_board_visual())

            self.stockfish.get_board_visual()

            self.stockfish.make_moves_from_current_position([move])

        return moves


if __name__=="__main__":

    games = []
    times = []
    for _ in tqdm(range(10)):
        start = time.time()
        game = Game(threads=8)
        moves = game.run()
        stop = time.time()

        times.append(stop - start)

        games.append(",".join(moves))

    with open("data.txt", 'w') as f:
        f.write("\n[SEP]\n".join(games))

    print(np.average(times))
