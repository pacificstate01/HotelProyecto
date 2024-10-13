//Array con datos de usuario para login, actua como una "base de datos"
const users = [
    {username: "andrecollao@gmail.com", password: "12345678"},
    {username: "benjazu@gmail.com", password: "987654321"},
    {username: "javierota@gmail.com", password: "01010101"}
];

//Valida si los datos ingresados estand entro del array
function credenciales(usermane,password){
    for(const user of users){
        if(user.username === usermane && user.password === password){
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
        window.location.replace("/Hotel/menu/");
        alert("datos validos");
    }
    else{
        alert("datos no validos");
        return;
    }

});
