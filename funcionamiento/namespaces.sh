# crear namespaces
ip netns add red
ip netns add green

# crear switch
ovs-vsctl add-br OVS1

# crear interface virtual ethernet
ip link add eth0-r type veth peer name veth-r
# conectamos un extremo al namspace
ip link set eth0-r netns red
# conectamos el otro extremo al switch
ovs-vsctl add-port OVS1 veth-r

# repetimos para el otro namespace
ip link add eth0-g type veth peer name veth-g
ip link set eth0-g netns green
ovs-vsctl add-port OVS1 veth-g

# Levantar interfaces y asignar direcciones
ip link set veth-r up
ip netns exec red ip link set dev lo up
ip netns exec red ip link set dev eth0-r up
ip netns exec red ip address add 10.0.0.1/24 dev eth0-r
ip link set dev veth-g up
ip netns exec green ip link set dev lo up
ip netns exec green ip link set dev eth0-g up

# setear MAC
ip netns exec red ip link set eth0-r address 00:00:00:00:00:01
ip netns exec green ip link set eth0-g address 00:00:00:00:00:02

# ping
ip netns exec green ip address add 10.0.0.2/24 dev eth0-g
