from transformers import AutoModelForQuestionAnswering
from datasets import load_dataset
import os

raw_datasets = load_dataset('text', data_files="/home/michael/Workspace/NLP-Chess/src/data/dataset_3_sep.txt",
                            split='train')

raw_datasets = raw_datasets.select(range(10000))
raw_datasets = raw_datasets.train_test_split()

from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-cased", use_fast=True)

def tokenize_function(examples):
    return tokenizer(examples["text"], padding='max_length', truncation=True)

import pickle

# if os.path.exists("dataset-tokenized.obj"):
#     with open("dataset-tokenized.obj", 'rb') as f:
#         tokenized_datasets = pickle.load(f)
# else:
#     print("tokenizing")
tokenized_datasets = raw_datasets.map(tokenize_function, batched=True, keep_in_memory=True, num_proc=20, remove_columns=["text"])
# tokenized_datasets = raw_datasets
#     with open("dataset-tokenized.obj", 'wb') as f:
#         pickle.dump(tokenized_datasets, f)

# block_size = tokenizer.model_max_length
block_size = 128

def group_texts(examples):
    # Concatenate all texts.
    concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
    total_length = len(concatenated_examples[list(examples.keys())[0]])
    # We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
        # customize this part to your needs.
    total_length = (total_length // block_size) * block_size
    # Split by chunks of max_len.
    result = {
        k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
        for k, t in concatenated_examples.items()
    }
    result["labels"] = result["input_ids"].copy()
    return result
print(tokenized_datasets["train"][1])
lm_datasets = tokenized_datasets.map(
    group_texts,
    batched=True,
    batch_size=1000,
    num_proc=20,
)

small_train_dataset = lm_datasets["train"].shuffle(seed=42).select(range(1000))
# small_train_dataset["labels"] = small_train_dataset["input_ids"]
small_eval_dataset = lm_datasets["test"].shuffle(seed=42).select(range(1000))
# small_eval_dataset["labels"] = small_eval_dataset["input_ids"]
full_train_dataset = lm_datasets["train"]
full_eval_dataset = lm_datasets["test"]

from transformers import AutoModelForMaskedLM
model = AutoModelForMaskedLM.from_pretrained("bert-base-cased")

from transformers import TrainingArguments

training_args = TrainingArguments(per_device_train_batch_size=240, output_dir='./output', num_train_epochs=200,)

from transformers import Trainer, DataCollatorForLanguageModeling

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm_probability=0.15,
)

trainer = Trainer(
    model=model, args=training_args, train_dataset=full_train_dataset, eval_dataset=full_eval_dataset, data_collator=data_collator
)

trainer.train()


