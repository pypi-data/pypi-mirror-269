from typing import Iterator
import torch

from yoggopoth import trainer
from yoggopoth.settings import Hyperparams


def train(
    data_path: str,
    p: dict | Hyperparams = Hyperparams(),
    fix_seed: bool = True,
    save: str | None = None,
):
    output = []
    if fix_seed:
        torch.manual_seed(666)
    if isinstance(p, dict):
        p = Hyperparams(**p)
    loader = trainer.Loader(data_path)
    tr = trainer.Trainer.from_loader(loader, p)
    loss = tr.train(steps=p.steps)
    if save:
        # TODO: Save the state dict instead of the whole model
        torch.save(tr.model, f"{save}.pth")
        loader.codec.save(f"{save}.vocab")
    output.append(f"final loss after {p.steps} steps: {loss}")
    output.append("generation sample:")
    torch.seed()
    m = trainer.Generator(tr.model, loader.get_decoder())
    output.append(m.generate())
    return "\n".join(output)


def gen(
    model_path: str,
    feed: str | None = None,
    tokens: int = 100,
    stream: bool = True,
) -> str:
    model, feed_idx = _prepare_gen(model_path, feed)
    return model.generate(feed_idx, tokens)


def stream_gen(
    model_path: str,
    feed: str | None = None,
    tokens: int = 100,
) -> Iterator[str]:
    model, feed_idx = _prepare_gen(model_path, feed)
    if feed:
        yield feed
    for char in model.stream_generate(feed_idx, tokens):
        yield char


def _prepare_gen(model_path, feed):
    model = torch.load(f"{model_path}.pth", map_location=trainer.torch_device)
    model.eval()
    codec = trainer.Codec.load(f"{model_path}.vocab")
    m = trainer.Generator(model, codec.decode)
    if feed:
        feed_idx = codec.as_tensor(feed)
        feed_idx = torch.stack([feed_idx] * model.batch_size)
    else:
        feed_idx = None
    return m, feed_idx
