# ThreatSim
 Threat Simulator for Enterprise Networks

## Warning

ThreatSim contains many dangerous commands which can greatly impact system functionality, features and stability.  
It is recommended to only run on a machine which can be immediately re-imaged or is otherwise not part of any production network.  
Additionally, any target provided via the -t/--target flag should also be able to be immediately re-imaged and not part of any 
production network.

No responsibility is taken for damages incurred on production networks through use of this software - please carefully read 
the license and the source code prior to execution in order to understand the potential dangers.

## What is it?

ThreatSim is a blue-team utility designed to simulate modern threat-actor TTPs in order to help defenders identify potential 
gaps in logging, EDR/AV controls, SIEM/UEBA detections or otherwise.  It is possible to generate both completely randomized 
but logical behavior as well as to simulate actual threat actors based on known procedures.


## Modular Adversary Simulation

ThreatSim works by incorporating packages based on real threat-actor activity - what commands they run, behaviors they 
invoke, techniques they utilize, etc to allow your blue-team to properly simulate real-life activity in a controlled and 
'defanged' manner.  Of course these TTPs are ever-changing and detecting ThreatSim activity for a particular threat actor 
should not lull your organization into a false sense of security.

Actor Packages are based on MITRE-provided data, currently auto-generated using the awesome PyAttck module - 
each Actor has an associated set of 'techniques' - these techniques in turn each have one or more associated 'commands'.  
When an actor is simulated, techniques are first sorted by 'order' from Privilege Escalation to Impact and then executed in 
order with a command chosen at random for each technique out of the available pool.

Actors may have multiple techniques under the same tactic - if an actor has >3 technique IDs under the same tactic, at most 3 will be chosen 
at random for execution to keep things relatively sensible.

## Usage

For best simulation results, ThreatSim requires running as local administrator as well as a remote host [-t/--target] - 
ThreatSim will leverage the current user context in any applicable remote techniques such as lateral movement, etc unless 
specifically given a Username and Password when invoked [-u/--user].


## Contents

* ./packages/actors/ -> YAML files containing two types of 'behaviors' for threat actors - step-based patterns choosing 
from a known set of TTPs and technique-based patterns where a random command that matches the ID is chosen from the available pool. [STEP-BASED NOT IMPLEMENTED YET]
* ./packages/mitre_mappings/mappings.yml -> Automatically generated YAML file which shows all available commands on a per-technique ID basis, used for random-pool choices of commands.
* ./packages/MITRE_TACTICS -> YAML files mapping vetted commands to MITRE Techniques/Tactics.

### Replacements Available in Command Strings

* Any Environment Variable in the format %VARNAME% is replaced by os module.
* $TARGET$ - Remote Target if supplied to ThreatSim
* $USER$ - User Given to Script [Not Done Yet]
* $PASSWORD$ - Password Give to Script [Not Done Yet]
* $TEMPFILE$ - Randomly Generated Temporary File
* $CURDIR$ - Replace with Current Working Directory
* $RANDOMURL$ - Replace with randomly generated DGA-style URL
* $RANDOMURL_PS1$ - Replace with randomly generated DGA-Style URL to a .PS1 script.
* $RANDOMURL_EXE$ - [Not Done Yet]
* $RANDOMUSER$ - Replace with randomly generated username.
* $RANDOMDOMAINUSER$ - Replace with randomly generated domain username. [Not Done Yet]
* $RANDOMPORTUNCOMMON$ - Replace with randomly generated uncommonly-used port.
* $RANDOMPORTCOMMON$ - Replace with randomly generated commonly-used port.
* $FQDN$ - Fully Qualified Domain Name (HOSTNAME (local), EXAMPLE.LAB, TEST.COM, etc)

### Some Very useful References
* https://github.com/dxnboy/redteam
* https://github.com/PowerShellMafia
* https://github.com/D4Vinci/One-Lin3r
* https://github.com/op7ic/EDR-Testing-Script
* https://github.com/NextronSystems/APTSimulator
* https://attack.mitre.org/
* https://github.com/swimlane/pyattck
* https://github.com/ethereal-vx/Antivirus-Artifacts
* https://github.com/CyberMonitor/Invoke-Adversary