document.addEventListener('DOMContentLoaded', function () {
    //Funcion para actualizar dashboard del index
    function actualizarDashboard(){
        //Se cargan las habitaciones guardadas
        const Habs_guardadas= localStorage.getItem('habs');

        let habs = JSON.parse(Habs_guardadas);
        //Se actualiza la cantidad de habitaciones como tambien cuantas se ->
        //Encuentran en otro estado, ya sea disponible, ocupada o en limpieza
        //A traves de filtros donde se crean arreglos con el largo de los tipos de estados activos
        const total = habs.length;
        const disponibles = habs.filter(hab => hab.estadoHab === 'Disponible').length;
        const ocupadas = habs.filter(hab => hab.estadoHab === 'Ocupada').length;
        const limpieza = habs.filter(hab => hab.estadoHab === 'Limpieza').length;
        //Se cambian los valores en el html
        document.getElementById('totalHab').textContent = total;
        document.getElementById('disponibleHab').textContent = disponibles;
        document.getElementById('ocupadaHab').textContent = ocupadas;
        document.getElementById('limpiezaHab').textContent = limpieza;

    }
    //Se actualiza el dashboard en caso de algun cambio en el localStorage
    window.addEventListener('storage', function (e) {
        if (e.key === 'habs') {
            actualizarDashboard();
        }
    });
    actualizarDashboard();

} );