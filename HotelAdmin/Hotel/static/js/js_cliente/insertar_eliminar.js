document.addEventListener("DOMContentLoaded", function () {
  
  let clients = [];

  function validar_input(id) {
    const inpt = document.getElementById(id);
    if (inpt.value.trim() === "") {
      console.log("Campos vacios");
      return;
    }
    return inpt.value.trim();
  }

 
  function validarEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  }

  
  function validar_nombre(nombre) {
    return nombre.trim().length > 0;
  }

  
  function validar_apellido(apellidos) {
    return apellidos.trim().length > 0;
  }

  function limpiar_campos() {
    const inputs = document.querySelectorAll('.input');
    inputs.forEach(e => {
        e.value = '';
    });
    document.getElementById("NuevoCorreo").value = "";
    document.getElementById("NuevoNombre").value = "";
    document.getElementById("NuevoApellido").value = "";
}
  //Funcion para cargar clientes en el html
  function cargar_cliente() {
    const bodyTabla = document.getElementById("clientTableBody");
    bodyTabla.innerHTML = "";

    clients.forEach(function (client) {
      const tr = document.createElement("tr");
      const row =["nroDocumento", "tipoDocumento", "nombre", "apellidos", "correo"];
      row.forEach(function (info) {
        const td = document.createElement("td");
        td.textContent = client[info];
        tr.appendChild(td);
      }); 
      //Se crea un checkbox al final de cada fila para marcar
      const checkboxCell = document.createElement("td");
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      //Se crean atributos adicionales al checkbox marcado del cliente seleccionado
      checkbox.dataset.correo = client.correo;
      checkbox.dataset.nombre = client.nombre;
      checkbox.dataset.apellidos = client.apellidos;
      checkboxCell.appendChild(checkbox);
      tr.appendChild(checkboxCell);

      bodyTabla.appendChild(tr);
    });
  }

  //Se captura boton para agregar cliente
  const btn = document.getElementById("btnRegistrarCliente");
  btn.addEventListener("click", function (event) {
    event.preventDefault();

    const nd = parseInt(validar_input("nroDocumento"));
    const td = validar_input("tipoDocumento");
    const nom = validar_input("nombres");
    const app = validar_input("apellidos");
    const co = validar_input("correo");

    if (!validarEmail(co)) {
      alert("Correo electrónico inválido");
      return;
    }
    //Se verifica si ya esta ingresado (existe) el cliente a traves del numero de documento
    const existingClient = clients.find((e) => e.nroDocumento === nd);

    if (!nd || !td || !nom || !app || !co) {
      alert("Ingrese información en todos los campos");
      return;
    } else {
      if (existingClient) {
        alert("El cliente ya existe");
      } else {
        const newClient = {
          nroDocumento: nd,
          tipoDocumento: td,
          nombre: nom,
          apellidos: app,
          correo: co,
        };
        //Se pushea al array clients y se almacena en localStorage
        clients.push(newClient);
        localStorage.setItem("clients", JSON.stringify(clients));

        alert("Cliente agregado correctamente");
        cargar_cliente();
        limpiar_campos();
      }
    }
  });

  //Captura el boton eliminar cliente
  const deleteBtn = document.getElementById("deleteClientBtn");
  deleteBtn.addEventListener("click", function () {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    checkboxes.forEach(function (checkbox) {
      const row = checkbox.closest("tr");
      row.remove();
      //Se almacena el numero de documento ubicado en el primer index del row ->
      //Con este numero se filtra el array creando uno nuevo sin ese cliente con ese nro de documento
      const nroDocumento = parseInt(row.cells[0].textContent, 10);
      clients = clients.filter((client) => client.nroDocumento !== nroDocumento);
    });
    //Se actualiza el localStorage
    localStorage.setItem("clients", JSON.stringify(clients));

    if (checkboxes.length === 0) {
      alert("No se han seleccionado clientes");
    } else {
      alert("Clientes seleccionados eliminados");
    }
  });

  //Se captura el boton actualizar(azul) y verifica que haya un checkbox marcado para mostrar el modal
  const actualizarBtn = document.getElementById("actualizarBtn");
  actualizarBtn.addEventListener("click", function () {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    if (checkboxes.length !== 1) {
      alert("Seleccione solo 1 cliente para modificar");
      return;
    }
    $("#myModal").modal("show");
  });

  //Se captura el boton modificar (dentro del modal) y los nuevos valores ingresados
  const modifyBtn = document.getElementById("modifyBtn");
  modifyBtn.addEventListener("click", function () {
    const newEmail = document.getElementById("NuevoCorreo").value;
    const newName = document.getElementById("NuevoNombre").value;
    const newApp = document.getElementById("NuevoApellido").value;
    const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');

    if (checkboxes.length !== 1) {
      alert("Seleccione solo 1 cliente para modificar");
      return;
    }
    //Se almacena el checkbox marcado y se captura el correo asociado del dataset del checkbox 
    const checkSelected = checkboxes[0];
    const currentEmail = checkSelected.dataset.correo;

    if (!validarEmail(newEmail)) {
      alert("Correo electrónico inválido");
      return;
    }

    if (!validar_nombre(newName) || !validar_apellido(newApp)) {
      alert("No pueden haber campos vacíos");
      return;
    }
    //Se actualizan los datos en funcion de que el correo del checkbox sea igual al correo actual ->
    //Y Se hace el cambio para el correo nuevo, nombre y apellido
    clients.forEach(function (client) {
      if (client.correo === currentEmail) {
        client.correo = newEmail;
        client.nombre = newName;
        client.apellidos = newApp;
      }
    });
    //Se actualiza el localStorage, se muestra en el html y se esconde el modal
    localStorage.setItem("clients", JSON.stringify(clients));
    cargar_cliente();
    $("#myModal").modal("hide");
    alert("La información se ha actualizado correctamente");
  });

  //Si existe un array clients en localStorage se parsea y se muestra en el html
  if (localStorage.getItem('clients')) {
    clients = JSON.parse(localStorage.getItem('clients'));
    cargar_cliente(); 
  }

  //Se limpian los inputs del modal cuando se esconde
  $("#myModal").on("hidden.bs.modal", function () {
    limpiar_campos();
  });
});
