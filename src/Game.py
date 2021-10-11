from stockfish import Stockfish
from tqdm import tqdm

import numpy as np

import time


class Game:

    def __init__(self, threads=2, ELO=1350):

        self.stockfish = Stockfish(parameters={"Threads": threads, "Minimum Thinking Time": 30})

        self.stockfish.set_skill_level(10)
        # self.stockfish.set_elo_rating(ELO)
        # self.ELO = ELO

    def run(self):

        num_moves = 0
        while True:
            num_moves = num_moves + 1
            if num_moves > 60:
                # stalemate
                break
            move = self.stockfish.get_best_move()

            if move is None:
                break

            # print(move)

            self.stockfish.make_moves_from_current_position([move])

if __name__=="__main__":

    times = []
    for _ in tqdm(range(1000)):
        start = time.time()
        game = Game()
        game.run()
        stop = time.time()

        times.append(stop - start)

    print(np.average(times))
