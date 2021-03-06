from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types

class Hub(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(Hub, self).__init__(*args, **kwargs)

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
        puerto_entrada = mensaje.in_port

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            #Ignorar el paquete link layer discovery protocol
            return

        destino = eth.dst
        fuente = eth.src
        dpid = dp.id #Identifica switch que envio mensaje


        acciones = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
        match = ofp_parser.OFPMatch(
                in_port=1
                )
        if 'ipv4_src' in match:
            print ("hay match")
            print match['ipv4_src']

        out = ofp_parser.OFPPacketOut(
            datapath=dp, buffer_id=mensaje.buffer_id,
            in_port=puerto_entrada,
            actions=acciones)
        dp.send_msg(out)
        '''
        self.logger.info("destino %s fuente %s puerto %s dpid %s",
                destino, fuente, puerto_entrada, dpid)
        '''
        if destino == '00:00:00:00:00:01':
            self.logger.info('destino host 1')

        if destino == '00:00:00:00:00:02':
            self.logger.info('destino host 2')

