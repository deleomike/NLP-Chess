from transformers import AutoModelForMaskedLM
from transformers import BertTokenizer
from transformers import pipeline
import os


class BertHarmon:

    def __init__(self, checkpoint_path, tokenizerpath, top_k=10):
        self.model = AutoModelForMaskedLM.from_pretrained(checkpoint_path, )
        self.tokenizer = BertTokenizer.from_pretrained(tokenizerpath, max_len=128)

        self.pipeline = pipeline("fill-mask", model=self.model, tokenizer=self.tokenizer, top_k=top_k)

    def validate_move(self, move:str):
        return True

    def make_move(self, game_str: str):
        """
        Example:

        NIM:

        a3/b5/c4 A [MOVESEP]

        Chess:

        rnbqkb1r/pppppppp/5n2/8/5P2/8/PPPPP1PP/RNBQKBNR w KQkq - 1 2 [MOVESEP]

        :param game_str: Refer above. it should be a sequence of the game
        :return: move
        """

        game_str += " [MASK]"

        return self.pipeline(game_str)

