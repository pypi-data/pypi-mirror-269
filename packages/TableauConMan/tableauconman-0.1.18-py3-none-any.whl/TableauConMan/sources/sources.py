from typing import Any, List, Protocol

from loguru import logger


class Source(Protocol):
    def get_assets(self, asset_type: str) -> List[Any]:
        return list()
