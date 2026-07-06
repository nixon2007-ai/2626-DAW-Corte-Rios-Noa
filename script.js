// ================================
// MAR & SELVA GASTROBAR
// script.js
// ================================

document.addEventListener("DOMContentLoaded", () => {

    // ================================
    // 1. Scroll suave del menú
    // ================================

    const enlaces = document.querySelectorAll('a[href^="#"]');

    enlaces.forEach(enlace => {

        enlace.addEventListener("click", function(e){

            const destino = document.querySelector(this.getAttribute("href"));

            if(destino){

                e.preventDefault();

                destino.scrollIntoView({
                    behavior:"smooth"
                });

            }

        });

    });

    // ================================
    // 2. Cambiar color del navbar
    // ================================

    const navbar = document.querySelector(".navbar");

    window.addEventListener("scroll", ()=>{

        if(window.scrollY > 100){

            navbar.classList.add("shadow");

        }else{

            navbar.classList.remove("shadow");

        }

    });
/*
    // ================================
    // 3. Animación de tarjetas
    // ================================

    const tarjetas = document.querySelectorAll(".card");

    tarjetas.forEach((card, index)=>{

        card.style.opacity = "40";
        card.style.transform = "translateY(40px)";

        setTimeout(()=>{

            card.style.transition = "0.8s";

            card.style.opacity = "1";
            card.style.transform = "translateY(0)";

        }, index * 200);

    }); 
*/

    // ================================
    // 4. Validación del formulario
    // ================================

    const formulario = document.querySelector("form");

    formulario.addEventListener("submit",(e)=>{

        e.preventDefault();

        const nombre = formulario.Nombre.value.trim();
        const correo = formulario.Correo.value.trim();
        const asunto = formulario.Asunto.value.trim();
        const mensaje = formulario.Mensaje.value.trim();

        if(nombre==="" || correo==="" || asunto==="" || mensaje===""){

            alert("Complete todos los campos.");

            return;

        }

        alert("Gracias por contactarnos.\nSu mensaje fue enviado correctamente.");

        formulario.reset();

    });

});
// ================================
// Botón volver arriba
// ================================

const boton = document.getElementById("btnArriba");

window.addEventListener("scroll",()=>{

    if(window.scrollY > 300){

        boton.style.display="block";

    }else{

        boton.style.display="none";

    }

});

boton.addEventListener("click",()=>{

    window.scrollTo({

        top:0,
        behavior:"smooth"

    });

});

const formulario = document.getElementById("formContacto");
const nombre = document.getElementById("nombre");
const correo = document.getElementById("correo");
const asunto = document.getElementById("asunto");
const mensaje = document.getElementById("mensaje");
const categoria = document.getElementById("categoria");

const contador = document.getElementById("contador");
const listaRegistros = document.getElementById("listaRegistros");
const mensajeGeneral = document.getElementById("mensajeGeneral");

let registros = [];
function validarNombre(){

    if(nombre.value.trim().length < 3){

        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");

        document.getElementById("errorNombre").textContent =
        "Mínimo 3 caracteres";

        return false;
    }

    nombre.classList.add("is-valid");
    nombre.classList.remove("is-invalid");

    document.getElementById("errorNombre").textContent = "";

    return true;
}
function validarCorreo(){

    let expresion = /\S+@\S+\.\S+/;

    if(!expresion.test(correo.value)){

        correo.classList.add("is-invalid");
        correo.classList.remove("is-valid");

        document.getElementById("errorCorreo").textContent =
        "Correo inválido";

        return false;
    }

    correo.classList.add("is-valid");
    correo.classList.remove("is-invalid");

    document.getElementById("errorCorreo").textContent = "";

    return true;
}
function validarAsunto(){

    if(asunto.value.trim().length < 5){

        asunto.classList.add("is-invalid");
        asunto.classList.remove("is-valid");

        document.getElementById("errorAsunto").textContent =
        "Mínimo 5 caracteres";

        return false;
    }

    asunto.classList.add("is-valid");
    asunto.classList.remove("is-invalid");

    document.getElementById("errorAsunto").textContent = "";

    return true;
}
function validarMensaje(){

    if(mensaje.value.trim().length < 10){

        mensaje.classList.add("is-invalid");
        mensaje.classList.remove("is-valid");

        document.getElementById("errorMensaje").textContent =
        "Mínimo 10 caracteres";

        return false;
    }

    mensaje.classList.add("is-valid");
    mensaje.classList.remove("is-invalid");

    document.getElementById("errorMensaje").textContent = "";

    return true;
}
function validarCategoria(){

    if(categoria.value===""){

        categoria.classList.add("is-invalid");

        document.getElementById("errorCategoria").textContent =
        "Seleccione una categoría";

        return false;
    }

    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");

    document.getElementById("errorCategoria").textContent = "";

    return true;
}
nombre.addEventListener("input", validarNombre);

correo.addEventListener("input", validarCorreo);

asunto.addEventListener("input", validarAsunto);

mensaje.addEventListener("input", validarMensaje);

categoria.addEventListener("blur", validarCategoria);
formulario.addEventListener("submit", function(e){

    e.preventDefault();
    alert("Entré al submit");

    if(
    validarNombre() &&
    validarCorreo() &&
    validarAsunto() &&
    validarMensaje() &&
    validarCategoria()
){

    registros.push({
        nombre:nombre.value,
        correo:correo.value,
        asunto:asunto.value,
        categoria:categoria.value
    });

    contador.textContent = registros.length;

    mensajeGeneral.innerHTML = `
    <div class="alert alert-success">
        Registro exitoso
    </div>
    `;

    formulario.reset();

}else{

    mensajeGeneral.innerHTML = `
    <div class="alert alert-danger">
        Corrija los errores
    </div>
    `;
}
});
formulario.addEventListener("submit",(e)=>{

    e.preventDefault();

    const nombre = formulario.Nombre.value.trim();
    const correo = formulario.Correo.value.trim();
    const asunto = formulario.Asunto.value.trim();
    const mensaje = formulario.Mensaje.value.trim();

    if(nombre === "" || correo === "" || asunto === "" || mensaje === ""){

        alert("Complete todos los campos.");
        return;
    }

    registros.push({
        nombre,
        correo,
        asunto,
        mensaje
    });

    document.getElementById("contador").textContent = registros.length;

    alert("Gracias por contactarnos.\nSu mensaje fue enviado correctamente.");

    formulario.reset();

});
