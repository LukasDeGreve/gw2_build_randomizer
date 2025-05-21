from __future__ import annotations

from enum import StrEnum, auto
from typing import Optional, Annotated, NewType, Any, Literal
import random
from pathlib import Path
from pydantic import BaseModel, BeforeValidator
import tomllib
from textwrap import dedent

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

Skill = NewType("Skill", str)

class Skills(BaseModel):
    heal: list[Skill]
    utility: list[Skill]
    elite: list[Skill]
    special: list[Skill] = []

class Profession(BaseModel):
    name: ProfessionName
    specializations: list[Specialization]
    weapons: dict[Expansion, dict[WeaponUsage, list[Weapon]]]
    skills: Skills


class Professions(BaseModel):
    professions: tuple[Profession, ...]


TraitChoice = Literal["bottom", "middle", "top"]

class Trait(BaseModel):
    specialization: Specialization
    trait_choices: tuple[TraitChoice, TraitChoice, TraitChoice]


class Build(BaseModel):
    profession: Profession
    traits: tuple[Trait, Trait, Trait]  # TODO sort by index for east
    heal: Skill
    utility: tuple[Skill, Skill, Skill]
    elite: Skill
    weapon_sets: tuple[tuple[Weapon, ...], ...]

    def _render_profession_name(self) -> str:
        maybe_elite_trait = self.traits[2]
        spec_index = self.profession.specializations.index(maybe_elite_trait.specialization)
        if spec_index < 5:
            return f"Core {self.profession.name.capitalize()}"  
        else:
            return f"{maybe_elite_trait.specialization} ({self.profession.name.capitalize()})"

    def render_for_display(self) -> str:
        
        return dedent(f"""
        Your class is: {self._render_profession_name()} 

        {self.traits[0].specialization}: {" ".join(self.traits[0].trait_choices)}

        {self.traits[1].specialization}: {" ".join(self.traits[1].trait_choices)}

        {self.traits[2].specialization}: {" ".join(self.traits[2].trait_choices)}

        Heal skill: {self.heal}

        Utility skill 1: {self.utility[0]}
        Utility skill 2: {self.utility[1]}
        Utility skill 3: {self.utility[2]}

        Elite skill: {self.elite}

        Weapon set 1: {", ".join(self.weapon_sets[0])}
        {f"Weapon set 2: {", ".join(self.weapon_sets[1])}" if len(self.weapon_sets) > 1 and self.profession.name not in {"engineer", "elementalist"} else ""}
        """).strip()
