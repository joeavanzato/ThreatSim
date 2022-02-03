# ThreatSim
 Threat Simulator for Enterprise Networks

## What is it?

ThreatSim is a blue-team utility designed to simulate modern threat-actor TTPs in order to help blue-teams identify potential gaps in logging, EDR/AV controls, SIEM/UEBA detections or otherwise.  It is possible to generate both completely randomized but logical behavior as well as to simulate actual threat actors based on known procedures.

## Modular Adversary Simulation

ThreatSim works by incorporating packages based on real threat-actor activity - what commands they run, behaviors they 
invoke, techniques they utilize, etc to allow your blue-team to properly simulate real-life activity in a controlled and 
'defanged' manner.  Of course these TTPs are ever-changing and detecting ThreatSim activity for a particular threat actor should not lull your organization into a false sense of security.

## Usage

For best simulation results, ThreatSim requires running as local administrator as well as a remote host [-t/--target] - 
ThreatSim will leverage the current user context in any applicable remote techniques such as lateral movement, etc unless 
specifically given a Username and Password when invoked [-u/--user].


## Contents

* ./packages/actors/ -> YAML files containing two types of 'behaviors' for threat actors - step-based patterns choosing from a known set of TTPs and technique-based patterns where a random command that matches the ID is chosen from the available pool.
* ./packages/mitre_mappings/mappings.yml -> Automatically generated YAML file which shows all available commands on a per-technique ID basis, used for random-pool choices of commands.
* ./packages/MITRE_TACTICS -> YAML files mapping commands to MITRE Techniques/Tactics.

###Replacements Available in Command Strings

* Any Environment Variable in the format %VARNAME% is replaced by os module.
* $CURDIR$ - Replace with Current Working Directory
* $RANDOMURL$ - Replace with randomly generated DGA-style URL
* $RANDOMUSER$ - Replace with randomly generated username.
* $RANDOMDOMAINUSER$ - Replace with randomly generated domain username.
* $RANDOMPORTUNCOMMON$ - Replace with randomly generated uncommonly-used port.
* $RANDOMPORTCOMMON$ - Replace with randomly generated commonly-used port.