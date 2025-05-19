from __future__ import annotations

from enum import StrEnum, auto
from typing import Optional, Annotated
import random
from pathlib import Path
from pydantic import BaseModel, BeforeValidator
import tomllib

RESOURCE_DIR = Path(__file__) / "resources"

class ClassNames(StrEnum):
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

def ClassNames_validator(values: list[str]) -> list[ClassNames]:
    return [ClassNames[value] for value in values]

class Settings(BaseModel):
    include_ClassNames: Annotated[list[ClassNames], BeforeValidator(ClassNames_validator)] = list(ClassNames)
    exclude_ClassNames: Annotated[list[ClassNames], BeforeValidator(ClassNames_validator)] = []

    def eligible_ClassNames(self) -> list[ClassNames]:
        return [i for i in ClassNames if i in self.include_ClassNames and i not in self.exclude_ClassNames]
    
    def get_class(self) -> ClassNames:
        return random.choice(self.eligible_ClassNames())

    @classmethod
    def from_toml(cls, path: Path) -> Settings:
        return Settings.model_validate(tomllib.loads(path.read_text()))
