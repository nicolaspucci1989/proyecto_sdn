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
