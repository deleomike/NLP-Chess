from BertHarmon import BertHarmon

model = BertHarmon("./models/bert-nim/", "./models/bert-nim-tokenizer/vocab.txt")

ans = model.pipeline("a0/b3/c3 A [MOVESEP] [MASK]")
print(ans)
for i in ans:
    print(f"{i['token_str'].replace(' ', '')}: {i['score']}")