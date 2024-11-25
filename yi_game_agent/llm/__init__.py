# -*- coding: utf-8 -*-
""" Import modules in models package."""
from typing import Type

from loguru import logger

from .base import ModelWrapperBase
from .openai import (
    OpenAIWrapperBase,
    OpenAIChatWrapper,
)

def _get_model_wrapper(model_type: str) -> Type[ModelWrapperBase]:
    """Get the specific type of model wrapper

    Args:
        model_type (`str`): The model type name.

    Returns:
        `Type[ModelWrapperBase]`: The corresponding model wrapper class.
    """
    wrapper = ModelWrapperBase.get_wrapper(model_type=model_type)
    if wrapper is None:
        logger.warning(
            f"Unsupported model_type [{model_type}],"
            "use PostApiModelWrapper instead.",
        )
        return OpenAIWrapperBase
    return wrapper
