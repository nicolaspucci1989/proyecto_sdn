# Switch Simple
## Secciones principales
 * __Registro e inicializacion de la aplicacion:__ esto ocurre antes de que los switches sean procesados por Ryu y es usado para permitir a la instancia de la aplicacion la inicializacion de datos que seran compartidos a traves de toda la red
 * __inicializacion en un switch que se conecta a Ryu:__ cuando un switch se conecta a Ryu durante la etapa de configuracion, la aplicacion tiene la opcion de escuchar al evento de Features Response del switch. Usualmente durante esta etapa se agregan flujos estaticos que son esperados por la aplicacion del controlador
 * __Manejo de paquetes entrantes:__ la aplicacion del controlador puede elegir escuchar los eventos de paquetes entrantes (Packet-In), que ocurre siempre que el switch encuentra una coincidencia que indica el forwarding del paquete al controlador.

## Responsabilidades del controlador
 * Cuando un switch se registra al controlador
   * Se agrega un flujo catch-all de baja prioridad indicando al switch que envie cualquier paquete recibido.
   * Se crea una tabla MAC-puerto para este switch en particular.
 * Cuando el switch envia un mensaje Packet-In.
   * Se agrega una entrada a la tabla MAC-puerto que asigna la MAC origen al puerto que recibe.
   * Se busca la MAC destino el la tabla MAC-puerto
     * Si no se encuentra se fija el puerto destino como FLOOD.
     * Si se encuentra.
       * Se fija el puerto destino al puerto asociado con la direccion MAC.
       * Se agrega un flujo al switch (con una prioridad mas alta que el catch-all) que esta asociada al puerto de entrada y a la direccion MAC. Esto previene la llegada de mensajes Packet-In adicionales al controlador para el mismo puerto y para la misma direccion MAC de destino, pero permite al controlador aprender mas direcciones MAC si el paquete llega al mismo puerto pero con una direccion MAC de destino distinta.
    * Se envia una mensaje PacketOut al switch indicandole que envie el paquete actual al puerto encontrado en la tabla o realizar un flood.

## Registro e inicializacion de la aplicacion
La primera seccion crea la aplicacion de ryu, especifica que version del protocolo OpenFlow con la que es compatible el controlador, e inicializa la tabla MAC-puerto.
``` python
class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
```

## Manejador de eventos para switches nuevos
Se define un metodo y se lo registra para que escuche cualquier evento del tipo `ryu.controller.ofp_event.EventOFPSwitchFeatures`. El principal proposito de esta seccion es que se ejecute siempre que se agrega un switch al controlador y se instala un flujo catch-all, lo que permite al switch enviar paquetes al controlador.
``` python
@set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
def switch_features_handler(self, ev):
    datapath = ev.msg.datapath
    ofproto = datapath.ofproto
    parser = datapath.ofproto_parser

    # install table-miss flow entry
    #
    # We specify NO BUFFER to max_len of the output action due to
    # OVS bug. At this moment, if we specify a lesser number, e.g.,
    # 128, OVS will send Packet-In with invalid buffer_id and
    # truncated packet data. In that case, we cannot output packets
    # correctly.  The bug has been fixed in OVS v2.1.0.
    match = parser.OFPMatch()
    actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                      ofproto.OFPCML_NO_BUFFER)]
    self.add_flow(datapath, 0, match, actions)
```
## Aprender la direccion MAC y el puerto asociado
Si no existe se crea la tabla MAC-puerto para el DPID del switch actual. Se loggea la informacion y se actualiza la tabla MAC-puerto con la direccion fuente del paquete asociado y el puerto al cual llego.
``` python
dpid = datapath.id
self.mac_to_port.setdefault(dpid, {})

self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

# Aprender la direccion mac para evitar el FLOOD
self.mac_to_port[dpid][src] = in_port
```

## Busqueda MAC-puerto y destino del paquete
Se checkea la tabla MAC-puerto asociada al switch para comprobar si ya se aprendio la direccion MAC. Si ese es el caso, se setea el puerto de salida al puerto aprendido, en caso contrario se setea a flood.
``` python
if dst in self.mac_to_port[dpid]:
    out_port = self.mac_to_port[dpid][dst]
else:
    out_port = ofproto.OFPP_FLOOD

actions = [parser.OFPActionOutput(out_port)]
```

## Agregar una entrada de flujo para el destino aprendido
Si se encontrol a direccion mac en la tabla MAC-puerto, se agrega un flujo al switch para asegurarse que los proximos paquetes del mismo puerto a la misma direccion sean enviados sin intervension del controlador.
``` python
# instalar flujo para evitar proximos packet_in
if out_port != ofproto.OFPP_FLOOD:
    match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
    # verificar si hay un buffer_id valido, si es valido evitar enviar
    # ambos flow_mod & packet_out
    if msg.buffer_id != ofproto.OFP_NO_BUFFER:
        self.add_flow(datapath, 1, match, actions, msg.buffer_id)
        return
    else:
        self.add_flow(datapath, 1, match, actions)
```

## Forwardear el paquete enviado al controlador
Una vez seteado el destino se le indica al switch que envie el paqeute que fue recibido por el controlador asi el paquete no se pierde durante el proceso de aprendizaje.
``` python
data = None
if msg.buffer_id == ofproto.OFP_NO_BUFFER:
    data = msg.data

out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                          in_port=in_port, actions=actions, data=data)
datapath.send_msg(out)
```
