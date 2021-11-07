from transformers import AutoModelForMaskedLM, RobertaForMaskedLM
from transformers import AutoTokenizer
from transformers import RobertaTokenizer, BertTokenizer
from transformers import pipeline
from tokenizers import ByteLevelBPETokenizer
import os


class BertHarmon:

    def __init__(self, checkpoint_path, tokenizerpath):
        self.model = AutoModelForMaskedLM.from_pretrained(checkpoint_path, )
        self.tokenizer = BertTokenizer.from_pretrained(tokenizerpath, max_len=128)

        self.pipeline = pipeline("fill-mask", model=self.model, tokenizer=self.tokenizer, top_k=50)

    def validate_move(self, move:str):
        return True

    def make_move(self, FEN_Position: str, IsWhiteMove: bool = True):
        move_str = FEN_Position
        if IsWhiteMove:
            move_str += " White <MOVE_SEP>"
        else:
            move_str += " Black <MOVE_SEP>"

        move_str += " [MASK]"

        # tokenized_move = self.tokenizer.encode(move_str).tokens

        # print(tokenized_move)

        return self.pipeline(move_str)

        # return self.model(tokenized_move)


class RobertHarmon:

    def __init__(self, checkpoint_path, tokenizerpath):
        self.model = RobertaForMaskedLM.from_pretrained(checkpoint_path, )
        self.tokenizer = RobertaTokenizer.from_pretrained(tokenizerpath, max_len=128)

        self.pipeline = pipeline("fill-mask", model=self.model, tokenizer=self.tokenizer, top_k=5)

    def validate_move(self, move:str):
        return True

    def branch_move(self, sequence):
        """
        Base case:
        Make sure there is a space after <MOVE_SEP>
        6RQ/8/8/4K3/8/4k3/2R5/8 w - - 1 94 White <MOVE_SEP>

        :param sequence:
        :param length:
        :return:
        """

        def branch_move_helper(sequence, length):

            # Sequence is already done
            if length == 4:
                return [sequence]

            # Add mask
            if type(sequence) == str:
                res_sequence = sequence + "<mask>"
            else:
                res_sequence = sequence["sequence"] + "<mask>"

            top_k_sequences = self.pipeline(res_sequence)

            # print(top_k_sequences, length)

            branch_sequences = []

            for sequence in top_k_sequences:
                # Requires a number as odd, or a letter as even
                if (length % 2 == 0 and sequence["token_str"].strip().isalpha()) or \
                        (length % 2 == 1 and sequence["token_str"].strip().isdigit()):
                    # Now extend this list by the branching of each sequence
                    branch_sequences.extend(branch_move_helper(sequence, length + 1))

            return branch_sequences

        res_sequences = branch_move_helper(sequence, 0)

        for i, sequence in enumerate(res_sequences):
            res_sequences[i] = {
                "sequence": sequence["sequence"],
                "token_str": sequence["sequence"].split("<MOVE_SEP>")[-1]
            }

        return res_sequences


    def make_move(self, FEN_Position: str, IsWhiteMove: bool = True):
        move_str = FEN_Position
        if IsWhiteMove:
            move_str += " White <MOVE_SEP> "
        else:
            move_str += " Black <MOVE_SEP> "

        sequences = self.branch_move(move_str)

        return sequences

        # tokenized_move = self.tokenizer.encode(move_str).tokens

        # print(tokenized_move)




        # return self.model(tokenized_move)

if __name__ == "__main__":

    BH = BertHarmon(checkpoint_path="./bert-harmon",
                    tokenizerpath="./vocab.txt")

    RH = RobertHarmon(checkpoint_path="./robert-harmon",
                    tokenizerpath="./roberta-harmon-tokenizer")

    tokenizer = ByteLevelBPETokenizer(
        os.path.abspath(os.path.join("./roberta-harmon-tokenizer", 'vocab.json')),
        os.path.abspath(os.path.join("./roberta-harmon-tokenizer", 'merges.txt'))
    )

    print(tokenizer.encode("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 White <move_sep> e2e4").tokens)

    print(RH.make_move("6RQ/8/8/4K3/8/4k3/2R5/8 w - - 1 94"))

    print(RH.make_move("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1", False))

    #
    # print(tokenizer.encode("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 White <move_sep> e2e4").tokens)
    #
    # print(BH.make_move("6RQ/8/8/4K3/8/4k3/2R5/8 w - - 1 94"))
    #
    # print(BH.make_move("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1", False))

