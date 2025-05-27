import requests
import json
import yaml
import numpy as np

class_file_path = None      # still uses the old class file to get the names of the classes
profession_file_path = None     # this is the new, TOML, file that has more information in them

with open(class_file_path, 'r') as infile:
    classes = yaml.safe_load(infile)

with open(profession_file_path, "w") as outfile:
    
    
    for profession in classes.keys():
        response = requests.get(f"https://api.guildwars2.com/v2/professions/{profession}?v=latest")
        json_content = json.loads(response.content)
        skills_by_palette = np.array(json_content["skills_by_palette"])
        outfile.write(f"[[professions]]\n")
        outfile.write(f"name = '{json_content['name']}'\n")
        outfile.write(f"specializations = []\n")
        outfile.write(f"[professions.skills]\n")

        for skill in json_content["skills"]:
            if skill["type"] in ["Utility", "Heal", "Elite"]:
                skill_response = requests.get(f"https://api.guildwars2.com/v2/skills?ids={skill['id']}&lang=en")
                skill_dict = json.loads(skill_response.content)[0]
                try:
                    palette_idx = np.nonzero(skills_by_palette[:, 1] == skill_dict["id"])
                    
                    outfile.write(f"[[professions.skills.{skill['type'].lower()}]]\n")
                    outfile.write(f"name = '{skill_dict['name']}'\n")
                    outfile.write(f"id = {skill_dict['id']}\n")
                    outfile.write(f"palette_id = {skills_by_palette[palette_idx, 0][0][0]}\n")
                except:
                    outfile.write(f"[[professions.skills.{skill['type'].lower()}]]\n")
                    outfile.write(f"name = '{skill_dict['name']}'\n")
                    outfile.write(f"id = {skill_dict['id']}\n")
                    outfile.write(f"palette_id = 0\n")
        
        outfile.write(f"[professions.weapons]\n")
        outfile.write("\n")
