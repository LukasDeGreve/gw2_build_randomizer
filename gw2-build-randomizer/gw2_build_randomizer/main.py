import random
from pathlib import Path
from typing import Optional
import tomllib

from gw2_build_randomizer.model import (
    Settings,
    Professions,
    Profession,
    Trait,
    Build,
    TraitChoice,
    Skill,
    Weapon,
)

RESOURCE_DIR = Path(__file__).parent / "resources"
SETTINGS = RESOURCE_DIR / "settings.toml"
PROFESSIONS = RESOURCE_DIR / "professions.toml"


def get_professions() -> Professions:
    return Professions.model_validate(tomllib.loads(PROFESSIONS.read_text()))


def get_settings(professions: Professions) -> Settings:
    known_professions = {profession.name for profession in professions.professions}
    settings = Settings.model_validate(tomllib.loads(SETTINGS.read_text()))
    assert all(i in known_professions for i in settings.include_professions)
    assert all(i in known_professions for i in settings.exclude_professions)
    return settings


def determine_random_profession(
    professions: Professions, settings: Settings
) -> Profession:
    include = set(settings.include_professions) or {
        profession.name for profession in professions.professions
    }
    after_exclude = include.difference(settings.exclude_professions)
    choices = [
        profession
        for profession in professions.professions
        if profession.name in after_exclude
    ]
    return random.choice(choices)

def generate_random_build() -> Build:
    professions = get_professions()
    settings = get_settings(professions)

    profession = determine_random_profession(professions, settings)

    elite_specs = [0, 5, 6, 7]
    elite_spec = random.choice(elite_specs)
    traits = range(5)

    if elite_spec == 0:  # core class: pick 3 traitlines
        traits_picked = random.sample(traits, 3)
    else:  # elite spec chosen: only 2 traitlines needed
        traits_picked = random.sample(traits, 2)
        traits_picked.append(elite_spec)

    # chose majors of each trait
    majors = list(TraitChoice)
    chosen_traits = (
        Trait(
            specialization=profession.specializations[traits_picked[0]],
            trait_choices=(
                random.choice(majors),
                random.choice(majors),
                random.choice(majors),
            ),
        ),
        Trait(
            specialization=profession.specializations[traits_picked[1]],
            trait_choices=(
                random.choice(majors),
                random.choice(majors),
                random.choice(majors),
            ),
        ),
        Trait(
            specialization=profession.specializations[traits_picked[2]],
            trait_choices=(
                random.choice(majors),
                random.choice(majors),
                random.choice(majors),
            ),
        ),
    )

    # prepare list of indexes corresponding to possible skills
    heal_choices = list(range(4))
    skill_choices = list(range(20))
    elite_choices = list(range(3))
    if elite_spec == 5:
        heal_choices.append(4)
        skill_choices.extend(range(20, 24))
        elite_choices.append(3)
    elif elite_spec == 6:
        heal_choices.append(5)
        skill_choices.extend(range(24, 28))
        elite_choices.append(4)
    elif elite_spec == 7:
        heal_choices.append(6)
        skill_choices.extend(range(28, 32))
        elite_choices.append(5)

    special: Optional[tuple[str, tuple[Skill, ...]]] = None

    # if revenenant, pick 2 legends instead of utility skills
    if profession.name == "revenant":
        special_choices = (
            heal_choices  # there are as many legends as another class has heal skills
        )
        possible_legends = [
            legend
            for i, legend in enumerate(profession.skills.special)
            if i in special_choices
        ]
        chosen_legends = random.sample(possible_legends, 2)
        heal = Skill(name="fake", palette_id=1)  # TODO
        skill = (heal, heal, heal)  # TODO
        elite = heal  # TODO
        special = "Legend", tuple(chosen_legends)
    else:
        # pick a random heal skill
        possible_heal = [
            s for i, s in enumerate(profession.skills.heal) if i in heal_choices
        ]
        heal = random.choice(possible_heal)

        # pick 3 different skills
        possible_skills = [
            s for i, s in enumerate(profession.skills.utility) if i in skill_choices
        ]
        skill: tuple[Skill, Skill, Skill] = tuple(random.sample(possible_skills, 3))  # type: ignore

        # pick a random elite skill
        possible_elite = [
            s for i, s in enumerate(profession.skills.elite) if i in elite_choices
        ]
        elite = random.choice(possible_elite)

    # pick 2 pets if you are a ranger

    if profession.name == "ranger":
        pets = random.sample(profession.skills.special, 2)
        special = "Pet", tuple(pets)

    main_hand_names = []
    off_hand_names = []
    two_handed_names = []
    for weapon in profession.weapons.values():
        for weapon_type, weapon_list in weapon.items():
            if weapon_type == "main_hand":
                main_hand_names.extend(weapon_list)
            elif weapon_type == "off_hand":
                off_hand_names.extend(weapon_list)
            elif weapon_type == "two_hand":
                two_handed_names.extend(weapon_list)

    main_hand_options = len(main_hand_names)
    off_hand_options = len(off_hand_names)
    two_handed_options = len(two_handed_names)

    # pick first weapon between main hand and two handed options
    chosen_weapons = random.sample(range(main_hand_options + two_handed_options), 2)

    # if weapon is one handed, choose offhand
    off_hands = 0
    if chosen_weapons[0] < main_hand_options:
        off_hands += 1
    if chosen_weapons[1] < main_hand_options:
        off_hands += 1
    chosen_off_hands = random.sample(range(off_hand_options), off_hands)

    # formatting so it prints nicely
    weapon_sets: list[tuple[Weapon, ...]] = []

    for chosen_weapon in chosen_weapons:
        if chosen_weapon < main_hand_options:
            weapon_sets.append(
                (
                    main_hand_names[chosen_weapon],
                    off_hand_names[chosen_off_hands.pop(0)],
                )
            )
        else:
            weapon_sets.append((two_handed_names[chosen_weapon - main_hand_options],))

    return Build(
        profession=profession,
        traits=chosen_traits,
        heal=heal,
        utility=skill,
        elite=elite,
        weapon_sets=tuple(weapon_sets),
        special=special,
    )

def main() -> str:
    return generate_random_build().render_for_display()


if __name__ == "__main__":
    print(main())
