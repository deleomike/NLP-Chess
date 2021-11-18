from stockfish import Stockfish
from tqdm import tqdm

import numpy as np
import random
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

        self.first_moves = [
            "a2a3",
            "b2b3",
            "c2c3",
            "d2d3",
            "e2e3",
            "f2f3",
            "g2g3",
            "h2h3",
            "a2a4",
            "b2b4",
            "c2c4",
            "d2d4",
            "e2e4",
            "f2f4",
            "g2g4",
            "h2h4",
            "b1a3",
            "b1c3",
            "g1f3",
            "g1h3"
        ]

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

            if num_moves == 1:
                # for the first move
                index = random.randint(0, len(self.first_moves))
                move = self.first_moves[index]
            else:
                move = self.stockfish.get_best_move()

            if num_moves > 30:
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

    f3 = open("dataset_fen.txt", 'a')

    for _ in tqdm(range(args.games)):
        start = time.time()
        moves, fen_positions = game.run()
        stop = time.time()

        times.append(stop - start)

        dataset_3 = map(" [MOVESEP] ".join, zip(fen_positions, moves))
        f3.write("\n".join(dataset_3) + "\n")

        all_fen_positions = []
        all_moves = []
        all_players_encoded = []

    print(np.average(times))
