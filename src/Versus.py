from stockfish import Stockfish
from tqdm import tqdm
import matplotlib.pyplot as plt

import numpy as np

import os
import time

import argparse

from src.bert.BertHarmon import BertHarmon, RobertHarmon

REPO_DIR = os.path.realpath(os.path.join(os.path.realpath(__file__), "..", ".."))

STOCKFISH_BINARY_PATH = os.path.join(REPO_DIR,
                                     "stockfish_build",
                                     "stockfish",
                                     "src",
                                     "stockfish")

STOCKFISH_BINARY_PATH = os.path.realpath(STOCKFISH_BINARY_PATH)

class Game:

    def __init__(self, threads=1, ELO=100, thinking_time=1, verbose=True):

        self.ELO = ELO
        self.threads = threads
        self.thinking_time = thinking_time

        self.stockfish = Stockfish(path=STOCKFISH_BINARY_PATH,
                                   parameters={"Threads": self.threads,
                                               "Minimum Thinking Time": self.thinking_time,
                                               "Use NNUE": True})

        self.stockfish.set_elo_rating(3900)
        self.stockfish.set_depth(1)

        self.verbose = verbose

        self.BertHarmon = BertHarmon(checkpoint_path="./bert/bert-harmon", tokenizerpath="./bert/vocab.txt")
        # self.BertHarmon = RobertHarmon(checkpoint_path="./bert/robert-harmon",
        #             tokenizerpath="./bert/roberta-harmon-tokenizer")

    def get_valid_move(self, FEN, isWhite):
        sequences = self.BertHarmon.make_move(FEN, isWhite)

        for sequence in sequences:
            move = sequence["token_str"].replace(" ","")
            if self.verbose:
                print(sequence)
                print(move)
            if self.stockfish.is_move_correct(move):
                return move

        # Forfeit, no valid move
        return None


    def play(self):

        isWhite = True

        moves = []

        while True:

            if self.verbose:
                print(self.stockfish.get_board_visual())

            if not isWhite:
                move = self.stockfish.get_best_move()
                if move is None:
                    if self.verbose:
                        print("game over bert won")
                    break

                # move = self.get_valid_move(self.stockfish.get_fen_position(), isWhite)

                self.stockfish.make_moves_from_current_position([move])

                if self.verbose:
                    print("Stockfish:", move)
                moves.append(move)

            else:
                if self.stockfish.get_best_move() is None:
                    if self.verbose:
                        print("game over stockfish won")
                    break
                move = self.get_valid_move(self.stockfish.get_fen_position(), isWhite)

                if move is None:
                    if self.verbose:
                        print("Bert forfeits")
                    break

                self.stockfish.make_moves_from_current_position([move])
                # self.stockfish.

                if self.verbose:
                    print("BERT: ", move)
                moves.append(move)

            isWhite = not isWhite

        return moves


if __name__ == "__main__":

    hist_data = []
    for _ in tqdm(range(1000)):
        game = Game(verbose=False)
        moves = game.play()
        hist_data.append(len(moves))

    plt.hist(hist_data)
    plt.show()

    print(hist_data)



    pgn = ""
    # for i, val in enumerate(moves):
    #     pgn += f"{i + 1}.{val} "
    #
    # with open("game.pgn", 'w') as f:
    #     f.write(pgn)