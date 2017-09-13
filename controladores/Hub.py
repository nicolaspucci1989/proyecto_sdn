from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0


class Hub( app_manager.RyuApp ):
    OFP_VERSIONS = [ ofproto_v1_0.OFP_VERSION ]

    def __init__( self, *args, **kwargs ):
        super( Hub, self ).__init__( *args, **kwargs )

    #ofp_event.EventOFPPacketIn
    #   que evento escuchar
    #MAIN_DISPATCHER
    #   despues de la negociacion inicial
    @set_ev_cls( ofp_event.EventOFPPacketIn, MAIN_DISPATCHER )
    def packet_in_handleR( self, evento ):
        mensaje = evento.msg #Estructura del packet_in
        dp = mensaje.datapath #Estructura que representa el switch
        ofp = dp.ofproto #Protocolo negociado entre switch y contro
        ofp_parser = dp.ofproto_parser
        puerto_entrada = mensaje.in_port

        acciones = [ ofp_parser.OFPActionOutput( ofp.OFPP_FLOOD ) ]

        out = ofp_parser.OFPPacketOut(
                    datapath=dp, buffer_id=mensaje.buffer_id,
                    in_port=puerto_entrada,
                    actions=acciones
                    )
        dp.send_msg( out )
