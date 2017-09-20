# Switch Simple
## Secciones principales
 * Registro e inicializacion de la aplicacion: esto ocurre antes de que los switches sean procesados por Ryu y es usado para permitir a la instancia de la aplicacion la inicializacion de datos que seran compartidos a traves de toda la red
 * inicializacion en un switch que se conecta a Ryu: cuando un switch se conecta a Ryu durante la etapa de configuracion, la aplicacion tiene la opcion de escuchar al evento de Features Response del switch. Usualmente durante esta etapa se agregan flujos estaticos que son esperados por la aplicacion del controlador
 * Manejo de paquetes entrantes: la aplicacion del controlador puede elegir escuchar los eventos de paquetes entrantes (Packet-In), que ocurre siempre que el switch encuentra una coincidencia que indica el forwarding del paquete al controlador.
