document.addEventListener("DOMContentLoaded", () => {

    // =====================================================
    // MENÚ DE ACCESIBILIDAD
    // =====================================================
    const btnAccesibilidad = document.getElementById("btnAccesibilidad");
    const menuAccesibilidad = document.getElementById("menuAccesibilidad");
    let tamanoTexto = 100; // porcentaje inicial

    if (btnAccesibilidad && menuAccesibilidad) {
        btnAccesibilidad.addEventListener("click", () => {
            menuAccesibilidad.classList.toggle("d-none");
        });

        // Cierra el menú si se hace clic afuera
        document.addEventListener("click", (e) => {
            if (!menuAccesibilidad.contains(e.target) && !btnAccesibilidad.contains(e.target)) {
                menuAccesibilidad.classList.add("d-none");
            }
        });

        document.querySelectorAll(".opcion-accesibilidad").forEach(boton => {
            boton.addEventListener("click", () => {
                const accion = boton.getAttribute("data-accion");

                if (accion === "aumentar") {
                    tamanoTexto = Math.min(tamanoTexto + 10, 150);
                    document.documentElement.style.fontSize = tamanoTexto + "%";
                }
                if (accion === "reducir") {
                    tamanoTexto = Math.max(tamanoTexto - 10, 80);
                    document.documentElement.style.fontSize = tamanoTexto + "%";
                }
                if (accion === "contraste") {
                    document.body.classList.toggle("alto-contraste");
                }
                if (accion === "restablecer") {
                    tamanoTexto = 100;
                    document.documentElement.style.fontSize = "100%";
                    document.body.classList.remove("alto-contraste");
                }
            });
        });
    }

    // =====================================================
    // SCROLL SUAVE DEL MENÚ
    // =====================================================
    document.querySelectorAll('a[href*="#"]').forEach(enlace => {
        enlace.addEventListener("click", function (e) {
            const url = new URL(this.href, window.location.origin);
            // Solo si el ancla es de la página actual
            if (url.pathname !== window.location.pathname || !url.hash) return;
            const destino = document.querySelector(url.hash);
            if (destino) {
                e.preventDefault();
                destino.scrollIntoView({ behavior: "smooth" });
            }
        });
    });

    // =====================================================
    // SOMBRA DEL NAVBAR AL HACER SCROLL
    // =====================================================
    const navbar = document.querySelector(".navbar");
    if (navbar) {
        window.addEventListener("scroll", () => {
            navbar.classList.toggle("shadow", window.scrollY > 100);
        });
    }

    // =====================================================
    // BOTÓN VOLVER ARRIBA
    // =====================================================
    const botonArriba = document.getElementById("btnArriba");
    if (botonArriba) {
        window.addEventListener("scroll", () => {
            botonArriba.style.display = window.scrollY > 300 ? "block" : "none";
        });
        botonArriba.addEventListener("click", () => {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    // =====================================================
    // FORMULARIO DE CONTACTO (solo existe en la página de inicio)
    // =====================================================
    const formulario = document.getElementById("formContacto");
    if (!formulario) return;

    const nombre = document.getElementById("nombre");
    const correo = document.getElementById("correo");
    const asunto = document.getElementById("asunto");
    const mensaje = document.getElementById("mensaje");
    const categoria = document.getElementById("categoria");
    const mensajeGeneral = document.getElementById("mensajeGeneral");
    const btnEnviar = formulario.querySelector('button[type="submit"]');

    function marcar(campo, idError, ok, textoError) {
        campo.classList.toggle("is-valid", ok);
        campo.classList.toggle("is-invalid", !ok);
        document.getElementById(idError).textContent = ok ? "" : textoError;
        return ok;
    }

    const validarNombre = () => marcar(nombre, "errorNombre", nombre.value.trim().length >= 3, "Mínimo 3 caracteres");
    const validarCorreo = () => marcar(correo, "errorCorreo", /\S+@\S+\.\S+/.test(correo.value), "Correo inválido");
    const validarAsunto = () => marcar(asunto, "errorAsunto", asunto.value.trim().length >= 5, "Mínimo 5 caracteres");
    const validarMensaje = () => marcar(mensaje, "errorMensaje", mensaje.value.trim().length >= 10, "Mínimo 10 caracteres");
    const validarCategoria = () => marcar(categoria, "errorCategoria", categoria.value !== "", "Seleccione una categoría");

    nombre.addEventListener("input", validarNombre);
    correo.addEventListener("input", validarCorreo);
    asunto.addEventListener("input", validarAsunto);
    mensaje.addEventListener("input", validarMensaje);
    categoria.addEventListener("change", validarCategoria);

    function mostrarAlerta(tipo, texto) {
        mensajeGeneral.innerHTML = "";
        const div = document.createElement("div");
        div.className = "alert alert-" + tipo;
        div.textContent = texto;
        mensajeGeneral.appendChild(div);
    }

    formulario.addEventListener("submit", async function (e) {
        e.preventDefault();

        const valido = [validarNombre(), validarCorreo(), validarAsunto(),
                        validarMensaje(), validarCategoria()].every(Boolean);
        if (!valido) {
            mostrarAlerta("danger", "Corrija los errores del formulario");
            return;
        }

        const datos = {
            name: nombre.value.trim(),
            email: correo.value.trim(),
            Asunto: asunto.value.trim(),
            Categoria: categoria.value,
            message: mensaje.value.trim(),
            _subject: "Nuevo mensaje web: " + asunto.value.trim(),
            _template: "table",
            _captcha: "false"
        };

        btnEnviar.disabled = true;
        btnEnviar.textContent = "Enviando...";

        try {
                       const control = new AbortController();
            const temporizador = setTimeout(() => control.abort(), 20000);
            const resp = await fetch("https://formsubmit.co/ajax/maryselvadaw@gmail.com", {
                method: "POST",
                headers: { "Content-Type": "application/json", "Accept": "application/json" },
                body: JSON.stringify(datos),
                signal: control.signal
            });
            clearTimeout(temporizador);
            const resultado = await resp.json().catch(() => ({}));

            if (resp.ok && (resultado.success === true || resultado.success === "true")) {
                mostrarAlerta("success", "¡Mensaje enviado! Te responderemos pronto.");
                formulario.reset();
                [nombre, correo, asunto, mensaje, categoria].forEach(c => c.classList.remove("is-valid"));
            } else {
                mostrarAlerta("danger", "No se pudo enviar el mensaje. Intenta de nuevo.");
            }
        } catch (err) {
            mostrarAlerta("danger", "Error de conexión. Intenta de nuevo.");
        } finally {
            btnEnviar.disabled = false;
            btnEnviar.textContent = "Enviar Mensaje";
        }
    });

});