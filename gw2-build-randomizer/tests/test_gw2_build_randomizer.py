import random
from collections import Counter

import pytest

from gw2_build_randomizer.main import main, get_professions, get_settings
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
    0: """Chat link: [&DQYRKh8qQzd1AAAAjwAAAHMAAABQAQAAlgAAAAAAAAAAAAAAAAAAAAAAAAACWQAzAAA=]

Your class is: Catalyst (Elementalist) 

Water: bottom middle middle

Fire: middle middle middle

Catalyst: bottom top bottom

Heal skill: Ether Renewal

Utility skill 1: Signet of Water
Utility skill 2: Glyph of Elemental Power
Utility skill 3: Arcane Blast

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


def test_validate_models() -> None:
    professions = get_professions()
    settings = get_settings(professions)
    assert len(settings.include_professions) == 9
    assert not settings.exclude_professions
    for profession in professions.professions:
        assert profession.code, f"No code for {profession.name}"
        for specialization in profession.specializations:
            assert specialization.code, f"No code for {specialization.name} for {profession.name}"
        all_skills = (*profession.skills.heal, *profession.skills.utility, *profession.skills.elite, *profession.skills.special)
        all_skills_ids = Counter((i.palette_id for i in all_skills))
        duplicated_skills = {i for i, v in all_skills_ids.items() if v > 1}
        if profession.name != "revenant":  #  TODO Fix me :)
            assert not duplicated_skills, profession.name
            for skill in all_skills:
                assert skill.palette_id, f"No palette_id for {skill.name} for {profession.name}"


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
        heal=Skill(name="Ether Renewal", palette_id=117),
        utility=(
            Skill(name="Signet of Water", palette_id=143),
            Skill(name="Glyph of Elemental Power", palette_id=115),
            Skill(name="Arcane Blast", palette_id=336),
        ),
        elite=Skill(name="Tornado", palette_id=150),
        weapon_sets=((Weapon("staff"),),(Weapon("hammer"),)),
    )
    assert build.render_as_chat_link() == "[&DQYRKh8qQzd1AAAAjwAAAHMAAABQAQAAlgAAAAAAAAAAAAAAAAAAAAAAAAACWQAzAAA=]"
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
    expected = '[&DQMmLgY3Rh2EAAAAhgAAABobAAAQGwAACRsAAAAAAAAAAAAAAAAAAAAAAAACVQAzAAA=]'
    assert build.render_as_chat_link() == expected
