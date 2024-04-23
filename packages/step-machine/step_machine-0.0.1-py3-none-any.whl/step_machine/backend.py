import enum
import json
import os.path
from dataclasses import dataclass
from typing import Any

from step_machine.backends.file import FileProgressBackendConfig, FileHistoryBackend
from step_machine.backends.pg import PgProgressBackendConfig, PgHistoryBackend

from step_machine.types import HistoryBackend


def load_json_file(filepath, model=None):
    with open(filepath) as f:
        if model is not None:
            return model(**json.load(f))
        else:
            return json.load(f)


@dataclass
class ProgressBackendChoice:
    name: str
    backend_class: Any
    config_class: Any = None
    default_config: Any = None
    require_config: bool = False


def load_config(config_path, cfg: ProgressBackendChoice):
    if config_path and os.path.exists(config_path):
        return load_json_file(config_path, model=cfg.config_class)
    if cfg.require_config:
        raise ValueError(f'Progress backend {cfg.name} requires config file.')
    return cfg.default_config


BACKENDS = {
    'pg': ProgressBackendChoice(
        name='pg',
        backend_class=PgHistoryBackend,
        config_class=PgProgressBackendConfig,
        default_config=PgProgressBackendConfig()
    ),
    'file': ProgressBackendChoice(
        name='file',
        backend_class=FileHistoryBackend,
        config_class=FileProgressBackendConfig,
        default_config=FileProgressBackendConfig(
            history_folder='./_stepm_history'
        )
    ),
}


def get_default_config(backend_name) -> HistoryBackend:
    backend: ProgressBackendChoice = BACKENDS[backend_name]
    return backend.default_config.model_dump(mode='json')


def get_backend(backend_name, config) -> HistoryBackend:
    backend: ProgressBackendChoice = BACKENDS[backend_name]
    return backend.backend_class(
        backend.config_class(**config)
    )


class BackendType(str, enum.Enum):
    FILE = 'file'
    PG = 'pg'
