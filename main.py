import yaml
import os


def read_packages():
    package_list = []
    file = 'packages\\discovery\\local_discovery.yml'
    for root, subdirs, files in os.walk('packages'):
        for file in files:
            if not root.endswith("mitre_mappings") and not root.endswith("actors"):
                package_list.append(os.path.join(root,file))
    return package_list
    #with open(file, 'r') as f:
    #    try:
    #        string_data = yaml.safe_load(f)
    #    except yaml.YAMLError as e:
    #        print(e)

def read_files(package_list):
    data = []
    for file in package_list:
        with open(file, 'r') as f:
            try:
                string_data = yaml.safe_load(f)
                data.append(string_data)
            except yaml.YAMLError as e:
                print(e)
    return data


def generate_mappings(yaml_data):
    command_list = []
    # {technique_id = X, technique_name = X, commands = [], technique_tactic = X}
    # command_list = [{}, {},...]
    for string_data in yaml_data:
        for item in string_data['commands']:
            temp_dict = {}
            #print(f"ID: {string_data['commands'][item]['id']}")
            #print(f"Command: {string_data['commands'][item]['command']}")
            try:
                for value in string_data['commands'][item]['mitre']:
                    try:
                        tactic, technique_id, technique_name = value.split(";")
                    except ValueError:
                        print(f"Error MITRE Processing: {string_data['commands'][item]['id']}")
                        continue
                    #print(f"Tactic: {tactic}")
                    #print(f"Technique ID: {technique_id}")
                    #print(f"Technique Name: {technique_name}")
                    technique_dict = {}
                    #technique_dict['command_id'] = string_data['commands'][item]['id']
                    technique_dict['technique_id'] = technique_id
                    technique_dict['technique_name'] = technique_name
                    technique_dict['technique_tactic'] = tactic
                    technique_dict['commands'] = []
                    technique_dict['commands'].append(string_data['commands'][item]['id'])
                    #technique_dict['commands'].append(string_data['commands'][item]['command'])
                    i = 0
                    index = "None"
                    for i in range(len(command_list)):
                        if technique_id == command_list[i]['technique_id']:
                            print(f"INSERTING: {string_data['commands'][item]['id']} INTO {command_list[i]['technique_id']}")
                            index = i
                            break
                        else:
                            pass
                    if index != "None":
                        if not string_data['commands'][item]['id'] in command_list[i]['commands']:
                            command_list[i]['commands'].append(string_data['commands'][item]['id'])
                    else:
                        command_list.append(technique_dict)
            except TypeError:
                print(f"Error MITRE Processing: {string_data['commands'][item]['id']}")
                continue

    with open('packages\\mitre_mappings\\mappings.yml', 'w') as f:
        yaml.dump(command_list, f, allow_unicode=True)



def main():
    package_list = read_packages()
    yaml_data = read_files(package_list)
    generate_mappings(yaml_data)
main()

