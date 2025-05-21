import numpy as np
import os
import random
from pathlib import Path
from typing import Union, Literal
import tomllib

from pydantic import TypeAdapter

RESOURCE_DIR = Path(__file__).parent / "resources"
SETTINGS = RESOURCE_DIR / "settings.toml"
PROFESSIONS = RESOURCE_DIR / "professions.toml"

from gw2_build_randomizer.model import ClassNames, Settings, Gw2Classes

class_list = list(ClassNames)
    
def main(print_out: bool = False) -> str:
    output_string = ""

    settings = Settings.from_toml(SETTINGS)
    
    profession = settings.get_class()
    class_name = profession.name.capitalize()

    professions = TypeAdapter(Gw2Classes).validate_python(tomllib.loads(PROFESSIONS.read_text()))

    profession_info = professions[profession]

    elite_specs = [0,5,6,7]
    elite_spec = random.choice(elite_specs)
    traits = range(5)
    
    if elite_spec == 0:     # core class: pick 3 traitlines
        traits_picked = random.sample(traits, 3)
        class_name2 = "Core " + class_name 
    else:                   # elite spec chosen: only 2 traitlines needed
        traits_picked = random.sample(traits, 2)
        traits_picked.append(elite_spec)
        class_name2 = profession_info.specializations[elite_spec] + " (" + class_name + ")"
    
    output = "Your class is: {} \n".format(class_name2)
    if print_out:
        print(output)
    else:
        output_string += output + "\n"

    # chose majors of each trait
    majors = ["top", "middle", "bottom"]
    for i in range(3):
        output = f"{profession_info.specializations[traits_picked[i]]}:"
        for j in range(3):
            output += f" {random.choice(majors)}"
        if print_out:
            print(output + "\n")
        else:
            output_string += output + "\n"
    output_string += "\n"

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
        skill_choices.extend(range(28,32))
        elite_choices.append(5)
    
    # if revenenant, pick 2 legends instead of utility skills
    if profession == ClassNames.REVENANT:         
        possible_legends = np.array(profession_info.skills.special)[heal_choices]  # there are as many legends as another class has heal skills
        chosen_legends = np.random.choice(possible_legends, 2, replace=False)
        output = f"Legend 1: Legendary {chosen_legends[0]} Stance \nLegend 2: Legendary {chosen_legends[1]} Stance\n"
        if print_out:
            print(output)
        else:
            output_string += output + "\n"
    
    else:
        # pick a random heal skill
        possible_heal = np.array(profession_info.skills.heal)[heal_choices]
        heal = random.choice(possible_heal)
        output = f"Heal skill: {heal}\n"
        if print_out:
            print(output)
        else:
            output_string += output
            
    
        # pick 3 different skills
        possible_skills = np.array(profession_info.skills.utility)[skill_choices]
        skill = np.random.choice(possible_skills, 3, replace=False)
        output = f"Utility skill 1: {skill[0]}\nUtility skill 2: {skill[1]}\nUtility skill 3: {skill[2]}\n"
        if print_out:
            print(output)
        else:
            output_string += output
        
        # pick a random elite skill
        possible_elite = np.array(profession_info.skills.elite)[elite_choices]
        elite = random.choice(possible_elite)
        output = f"Elite skill: {elite}\n"
        if print_out:
            print(output)
        else:
            output_string += output + "\n"
    
    # pick 2 pets if you are a ranger

    if profession == ClassNames.RANGER:
        pets = random.sample(profession_info.skills.special, 2)
        output = f"Pet 1: {pets[0]}\nPet 2: {pets[1]}\n"
        if print_out:
            print(output)
        else:
            output_string += output + "\n"

    main_hand_names = []
    off_hand_names = []
    two_handed_names = []
    for weapon in profession_info.weapons.values():
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
    weapon_set = []
    
    for chosen_weapon in chosen_weapons:
        if chosen_weapon < main_hand_options:
            weapon_set.append([main_hand_names[chosen_weapon], off_hand_names[chosen_off_hands.pop(0)]])
        else:
            weapon_set.append([two_handed_names[chosen_weapon - main_hand_options]])

    # Weapon choice printing. currently does not support bladesworn to only have a single weapon
    output = f"Weapon set 1: {", ".join(weapon_set[0])}"
    if profession not in {ClassNames.ENGINEER, ClassNames.ELEMENTALIST}:
        output += f"\nWeapon set 2: {", ".join(weapon_set[1])}"
    if print_out:
        print(output)
    else:
        output_string += output

    return output_string
    
    
if __name__ == "__main__":
    main(print_out=True)
