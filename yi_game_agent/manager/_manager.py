# -*- coding: utf-8 -*-
"""A manager for yi-game-agent."""
import os
from typing import Union, Any
from copy import deepcopy

from loguru import logger

from ._model import ModelManager
from ._file import FileManager
from ..logging import LOG_LEVEL, setup_logger
from .._version import __version__
from ..utils.common import (
    _generate_random_code,
    _get_process_creation_time,
    _get_timestamp,
)
from ..constants import _RUNTIME_ID_FORMAT, _RUNTIME_TIMESTAMP_FORMAT


class YIManager:
    """A manager for yi-game-agent."""

    _instance = None

    __serialized_attrs = [
        "project",
        "name",
        "disable_saving",
        "run_id",
        "pid",
        "timestamp",
    ]

    def __new__(cls, *args: Any, **kwargs: Any) -> "YIManager":
        if cls._instance is None:
            cls._instance = super(YIManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> "YIManager":
        """Get the instance of the singleton class."""
        if cls._instance is None:
            raise ValueError(
                "yi_game_agent hasn't been initialized. Please call "
                "`yi_game_agent.init` function first.",
            )
        return cls._instance

    def __init__(self) -> None:
        """Initialize the manager. Note we initialize the managers by default
        arguments to avoid unnecessary errors when user doesn't call
        `yi_game_agent.init` function"""
        self.project = ""
        self.name = ""
        self.run_id = ""
        self.pid = -1
        self.timestamp = ""
        self.disable_saving = True

        self.file = FileManager()
        self.model = ModelManager()

        # TODO: unified with logger and studio
        self.logger_level: LOG_LEVEL = "INFO"

    def initialize(
        self,
        model_configs: Union[dict, str, list, None],
        project: Union[str, None],
        name: Union[str, None],
        disable_saving: bool,
        save_dir: str,
        save_log: bool,
        save_code: bool,
        save_api_invoke: bool,
        cache_dir: str,
        use_monitor: bool,
        logger_level: LOG_LEVEL,
        run_id: Union[str, None],
        studio_url: Union[str, None],
    ) -> None:
        """Initialize the package."""
        # =============== Init the runtime ===============
        self.project = project or _generate_random_code()
        self.name = name or _generate_random_code(uppercase=False)

        self.pid = os.getpid()
        timestamp = _get_process_creation_time()

        self.timestamp = timestamp.strftime(_RUNTIME_TIMESTAMP_FORMAT)

        self.run_id = run_id or _get_timestamp(
            _RUNTIME_ID_FORMAT,
            timestamp,
        ).format(self.name)

        self.disable_saving = disable_saving

        # =============== Init the file manager ===============
        if disable_saving:
            save_log = False
            save_code = False
            save_api_invoke = False
            use_monitor = False
            run_dir = None
        else:
            run_dir = os.path.abspath(os.path.join(save_dir, self.run_id))

        self.file.initialize(
            run_dir=run_dir,
            save_log=save_log,
            save_code=save_code,
            save_api_invoke=save_api_invoke,
            cache_dir=cache_dir,
        )
        # Save the python code here to avoid duplicated saving in the child
        # process (when calling deserialize function)
        if save_code:
            self.file.save_python_code()

        if not disable_saving:
            # Save the runtime information in .config file
            self.file.save_runtime_information(self.state_dict())

        # =============== Init the logger         ===============
        # TODO: unified with studio and gradio
        self.logger_level = logger_level
        # run_dir will be None if save_log is False
        setup_logger(self.file.run_dir, logger_level)

        # =============== Init the model manager  ===============
        self.model.initialize(model_configs)

    def state_dict(self) -> dict:
        """Serialize the runtime information."""
        serialized_data = {k: getattr(self, k) for k in self.__serialized_attrs}

        serialized_data["yi-game-agent_version"] = __version__

        serialized_data["file"] = self.file.state_dict()
        serialized_data["model"] = self.model.state_dict()
        serialized_data["logger"] = {
            "level": self.logger_level,
        }

        return deepcopy(serialized_data)

    def load_dict(self, data: dict) -> None:
        """Load the runtime information from a dictionary"""
        for k in self.__serialized_attrs:
            assert k in data, f"Key {k} not found in data."
            setattr(self, k, data[k])

        self.file.load_dict(data["file"])
        # TODO: unified the logger with studio and gradio
        self.logger_level = data["logger"]["level"]
        setup_logger(self.file.run_dir, self.logger_level)
        self.model.load_dict(data["model"])

    def flush(self) -> None:
        """Flush the runtime information."""
        self.project = ""
        self.name = ""
        self.run_id = ""
        self.pid = -1
        self.timestamp = ""
        self.disable_saving = True

        self.file.flush()
        self.model.flush()
        logger.remove()

        self.logger_level = "INFO"
