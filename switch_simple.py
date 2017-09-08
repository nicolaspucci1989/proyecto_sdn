from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
 #from ryu.ofproto import ofproto_v1_3

class SimpleHub(app_manager.RyuApp):
    #En version 1.0, si hay un table miss la accion por defecto es enviarla al controlador
    #En version 1.3, si hay un table miss la accion por defecto es dropearlo


    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]
    #OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]


    def __init__(self, *args, **kwargs):
        super(SimpleHub, self).__init__(*args, **kwargs)

    #Decorador del event handler, toma dos argumentos. El primero indica que evento invocara a la
    #funcion. El segundo indica el estado del switch
    #En este caso estamos invocando la funcion cuando hay un evento "Switch Features"; CONFIG_DISPATCHER
    #significa que el switch esta en la fase de negociacion de version y envio del mensaje de
    #"features-request"
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        message = ev.msg
        print("message: ", message)


    #MAIN_DISPATCHER indica que la funcion debe ser llamada despues que la negociacion de features
    #se haya completado
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        print("ev message: ", ev.msg)

        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        out = parser.OFPPacketOut(
                datapath=datapath,
                buffer_id=msg.buffer_id,
                in_port=msg.in_port,
                actions=actions)
        datapath.send_msg(out)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                            actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)

        datapath.send_msg(mod)
