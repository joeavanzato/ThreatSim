import yaml
import os
import sys
import argparse
import random
import logging
import datetime

import deliveries.CMD_REPLACEMENTS


def parse_args():
    arguments = {}
    parser = argparse.ArgumentParser(usage='''
    ### ThreatSim ###
    ### github.com/joeavanzato/threatsim ###

    ''')
    parser.add_argument("-t", "--target", help="Provide a target for use in remote-techniques such as lateral movement, execution, etc",
                        required=False, nargs=1, type=str)
    parser.add_argument("-a", "--actor", help="Which Threat Actor to simulate using MITRE GXXXX notation.  Use 'random' to"
                                              " select one at random or 'generic' to implement random choices in techniques.  If not specified, will use 'random'",
                        required=False, nargs=1, type=str)
    parser.add_argument("-dr", "--disable_remote", action='store_true', help="Disable Techniques marked as remote=true such as Proxy/DNS Requests, Domain Queries, etc")
    args = parser.parse_args()

    actor_list = os.listdir('packages\\actors')
    if args.actor:
        if args.actor[0] in actor_list:
            arguments['actor'] = f'packages\\actors\\{args.actor[0]}'
        elif args.actor[0] == 'random':
            arguments['actor'] = f'packages\\actors\\{random.choice(actor_list)}'
        elif args.actor[0] == 'generic':
            arguments['actor'] == 'packages\\mitre_mappings\\generic_ta.yml'
        else:
            print(f"Could not find specified Threat Actor: {args.actor[0]}")
            sys.exit(1)
    else:
        arguments['actor'] = f'packages\\actors\\{random.choice(actor_list)}'

    if args.target:
        arguments['target'] = args.target[0]
    else:
        arguments['target'] = 'NONE'

    if args.disable_remote:
        arguments['remote'] = False
    else:
        arguments['remote'] = True
    return arguments


def read_packages():
    package_list = []
    file = 'packages\\discovery\\local_discovery.yml'
    for root, subdirs, files in os.walk('packages'):
        for file in files:
            if not root.endswith("mitre_mappings") and not root.endswith("actors"):
                package_list.append(os.path.join(root,file))
    return package_list


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
    command_dict = {}
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
                    command_dict[string_data['commands'][item]['id']] = string_data['commands'][item]['command']
                    #technique_dict['commands'].append(string_data['commands'][item]['command'])
                    i = 0
                    index = "None"
                    for i in range(len(command_list)):
                        if technique_id == command_list[i]['technique_id']:
                            index = i
                            break
                        else:
                            pass
                    if index != "None":
                        if not string_data['commands'][item]['id'] in command_list[i]['commands']:
                            print(f"INSERTING: {string_data['commands'][item]['id']} INTO {command_list[i]['technique_id']}")
                            command_list[i]['commands'].append(string_data['commands'][item]['id'])
                    else:
                        print(f"INSERTING: {string_data['commands'][item]['id']} INTO {technique_dict['technique_id']}")
                        command_list.append(technique_dict)
            except TypeError:
                print(f"Error MITRE Processing: {string_data['commands'][item]['id']}")
                continue

    with open('packages\\mitre_mappings\\mappings.yml', 'w') as f:
        yaml.dump(command_list, f, allow_unicode=True)

    for k,v in command_dict.items():
        print(f"{k}: {v}")


def logger_setup():
    log_file = "threatsim_log.log"
    logging.basicConfig(filename=log_file, level=logging.DEBUG)
    logging.info(str(datetime.datetime.now()) + " ThreatSim Starting..")

def main():
    logger_setup()
    args = parse_args()
    package_list = read_packages()
    yaml_data = read_files(package_list)
    generate_mappings(yaml_data)
    print(deliveries.CMD_REPLACEMENTS.RANDOMURL)
    logging.info(str(datetime.datetime.now()) + f" RANDOMURL: {deliveries.CMD_REPLACEMENTS.RANDOMURL}")
    print(deliveries.CMD_REPLACEMENTS.RANDOMURL_PS1)
    logging.info(str(datetime.datetime.now()) + f" RANDOMURL_PS1: {deliveries.CMD_REPLACEMENTS.RANDOMURL_PS1}")
    print(deliveries.CMD_REPLACEMENTS.RANDOMPORTCOMMON)
    logging.info(str(datetime.datetime.now()) + f" RANDOMPORTCOMMON: {deliveries.CMD_REPLACEMENTS.RANDOMPORTCOMMON}")
    print(deliveries.CMD_REPLACEMENTS.RANDOMPORTUNCOMMON)
    logging.info(str(datetime.datetime.now()) + f" RANDOMPORTUNCOMMON: {deliveries.CMD_REPLACEMENTS.RANDOMPORTUNCOMMON}")
    print(deliveries.CMD_REPLACEMENTS.CURDIR)
    print(f"Simulating: {args['actor']}")
    logging.info(str(datetime.datetime.now()) + f" Simulating Actor: {args['actor']}")
    print(f"Remote Techniques: {args['remote']}")
    logging.info(str(datetime.datetime.now()) + f" Remote Techniques Enabled: {args['remote']}")
    print(f"FQDN: {deliveries.CMD_REPLACEMENTS.FQDN}")
main()

