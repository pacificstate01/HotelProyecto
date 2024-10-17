document.addEventListener('DOMContentLoaded', function () {
    //Funcion para mostrar todos los usuarios ingresados al sistema
    function mostrar_clientes() {
        //Captura el aray de objetos llamado reserva del localStorage para mostrar uno por uno
        const clientes_storage = localStorage.getItem('reserva');
        clientes = JSON.parse(clientes_storage);
        const bodyTabla = document.getElementById('clientTableBody');
        bodyTabla.innerHTML = '';
        clientes.forEach(function (p) {
            const tr = document.createElement('tr');
            //Muestra todos los datos del usuario incluido la habitacion que hospeda
            const fila = ['nro', 'nom','app', 'email','hab']; 
            fila.forEach(function (info) {
                const td = document.createElement('td');
                td.textContent = p[info];
                tr.appendChild(td);
            });
            bodyTabla.appendChild(tr);
        });
    }
    //La pagina se actualiza automaticamente en caso de alguna adicion en el localStorage
    window.addEventListener('storage', function (e) {
        if (e.key === 'reserva') {
            mostrar_clientes();
        }
    });


    mostrar_clientes();
});
