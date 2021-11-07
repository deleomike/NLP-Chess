import matplotlib.pyplot as plt
import json
from tqdm import tqdm

with open("./bert-harmon/trainer_state.json", 'r') as f:
    data = json.load(f)["log_history"]

epochs = []
loss = []
lr = []

for entry in tqdm(data):
    epochs.append(entry["epoch"])
    loss.append(entry["loss"])
    lr.append(entry["learning_rate"])


plt.figure(1)
plt.plot(epochs, loss)
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("Training - BertHarmon")

plt.figure(2)
plt.plot(epochs, lr)
plt.xlabel("Epochs")
plt.ylabel("Learning Rate")
plt.title("LR Decay - BertHarmon")
plt.show()