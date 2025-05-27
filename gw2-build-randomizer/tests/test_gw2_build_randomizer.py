import random

import pytest

from gw2_build_randomizer.main import main, get_professions
from gw2_build_randomizer.model import (
    Build,
    Trait,
    TraitChoice,
    Profession,
    ProfessionName,
    Skill,
    Weapon,
    Specialization,
)

EXPECTED = {
    0: """Your class is: Catalyst (Elementalist) 

Water: bottom middle middle

Fire: middle middle middle

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
                specialization=Specialization(name="Water", code=17),
                trait_choices=(TraitChoice.BOTTOM, TraitChoice.MIDDLE, TraitChoice.MIDDLE),
            ),
            Trait(
                specialization=Specialization(name="Fire", code=31),
                trait_choices=(TraitChoice.MIDDLE, TraitChoice.MIDDLE, TraitChoice.MIDDLE),
            ),
            Trait(
                specialization=Specialization(name="Catalyst", code=67),
                trait_choices=(TraitChoice.BOTTOM, TraitChoice.TOP, TraitChoice.BOTTOM),
            ),
        ),
        heal=Skill(name="Ether Renewal", palette_id=0),
        utility=(
            Skill(name="Conjure Flame Axe", palette_id=0),
            Skill(name="Armor of Earth", palette_id=0),
            Skill(name="Arcane Wave", palette_id=0),
        ),
        elite=Skill(name="Tornado", palette_id=0),
        weapon_sets=((Weapon("staff"),),),
    )
    assert build.render_for_display() == EXPECTED[0].strip()

def test_chat_code_rendering(professions_by_name: dict[ProfessionName, Profession]) -> None:
    build = Build(
        profession=professions_by_name[ProfessionName("engineer")],
        traits=(
            Trait(
                specialization=Specialization(name="Firearms", code=38),
                trait_choices=(TraitChoice.BOTTOM, TraitChoice.BOTTOM, TraitChoice.MIDDLE),
            ),
            Trait(
                specialization=Specialization(name="Explosives", code=6),
                trait_choices=(TraitChoice.BOTTOM, TraitChoice.TOP, TraitChoice.BOTTOM),
            ),
            Trait(
                specialization=Specialization(name="Mechanist", code=70),
                trait_choices=(TraitChoice.BOTTOM, TraitChoice.BOTTOM, TraitChoice.TOP),
            ),
        ),
        heal=Skill(name="Med Kit", palette_id=132),
        utility=(
            Skill(name="Grenade Kit", palette_id=134),
            Skill(name="Force Signet", palette_id=6938),
            Skill(name="Shift Signet", palette_id=6928),
        ),
        elite=Skill(name="Overclock Signet", palette_id=6921),
        weapon_sets=(
            (Weapon("rifle"),),
            (Weapon("hammer"),),
            ),
    )
    expected = '[&DQMmLAY0RhyEAAAAhgAAABobAAAQGwAACRsAAAAAAAAAAAAAAAAAAAAAAAACVQAzAAA=]'
    assert build.render_as_chat_link() == expected
