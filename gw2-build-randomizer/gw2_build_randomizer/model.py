from __future__ import annotations

from enum import StrEnum, auto
from typing import Optional, Annotated, NewType, Any
import random
from pathlib import Path
from pydantic import BaseModel, BeforeValidator
import tomllib

RESOURCE_DIR = Path(__file__) / "resources"

ProfessionName = NewType("ProfessionName", str)

class Settings(BaseModel):
    include_professions: tuple[ProfessionName, ...] = tuple()
    exclude_professions: tuple[ProfessionName, ...] = tuple()

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

class Profession(BaseModel):
    name: ProfessionName
    specializations: list[Specialization]
    weapons: dict[Expansion, dict[WeaponUsage, list[Weapon]]]
    skills: Skills


class Professions(BaseModel):
    professions: list[Profession]
