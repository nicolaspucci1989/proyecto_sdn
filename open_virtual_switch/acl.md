ovs-vsctl add-br br0 -- set Bridge br0 fail-mode=secure
for i in 1 2 3 4; do
    ovs-vsctl add-port br0 p$i -- set Interface p$i ofport_request=$i
    ovs-ofctl mod-port br0 p$i up
done
ovs-ofctl add-flow br0 \
    "table=0, dl_src=01:00:00:00:00:00/01:00:00:00:00:00, actions=drop"
ovs-ofctl add-flow br0 \
    "table=0, dl_dst=01:80:c2:00:00:00/ff:ff:ff:ff:ff:f0, actions=drop"
ovs-ofctl add-flow br0 "table=0, priority=0, actions=resubmit(,1)"


test tabla 0
ovs-appctl ofproto/trace br0 in_port=1,dl_dst=01:80:c2:00:00:05

ovs-appctl ofproto/trace br0 in_port=1,dl_dst=01:80:c2:00:00:10


implementar procesamiento de vlans
ovs-ofctl add-flow br0 "table=1, priority=0, actions=drop"

ovs-ofctl add-flow br0 \
    "table=1, priority=99, in_port=1, actions=resubmit(,2)"
ovs-ofctl add-flows br0 - <<'EOF'
table=1, priority=99, in_port=2, vlan_tci=0, actions=mod_vlan_vid:20, resubmit(,2)
table=1, priority=99, in_port=3, vlan_tci=0, actions=mod_vlan_vid:30, resubmit(,2)
table=1, priority=99, in_port=4, vlan_tci=0, actions=mod_vlan_vid:30, resubmit(,2)
