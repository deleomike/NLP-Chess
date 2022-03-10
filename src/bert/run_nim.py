from BertHarmon import BertHarmon

model = BertHarmon("./models/bert-nim/", "./models/bert-nim-tokenizer/vocab.txt")

ans = model.pipeline("a3/b5/c4 A [MOVESEP] [MASK]")
print(ans)
for i in ans:
    print(i["token_str"].replace(" ", ""))