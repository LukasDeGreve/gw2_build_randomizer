import random
from collections import Counter

import pytest

from gw2_build_randomizer.main import (
    get_professions,
    get_settings,
    generate_random_build,
)
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

EXPECTED_DISPLAY = {
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

EXPECTED_CHAT_LINK = {
    0: "[&DQYRKh8qQzd1AAAAjwAAAHMAAABQAQAAlgAAAAAAAAAAAAAAAAAAAAAAAAACWQAzAAA=]"
}


@pytest.mark.parametrize("seed", range(10))
def test_build_rendering(seed: int) -> None:
    """The most basic test, just so I know I can refactor without something going bang"""
    random.seed(seed)
    build = generate_random_build()

    if build.profession.name != "revenant":
        chat_link = build.render_as_chat_link()
        if seed not in EXPECTED_CHAT_LINK:
            print(chat_link)
        assert chat_link == EXPECTED_CHAT_LINK.get(seed, chat_link)

    display_str = build.render_for_display()
    assert display_str == EXPECTED_DISPLAY.get(seed, display_str).strip()


def test_validate_models() -> None:
    professions = get_professions()
    settings = get_settings(professions)
    assert len(settings.include_professions) == 9
    assert not settings.exclude_professions
    for profession in professions.professions:
        assert profession.code, f"No code for {profession.name}"
        for specialization in profession.specializations:
            assert specialization.code, (
                f"No code for {specialization.name} for {profession.name}"
            )
        all_skills = (
            *profession.skills.heal,
            *profession.skills.utility,
            *profession.skills.elite,
            *(profession.skills.special if profession.name != "ranger" else ()),
        )
        all_skills_ids = Counter((i.palette_id for i in all_skills))
        duplicated_skills = {i for i, v in all_skills_ids.items() if v > 1}
        if profession.name != "revenant":  #  TODO Fix me :)
            assert not duplicated_skills, profession.name
            for skill in all_skills:
                assert skill.palette_id, (
                    f"No palette_id for {skill.name} for {profession.name}"
                )


@pytest.fixture
def professions_by_name() -> dict[ProfessionName, Profession]:
    return {p.name: p for p in get_professions().professions}


def test_chat_code_rendering(
    professions_by_name: dict[ProfessionName, Profession],
) -> None:
    build = Build(
        profession=professions_by_name[ProfessionName("engineer")],
        traits=(
            Trait(
                specialization=Specialization(name="Firearms", code=38),
                trait_choices=(
                    TraitChoice.BOTTOM,
                    TraitChoice.BOTTOM,
                    TraitChoice.MIDDLE,
                ),
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
    expected = "[&DQMmLgY3Rh2EAAAAhgAAABobAAAQGwAACRsAAAAAAAAAAAAAAAAAAAAAAAACVQAzAAA=]"
    assert build.render_as_chat_link() == expected
