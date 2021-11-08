---
thumbnail: "https://en.memesrandom.com/wp-content/uploads/2020/11/juega-ajedrez.jpeg"
widget:
- text: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 White <MOVE_SEP> [MASK]"
- example_title: Empty Board
- text: "6Q1/5k2/3P4/1R3p2/P4P2/7Q/6RK/8 b - - 2 60 Black <MOVE_SEP> [MASK]"
- example_title: Late Game Board
---



# BertHarmon

Research done at Johns Hopkins University by Michael DeLeo![iu-13](logo.png)

Contact: mdeleo2@jh.edu

## Links

[Github](https://github.com/deleomike/NLP-Chess)

[HuggingFace](https://huggingface.co/squish/BertHarmon)

## Introduction

BertHarmon is a BERT model trained for the task of Chess.

![IMG_0145](chess-example.GIF)

## Sample Usage

```python
from transformers import pipeline
task = pipeline('fill-mask', model='BertHarmon')
task("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 White <MOVE_SEP> [MASK]")
```

The base string consists of the FEN_position followed by the player color and a move seperator. Finally with the [MASK] token. The mask token is the algebraic notation for a chess move to be taken givent the current board state in FEN Notation