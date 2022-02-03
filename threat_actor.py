import subprocess
import logging
import datetime
import yaml
import sys
import traceback
import random

# TODO - Ordering Technique Execution by Tactic

class Actor():

    def __init__(self, args, command_list, command_dict):
        self.tactic_order = {}
        self.tactic_order['Reconnaissance'] = 0
        self.tactic_order['Resource Development'] = 1
        self.tactic_order['Initial Access'] = 2
        self.tactic_order['Execution'] = 3
        self.tactic_order['Persistence'] = 4
        self.tactic_order['Privilege Escalation'] = 5
        self.tactic_order['Defense Evasion'] = 6
        self.tactic_order['Credential Access'] = 7
        self.tactic_order['Discovery'] = 8
        self.tactic_order['Lateral Movement'] = 9
        self.tactic_order['Collection'] = 10
        self.tactic_order['Command and Control'] = 11
        self.tactic_order['Exfiltration'] = 12
        self.tactic_order['Impact'] = 13
        self.command_list = command_list #Technique ID -> List of Command IDs
        self.command_dict = command_dict #ID -> COMMAND
        self.mode = args['mode']
        self.actor_file = args['actor']
        self.target = args['target']
        self.remote = args['remote']

        self.read_configs()
        #self.order_techniques() # Probably not needed anymore.
        print(self.actor_name)
        print(self.actor_id)
        print(self.actor_description)

        self.choose_commands()
        self.execute()

    def execute(self):
        for k in self.tactic_order:
            print(f"STARTING {k}")
            if k in self.available_commands:
                commands = self.available_commands[k]
                for c in commands:
                    print("EXECUTING: "+self.command_dict[c])
                    result = 0
                    #result = self.command_check(str(self.command_dict[c]))
                    if result == "ERROR":
                        print("Error Executing Command")
                    else:
                        print("Successfully Executed Command")
            else:
                print("NO COMMANDS FOUND\n")

    def choose_commands(self):
        self.available_commands = {}
        for technique in self.actor_techniques:
            for item in self.command_list:
                if item['technique_id'] == technique:
                    #print("Technique: "+technique)
                    #print("Technique Name: "+item['technique_name'])
                    #print("Tactic: "+item['technique_tactic'])
                    #print("Available Commands: "+str(item['commands']))
                    if len(item['commands']) > 3:  # Choosing 3 per TechniqueID at max
                        added_commands = random.sample(item['commands'], 3)
                    else:
                        added_commands = item['commands']
                    if not item['technique_tactic'] in self.available_commands:
                        self.available_commands[item['technique_tactic']] = []
                        for c in added_commands:
                            self.available_commands[item['technique_tactic']].append(c)
                    else:
                        for c in added_commands:
                            self.available_commands[item['technique_tactic']].append(c)

        if len(self.available_commands) == 0:
            print("No Commands Available for Threat Actor Simulation!")
            sys.exit(1)
        else:
            print("\nSTARTING EXECUTION\n")

    def command_check(command):
        try:
            logging.info(str(datetime.datetime.now()) + " Executing: " + str(command))
            subprocess.run(args=command, capture_output=True, check=True)
            return "SUCCESS"
        except subprocess.CalledProcessError:
            logging.exception(str(datetime.datetime.now()) + " Error Executing Command: " + str(command))
            print(traceback.print_exc(limit=None, file=None, chain=True))
            return "ERROR"

    def order_techniques(self):
        self.ordered_techniques = []
        for technique in self.actor_techniques:
            for item in self.technique_data:
                if item['id'] == technique:
                    for tac in item['tactics']:
                        print(self.tactic_order[tac])

    def read_configs(self):
        with open(self.actor_file) as f:
            try:
                actor_data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(e)
                sys.exit(1)
        self.actor_id = actor_data['id']
        self.actor_name = actor_data['name']
        self.actor_aliases = actor_data['aliases']
        self.actor_description = actor_data['comments']
        self.actor_reference = actor_data['reference']
        self.actor_techniques = actor_data['techniques']

        with open('packages\\pyattck_techniques\\technique_reference.yml', 'r') as f:
            try:
                self.technique_data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(e)
                sys.exit(1)

        with open('packages\\pyattck_techniques\\tactic_reference.yml', 'r') as f:
            try:
                self.tactic_data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(e)
                sys.exit(1)
