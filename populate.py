from pyattck import Attck
import yaml

# Update reference files, actor patterns, etc.

def update_actors(attack):
    main_list = []
    for actor in attack.enterprise.actors:
        actor_dict = {}
        actor_dict['id'] = actor.id
        actor_dict['name'] = actor.name
        actor_dict['aliases'] = []
        for alias in actor.aliases:
            actor_dict['aliases'].append(alias)
        actor_dict['comments'] = actor.description
        actor_dict['reference'] = actor.wiki
        actor_dict['techniques'] = []
        for technique in actor.techniques:
            actor_dict['techniques'].append(technique.id)
        main_list.append(actor_dict)

    for object in main_list:
        with open('packages\\actors\\'+object['id']+'.yml', 'w') as f:
            yaml.dump(object, f, allow_unicode=True)


def update_techniques_readme(attack):
    for technique in attack.enterprise.techniques:
        with open('packages\\pyattck_techniques\\README.MD', 'a') as f:
            f.write(f'## {technique.id}: {technique.name}\n')
            try:
                for c in technique.command_list:
                    c = c.replace('#{node}', '$TARGET$') #Given to Script
                    c = c.replace('#{remote.host.fqdn}', '$TARGET$') #Given to Script
                    c = c.replace('#{domain.user.name}', '$USER$') #Given to Script
                    c = c.replace('#{domain.user.password}', '$PASSWORD$') #Given to Script
                    c = c.replace('#{server}', '$RANDOMURL$')
                    c = c.replace('#{group}', '1010')
                    c = c.replace('#{xmlfile}', 'deliveries\\files\\test.xsl')
                    c = c.replace('#{service_search_string}', 'vulnerable_service') #Random String maybe
                    c = c.replace('shell', 'cmd.exe /c')
                    f.write('* '+c+'\n')
            except:
                pass


def update_techniques_reference(attack):
    technique_list = []
    tactic_list = []
    tactic_dict = {}
    for t in attack.enterprise.techniques:
        technique_dict = {}
        technique_dict['id'] = t.id
        technique_dict['tactics'] = []
        for tactic in t.tactics:
            if not tactic.name in tactic_dict:
                tactic_dict[tactic.name] = []
                tactic_dict[tactic.name].append(t.id)
            else:
                tactic_dict[tactic.name].append(t.id)
            technique_dict['tactics'].append(tactic.name)
        technique_list.append(technique_dict)
    with open('packages\\pyattck_techniques\\technique_reference.yml', 'w') as f:
        yaml.dump(technique_list, f)
    with open('packages\\pyattck_techniques\\tactic_reference.yml', 'w') as f:
        yaml.dump(tactic_dict, f)

def main():
    with open('packages\\pyattck_techniques\\README.MD', 'w') as f:
        pass
    attack = Attck()
    update_actors(attack)
    update_techniques_reference(attack)
    update_techniques_readme(attack)

main()