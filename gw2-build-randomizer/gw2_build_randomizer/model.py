from __future__ import annotations

from enum import StrEnum, auto
from typing import Optional, Annotated, NewType, Any
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
        return cls.model_validate(tomllib.loads(path.read_text()))

Specialization = NewType("Specialization", str)

class Expansion(StrEnum):
    BASE = auto()
    HEART_OF_THORNS = auto()
    PATH_OF_FIRE = auto()
    END_OF_DRAGONS = auto()
    SECRETS_OF_THE_OBSCURE = auto()
    JANTHIR_WILDS = auto()

class WeaponUsage(StrEnum):
    MAIN_HAND = auto()
    OFF_HAND = auto()
    TWO_HAND = auto()
    AQUATIC = auto()

class Weapon(StrEnum):
    AXE = auto()
    DAGGER = auto()
    MACE = auto()
    PISTOL = auto()
    SWORD = auto()
    SCEPTER = auto()
    FOCUS = auto()
    SHIELD = auto()
    TORCH = auto()
    WARHORN = auto()
    GREATSWORD = auto()
    HAMMER = auto()
    LONGBOW = auto()
    RIFLE = auto()
    SHORTBOW = auto()
    STAFF = auto()
    SPEAR = auto()
    HARPOON_GUN = auto()
    TRIDENT = auto()

SkillType = NewType("SkillType", str)

class Skills(BaseModel):
    heal: list[str]
    utility: list[str]
    elite: list[str]
    special: list[str] = []

class Gw2Profession(BaseModel):
    specializations: list[Specialization]
    weapons: dict[Expansion, dict[WeaponUsage, list[Weapon]]]
    skills: Skills


Gw2Classes = dict[ClassNames, Gw2Profession]
