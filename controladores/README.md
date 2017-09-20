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
