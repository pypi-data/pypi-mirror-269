# YogGoPoTh - learning Transformers with the Cthulhu Mythos!

<div style="text-align: right">

> There it was the once I had disglard of that as a daper and cristantent, the tant me trurry that years tabs is deark from a small Noth-eyirly dub to that for the eyard both the land to himself horry bowledge the nolight.
>
> &mdash; ygpt-0.1-32-64

</div>

## Intro

This is a simple implementation of a Transformer encoder model for text generation, based on Andrej Karpathy's "Let's build GPT" video https://www.youtube.com/watch?v=kCc8FmEb1nY&t=970s. While it can be trained on any text, I used the Lovecraft Cthulhu Mythos corpus for training, which made the not-quite-English outputs it produces very fitting (and a bit disturbing).

## Usage

### Installation

1. Create a virtual environment and activate it
2. Install the package into the environment with `make install` (or `make install-dev` to install in the editable mode)

### Training

1. Download the Cthulhu Mythos corpus from https://www.hplovecraft.com/writings/texts/. Cleaning and concatenating the texts is left as an exercise to the reader.
2. Train the model with `python -m yoggopoth train path/to/corpus.txt -s path/to/save/model`

The training produces two files: `model.pth` with the saved model and `model.vocab` with the vocabulary.

The hyperparameters can be adjusted by passing them as the `-p` argument, e.g. `python -m yoggopoth train path/to/corpus.txt -s path/to/save/model -p '{"n_layers": 4, "n_heads": 8}'`. The full list of parameters can be found in `yoggopoth/settings.py`.

Full help available by running `python -m yoggopoth train -h`.

### Generation

1. Generate text with `python -m yoggopoth gen path/to/model`

Optional parameters: `-f` to set the initial text, `-t` to set the length of the generated text, `--stream` to enable streaming output (default), `--nostream` to disable.

Full help available by running `python -m yoggopoth gen -h`.
