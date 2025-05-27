import requests
import json
import yaml

# still uses old yaml format

class_dict = {}
for i in range(72):
    response = requests.get(f"https://api.guildwars2.com/v2/specializations/{i+1}")
    json_content = json.loads(response.content)
    id = json_content["id"]
    name = json_content["name"]
    profession = json_content["profession"]
    print(id)
    try:
        class_dict[profession].append(name + "|" + str(id))
    except KeyError:
        class_dict[profession] = [name + "|" + str(id)]
        
class_file_path = None
with open(class_file_path, 'w') as outfile:
    yaml.dump(class_dict, outfile, default_flow_style=False)