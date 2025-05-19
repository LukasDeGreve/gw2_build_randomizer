from __future__ import annotations

from enum import StrEnum, auto
from typing import Optional, Annotated
import random
from pathlib import Path
from pydantic import BaseModel, BeforeValidator
import tomllib

RESOURCE_DIR = Path(__file__) / "resources"

class Classes(StrEnum):
    WARRIOR = auto()
    GUARDIAN = auto()
    REVENANT = auto()
    RANGER = auto()
    THIEF = auto()
    ENGINEER = auto()
    ELEMENTALIST = auto()
    MESMER = auto()
    NECROMANCER = auto()

    def _missing_(cls, name) -> None:
        try:
            return cls[name.upper()]
        except:
            return None

def classes_validator(values: list[str]) -> list[Classes]:
    return [Classes[value] for value in values]

class Settings(BaseModel):
    include_classes: Annotated[list[Classes], BeforeValidator(classes_validator)] = list(Classes)
    exclude_classes: Annotated[list[Classes], BeforeValidator(classes_validator)] = []

    def eligible_classes(self) -> list[Classes]:
        return [i for i in Classes if i in self.include_classes and i not in self.exclude_classes]
    
    def get_class(self) -> Classes:
        return random.choice(self.eligible_classes())

    @classmethod
    def from_toml(cls, path: Path) -> Settings:
        return Settings.model_validate(tomllib.loads(path.read_text()))
