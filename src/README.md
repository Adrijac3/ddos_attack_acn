## Environment Set-Up Guidelines

### Ubuntu/Windows/MacOS Operating System
The experiments were carried out in MacOS BigSur 11.6 and Ubuntu 20.04

### Mininet set-up
* Mininet can be downloaded from "http:://mininet.org/download"

### POX controller
* Depending upon the type of mininet installation, the pox controller will either be pre-installed with it, or can be done by typing following commands:
  * `$ git clone http://github.com/noxrepo/pox`
  * `$ cd pox`

### Python3
* If python3 is not present, it can be installed by typing following command:
  * `$ sudo apt-get install python3`

### Scapy
* If scapy is not present, it can be installed by typing the following command:
  * `$ sudo apt-get install python3-scapy"

### xterm
* If xterm is not present, it can be installed by typing the following command:
  * `$ sudo apt-get install xterm`

## Procedure to Perform the Experiment

* There are two python scripts present in the src folder, named **spoofing.py** and **l3_modified.py**
* The script **l3_modified.py** is suggested be placed in the folder *~/pox/pox/forwarding* (or remember to put it in ~/pox/ext and run via `./pox.py l3_editing`)
* The script **spoofing.py** is suggested to be placed in the folder *~/mininet/custom* (or remember to provide correct path while its execution)

### Start remote controller POX in one terminal
* `$ cd pox`
* $ ./pox.py forwarding.l3_modified

### launch an emulated network topology using mininet in another terminal
*`$sudo mn --topo tree,depth=2,fanout=8 --controller=remote,ip=127.0.0.1`
### launch xterm for 4 hosts
* `mininet> xterm h1 h2 h3 h4`
#### Test normal traffic
* In the xterm window of h1, we first analyze the normal traffic by running the spoofing.py script as follows:
  * `python3 ~/mininet/custom/spoofing.py normal --min 2 --max 64`. (the min= minimum number of hosts, max = maximum number of hosts. We have taken packet window size of 50, so it is advised to take maximum > 50)
  * This generates spoofed IP addresses as source IP and randomly selects host IP addresses as destination IP.
  * This way, we ensure packets are uniformly distributed during normal traffic simulation, and also spoofed IP addresses will be sent to controller due to no match in switch's entry tables
 * We look at the entropy of window size = 50 packets for a total of 1000 packets sent, and observe the minimum value of entropy and set it as threshold for normal traffic flow.
#### Create script to store tcpdump before DDOS attack
* On xterm of h4, we enter:
  * `script h4.txt`
  * `tcpdump -v`
#### Launch DDOS attack
* in xterm of h1, we re-run `python3 ~/mininet/custom/spoofing.py normal --min 2 --max 64` to simulate normal traffic flow
* Parallely from h2 and h3, we launch ddos attack by run spoofing.py in attack mode i.e, tragetting only one particular host IP (here, h4) as destination IP:
  * `python3 ~/mininet/custom/spoofing.py attack --dest 10.0.0.4`

* We notice this makes the entropy value drop below threshold. We test for a consecutive 10 windows and if the low entropy persists, it means there has been a ddos attack.

### Exiting the environment
* To close tcpdump, we press `ctrl + c`
* To exit mininet we type: `mininet> exit`
* To clear existing network connections, we type: `$ sudo mn -c`
