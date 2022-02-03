import yaml
import os
import sys
import argparse
import random
import logging
import datetime

import deliveries.CMD_REPLACEMENTS
import threat_actor

binary_dir = os.getcwd()
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
try:
    os.chdir(application_path)
except:
    pass

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
    parser.add_argument("-s", "--steps", help="Use Known Step-Based Patterns", action='store_true')
    parser.add_argument("-te", "--techniques", help="Use Known Technique-Based Patterns", action='store_true')
    args = parser.parse_args()

    actor_list = os.listdir('packages\\actors')
    name_list = []
    for item in actor_list:
        name_list.append(os.path.splitext(item)[0])

    if args.actor:
        if args.actor[0] in name_list:
            arguments['actor'] = f'packages\\actors\\{args.actor[0]}.yml'
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

    if args.steps and args.techniques:
        print("Choose Only One of -s/--steps and -te/--techniques!")
        sys.exit(1)
    elif args.steps and not args.techniques:
        arguments['mode'] = 'steps'
    elif args.techniques and not args.steps:
        arguments['mode'] = 'techniques'
    else:
        arguments['mode'] = 'techniques'

    return arguments


def read_packages():
    package_list = []
    file = 'packages\\discovery\\local_discovery.yml'
    for root, subdirs, files in os.walk('packages'):
        for file in files:
            if not root.endswith("mitre_mappings") and not root.endswith("actors") and not root.endswith("actors_old") and not root.endswith('pyattck_techniques'):
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


def generate_mappings(yaml_data, args):
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
                    command_dict[string_data['commands'][item]['id']] = string_data['commands'][item]['command'].replace("$CURDIR$", args['CURDIR'])\
                        .replace("$RANDOMURL$", args['RANDOMURL']).replace("$RANDOMURL_PS1$",args['RANDOMURL_PS1']).replace("$RANDOMPORTCOMMON$",str(args['RANDOMPORTCOMMON']))\
                        .replace("$RANDOMPORTUNCOMMON$",str(args['RANDOMPORTUNCOMMON'])).replace("$TARGET$", args['target']).replace("$FQDN$", args['FQDN'])
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
                            logging.info(str(datetime.datetime.now()) +f" INSERTING: {string_data['commands'][item]['id']} INTO {command_list[i]['technique_id']}")
                            #print(f"INSERTING: {string_data['commands'][item]['id']} INTO {command_list[i]['technique_id']}")
                            command_list[i]['commands'].append(string_data['commands'][item]['id'])
                    else:
                        logging.info(str(datetime.datetime.now()) +f" INSERTING: {string_data['commands'][item]['id']} INTO {technique_dict['technique_id']}")
                        #print(f"INSERTING: {string_data['commands'][item]['id']} INTO {technique_dict['technique_id']}")
                        command_list.append(technique_dict)
            except TypeError as e:
                print(f"Error MITRE Processing: {string_data['commands'][item]['id']}")
                print(e)
                continue

    with open('packages\\mitre_mappings\\mappings.yml', 'w') as f:
        yaml.dump(command_list, f, allow_unicode=True)

    #for k,v in command_dict.items():
    #    print(f"{k}: {v}")

    return command_list, command_dict


def logger_setup():
    log_file = "threatsim_log.log"
    logging.basicConfig(filename=log_file, level=logging.DEBUG)
    logging.info(str(datetime.datetime.now()) + " ThreatSim Starting..")


def update_args(args):
    print(f"RANDOMURL: {deliveries.CMD_REPLACEMENTS.RANDOMURL}")
    args['RANDOMURL'] = deliveries.CMD_REPLACEMENTS.RANDOMURL
    logging.info(str(datetime.datetime.now()) + f" RANDOMURL: {deliveries.CMD_REPLACEMENTS.RANDOMURL}")
    print(f"RANDOMURL_PS1: {deliveries.CMD_REPLACEMENTS.RANDOMURL_PS1}")
    args['RANDOMURL_PS1'] = deliveries.CMD_REPLACEMENTS.RANDOMURL_PS1
    logging.info(str(datetime.datetime.now()) + f" RANDOMURL_PS1: {deliveries.CMD_REPLACEMENTS.RANDOMURL_PS1}")
    print(f"RANDOMPORTCOMMON: {deliveries.CMD_REPLACEMENTS.RANDOMPORTCOMMON}")
    args['RANDOMPORTCOMMON'] = deliveries.CMD_REPLACEMENTS.RANDOMPORTCOMMON
    logging.info(str(datetime.datetime.now()) + f" RANDOMPORTCOMMON: {deliveries.CMD_REPLACEMENTS.RANDOMPORTCOMMON}")
    print(f"RANDOMPORTUNCOMMON: {deliveries.CMD_REPLACEMENTS.RANDOMPORTUNCOMMON}")
    args['RANDOMPORTUNCOMMON'] = deliveries.CMD_REPLACEMENTS.RANDOMPORTUNCOMMON
    logging.info(str(datetime.datetime.now()) + f" RANDOMPORTUNCOMMON: {deliveries.CMD_REPLACEMENTS.RANDOMPORTUNCOMMON}")
    print(f"CURDIR: {deliveries.CMD_REPLACEMENTS.CURDIR}")
    args['CURDIR'] = deliveries.CMD_REPLACEMENTS.CURDIR
    logging.info(str(datetime.datetime.now()) + f" CURDIR: {deliveries.CMD_REPLACEMENTS.CURDIR}")
    print(f"Simulating: {args['actor']}")
    logging.info(str(datetime.datetime.now()) + f" Simulating Actor: {args['actor']}")
    print(f"Remote Techniques: {args['remote']}")
    logging.info(str(datetime.datetime.now()) + f" Remote Techniques Enabled: {args['remote']}")
    print(f"FQDN: {deliveries.CMD_REPLACEMENTS.FQDN}")
    args['FQDN'] = deliveries.CMD_REPLACEMENTS.FQDN
    logging.info(str(datetime.datetime.now()) + f" FQDN: {deliveries.CMD_REPLACEMENTS.FQDN}")
    print(f"TARGET: {args['target']}")
    logging.info(str(datetime.datetime.now()) + f" TARGET: {args['target']}")
    print(f"MODE: {args['mode']}")
    logging.info(str(datetime.datetime.now()) + f" MODE: {args['mode']}")
    return args

def main():
    logger_setup()
    args = parse_args()
    updated_args = update_args(args)
    package_list = read_packages()
    yaml_data = read_files(package_list)
    command_list, command_dict = generate_mappings(yaml_data, updated_args)
    ta = threat_actor.Actor(updated_args, command_list, command_dict, binary_dir)

main()

