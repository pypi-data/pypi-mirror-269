"""ML Adapter plugin for waylay-sdk."""

from .tool import MLTool

PLUGINS = [MLTool]

__all__ = ["MLTool"]
