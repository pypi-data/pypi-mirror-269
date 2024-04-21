from abc import ABC, abstractmethod
import torch
import numpy as np
from typing import List, Dict, Union
from huggingface_hub import scan_cache_dir


def records_to_list(list_of_dicts: Union[List[Dict[str, int]], Dict[str, int]]):
    """Transform a list of dictionaries to a dictionary of lists.
    If list_of_dicts is a dictionary, it will simply make a list of each values.
    From: https://stackoverflow.com/questions/5558418/list-of-dicts-to-from-dict-of-lists

    Args:
        list_of_dicts (list[dict[str, int]] | dict[str, int]): List of dictionaries, assuming each dictionary has the same keys.

    Returns:
        dict[list]: Dictionary of lists.
    """
    if not isinstance(list_of_dicts, list):
        list_of_dicts = [list_of_dicts]
    return {k: [dic[k] for dic in list_of_dicts] for k in list_of_dicts[0]}


def chunk(L, n):
    """
    Partition L into n chunks using every item in L and
    such that the resulting chunks differ in size by at
    most one element.

    >>> L = ['a', 'b', 'c', 'd']
    ['a', 'b', 'c', 'd']
    >>> chunk(L, 2)
    [['a', 'b'], ['c', 'd']]
    >>> chunk(L, 3)
    [['a'], ['b', 'c'], ['d']]
    >>> chunk(L, 4)
    [['a'], ['b'], ['c'], ['d']]
    >>> chunk(L, 5)
    [['a'], ['b'], [], ['c'], ['d']]
    """
    size = len(L) / float(n)

    def I(i):
        return int(round(i))

    return [L[I(size * i) : I(size * (i + 1))] for i in range(n)]


class AbstractCheckpoints(ABC):
    """Abstract class for iterating over model checkpoints"""

    def __init__(self, device: str = "cpu", clean_cache: bool = False):
        self.low_cpu_mem_usage = True if device == "cpu" else False

        self._device = device
        if device == "cpu":
            self.device = torch.device("cpu")
        elif device == "cuda":
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        elif device == "mps":
            self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

        self.clean_cache = clean_cache

    @staticmethod
    def get_revision_hash(name: str, revision: str) -> str:
        """Returns the commit hash for the model and revision (e.g., step) combination"""
        for x in iter(scan_cache_dir().repos):
            if x.repo_id == name:
                return x.refs[revision].commit_hash
        return None

    def split(self, n):
        """Convenience function for splitting checkpoints for e.g. parallel computing.
        If n > m (number of total checkpoints), it will return a list of m checkpoints objects instead.
        """
        total_length = len(self)
        chunk_indices = np.array_split(range(total_length), n)

        ckpts = []
        for ci in chunk_indices:
            if len(ci) > 0:
                start = ci[0].item()
                end = ci[-1].item()
                cfg = self.config
                cfg.update({k: set(v) for k, v in records_to_list(self.checkpoints[start : end + 1]).items()})
                # ckpts.append(self.__class__(seeds=set(cfg["seed"]), steps=set(cfg["step"])))
                ckpts.append(self.__class__(**cfg))
        return ckpts

    @property
    @abstractmethod
    def name():
        pass

    @property
    @abstractmethod
    def checkpoints(self):
        pass

    @staticmethod
    @abstractmethod
    def last_step():
        pass

    @abstractmethod
    def get_checkpoint(self):
        pass

    @classmethod
    def final_checkpoints(cls, **kwargs):
        return cls(step=[cls.last_step()], **kwargs)

    @abstractmethod
    def __len__(self):
        pass

    def __getitem__(self, index):
        cfg = self.checkpoints[index]
        ckpt = self.get_checkpoint(**cfg)
        return ckpt

    def __iter__(self):
        delete_hash = []
        for cfg in self.checkpoints:
            if self.clean_cache and len(delete_hash) > 0:
                for commit_hash in delete_hash:
                    cache_info = scan_cache_dir()
                    delete_strategy = cache_info.delete_revisions(commit_hash)
                    delete_strategy.execute()

            ckpt = self.get_checkpoint(**cfg)

            # Add commit_hash to be deleted if self.clean_cache strategy
            if "commit_hash" in ckpt.config:
                commit_hash = ckpt.config["commit_hash"]
                if commit_hash:
                    delete_hash.append(commit_hash)
            yield ckpt


class Checkpoint:
    """Convenience class for representing a checkpoint.
    Each checkpoint should at least have a model and model_name.
    """

    def __init__(self, model, model_name, tokenizer=None, **kwargs):
        self._model = model
        self._tokenizer = tokenizer
        self._config = {"model_name": model_name}
        self._config.update(kwargs)

    @property
    def config(self):
        return self._config

    @property
    def model(self):
        return self._model

    @property
    def tokenizer(self):
        if not self._tokenizer:
            raise ValueError("This checkpoint has no corresponding tokenizer.")
        return self._tokenizer
