document.addEventListener('DOMContentLoaded', function() {
    console.log("login.js is loaded");
   //Array con datos de usuario para login, actua como una "base de datos"
    const users = [
        {username: "andrecollao@gmail.com", password: "12345678"},
        {username: "benjazu@gmail.com", password: "987654321"},
        {username: "javierota@gmail.com", password: "01010101"}
    ];

    //Valida si los datos ingresados estand entro del array
    function credenciales(username,password){
        for(const user of users){
            if(user.username === username && user.password === password){
                return true;
            }
        }
        return false;
    }


    //En caso de que todo este correcto, al apretar el boton ingresar redirecciona a la pagina principal
    document.querySelector('#boton').addEventListener('click', function(event) {
        event.preventDefault();
        const username = document.getElementById("correo").value;
        const password = document.getElementById("contraseña").value;

        if(credenciales(username,password)){
            //Se guarda el usuario que ingreso en localStorage
            localStorage.setItem('loggedInUser', username);
            Swal.fire({
                title: 'Datos ingresados correctamente',
                icon: 'success',
                timer: 1500,
                showConfirmButton: false
            }).then(() => {
                window.location.replace("/Hotel/menu/"); 
            });
        }
        else{
            Swal.fire({
                title: 'Datos incorrectos',
                text: 'Vuelva a intentar',
                icon: 'error',
                confirmButtonText: 'OK'
            })
        }
    });
});
