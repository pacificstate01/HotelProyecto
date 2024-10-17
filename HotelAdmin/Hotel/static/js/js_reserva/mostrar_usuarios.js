document.addEventListener('DOMContentLoaded', function () {
    //Funcion para mostrar los usuarios creados activos para la reserva
    function mostrar_usuarios(){
        const clients_guardados= localStorage.getItem('clients');
        let clientes = JSON.parse(clients_guardados);
        const bodyTabla = document.getElementById('clientTableBody');
        bodyTabla.innerHTML = '';
        clientes.forEach(function (p) {
            const tr = document.createElement('tr');

            const fila = ['nroDocumento','nombre', 'apellidos', 'correo'];
            fila.forEach(function (info) {
                const td = document.createElement('td');
                td.textContent = p[info];
                tr.appendChild(td);
            });
            bodyTabla.appendChild(tr);
        });

    }
    //Se actualiza la tabla a traves de algun cambio en localStorage
    window.addEventListener('storage', function (e) {
        if (e.key === 'clients') {
            mostrar_usuarios();
        }
    });
    mostrar_usuarios();
});