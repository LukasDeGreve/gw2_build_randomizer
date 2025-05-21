import random
import numpy.random
from textwrap import dedent

import pytest

from gw2_build_randomizer.main import main, get_professions
from gw2_build_randomizer.model import Build, Trait, Profession, Professions, ProfessionName

EXPECTED = {
    0: """Your class is: Catalyst (Elementalist) 

Fire: bottom middle middle

Earth: middle middle middle

Catalyst: bottom top bottom

Heal skill: Ether Renewal

Utility skill 1: Conjure Lightning Hammer
Utility skill 2: Conjure Frost Bow
Utility skill 3: Invigorating Air

Elite skill: Tornado

Weapon set 1: scepter, warhorn
"""
}

@pytest.mark.parametrize("seed", range(1))
def test_can_run(capsys, seed: int) -> None:
    """The most basic test, just so I know I can refactor without something going bang"""
    random.seed(0)
    numpy.random.seed(0)
    main(print_out=True)
    captured = capsys.readouterr()
    if seed in EXPECTED:
        assert captured.out == EXPECTED[seed]


@pytest.fixture
def professions_by_name() -> dict[ProfessionName, Professions]:
    return {p.name: p for p in get_professions().professions}


def test_build_rendering(professions_by_name: dict[ProfessionName, Professions]) -> None:
    build = Build(
        profession=professions_by_name["elementalist"],
        traits=(
            Trait(specialization="Fire", trait_choices=("bottom", "middle", "middle")),
            Trait(specialization="Earth", trait_choices=("middle", "middle", "middle")),
            Trait(specialization="Catalyst", trait_choices=("bottom", "top", "bottom")),
        ),
        heal="Ether Renewal",
        utility=(
            "Conjure Lightning Hammer",
            "Conjure Frost Bow",
            "Invigorating Air",
        ),
        elite="Tornado",
        weapon_sets=(
            ("scepter", "warhorn"),
        )
    )
    assert build.render_for_display() == EXPECTED[0].strip()