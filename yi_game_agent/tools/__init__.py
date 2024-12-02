# -*- coding: utf-8 -*-
""" Import all service-related modules in the package."""
from loguru import logger

from .service_response import ServiceResponse
from .service_toolkit import ServiceToolkit
from .service_status import ServiceExecStatus


def get_help() -> None:
    """Get help message."""

    help_msg = "\n - ".join(
        ["The following services are available:"] + __all__[4:],
    )
    logger.info(help_msg)


__all__ = [
    "ServiceResponse",
    "ServiceExecStatus",
    "ServiceToolkit",
    "get_help",
]
