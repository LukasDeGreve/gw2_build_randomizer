from gw2_build_randomizer.main import WEAPONS, SPECIALIZATIONS, SKILLS
import yaml

exps = {
    "base": "base",
    "HoT": "heart_of_thorns",
    "PoF": "path_of_fire",
    "EoD": "end_of_dragons",
    "SotO": "secrets_of_the_obscure",
    "JW": "janthir_wilds",
}


with WEAPONS.open() as f:
    #              prof      exp       hand      wep
    weapons: dict[str, dict[str, dict[str, list[str]]]] = yaml.safe_load(f)

with SPECIALIZATIONS.open() as f:
        specs = yaml.safe_load(f)

with SKILLS.open() as f:
    skills = yaml.safe_load(f)

for prof, exp_hand_wep in weapons.items():
    print(f"[{prof.lower()}]")
    print(f"specializations = {specs[prof]}")
    print(f"[{prof.lower()}.skills]")
    print(f"heal = {skills[prof]["heal_skills"]}")
    print(f"utility = {skills[prof]["utility_skills"]}")
    print(f"elite = {skills[prof]["elite_skills"]}")
    
    print(f"[{prof.lower()}.weapons]")
    for exp, hand_wep in exp_hand_wep.items():
        print(f"[{prof.lower()}.weapons.{exps[exp]}]")
        for hand, wep in hand_wep.items():
            print(f"{hand} = {wep}")
