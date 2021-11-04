from transformers import AutoModelForMaskedLM
from transformers import AutoTokenizer
from transformers import BertTokenizer
from transformers import pipeline

class BertHarmon:

    def __init__(self, checkpoint_path, tokenizerpath):
        self.model = AutoModelForMaskedLM.from_pretrained(checkpoint_path)
        self.tokenizer =  BertTokenizer.from_pretrained(tokenizerpath)

        self.pipeline = pipeline("fill-mask", model=checkpoint_path, tokenizer=self.tokenizer)

    def validate_move(self, move:str):
        return True

    def make_move(self, FEN_Position: str, IsWhiteMove: bool = True):
        move_str = FEN_Position
        if IsWhiteMove:
            move_str += " White <MOVE_SEP>"
        else:
            move_str += " Black <MOVE_SEP>"

        move_str += " [MASK]\n"

        tokenized_move = self.tokenizer(move_str)

        print(tokenized_move)

        return self.pipeline(move_str)

        # return self.model(tokenized_move)

if __name__ == "__main__":

    BH = BertHarmon(checkpoint_path="/home/michael/Workspace/transformers/examples/pytorch/language-modeling/output/checkpoint-6000",
                    tokenizerpath="/home/michael/Workspace/transformers/examples/pytorch/language-modeling/bert-harmon/vocab.txt")

    print(BH.make_move("6RQ/8/8/4K3/8/4k3/2R5/8 w - - 1 94"))

    print(BH.make_move("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1", False))

