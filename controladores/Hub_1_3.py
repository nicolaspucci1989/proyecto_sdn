'''
Agregar flujo con ovs-ofctl add-flow s1 actions=CONTROLLER:65535

'''

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet


class Hub_1_3( app_manager.RyuApp ):
    OFP_VERSIONS = [ ofproto_v1_3.OFP_VERSION ]

    def __init__( self, *args, **kwargs ):
        super( Hub_1_3, self ).__init__( *args, **kwargs )

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def hub_features_handlers( self, ev ):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                        ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)


    def imprimirProtocolos( self, evento):
        paquete = packet.Packet( evento.msg.data )
        for p in paquete.protocols:
            print( p.protocol_name, p)
            print( "- - - - - - - - - - - - -")
        print "=================================================================="

    #ofp_event.EventOFPPacketIn
    #   que evento escuchar, PacketIn se da cuando hay table miss
    #MAIN_DISPATCHER
    #   despues de la negociacion inicial
    @set_ev_cls( ofp_event.EventOFPPacketIn, MAIN_DISPATCHER )
    def packet_in_handler( self, evento ):
        self.imprimirProtocolos( evento )
        mensaje = evento.msg #Estructura del packet_in
        dp = mensaje.datapath #Estructura que representa el switch
        ofp = dp.ofproto #Protocolo negociado entre switch y contro
        ofp_parser = dp.ofproto_parser
        puerto_entrada = mensaje.match[ 'in_port' ]

        acciones = [ ofp_parser.OFPActionOutput( ofp.OFPP_FLOOD ) ]

        out = ofp_parser.OFPPacketOut(
                    datapath=dp, buffer_id=mensaje.buffer_id,
                    in_port=puerto_entrada,
                    actions=acciones
                    )
        dp.send_msg( out )
