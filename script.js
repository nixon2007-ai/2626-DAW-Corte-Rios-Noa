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