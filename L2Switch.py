from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types

class L2Switch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(L2Switch, self).__init__(*args, **kwargs)

    #ofp_event.EventOFPPacketIn
    #   que evento escuchar
    #MAIN_DISPATCHER
    #   despues de la negociacion inicial
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handleR(self, evento):
        mensaje = evento.msg #Estructura del packet_in
        dp = mensaje.datapath #Estructura que representa el switch
        ofp = dp.ofproto #Protocolo negociado entre switch y contro
        ofp_parser = dp.ofproto_parser

        paquete = packet.Packet(mensaje.data)
        eth = paquete.get_protocol(ethernet.ethernet)

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            #Ignorar el paquete link layer discovery protocol
            return

        destino = eth.dst
        fuente = eth.src
        dpid = dp.id #Identifica switch que envio mensaje


        actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
        out = ofp_parser.OFPPacketOut(
            datapath=dp, buffer_id=mensaje.buffer_id,
            in_port=mensaje.in_port,
            actions=actions)
        dp.send_msg(out)
        self.logger.info("destino %s fuente %s puerto %s dpid %s",
                destino, fuente, mensaje. in_port, dpid)

