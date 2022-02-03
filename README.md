# ThreatSim
 Threat Simulator for Enterprise Networks

## Modular Adversary Simulation

ThreatSim works by incorporating packages based on real threat-actor activity - what commands they run, behaviors they 
invoke, techniques they utilize, etc to allow your blue-team to properly simulate real-life activity in a controller and 
'defanged' manner.  

## Usage

For best simulation results, ThreatSim requires running as local administrator as well as a remote host [-t/--target] - 
ThreatSim will leverage the current user context in any applicable remote techniques such as lateral movement, etc unless 
specifically given a Username and Password when invoked [-u/--user].



commands.yml -> Contains MITRE mapped commands
actor_patterns.yml -> Sequences of commands by ID associated with threat actors, referencing commands.yml

REPLACEMENTS in Command Strings

$CURDIR$