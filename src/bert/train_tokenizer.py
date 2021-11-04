from tokenizers import Tokenizer, AutoConfig
from tokenizers.models import BPE

tokenizer = Tokenizer(BPE())

# Initialize a tokenizer
# tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

from tokenizers.trainers import BpeTrainer

trainer = BpeTrainer(special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"], show_progress=True)
tokenizer.train(files=["/home/michael/Workspace/NLP-Chess/src/data/dataset_3_sep.txt",
                       "/home/michael/Workspace/NLP-Chess/src/data/dataset_1.txt"], trainer=trainer)

# # Customize training
# tokenizer.train(files="/home/michael/Workspace/NLP-Chess/src/data/dataset_3_sep.txt", vocab_size=52_000, min_frequency=2, special_tokens=[
#     "<s>",
#     "<pad>",
#     "</s>",
#     "<unk>",
#     "<mask>",
# ])

tokenizer.save()
tokenizer.
# Save files to disk
tokenizer.save_model(".", "bert-harmon")