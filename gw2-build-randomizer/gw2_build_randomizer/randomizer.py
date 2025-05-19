# Created by Xinatron (discord xinatron, gw2: xinatron.7149) along with foxgloria. Updated for EoD by REMagic42
# Send me (xinatron) a message if you have any questions/remarks

import random
import numpy as np
 
# randomly pick a class
class_pick = input('Pick a class: "Warrior", "Guardian", "Revenant", "Ranger", "Thief", "Engineer", "Elementalist", "Mesmer", "Necromancer" or "Random"\n')
class_list = ["Warrior", "Guardian", "Revenant", "Ranger", "Thief", "Engineer", "Elementalist", "Mesmer", "Necromancer"]
if class_pick == "Random":
  classes = random.randint(0, 8)
else:
  classes = class_list.index(class_pick)

print()
print("Your random build is:") 
print()
  
# choose traitlines
elite_specs = [0,5,6,7]
elite_spec = random.choice(elite_specs)
 
trait_list = [["Strength", "Arms", "Defence", "Tactics", "Discipline", "Spellbreaker", "Berserker", "Bladesworn"],
              ["Zeal", "Radiance", "Valor", "Honor", "Virtues", "Dragonhunter", "Firebrand", "Willbender"],
              ["Corruption", "Retribution", "Salvation", "Invocation", "Devastation", "Herald", "Renegade", "Vindicator"],
              ["Marksmanship", "Skirmishing", "Wilderness Survival", "Nature Magic", "Beastmastery", "Druid","Soulbeast", "Untamed"], 
              ["Deadly Arts", "Critical Strikes", "Shadow Arts", "Acrobatics", "Trickery", "Daredevil", "Deadeye", "Specter"], 
              ["Explosives", "Firearms", "Inventions", "Alchemy", "Tools", "Scrapper", "Holosmith", "Mechanist"],
              ["Fire", "Air", "Earth", "Water", "Arcane", "Tempest", "Weaver", "Catalyst"],
              ["Domination", "Dueling", "Chaos", "Inspiration", "Illusions", "Chronomancer", "Mirage", "Virtuoso"],
              ["Spite", "Curses", "Death Magic", "Blood Magic", "Soul Reaping", "Reaper", "Scourge", "Harbinger"]]
 
 
traits = range(5)
 
if elite_spec == 0:     # core class: pick 3 traitlines
  traits_picked = random.sample(traits, 3)
  class_name = class_list[classes]
  class_name2 = class_name
else:                   # elite spec chosen: only 2 traitlines needed
  traits_picked = random.sample(traits, 2)
  traits_picked.append(elite_spec)
  class_name = trait_list[classes][elite_spec] + " (" + class_list[classes] + ")"
  class_name2 = trait_list[classes][elite_spec]
print(class_name)  
 
# chose majors of each trait
majors = ["top", "middle", "bottom"]
for i in range(3):
  print()
  print(trait_list[classes][traits_picked[i]])
  for j in range(3):
    print(random.choice(majors))

print()

# Skills pick method, done and can be updated to include expansion when needed.
 
# pick random skills based on the class chosen, pets for rangers as well
skill_list = []
 
heal_skills =   [['Mending','To the Limit!','Healing Signet','Defiant Stance','Natural Healing','Blood Reckoning','Combat Stimulant'],
                ['Receive the Light','Litany of Wrath','Shelter','Signet of Resolve','Purification','Mantra of Solace','Reversal of Fortune'],
                [''],
                ['We Heal as one!','Water Spirit','Troll Unguent','Healing Spring','Glyph of Rejuvenation','Bear Stance','Perilous Gift'],
                ['Hide in Shadows','Signet of Malice','Withdraw','Skelk Venom','Channeled Vigor','Malicious Restoration','Well of Gloom'],
                ['A.E.D.','Elixer H','Healing Turret','Medkit','Medic Gyro','Coolant Blast', 'Rectifier Signet'],
                ['Arcane Brilliance','Ether Renewal','Glyph of Elemental Harmony','Signet of Restoration','Wash the Pain Away!','Aquatic Stance','Soothing Water'],
                ['Ether Feast','Mirror','Mantra of Recovery','Signet of the Ether','Well of Eternity','False Oasis','Twin Blade Restoration'],
                ['Consume Conditions','Summon Blood Fiend','Signet of Vamparism','Well of Blood','Your Soul is Mine!','Sand Flare','Elixir of Promise']]
 
util_skills = [['Banner of Defence','Banner of Dicipline','Banner of Strenght','Banner of Tactics','Bulls Charge','Kick','Stomp','Throw Bolas','Fear me!','For Great Justice!','On My Mark!','Shake It Off!','Dolyak Signet','Signet of Fury','Signet of Might','Signet of Stamina','Balanced Stance','Berserker Stance','Endure Pain','Frenzy','Sight Beyond Sight','Featherfoot Grace','Imminent Threat','Break Enchantments','Outrage','Shattering Blow','Sundering Leap','Wild Blow','Dragonspike Mine', 'Electric Fence', 'Flow Stabilizer', 'Overcharged Cartridges'],
                ['Hallowed Ground','Purging Flames','Sanctuary','Wall of Reflection','Contemplation of Purity',"Judge's Intervention",'Merciful Intervention','Smite Condition','Hold The Line!','Advance!','Save Yourselves!','Stand Your Ground','Bane Signet','Signet of Judgment','Signet of Mercy','Signet of Wrath','Bow of Truth','Hammer of Wisdom','Shield of the Avenger','Sword of Justice','Fragments of Faith',"Light's Judgment",'Test of Faith','Procession of Blades','Mantra of Flame','Mantra of Lore','Matra of Truth','Mantra of Potence','Flash Combo', 'Heel Crack', 'Roiling Light', 'Whirling Light'],
                [''],
                ['Guard!','Protect Me!','Search and Rescue!',"Sic'em",'Signet of Renewal','Signet of Stone','Signet of the Hunt','Signet of the Wild','Frost Spirit','Stone Spirit','Storm Spirit','Sun Spirit','Lightning Reflexes','Muddy Terrain','Quickening Zephyr','Sharpening Stone','Flame Trap','Frost Trap','Spike Trap',"Viper's Nest",'Glyph of Alignment','Glyph of Equality','Glyph of Unity','Glyph of the Tides','Dolyak Stance','Griffon Stance','Moa Stance','Vulture Stance','Exploding Spores','Mutate Conditions','Natures Binding','Unnatural Traversal'],
                ['Blinding Powder','Shadow Refuge','Shadowstep','Smoke Screen','Prepare Pitfall','Prepare Thousand Needles','Prepare Shadow Portal','Prepare Seal Area',"Assassin's Signet","Infiltrator's Signet","Signet of Agility",'Signet of Shadows','Caltrops','Haste','Roll for Initiative','Scorpion Wire','Devourer Venom','Ice Drake Venom','Skale Venom','Spider Venom',"Bandit's Defense",'Distracting Daggers','Fist Furry','Impairing Daggers','Binding Shadow','Mercy','Shadow Flare','Shadow Gust','Well of Bounty','Well of Silence','Well of Sorrow','Well of Tears'],
                ['Bomb kit','Grenade Kit','Elixir Gun','Flamethrower','Tool Kit','Elixir B','Elixir C','Elixir R','Elixir S','Elixir U','Personal Battering Ram','Rocket Boots','Slick Shoes','Throw Mine','Utility Goggles','Flame Turret','Net Turret','Rifle Turret','Harpoon Turret','Rocket Turret','Thumper Turret','Blast Gyro','Bulwark Gyro','Purge Gyro','Shredder Gyro','Spectrum Shield','Hard Light Arena','Laser Disk','Photon Wall','Barrier Signet','Force Signet','Shift Signet','Superconducting Signet'],
                ['Arcane Blast','Arcane Power','Arcane Shield','Arcane Wave','Armor of Earth','Cleansing Fire','Lightning Flash','Mist Form','Conjure Earth Shield','Conjure Flame Axe','Conjure Frost Bow','Conjure Lightning Hammer','Glyph of Elemental Power','Glyph of Lesser Elementals','Glyph of Renewal','Glyph of Storms','Signet of Air','Signet of Earth','Signet of Fire','Signet of Water','Feel the Burn!','Eye of the Storm!','Aftershock!','Flash-Freeze!','Primordial Stance','Stone Resonance','Unravel','Twist of Fate','Fortified Earth','Relentless Fire','Invigorating Air','Shattering Ice'],
                ['Decoy','Mirror Image','Feedback','Nullfield','Portal Entre','Veil','Arcane Thievery','Blink','Illusion of Life','Mimic','Mantra of Concentration','Mantra of distraction','Mantra of Pain','Mantra of Resolve','Phantasmal Defender','Phantasmal Disenchanter','Signet of Domination','Signet of Illusions','Signet of Inspiration','Signet of Midnight','Well of Action','Well of Calamity','Well of Precognition','Well of Recall','Crystal Sands','Illusionary Ambush','Mirage Advance','Sand Through Glass','Blade Renewal','Psychic Force','Rain of Swords','Sword of Decimation'],
                ['Blood is Power','Corrosive Poison Cloud','Corrupt Boon','Epidemic','Summon Bone Fiend','Summon Bone Minion','Summon Flesh Worm','Summon Shadow Fiend','Plague Signet','Signet of Spite','Signet of the Locust','Signet of Undeath','Spectral Armor','Spectral Grasp','Spectral Walk','Spectral Ring','Well of Corruption','Well of Darkness','Well of Power','Well of Suffering','Nothing can save you!','Rise!','Suffer!','You are all Weaklings!','Trail of Anguish','Dessicate','Sand Swell','Serpent Siphon','Elixir of Anguish','Elixir of Bliss','Elixir of Ignorance','Elixir of Risk']]
elite_skills = [['Battle Standard','Rampage','Signet of Rage','Winds of Disenchantment','Head Butt','Tactical Reload'],
                ['Feel my Wrath!','Renewed Focus','Signet of Courage',"Dragon's Maw",'Mantra of Liberation','Heavens Palm'],
                [''],
                ['Strength of the Pack!','Spirit of Nature','Entangle','Glyph of the Stars','One Wolf Pack','Forests Fortification'],
                ['Thieves Guild','Basilisk Venom','Dagger Storm','Impact Strike','Shadow Meld','Shadowfall'],
                ['Elite Mortar Kit','Elixir X','Supply Crate','Sneak Gyro','Prime Light Beam','Overclock Signet'],
                ['Conjure Fiery Greatsword','Glyph of Elementals','Tornado','Rebound!','Weave Self','Elemental Celerity'],
                ['Time Warp','Mass Invisibility','Signet of Humility','Gravity Well','Jaunt','Thousand Cuts'],
                ['Plaguelands','Summon Flesh Golem','Lich Form','Chill to the Bone!','Ghastly Breach','Elixir of Ambition']]
rev_legends = np.array(['Assassin','Centaur','Demon','Dwarf','Dragon','Renegade','Alliance'])
ranger_pets = ['Arctodus','Black Bear','Brown Bear','Murrelow','Polar bear','Eagle','Hawk','Owl','Raven','White Raven','Alpine Wolf','Fern hound','Hyena','Krytan Drakehound','Wolf','Carrion Devourer','Lashtail Devourer','Whiptail Devourer','Ice Drake','Marsh Drake','Reef Drake','River Drake','Salamander Drake','Cheetah','Jaguar','Jungle Stalker','Lynx','Sand Lion','Snow Leopard','Tiger','Black Moa','Blue Moa','Pink Moa','Red Moa','White Moa','Boar','Pig','Siamoth','Warthog','Black Widow Spider','Cave Spider','Forest Spider','Jungle Spider','Electric Wyvern','Fire Wyvern','Armor Fish','Bristleback','Fanged Iboga','Jacaranda','Rock Gazelle','Smoke Scale','Phoenix','White Tiger','Wallow','Siege Turtle']
 
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
if classes == 2:         
  possible_legends = rev_legends[heal_choices]  # there are as many legends as another class has heal skills
  chosen_legends = np.random.choice(possible_legends, 2, replace=False)
  print("Legend 1: Legendary {} Stance".format(chosen_legends[0]))
  print("Legend 2: Legendary {} Stance".format(chosen_legends[1]))
 
else:
  # pick a random heal skill
  possible_heal = np.array(heal_skills[classes])[heal_choices]
  heal = random.choice(possible_heal)
  print("Heal skill: {}".format(heal))
 
  # pick 3 different skills
  possible_skills = np.array(util_skills[classes])[skill_choices]
  skill = np.random.choice(possible_skills, 3, replace=False)
  print("Utility skill 1: {}".format(skill[0]))
  print("Utility skill 2: {}".format(skill[1]))
  print("Utility skill 3: {}".format(skill[2]))
 
  # pick a random elite skill
  possible_elite = np.array(elite_skills[classes])[elite_choices]
  elite = random.choice(possible_elite)
  print("Elite skill: {}".format(elite))
 
# pick 2 pets if you are a ranger

if classes == 3:
  pets = random.sample(ranger_pets, 2)
  print("Pet 1: {}".format(pets[0]))
  print("Pet 2: {}".format(pets[1]))

print()

# dict of all weapons each class can use. mh is main hand, oh is off hand, th is two-handed
weapon_dict = {
 
"Guardian_mh" : ["mace", "sword", "scepter"],
"Guardian_oh" : ["focus", "shield", "torch"],
"Guardian_th" : ["greatsword", "hammer", "staff"],
 
"Dragonhunter_mh" : ["mace", "sword", "scepter"],
"Dragonhunter_oh" : ["focus", "shield", "torch"],
"Dragonhunter_th" : ["greatsword", "hammer", "longbow", "staff"],
 
"Firebrand_mh" : ["axe", "mace", "sword", "scepter"],
"Firebrand_oh" : ["focus", "shield", "torch"],
"Firebrand_th" : ["greatsword", "hammer", "staff"],
 
"Willbender_mh" : ["mace", "sword", "scepter"],
"Willbender_oh" : ["focus", "shield", "torch", "sword"],
"Willbender_th" : ["greatsword", "hammer", "staff"],
 
"Revenant_mh" : ["mace", "sword"],
"Revenant_oh" : ["axe", "sword"],
"Revenant_th" : ["hammer", "staff"],
 
"Herald_mh" : ["mace", "sword"],
"Herald_oh" : ["axe", "sword",  "shield"],
"Herald_th" : ["hammer", "staff"],
 
"Renegade_mh" : ["mace", "sword"],
"Renegade_oh" : ["axe", "sword"],
"Renegade_th" : ["hammer", "short bow", "staff"],
 
"Vindicator_mh" : ["mace", "sword"],
"Vindicator_oh" : ["axe", "sword"],
"Vindicator_th" : ["hammer", "staff", "greatsword"],
 
"Warrior_mh" : ["axe", "mace", "sword"],
"Warrior_oh" : ["axe", "mace", "sword", "shield", "warhorn"],
"Warrior_th" : ["greatsword", "hammer", "longbow", "rifle"],
 
"Berserker_mh" : ["axe", "mace", "sword"],
"Berserker_oh" : ["axe", "mace", "sword", "shield", "torch", "warhorn"],
"Berserker_th" : ["greatsword", "hammer", "longbow", "rifle"],
 
"Spellbreaker_mh" : ["axe", "dagger", "mace", "sword"],
"Spellbreaker_oh" : ["axe", "dagger", "mace", "sword", "shield", "warhorn"],
"Spellbreaker_th" : ["greatsword", "hammer", "longbow", "rifle"],
 
"Bladesworn_mh" : ["axe", "mace", "sword"],
"Bladesworn_oh" : ["axe", "mace", "sword", "shield", "warhorn", "pistol"],
"Bladesworn_th" : ["greatsword", "hammer", "longbow", "rifle"],
 
"Ranger_mh" : ["axe", "sword"],
"Ranger_oh" : ["axe", "dagger", "torch", "warhorn"],
"Ranger_th" : ["greatsword", "longbow", "short bow"],
 
"Druid_mh" : ["axe", "sword"],
"Druid_oh" : ["axe", "dagger", "torch", "warhorn"],
"Druid_th" : ["greatsword", "longbow", "short bow", "staff"],
 
"Soulbeast_mh" : ["axe", "dagger","sword"],
"Soulbeast_oh" : ["axe", "dagger", "torch", "warhorn"],
"Soulbeast_th" : ["greatsword", "longbow", "short bow"],
 
"Untamed_mh" : ["axe", "sword"],
"Untamed_oh" : ["axe", "dagger", "torch", "warhorn"],
"Untamed_th" : ["greatsword", "longbow", "short bow", "hammer"],
 
"Thief_mh" : ["dagger", "pistol", "sword"],
"Thief_oh" : ["dagger", "pistol"],
"Thief_th" : ["short bow"],
 
"Daredevil_mh" : ["dagger", "pistol", "sword"],
"Daredevil_oh" : ["dagger", "pistol"],
"Daredevil_th" : ["short bow", "staff"],
 
"Deadeye_mh" : ["dagger", "pistol", "sword"],
"Deadeye_oh" : ["dagger", "pistol"],
"Deadeye_th" : ["rifle", "short bow"],
 
"Specter_mh" : ["scepter", "dagger", "pistol", "sword"],
"Specter_oh" : ["dagger", "pistol"],
"Specter_th" : ["short bow"],
 
 
"Engineer_mh" : ["pistol"],
"Engineer_oh" : ["pistol", "shield"],
"Engineer_th" : ["rifle"],
 
"Scrapper_mh" : ["pistol"],
"Scrapper_oh" : ["pistol", "shield"],
"Scrapper_th" : ["hammer", "rifle"],
 
"Holosmith_mh" : ["pistol", "sword"],
"Holosmith_oh" : ["pistol", "shield"],
"Holosmith_th" : ["rifle"],
 
"Mechanist_mh" : ["pistol, mace"],
"Mechanist_oh" : ["pistol", "shield"],
"Mechanist_th" : ["rifle"],
 
"Elementalist_mh" : ["dagger", "scepter"],
"Elementalist_oh" : ["dagger", "focus"],
"Elementalist_th" : ["staff"],
 
"Tempest_mh" : ["dagger", "scepter"],
"Tempest_oh" : ["dagger", "focus", "warhorn"],
"Tempest_th" : ["staff"],
 
"Weaver_mh" : ["dagger", "sword", "scepter"],
"Weaver_oh" : ["dagger", "focus"],
"Weaver_th" : ["staff"],
 
"Catalyst_mh" : ["dagger", "scepter"],
"Catalyst_oh" : ["dagger", "focus"],
"Catalyst_th" : ["staff", "hammer"],
 
"Mesmer_mh" : ["sword", "scepter"],
"Mesmer_oh" : ["pistol", "sword", "focus", "torch"],
"Mesmer_th" : ["greatsword", "staff"],
 
"Chronomancer_mh" : ["sword", "scepter"],
"Chronomancer_oh" : ["pistol", "sword", "focus", "shield", "torch"],
"Chronomancer_th" : ["greatsword", "staff"],
 
"Mirage_mh" : ["axe", "sword", "scepter"],
"Mirage_oh" : ["pistol", "sword", "focus", "torch"],
"Mirage_th" : ["greatsword", "staff"],
 
"Virtuoso_mh" : ["sword", "scepter", "dagger"],
"Virtuoso_oh" : ["pistol", "sword", "focus", "torch"],
"Virtuoso_th" : ["greatsword", "staff"],
 
"Necromancer_mh" : ["axe", "dagger", "scepter"],
"Necromancer_oh" : ["dagger", "focus", "warhorn"],
"Necromancer_th" : ["staff"],
 
"Reaper_mh" : ["axe", "dagger", "scepter"],
"Reaper_oh" : ["dagger", "focus", "warhorn"],
"Reaper_th" : ["greatsword", "staff"],
 
"Scourge_mh" : ["axe", "dagger", "scepter"],
"Scourge_oh" : ["mace", "focus", "torch", "warhorn"],
"Scourge_th" : ["staff"],
 
"Harbinger_mh" : ["pistol", "axe", "dagger", "scepter"],
"Harbinger_oh" : ["dagger", "focus", "warhorn"],
"Harbinger_th" : ["staff"]}
 
main_hand = weapon_dict[class_name2+"_mh"]
off_hand = weapon_dict[class_name2+"_oh"]
two_handed = weapon_dict[class_name2+"_th"]
 
main_hand_options = len(main_hand)
off_hand_options = len(off_hand)
two_handed_options = len(two_handed)
 
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
    weapon_set.append([main_hand[weapon], off_hand[chosen_off_hands.pop(0)]])
  else:
    weapon_set.append([two_handed[weapon - main_hand_options]])

# Weapon choice printing. currently does not support bladesworn to only have a single weapon
print("Weapon set 1: {}".format(", ".join(weapon_set[0])))
if classes not in [5, 6]:
  print("Weapon set 2: {}".format(", ".join(weapon_set[1])))
 