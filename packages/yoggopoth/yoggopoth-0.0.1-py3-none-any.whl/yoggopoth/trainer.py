import time
from pathlib import Path

import torch

from yoggopoth.models import AttentionLanguageModel
from yoggopoth.settings import Hyperparams

if torch.cuda.is_available():
    torch_device = torch.device("cuda")
# MPS brings a lot of overhead for small models like this
# elif torch.backends.mps.is_available():
#     torch_device = torch.device("mps")
else:
    torch_device = torch.device("cpu")

print(f"Using device: {torch_device}")


class Codec:
    def __init__(self, chars):
        self.chars = chars
        self.vocab_size = len(chars)
        self.stoi = {ch: i for i, ch in enumerate(chars)}
        self.itos = {i: ch for i, ch in enumerate(chars)}

    @classmethod
    def from_text(cls, text):
        return cls(sorted(list(set(text))))

    def encode(self, string):
        return [self.stoi[c] for c in string]

    def decode(self, line):
        return "".join(self.itos[i] for i in line)

    def as_tensor(self, text):
        return torch.tensor(self.encode(text), dtype=torch.long)

    def save(self, path):
        Path(path).write_text("".join(self.chars))

    @classmethod
    def load(cls, path):
        return cls(Path(path).read_text())


class Loader:
    def __init__(self, dataset):
        self.text = Path(dataset).read_text().strip()
        self.codec = Codec.from_text(self.text)
        self.vocab_size = self.codec.vocab_size

    def __len__(self):
        return len(self.text)

    def as_tensor(self, text=None):
        return self.codec.as_tensor(text or self.text)

    def get_encoder(self):
        return self.codec.encode

    def get_decoder(self):
        return self.codec.decode


class Trainer:
    eval_iters = 100
    eval_interval = 100
    model_cls = AttentionLanguageModel
    optimizer_cls = torch.optim.AdamW

    @classmethod
    def from_loader(cls, loader, hyperparams):
        return cls(loader.as_tensor(), loader.vocab_size, hyperparams)

    def __init__(
        self,
        data: torch.Tensor,
        vocab_size: int,
        h: Hyperparams,
    ):
        self.h = h
        self.model = self.model_cls(h, vocab_size).to(torch_device)
        self.optimizer = self.optimizer_cls(self.model.parameters(), lr=h.learning_rate)
        self.data = data
        n = int((1 - h.test_size) * len(data))
        self.train_data, self.val_data = data[:n], data[n:]

    def get_batch(self, split):
        data = self.train_data if split == "train" else self.val_data
        ix = torch.randint(len(data) - self.h.block_size, (self.h.batch_size,))
        x = torch.stack([data[i : i + self.h.block_size] for i in ix])
        y = torch.stack([data[i + 1 : i + self.h.block_size + 1] for i in ix])
        x, y = x.to(torch_device), y.to(torch_device)
        return x, y

    @torch.no_grad()
    def estimate_loss(self):
        out = {}
        self.model.eval()
        for split in ["train", "val"]:
            losses = torch.zeros(self.eval_iters)
            for k in range(self.eval_iters):
                xb, yb = self.get_batch(split)
                logits, loss = self.model(xb, yb)
                losses[k] = loss.item()
            out[split] = losses.mean()
        self.model.train()
        return out

    def train(self, steps=10000):
        eval_interval = max(steps // 10, self.eval_interval)
        last_time = time.time()
        for step in range(steps):
            if step % eval_interval == 0:
                losses = self.estimate_loss()
                this_time = time.time()
                print(
                    f"step: {step}, train loss: {losses['train']:.4f}, "
                    f"val loss: {losses['val']:.4f}, time: {this_time - last_time:.2f}s"
                )
                last_time = this_time
            xb, yb = self.get_batch("train")
            logits, loss = self.model(xb, yb)
            self.optimizer.zero_grad(set_to_none=True)
            loss.backward()
            self.optimizer.step()
        return loss.item()


class Generator:
    def __init__(self, model, decoder):
        self.model = model.to(torch_device)
        self.decoder = decoder

    def generate(self, idx=None, max_new_tokens=100):
        if idx is None:
            idx = torch.zeros((1, 1), dtype=torch.long)
        idx = idx.to(torch_device)
        return self.decoder(
            self.model.generate(idx, max_new_tokens=max_new_tokens)[0].tolist()
        )

    def stream_generate(self, idx=None, max_new_tokens=100):
        if idx is None:
            idx = torch.zeros((1, 1), dtype=torch.long)
        idx = idx.to(torch_device)
        for i in self.model.stream_generate(idx, max_new_tokens=max_new_tokens):
            yield self.decoder(i[0].tolist())
