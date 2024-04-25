from dataclasses import dataclass
from abc import ABC, abstractproperty


@dataclass
class Asset(ABC):
    @abstractproperty
    def specification_id(self):
        pass

    @abstractproperty
    def update_checksum(self):
        pass

    @abstractproperty
    def update_value(self):
        pass
