# ESE-client
Receives xml messages from Earthquake Early Warning from [ESE](https://docs.gempa.de/sed-eew/current/seiscomp/share/doc/eew/html/index.html) via [activeMQ and the sceewlog ESE module](https://docs.gempa.de/sed-eew/current/seiscomp/share/doc/eew/html/apps/sceewlog.html). In order to receive xml messages from an ESE server, one needs to request appropriate access and permissions to the relevant EEW system operator. 

## Install dependencies
```shell
conda create -n stomp stomp.py
conda activate stomp
```

## Clone and create `useraction.py`
Copy `useractions-template.py` to `useractions.py`. `useractions-template.py` is just an example. `useractions.py` is actually imported in the main client module and used for message processing. 
```shell
git pull https://github.com/ATTAC-EEW-in-Central-America/ESE-client
cp ESE-client/useractions-template.py ESE-client/useractions.py
```

## Receive continously
`./main.py -h` should provide all required informations for appropriate usage, e.g.:
```shell
./main.py -H <hostname> -u <user> -p <password> -P <port> -t <topic> -c receiver
```

## Implement user action
You might implement your own functionalities in response to an [ESE xml alert](https://docs.gempa.de/sed-eew/current/seiscomp/share/doc/eew/html/apps/sceewlog.html#description) in `useractions.respond()` (initially a copy of `useractions-template.respond()`). You might also implement response to heartbeat (sent every 5 seconds) in `useractions.respond_heartbeat()` (initially a copy of `useractions-template.respond_heartbeat()`).

## Maintain
Updates can be provided to this client. To get the latest version, open a terminal in the client folder and run:
```shell
git pull
```
> No update will be provided for your `useractions.py` they will only be suggested in `useractions-template.py`. Consider new features added to `useractions-template.py` for implementation in your `useractions.py`. 
