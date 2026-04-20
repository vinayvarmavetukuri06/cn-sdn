# SDN Mininet Project: Link Failure Detection (Orange Problem)

## 🎯 Goal
This project demonstrates an SDN-based solution using Mininet and the Ryu controller to monitor network topology, detect link failures via OpenFlow, and manage flow rules dynamically.

## 🏗️ Topology
- **Controller:** Ryu (Remote)
- **Switches:** 2 Open vSwitch (OVS) instances (s1, s2)
- **Hosts:** 2 Hosts (h1, h2)
- **Connectivity:** h1 -- s1 -- s2 -- h2

## 🛠️ Implementation Details
- **Controller Logic:** The script `my_controller.py` handles:
  - `EventOFPPacketIn`: For learning MAC addresses and installing flow rules.
  - `EventOFPSwitchFeatures`: To set the default table-miss entry.
  - `EventOFPPortStatus`: To detect when a link goes down or up.
- **Match-Action:** Rules match based on `in_port` and `eth_dst` to forward packets efficiently.

## 🧪 Test Scenarios

### Scenario 1: Normal Forwarding (Control Plane Delay)
1. Start the controller and topology.
2. Run `h1 ping h2`. 
3. **Observation:** The first ping has a higher latency (~7ms) because the switch must communicate with the controller. Subsequent pings are faster (~0.1ms) as they match the flow table rules.

### Scenario 2: Link Failure Detection
1. Run a continuous ping or multiple pings.
2. Execute `link s1 s2 down` in Mininet.
3. **Observation:** The Ryu controller terminal immediately prints an "ALERT: Link Failure" message. This proves the controller is monitoring the network state in real-time.

## 🚀 How to Run
1. Start the controller: `python3 run_ryu.py`
2. Start the topology: `sudo mn --custom topo.py --topo orangetopo --controller remote`
3. Check flow rules: `sh ovs-ofctl dump-flows s1 -O OpenFlow13`




1. File Setup
Bash
# Edit your controller
nano my_controller.py

# Edit your topology
nano topo.py

# Edit your launcher (with the compatibility patches)
nano run_ryu.py





2. Execution (Open two terminal windows)
Terminal 1 (Ryu):

Bash
source ryu_env/bin/activate
python3 run_ryu.py

Terminal 2 (Mininet):

Bash
sudo mn --custom topo.py --topo orangetopo --controller remote





3. Testing in Mininet CLI
Bash
# Check connectivity
mininet> h1 ping h2 -c 5

# Inspect Flow Tables (The "Match-Action" proof)
mininet> sh ovs-ofctl dump-flows s1 -O OpenFlow13

# Fail the link (The "Failure Detection" proof)
mininet> link s1 s2 down

# Exit Mininet
mininet> exit
# Clean up (Run this if Mininet crashes)
sudo mn -c






💡 Part 3: Clear Explanation (The "Why")
1. How Packet Forwarding Works (Scenario 1)
SDN switches are "dumb" by default. When h1 sends a packet to h2, Switch 1 has no idea what to do. It triggers a Packet-In event, sending the packet header to Ryu. Ryu looks at the MAC address, decides which port it should go out of, and sends a Flow-Mod message back to the switch. The switch now has a "rule" and doesn't need to ask the controller for the next packet.

2. How Link Failure is Detected (Scenario 2)
In a traditional network, a switch would use a protocol like STP (Spanning Tree) to find a new path, which is slow. In SDN, the switch detects the physical link loss and sends an OFP_PORT_STATUS message to the controller. Because the controller has a "Global View" of the network, it can instantly see the failure and (in a larger network) reroute traffic through a different path.

3. Match-Action Explained
Your project demonstrates the core of OpenFlow:

Match: "Is this packet coming from Port 1 and going to h2's MAC address?"

Action: "If yes, send it out of Port 2."

This allows the network to be programmed like software, rather than configured manually on every device.

You are now fully prepared to submit! Just remember to include your screenshots of the pings and flow tables in your GitHub report.
