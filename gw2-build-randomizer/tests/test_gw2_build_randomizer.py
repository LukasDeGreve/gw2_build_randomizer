import random

import pytest

from gw2_build_randomizer.main import main, get_professions
from gw2_build_randomizer.model import (
    Build,
    Trait,
    Profession,
    ProfessionName,
    Skill,
    Weapon,
    Specialization,
)

EXPECTED = {
    0: """Your class is: Catalyst (Elementalist) 

Fire: bottom middle middle

Earth: middle middle middle

Catalyst: bottom top bottom

Heal skill: Ether Renewal

Utility skill 1: Conjure Flame Axe
Utility skill 2: Armor of Earth
Utility skill 3: Arcane Wave

Elite skill: Tornado

Weapon set 1: staff
"""
}


@pytest.mark.parametrize("seed", range(1))
def test_can_run(seed: int) -> None:
    """The most basic test, just so I know I can refactor without something going bang"""
    random.seed(0)
    actual = main()
    if seed in EXPECTED:
        assert actual == EXPECTED[seed].strip()


@pytest.fixture
def professions_by_name() -> dict[ProfessionName, Profession]:
    return {p.name: p for p in get_professions().professions}


def test_build_rendering(professions_by_name: dict[ProfessionName, Profession]) -> None:
    build = Build(
        profession=professions_by_name[ProfessionName("elementalist")],
        traits=(
            Trait(
                specialization=Specialization("Fire"),
                trait_choices=("bottom", "middle", "middle"),
            ),
            Trait(
                specialization=Specialization("Earth"),
                trait_choices=("middle", "middle", "middle"),
            ),
            Trait(
                specialization=Specialization("Catalyst"),
                trait_choices=("bottom", "top", "bottom"),
            ),
        ),
        heal=Skill("Ether Renewal"),
        utility=(
            Skill("Conjure Flame Axe"),
            Skill("Armor of Earth"),
            Skill("Arcane Wave"),
        ),
        elite=Skill("Tornado"),
        weapon_sets=((Weapon("staff"),),),
    )
    assert build.render_for_display() == EXPECTED[0].strip()

def test_chat_code_rendering(professions_by_name: dict[ProfessionName, Profession]) -> None:
    build = Build(
        profession=professions_by_name[ProfessionName("engineer")],
        traits=(
            Trait(
                specialization=Specialization("Firearms"),
                trait_choices=("bottom", "bottom", "middle"),
            ),
            Trait(
                specialization=Specialization("Explosives"),
                trait_choices=("bottom", "top", "bottom"),
            ),
            Trait(
                specialization=Specialization("Mechanist"),
                trait_choices=("bottom", "bottom", "top"),
            ),
        ),
        heal=Skill("Med Kit"),
        utility=(
            Skill("Grenade Kit"),
            Skill("Force Signet"),
            Skill("Shift Signet"),
        ),
        elite=Skill("Jade Buster Cannon"),
        weapon_sets=((Weapon("rifle"),),),
    )
    expected = '[&DQMmLwY3Rh+EAIQAhgCGABobGhsQGwsbCRsSAQAAAAAAAAAAAAAAAAAAAAACVQAzAAA=]'
    assert build.render_as_chat_link() == expected