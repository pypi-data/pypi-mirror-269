import fire
from yoggopoth import api, settings


def train(
    data_path: str,
    p: dict | settings.Hyperparams = settings.Hyperparams(),
    fix_seed: bool = True,
    save: str | None = None,
):
    print(api.train(data_path, p, fix_seed, save))


def gen(
    model_path: str, feed: str | None = None, tokens: int = 100, stream: bool = True
):
    if stream:
        for ch in api.stream_gen(model_path, feed, tokens):
            print(ch, end="")
    else:
        print(api.gen(model_path, feed, tokens))


if __name__ == "__main__":
    fire.Fire()
