""" Abstract class defining the structure of a converter
"""
from abc import ABC, abstractmethod
from TableauConMan.assets.asset import Asset


class Converter(ABC):
    """Methods for converting between TSC Items and ConMan Assets"""

    @abstractmethod
    def convert_to_asset(self, source_item) -> Asset:
        """factory method for converting from a source"""

    @abstractmethod
    def convert_to_source(self, asset):
        """factory method for converting to a source"""
