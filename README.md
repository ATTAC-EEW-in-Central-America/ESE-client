
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

## XML Incoming Messages through ActiveMQ
There are two types of messages which are sent from the *Earthquake Early Warning System*  (server side):

 1. Common Alerting Protocol 1.2 [(CAP1.2](http://docs.oasis-open.org/emergency/cap/v1.2/CAP-v1.2.html))
 2. Heartbeat

### CAP1.2
The [documentation](https://docs.oasis-open.org/emergency/cap/v1.2/pr03/CAP-v1.2-PR03.pdf) about CAP1.2 says: *The Common Alerting Protocol (CAP) is a simple but general format for exchanging all-hazard emergency alerts and public warnings over all kinds of networks. CAP allows a consistent warning message to be disseminated simultaneously over many different warning systems, thus increasing warning effectiveness while simplifying the warning task*.
In the project *"Alerta Temprana de Terremotos de Centroamérica"* (ATTAC) there is a dissemination system that receives the CAP1.2 XML message through ActiveMQ: this is the Digital TV Channel through an interface called *eews2ewbs*. 
One example of this XML file containing information about an earthquake, in both Spanish and English, is below:
```xml
<alert xmlns="urn:oasis:names:tc:emergency:cap:1.2">
  <identifier>marn2023evgi</identifier>
  <sender>MARN</sender>
  <sent>2023-03-10T13:12:21.325421Z</sent>
  <status>Actual</status>
  <msgType>Alert</msgType>
  <scope>Private</scope>
  <info>
    <language>en-US</language>
    <category>Geo</category>
    <event>Earthquake</event>
    <urgency>Immediate</urgency>
    <severity>Unknown</severity>
    <certainty>Unknown</certainty>
    <headline>MARN/Earthquake - Magnitude 4.8, Near Coast of Guatemala</headline>
    <instruction>Drop, Cover and Hold on</instruction>
    <parameter>
      <valueName>magnitudeCreationTime</valueName>
      <value>2023-03-10T13:12:21.325421Z</value>
    </parameter>
    <parameter>
      <valueName>originTime</valueName>
      <value>2023-03-10T13:11:36.571136Z</value>
    </parameter>
    <parameter>
      <valueName>magnitude</valueName>
      <value>4.810015202</value>
    </parameter>
    <parameter>
      <valueName>latitude</valueName>
      <value>13.86451741</value>
    </parameter>
    <parameter>
      <valueName>longitude</valueName>
      <value>-91.82912431</value>
    </parameter>
    <parameter>
      <valueName>depth</valueName>
      <value>52.77099609</value>
    </parameter>
    <parameter>
      <valueName>status</valueName>
      <value> solution</value>
    </parameter>
    <area>
      <areaDesc>Near Coast of Guatemala</areaDesc>
    </area>
  </info>
  <info>
    <language>es-US</language>
    <category>Geo</category>
    <event>Sismo</event>
    <urgency>Immediata</urgency>
    <severity>Unknown</severity>
    <certainty>Unknown</certainty>
    <headline>MARN/Sismo - Magnitud 4.8, 49 km al SSE de Champerico, Guatemala</headline>
    <instruction>Mantengase alejado de ventanas y objetos que puedan caer. Vaya a un lugar seguro y cubrase.</instruction>
    <parameter>
      <valueName>magnitudeCreationTime</valueName>
      <value>2023-03-10T13:12:21.325421Z</value>
    </parameter>
    <parameter>
      <valueName>originTime</valueName>
      <value>2023-03-10T13:11:36.571136Z</value>
    </parameter>
    <parameter>
      <valueName>magnitude</valueName>
      <value>4.810015202</value>
    </parameter>
    <parameter>
      <valueName>latitude</valueName>
      <value>13.86451741</value>
    </parameter>
    <parameter>
      <valueName>longitude</valueName>
      <value>-91.82912431</value>
    </parameter>
    <parameter>
      <valueName>depth</valueName>
      <value>52.77099609</value>
    </parameter>
    <parameter>
      <valueName>status</valueName>
      <value> solution</value>
    </parameter>
    <area>
      <areaDesc>Near Coast of Guatemala</areaDesc>
    </area>
  </info>
</alert>
```
### Heartbeat
A heartbeat is sent from the server side each 5 seconds to notify the clients this is alive. It is a XML format message. An example is below:

```xml
<?xml version='1.0' encoding='UTF-8'?>
<hb originator="vssc3" sender="vssc3" xmlns="http://heartbeat.reakteu.org" timestamp="2023-03-10T20:19:02.140984Z"/>
```
It contains the system that originates the heartbeat and the sender. 
