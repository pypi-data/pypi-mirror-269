import fire
import torch

from yoggopoth import trainer
from yoggopoth.settings import Hyperparams


def train(
    data_path: str,
    p: dict | Hyperparams = Hyperparams(),
    fix_seed: bool = True,
    save: str | None = None,
):
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
    print(f"final loss after {p.steps} steps: {loss}")
    print("generation sample:")
    torch.seed()
    m = trainer.Generator(tr.model, loader.get_decoder())
    print(m.generate())


def gen(
    model_path: str,
    feed: str | None = None,
    tokens: int = 100,
    stream: bool = True,
):
    # TODO: Load the model state dict instead of the whole model
    model = torch.load(f"{model_path}.pth", map_location=trainer.torch_device)
    model.eval()
    codec = trainer.Codec.load(f"{model_path}.vocab")
    m = trainer.Generator(model, codec.decode)
    if feed:
        feed_idx = codec.as_tensor(feed)
        feed_idx = torch.stack([feed_idx] * model.batch_size)
    else:
        feed_idx = None
    if stream:
        print(feed, end="")
        for char in m.stream_generate(feed_idx, tokens):
            print(char, end="")
    else:
        print(m.generate(feed_idx, tokens))


if __name__ == "__main__":
    fire.Fire()
