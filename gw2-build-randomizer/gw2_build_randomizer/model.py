from __future__ import annotations

from enum import StrEnum, auto, IntEnum
from typing import Optional, NewType, Any
from pathlib import Path
from pydantic import BaseModel, model_validator
from textwrap import dedent
from base64 import b64encode

RESOURCE_DIR = Path(__file__) / "resources"

ProfessionName = NewType("ProfessionName", str)


class Settings(BaseModel):
    include_professions: tuple[ProfessionName, ...] = tuple()
    exclude_professions: tuple[ProfessionName, ...] = tuple()


class Specialization(BaseModel):
    name: str
    code: int


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

WeaponIDs = {
    Weapon.AXE: 5,
    Weapon.DAGGER: 47,
    Weapon.MACE: 53,
    Weapon.PISTOL: 54,
    Weapon.SWORD: 90,
    Weapon.SCEPTER: 86,
    Weapon.FOCUS: 49,
    Weapon.SHIELD: 87,
    Weapon.TORCH: 102,
    Weapon.WARHORN: 103,
    Weapon.GREATSWORD: 50,
    Weapon.HAMMER: 51,
    Weapon.LONGBOW: 35,
    Weapon.RIFLE: 85,
    Weapon.SHORTBOW: 107,
    Weapon.STAFF: 89,
    Weapon.SPEAR: 265,
}

class Skill(BaseModel):
    name: str
    palette_id: int

    @model_validator(mode='before')
    @classmethod
    def from_str(cls, data: Any) -> Any:  
        if isinstance(data, str):  
            return {"name": data, "palette_id": 0}
        return data


class Skills(BaseModel):
    heal: list[Skill]
    utility: list[Skill]
    elite: list[Skill]
    special: list[Skill] = []


class Profession(BaseModel):
    name: ProfessionName
    code: int
    specializations: list[Specialization]
    weapons: dict[Expansion, dict[WeaponUsage, list[Weapon]]]
    skills: Skills


class Professions(BaseModel):
    professions: tuple[Profession, ...]


class TraitChoice(IntEnum):
    TOP = 1
    MIDDLE = 2
    BOTTOM = 3


class Trait(BaseModel):
    specialization: Specialization
    trait_choices: tuple[TraitChoice, TraitChoice, TraitChoice]

    
    def render_for_display(self) -> str:
        return f"{self.specialization.name}: {" ".join([c.name.lower() for c in self.trait_choices])}"

    def render_as_chat_link(self) -> bytes:
        third = self.trait_choices[2].value << 4
        second = self.trait_choices[1].value << 2
        first = self.trait_choices[2].value << 4
        trait_choices = int.to_bytes(third | second | first)
        return int.to_bytes(self.specialization.code) + trait_choices


class Build(BaseModel):
    profession: Profession
    traits: tuple[Trait, Trait, Trait]  # TODO sort by index for east
    heal: Skill
    utility: tuple[Skill, Skill, Skill]
    elite: Skill
    weapon_sets: tuple[tuple[Weapon, ...], ...]
    special: Optional[tuple[str, tuple[Skill, ...]]] = None

    def _render_profession_name(self) -> str:
        maybe_elite_trait = self.traits[2]
        spec_index = self.profession.specializations.index(
            maybe_elite_trait.specialization
        )
        if spec_index < 5:
            return f"Core {self.profession.name.capitalize()}"
        else:
            return f"{maybe_elite_trait.specialization.name} ({self.profession.name.capitalize()})"

    def _render_special_skills(self) -> str:
        if self.special is None:
            return ""
        special_name, special_skills = self.special
        return ", ".join(
            [
                f"{special_name} {i + 1}: {special_skill}"
                for i, special_skill in enumerate(special_skills)
            ]
        )

    def render_for_display(self) -> str:
        return dedent(f"""
        Your class is: {self._render_profession_name()} 

        {self.traits[0].render_for_display()}

        {self.traits[1].render_for_display()}

        {self.traits[2].render_for_display()}

        Heal skill: {self.heal.name}

        Utility skill 1: {self.utility[0].name}
        Utility skill 2: {self.utility[1].name}
        Utility skill 3: {self.utility[2].name}

        Elite skill: {self.elite.name}

        Weapon set 1: {", ".join(self.weapon_sets[0])}
        {f"Weapon set 2: {', '.join(self.weapon_sets[1])}" if len(self.weapon_sets) > 1 and self.profession.name not in {"engineer", "elementalist"} else ""}

        {self._render_special_skills()}
        """).strip()

    def render_as_chat_link(self) -> str:
        arr = bytearray()
        arr.append(0x0D)  # Header
        arr.append(self.profession.code)
        for trait in self.traits:
            arr.extend(trait.render_as_chat_link())  # spec/trait
        for skill in (self.heal, *self.utility, self.elite):
            arr.extend(int.to_bytes(skill.palette_id, 2, byteorder='little'))  # above ground
            arr.extend(b'\x00\x00')  # aquatic, empty
        if self.special:
            raise NotImplementedError()
        else:
            arr.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')    
        all_weapons = [weapon for weapon_set in self.weapon_sets for weapon in weapon_set]
        arr.append(len(all_weapons))
        for weapon in all_weapons:
            arr.extend(int.to_bytes(WeaponIDs[weapon], 2, byteorder='little'))
        arr.append(0)  # Weaponmaster length
        return f"[&{b64encode(arr).decode()}]"
