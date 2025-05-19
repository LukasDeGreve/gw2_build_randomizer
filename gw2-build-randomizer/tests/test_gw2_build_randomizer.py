import random
import numpy.random
from textwrap import dedent
from gw2_build_randomizer.main import main

EXPECTED = """Your class is: Catalyst (Elementalist) 

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


def test_can_run(capsys) -> None:
    """The most basic test, just so I know I can refactor without something going bang"""
    random.seed(0)
    numpy.random.seed(0)
    main(print_out=True)
    captured = capsys.readouterr()
    assert captured.out == EXPECTED
