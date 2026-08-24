document.addEventListener("DOMContentLoaded", () => {

    // FORMULARIO DE LOGIN (Ingresar al Sistema)
    const formLogin = document.getElementById("formLogin");

    if (formLogin) {
        const usuario = document.getElementById("usuario");
        const contrasena = document.getElementById("contrasena");
        const mensajeLogin = document.getElementById("mensajeLogin");

        // Usuarios y contraseñas de prueba (demostrativos, sin base de datos)
        const USUARIOS_VALIDOS = [
            { usuario: "yg.noai@maryselva.ec", contrasena: "yg.noai" },
            { usuario: "nd.cortes@maryselva.ec", contrasena: "nd.cortes" },
            { usuario: "sb.riosv@maryselva.ec", contrasena: "sb.riosv" }
        ];

        formLogin.addEventListener("submit", function (e) {
            e.preventDefault();

            document.getElementById("errorUsuario").textContent = "";
            document.getElementById("errorContrasena").textContent = "";

            let valido = true;

            if (usuario.value.trim() === "") {
                document.getElementById("errorUsuario").textContent = "Ingrese su usuario";
                valido = false;
            }

            if (contrasena.value.trim() === "") {
                document.getElementById("errorContrasena").textContent = "Ingrese su contraseña";
                valido = false;
            }

            if (!valido) {
                return;
            }

            const coincide = USUARIOS_VALIDOS.some(
                u => u.usuario === usuario.value && u.contrasena === contrasena.value
            );

            if (coincide) {
                sessionStorage.setItem("sesionActiva", "true");
                sessionStorage.setItem("usuarioActivo", usuario.value);

                mensajeLogin.innerHTML = `
                    <div class="alert alert-success">
                        Acceso correcto. Ingresando al panel...
                    </div>
                `;
                setTimeout(() => {
                    window.location.href = "/panel";
                }, 800);
            } else {
                mensajeLogin.innerHTML = `
                    <div class="alert alert-danger">
                        Usuario o contraseña inválida.
                    </div>
                `;
            }
        });
    }

    // PROTECCIÓN Y CIERRE DE SESIÓN DEL PANEL
    const nombreUsuario = document.getElementById("nombreUsuario");
    const btnCerrarSesion = document.getElementById("btnCerrarSesion");

    if (btnCerrarSesion) {
        // Si no hay sesión activa, no deja ver el panel y regresa al login
        if (sessionStorage.getItem("sesionActiva") !== "true") {
            window.location.href = "/login";
        } else {
            nombreUsuario.textContent = sessionStorage.getItem("usuarioActivo");
        }

        btnCerrarSesion.addEventListener("click", () => {
            sessionStorage.removeItem("sesionActiva");
            sessionStorage.removeItem("usuarioActivo");
            window.location.href = "/";
        });
    }

    // MENÚ DE ACCESIBILIDAD
    const btnAccesibilidad = document.getElementById("btnAccesibilidad");
    const menuAccesibilidad = document.getElementById("menuAccesibilidad");
    let tamanoTexto = 100; // porcentaje inicial

    if (btnAccesibilidad && menuAccesibilidad) {
        btnAccesibilidad.addEventListener("click", () => {
            menuAccesibilidad.classList.toggle("d-none");
        });

        // Cierra el menú si se hace clic afuera
        document.addEventListener("click", (e) => {
            if (!menuAccesibilidad.contains(e.target) && e.target !== btnAccesibilidad && !btnAccesibilidad.contains(e.target)) {
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

    // SCROLL SUAVE DEL MENÚ
    const enlaces = document.querySelectorAll('a[href^="#"]');

    enlaces.forEach(enlace => {
        enlace.addEventListener("click", function (e) {
            const destino = document.querySelector(this.getAttribute("href"));

            if (destino) {
                e.preventDefault();
                destino.scrollIntoView({
                    behavior: "smooth"
                });
            }
        });
    });

    // CAMBIAR SOMBRA DEL NAVBAR
    const navbar = document.querySelector(".navbar");
    window.addEventListener("scroll", () => {
        if (window.scrollY > 100) {
            navbar.classList.add("shadow");
        } else {
            navbar.classList.remove("shadow");
        }
    });

    // FORMULARIO
    const formulario = document.getElementById("formContacto");
    const nombre = document.getElementById("nombre");
    const correo = document.getElementById("correo");
    const asunto = document.getElementById("asunto");
    const mensaje = document.getElementById("mensaje");
    const categoria = document.getElementById("categoria");
    const contador = document.getElementById("contador");
    const mensajeGeneral = document.getElementById("mensajeGeneral");
    let registros = [];

    // VALIDAR NOMBRE
    function validarNombre() {
        if (nombre.value.trim().length < 3) {
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

    // VALIDAR CORREO
    function validarCorreo() {
        const expresion = /\S+@\S+\.\S+/;
        if (!expresion.test(correo.value)) {
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

    // VALIDAR ASUNTO
    function validarAsunto() {
        if (asunto.value.trim().length < 5) {
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

    // VALIDAR MENSAJE
    function validarMensaje() {
        if (mensaje.value.trim().length < 10) {
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

    // VALIDAR CATEGORÍA
    function validarCategoria() {
        if (categoria.value === "") {
            categoria.classList.add("is-invalid");
            categoria.classList.remove("is-valid");
            document.getElementById("errorCategoria").textContent =
                "Seleccione una categoría";
            return false;
        }

        categoria.classList.remove("is-invalid");
        categoria.classList.add("is-valid");
        document.getElementById("errorCategoria").textContent = "";
        return true;
    }

    // VALIDACIONES EN TIEMPO REAL
    nombre.addEventListener("input", validarNombre);
    correo.addEventListener("input", validarCorreo);
    asunto.addEventListener("input", validarAsunto);
    mensaje.addEventListener("input", validarMensaje);
    categoria.addEventListener("change", validarCategoria);

    // ENVÍO DEL FORMULARIO
    formulario.addEventListener("submit", function (e) {
        e.preventDefault();
        if (
            validarNombre() &&
            validarCorreo() &&
            validarAsunto() &&
            validarMensaje() &&
            validarCategoria()
        ) {

            registros.push({
                nombre: nombre.value,
                correo: correo.value,
                asunto: asunto.value,
                categoria: categoria.value
            });

            contador.textContent = registros.length;
            mensajeGeneral.innerHTML = `
                <div class="alert alert-success">
                    Registro exitoso
                </div>
            `;

            formulario.reset();
            nombre.classList.remove("is-valid");
            correo.classList.remove("is-valid");
            asunto.classList.remove("is-valid");
            mensaje.classList.remove("is-valid");
            categoria.classList.remove("is-valid");
        } else {
            mensajeGeneral.innerHTML = `
                <div class="alert alert-danger">
                    Corrija los errores del formulario
                </div>
            `;
        }
    });

});

// BOTÓN VOLVER ARRIBA
const boton = document.getElementById("btnArriba");
window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {
        boton.style.display = "block";
    } else {
        boton.style.display = "none";
    }
});
boton.addEventListener("click", () => {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});