import numpy as np
import yaml
import os
import random

class_list = ["warrior", "guardian", "revenant", "ranger", "thief", "engineer", "elementalist", "mesmer", "necromancer"]

def class_to_index(class_pick):
    if isinstance(class_pick, str):
        class_pick = class_pick.lower()
    else:
        class_pick = [single_class.lower() for single_class in class_pick]
        
    if class_pick == "random":
        return random.randint(0, 8)
    elif class_pick in class_list:
        return class_list.index(class_pick)
    else:
        possible_ind = []
        for single_class in class_pick:
            possible_ind.append(class_list.index(single_class))
        return possible_ind[random.randint(0, len(possible_ind)-1)]

    
def main(print_out=False):
    output_string = ""
    program_dir = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(program_dir, "specializations.yaml"), "r") as f:
        specs = yaml.safe_load(f)

    with open(os.path.join(program_dir, "skills.yaml"), "r") as f:
        skills = yaml.safe_load(f)
        
    with open(os.path.join(program_dir, "weapons.yaml"), "r") as f:
        weapons = yaml.safe_load(f)
        
    with open(os.path.join(program_dir, "settings.yaml"), "r") as f:
        settings = yaml.safe_load(f)
        
    class_index = class_to_index(settings["class"])
    class_name = class_list[class_index].capitalize()


    elite_specs = [0,5,6,7]
    elite_spec = random.choice(elite_specs)
    traits = range(5)
    
    if elite_spec == 0:     # core class: pick 3 traitlines
        traits_picked = random.sample(traits, 3)
        class_name2 = "Core " + class_name 
    else:                   # elite spec chosen: only 2 traitlines needed
        traits_picked = random.sample(traits, 2)
        traits_picked.append(elite_spec)
        class_name2 = specs[class_name][elite_spec] + " (" + class_name + ")"
    
    output = "Your class is: {} \n".format(class_name2)
    if print_out:
        print(output)
    else:
        output_string += output + "\n"

    # chose majors of each trait
    majors = ["top", "middle", "bottom"]
    for i in range(3):
        output = f"{specs[class_name][traits_picked[i]]}:"
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
    if class_index == 2:         
        possible_legends = np.array(skills["rev_legends"])[heal_choices]  # there are as many legends as another class has heal skills
        chosen_legends = np.random.choice(possible_legends, 2, replace=False)
        output = f"Legend 1: Legendary {chosen_legends[0]} Stance \nLegend 2: Legendary {chosen_legends[1]} Stance\n"
        if print_out:
            print(output)
        else:
            output_string += output + "\n"
    
    else:
        # pick a random heal skill
        possible_heal = np.array(skills[class_name]["heal_skills"])[heal_choices]
        heal = random.choice(possible_heal)
        output = f"Heal skill: {heal}\n"
        if print_out:
            print(output)
        else:
            output_string += output
            
    
        # pick 3 different skills
        possible_skills = np.array(skills[class_name]["utility_skills"])[skill_choices]
        skill = np.random.choice(possible_skills, 3, replace=False)
        output = f"Utility skill 1: {skill[0]}\nUtility skill 2: {skill[1]}\nUtility skill 3: {skill[2]}\n"
        if print_out:
            print(output)
        else:
            output_string += output
        
        # pick a random elite skill
        possible_elite = np.array(skills[class_name]["elite_skills"])[elite_choices]
        elite = random.choice(possible_elite)
        output = f"Elite skill: {elite}\n"
        if print_out:
            print(output)
        else:
            output_string += output + "\n"
    
    # pick 2 pets if you are a ranger

    if class_index == 3:
        pets = random.sample(skills["ranger_pets"], 2)
        output = f"Pet 1: {pets[0]}\nPet 2: {pets[1]}\n"
        if print_out:
            print(output)
        else:
            output_string += output + "\n"

    main_hand_names = []
    off_hand_names = []
    two_handed_names = []
    for weapon in weapons[class_name].values():
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
    
    for weapon in chosen_weapons:
        if weapon < main_hand_options:
            weapon_set.append([main_hand_names[weapon], off_hand_names[chosen_off_hands.pop(0)]])
        else:
            weapon_set.append([two_handed_names[weapon - main_hand_options]])

    # Weapon choice printing. currently does not support bladesworn to only have a single weapon
    output = f"Weapon set 1: {", ".join(weapon_set[0])}"
    if class_index not in [5, 6]:
        output += f"\nWeapon set 2: {", ".join(weapon_set[1])}"
    if print_out:
        print(output)
    else:
        output_string += output

    return output_string
    
    
if __name__ == "__main__":
    main(print_out=True)