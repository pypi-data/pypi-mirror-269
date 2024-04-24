from pydantic_settings import BaseSettings


class Hyperparams(BaseSettings):
    batch_size: int = 16
    block_size: int = 16
    test_size: float = 0.1
    learning_rate: float = 1e-3
    steps: int = 10000
    n_embed: int = 32
    n_heads: int = 4
    n_layers: int = 4
    dropout: float = 0.1
