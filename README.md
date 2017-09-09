### Trabajos a realizar
1. Que el grupo conozca el software y los rudimentos del uso de SDN
2. Armar maqueta con una red virtual para poder realizar diferentes pruebas. (mininet)
   * 3 switches en cascada (FETH)
   * 1 controlador
   * 1 servidor
   * 1 PC
3. Correr ejercicios, realizar pruebas y obtener resultados
   * Prueba de conectividad entre los nodos
      * Ping
      * Trafico
      * Falla
      * Redundancia
   * Implementacion de SDN
     * Uso sin configurar
     * Configurar Switches como HUBS
     * Configurar Switches como Switches
     * Configurar Switches como Routers
     * Medir performace de cada configuracion

#### Software Necesario
1. Sistema operativo Linux.
2. Mininet.
    Instalacion:
    ```bash
    git clone git://github.com/mininet/mininet
    mininet/util/install.sh -a
    ```
    Test funcionalidad basica:
    ```bash
    sudo mn --test pingall
    ```
3. Ryu.

