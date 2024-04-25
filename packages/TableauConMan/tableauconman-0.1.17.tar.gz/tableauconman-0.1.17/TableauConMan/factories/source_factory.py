from TableauConMan.sources.server_source import ServerSource
from TableauConMan.sources.specification_source import SpecificationSource


class SourceFactory:
    def get_source(self, source_type_config: str):
        if source_type_config == "server":
            return ServerSource
        elif source_type_config == "specification":
            return SpecificationSource
        raise TypeError(f"No source for the {source_type_config} source type")
