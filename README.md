# ESE-client

## Install dependencies
```
conda create -n stomp stomp.py
conda activate stomp
```

## Receive continously
```
./main.py -H <hostname> -u <user> -p <password> -P <port> -t <topic> -c receiver
```

## Implement user action
In order to respond to each message received with automatic actions, the user should implement required functionalities in  `useractions.py` in function: 
- `respond()` for all messages but heartbeats.
- `respond_heartbeat()` for all heartbeats.