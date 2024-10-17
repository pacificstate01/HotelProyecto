document.addEventListener('DOMContentLoaded', function () {
    //Funcion para limpiar campos y dejar los select en el primer index la seleccion
    function limpiar_campos() {
        const inputs = document.querySelectorAll('.input');
        inputs.forEach(e => {
            e.value = '';
        });
        document.getElementById('nroDocumento').selectedIndex = 0;
        document.getElementById('Correo').selectedIndex = 0; 
        document.getElementById('Habitacion').selectedIndex = 0; 
    }
    //Funcion para guardar las reservas en localStorage
    function guardar_reservas_en_localStorage() {
        localStorage.setItem('reserva', JSON.stringify(reserva));
    }
    //Funcion para cargas las reservas del localStorage en caso de existir
    function cargar_reservas_desde_localStorage() {
        const storedReservas = localStorage.getItem('reserva');
        if (storedReservas) {
            reserva = JSON.parse(storedReservas);
        }
    }
    //Funcion para cargar en el html las reservas
    function cargar_reserva() {
      const bodyTabla = document.getElementById('ReservasTableBody');
      bodyTabla.innerHTML = '';
      reserva.forEach(function (p) {
          const tr = document.createElement('tr');
          const row = ['id', 'nro', 'email', 'hab', 'nom', 'app'];
          //Solo se muestran los primeros 4 atributos del objecto, pero los 6 estan guardados en localStorage
          row.forEach(function (i) {
              if (i !== 'nom' && i !== 'app') { 
                const td = document.createElement('td');
                td.textContent = p[i];
                tr.appendChild(td);
              }
          });

          //Se crea y se agrega un checkbox al final de la fila
          const checkboxCell = document.createElement("td");
          const checkbox = document.createElement("input");
          checkbox.type = "checkbox";
          checkboxCell.appendChild(checkbox);
          tr.appendChild(checkboxCell);

          bodyTabla.appendChild(tr);
      });
  }
    limpiar_campos();
    let reserva = [];
    cargar_reservas_desde_localStorage();
    //Valores numero documento

    const reservas = localStorage.getItem('clients');
    const nroDocumento = JSON.parse(reservas);

    const selectNro = document.getElementById('nroDocumento');
    //Se cargan en el select los numeros de documentos almacenados en localStorage
    nroDocumento.forEach(function(i){
      //Se crea un option en el select
        const option = document.createElement('option');
        //Se carga el valor de la opcion
        option.value = i.nroDocumento;
        //Se muestra en el html
        option.innerHTML = i.nroDocumento;
        selectNro.appendChild(option);
    });
    //Valores correo
    const correo =  JSON.parse(reservas);
    const selectCorreo = document.getElementById('Correo');
    correo.forEach(function(i){
        const option = document.createElement('option');
        option.value = i.correo;
        option.innerHTML = i.correo;
        selectCorreo.appendChild(option);
    });
    //El nombre y el apellido se cargan automaticamente en cuanto se seleccione el numero de documento ->
    //Al igual que el correo, pero la diferencia es en que el nombre y el apellido se almacenan en ->
    //localStorage pero no se muestran en el html
    const selectnombre = document.getElementById('nombre');
    correo.forEach(function(i){
      const option = document.createElement('option');
      option.value = i.nombre;
      selectnombre.appendChild(option);
  });

    const selectapp = document.getElementById('apellido');
    correo.forEach(function(i){
      const option = document.createElement('option');
      option.value = i.apellidos;
      selectapp.appendChild(option);
  });

    //Valores numero de habitacion
    //Al igual que el numero de documento, se cargan los numeros de habitaciones disponibles ->
    //Y se muestran en el select del html
    const hab = JSON.parse(localStorage.getItem('habs'));
   
    const selectHab = document.getElementById('Habitacion');

    hab.forEach(function(i){
        const option = document.createElement('option');
        option.value = i.nroHabitacion;
        option.innerHTML = i.nroHabitacion;
        selectHab.appendChild(option);
    });
    //Se capturan botones para el CRUD
    const addBtn = document.getElementById('btnRegistrarReserva');
    const deleteBtn = document.getElementById('deleteReservaBtn');
    const modify = document.getElementById('actualizarReserva');
    //Agregar reserva
    addBtn.addEventListener("click", function (e) {
      e.preventDefault();
      //Se capturan atributos para crear objeto
      const nro = parseInt(document.getElementById("nroDocumento").value);
      const email = document.getElementById("Correo").value;
      const hab = parseInt(document.getElementById("Habitacion").value);
      const nom = selectnombre.value;
      const app = selectapp.value;
      let id = 1;
      //En caso de que la reserva exista o la habitacion este ya ingresada no se podra hacer la reserva
      let reserve = reserva.find((e) => e.nro === nro);
      let habocu = reserva.find((e) => e.hab === hab);
      if (reserve || habocu) {
        alert("Cliente o habitacion ya ingresadas.");
      } else {
        //Se crea el objeto reserva
        if (!reserve) {
          if (!nro || !hab || !email) {
            alert("Ingrese información en todos los campos");
            return;
          } else {
            const newReserva = {
              id: reserva.length + 1,
              nro: nro,
              email: email,
              hab: hab,
              nom:nom,
              app:app 
            };
            //Se pushea al array
            reserva.push(newReserva);
            //Se guarda en localStorage
            guardar_reservas_en_localStorage();
            alert("Reserva agregada correctamente");
            cargar_reserva();
            limpiar_campos();
          }
        } else {
          reserve.id += 1;
        }
      }
    });
    //Borrar reserva
    deleteBtn.addEventListener('click',function(e){
        e.preventDefault();
        const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
        //Se borra la fila en caso de estar marcada por el checkbox
        checkboxes.forEach(function (checkbox) {
            const row = checkbox.closest("tr");
            row.remove();
            //Se filtra por numero de documento
            const nro = parseInt(row.cells[1].textContent, 10);
            reserva = reserva.filter(r => r.nro !== nro);
        });
        //Se guarda el array actualizado 
        guardar_reservas_en_localStorage();
        //Se revisa si hay habitaciones marcadas para eliminar
        if (checkboxes.length === 0) {
          alert("No se han seleccionado habitaciones");
          return;
        }else{
            alert("Habitaciones seleccionadas eliminadas");
        }
        
    });
    //Se hace un listener de evento para cuando se seleccione un numero de documento
    selectNro.addEventListener('change', function () {
        const selectedNro = parseInt(selectNro.value);
        //Se busca si existe el numero
        const selectedClient = nroDocumento.find(client => client.nroDocumento === selectedNro);
        //En caso de ser true se actualizan los valores del correo, nombre y apellido en la fila
        if (selectedClient) {
            selectCorreo.value = selectedClient.correo;
            selectnombre.value = selectedClient.nombre;
            selectapp.value = selectedClient.apellidos;
        } else {
          //De caso contrario se deja vacio 
            selectCorreo.value = '';
            selectnombre.value = '';
            selectapp.value = '';
        }
    });
    //Se cargan y muestran las reservas hechas
    cargar_reservas_desde_localStorage();
    cargar_reserva(); 
});