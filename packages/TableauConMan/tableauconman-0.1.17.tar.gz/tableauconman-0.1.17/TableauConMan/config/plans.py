from typing import Optional, Type, List
from dataclasses import dataclass, field
from loguru import logger
from TableauConMan.sources.sources import Source
from TableauConMan.factories.source_factory import SourceFactory


@dataclass
class Plan:
    target: Optional[Source] = None
    reference: Source = None
    assets: list = field(default_factory=list)
    _options: list = None

    @property
    def project_options(self) -> List[dict]:
        """_summary_

        :return: _description_
        """
        return self._options.get("projects", {}).get("options")

    @classmethod
    def load(cls: Type["Plan"], plan_file: str):
        """_summary_

        :param cls: _description_
        :param plan_file: _description_
        :return: _description_
        """
        valid_plan = cls.validate_plan(plan_file)

        source_factory = SourceFactory()

        target_source = source_factory.get_source(
            valid_plan.get("target", {}).get("type")
        )

        reference_source = source_factory.get_source(
            valid_plan.get("reference", {}).get("type")
        )

        return cls(
            target=target_source.load(valid_plan.get("target")),
            reference=reference_source.load(valid_plan.get("reference")),
            assets=list(valid_plan.get("assets").keys()),
            _options=valid_plan.get("assets"),
        )

    @staticmethod
    def validate_plan(plan_file):
        """_summary_

        :param plan_file: _description_
        :return: _description_
        """
        return plan_file
