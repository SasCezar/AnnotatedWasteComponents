from functools import partial
from typing import Callable, List, Dict, Union

from hydra.utils import call, instantiate
from loguru import logger
from omegaconf import DictConfig


def instantiate_community_extractors(cfg: DictConfig) -> Dict[str, Callable]:
    annotators: Dict[str, Callable] = {}

    for name, cb_conf in cfg.items():
        if isinstance(cb_conf, DictConfig):
            logger.info(f"Instantiating annotator <{name}>")
            annotators[name] = instantiate(cb_conf)

    return annotators
