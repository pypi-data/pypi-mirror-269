import torch
from torch import nn
from torch.nn import functional as F

from yoggopoth.settings import Hyperparams


class BigramLanguageModel(nn.Module):
    def __init__(self, vocab_size: int):
        super().__init__()
        self.token_embedding_table = nn.Embedding(vocab_size, vocab_size)

    def forward(self, idx, targets=None):
        # idx and targets are both (B, T) tensors of integers
        logits = self.token_embedding_table(idx)  # (B, T, C)
        if targets is None:
            return logits, None
        B, T, C = logits.shape
        logits = logits.view(B * T, C)
        targets = targets.view(B * T)
        # Cross-entropy expects C as the
        loss = F.cross_entropy(logits, targets)
        return logits, loss

    def generate(self, idx, max_new_tokens):
        # idx is (B, T) array in the current context
        for _ in range(max_new_tokens):
            logits, _ = self(idx)
            # focus on the last time step
            logits = logits[:, -1, :]  # -> (B, C)
            # get probabilities on the last dimension (which has logits for each token in the vocab)
            probs = F.softmax(logits, dim=-1)  # (B, C)
            # sample from the distribution
            idx_next = torch.multinomial(probs, num_samples=1)  # (B, 1)
            # append sampled index to the running sequence
            idx = torch.cat((idx, idx_next), dim=1)  # (B, T+1)

        return idx


class Head(nn.Module):
    """
    A single attention head.
    """

    def __init__(self, h: Hyperparams, head_size: int):
        # Specifying the head size different from the embedding size is not supported for now
        # TODO: Figure out how to support this
        super().__init__()
        self.query = nn.Linear(h.n_embed, head_size, bias=False)
        self.key = nn.Linear(h.n_embed, head_size, bias=False)
        self.value = nn.Linear(h.n_embed, head_size, bias=False)
        self.dropout = nn.Dropout(h.dropout)
        self.register_buffer("tril", torch.tril(torch.ones(h.block_size, h.block_size)))

    def forward(self, x):
        B, T, C = x.shape
        q = self.query(x)  # (B, T, head_size C)
        k = self.key(x)  # (B, T, C)
        # compute the attention scores, normalized by the square root of the head size
        # to keep the variance of the output independent of the head size
        w = q @ k.transpose(-2, -1) * (C**-0.5)  # (B, T, C) @ (B, C, T) -> (B, T, T)
        # mask out the upper half of the matrix to prevent attending to future tokens
        w = w.masked_fill(self.tril[:T, :T] == 0, float("-inf"))  # (B, T, T)
        # apply softmax to the head dimension to get the normal distribution of attention weights
        w = F.softmax(w, dim=-1)  # (B, T, T)
        w = self.dropout(w)
        # perform the weighted sum of the values
        v = self.value(x)  # (B, T, C)
        return w @ v  # (B, T, T) @ (B, T, C) -> (B, T, C)


class MultiHeadAttention(nn.Module):
    def __init__(self, h: Hyperparams):
        super().__init__()
        self.heads = nn.ModuleList(
            [Head(h, h.n_embed // h.n_heads) for _ in range(h.n_heads)]
        )
        self.proj = nn.Linear(h.n_embed, h.n_embed)
        self.dropout = nn.Dropout(h.dropout)

    def forward(self, x):
        # Concatenate over the embedding dimension
        out = torch.cat([head(x) for head in self.heads], dim=-1)
        # Linear projection to the embedding dimension
        return self.dropout(self.proj(out))


class FeedForward(nn.Module):
    mult = 4

    def __init__(self, h: Hyperparams):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(h.n_embed, self.mult * h.n_embed),
            nn.ReLU(),
            nn.Linear(self.mult * h.n_embed, h.n_embed),
            nn.Dropout(h.dropout),
        )

    def forward(self, x):
        return self.net(x)


class Block(nn.Module):
    def __init__(self, h: Hyperparams):
        super().__init__()
        self.sa = MultiHeadAttention(h)
        self.ffwd = FeedForward(h)
        self.ln1 = nn.LayerNorm(h.n_embed)
        self.ln2 = nn.LayerNorm(h.n_embed)

    def forward(self, x):
        x = x + self.sa(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x


class AttentionLanguageModel(nn.Module):
    def __init__(
        self,
        h: Hyperparams,
        vocab_size: int,
    ):
        super().__init__()
        self.batch_size = h.batch_size
        self.block_size = h.block_size
        self.token_embedding_table = nn.Embedding(vocab_size, h.n_embed)
        self.position_embedding_table = nn.Embedding(h.block_size, h.n_embed)
        self.blocks = nn.Sequential(
            *[Block(h) for _ in range(h.n_layers)],
            nn.LayerNorm(h.n_embed),
        )
        self.lm_head = nn.Linear(h.n_embed, vocab_size)

    def forward(self, idx, targets=None):
        B, T = idx.shape  # B is batch size, T is sequence length
        # C is the embedding dimension
        # idx and targets are both (B, T) tensors of integers
        tok_emb = self.token_embedding_table(idx)  # (B, T, C)
        pos_emb = self.position_embedding_table(
            torch.arange(T, device=idx.device)
        )  # (T, C)
        x = tok_emb + pos_emb  # (B, T, C) - pos_emb is broadcasted across all batches
        x = self.blocks(x)
        logits = self.lm_head(x)  # (B, T, vocab_size)
        if targets is None:
            return logits, None
        B, T, C = logits.shape
        logits = logits.view(B * T, C)
        targets = targets.view(B * T)
        # Cross-entropy expects C as the
        loss = F.cross_entropy(logits, targets)
        return logits, loss

    def generate(self, idx, max_new_tokens):
        # idx is (B, T) array in the current context
        for _ in range(max_new_tokens):
            # crop the sequence to the last block_size tokens
            idx_cond = idx[:, -self.block_size :]
            logits, _ = self(idx_cond)
            # focus on the last time step
            logits = logits[:, -1, :]  # -> (B, C)
            # get probabilities on the last dimension (which has logits for each token in the vocab)
            probs = F.softmax(logits, dim=-1)  # (B, C)
            # sample from the distribution
            idx_next = torch.multinomial(probs, num_samples=1)  # (B, 1)
            # append sampled index to the running sequence
            idx = torch.cat((idx, idx_next), dim=1)  # (B, T+1)

        return idx

    def stream_generate(self, idx, max_new_tokens):
        # idx is (B, T) array in the current context
        for _ in range(max_new_tokens):
            # crop the sequence to the last block_size tokens
            idx_cond = idx[:, -self.block_size :]
            logits, _ = self(idx_cond)
            # focus on the last time step
            logits = logits[:, -1, :]  # -> (B, C)
            # get probabilities on the last dimension (which has logits for each token in the vocab)
            probs = F.softmax(logits, dim=-1)  # (B, C)
            # sample from the distribution
            idx_next = torch.multinomial(probs, num_samples=1)  # (B, 1)
            # append sampled index to the running sequence
            idx = torch.cat((idx, idx_next), dim=1)  # (B, T+1)
            yield idx_next
