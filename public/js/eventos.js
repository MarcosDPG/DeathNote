const messageQueue = [];
let mostrandoMensaje = false;
let burbuja = document.getElementById("burbuja-mensaje");
let texto = document.getElementById("texto-mensaje");
let cursor = document.getElementById("cursor-escritura");
let shinigami = document.getElementById("shinigami");

// Configuraciones
const delayPensamiento = 1500;
const velocidadEscritura = 40;
const tiempoMinimoVisible = 3000;
const maxCaracteresPorPagina = 160;

// Función para agregar mensajes a la cola
function gestionarColaMensajes(mensaje) {
    messageQueue.push(mensaje);
    if (!mostrandoMensaje) {
        mostrarSiguienteMensaje();
    }
}

// Lógica principal
async function mostrarSiguienteMensaje() {
    if (messageQueue.length === 0) {
        ocultarShinigami();
        mostrandoMensaje = false;
        return;
    }

    mostrandoMensaje = true;
    mostrarShinigami();

    const mensaje = messageQueue.shift();
    const partes = dividirMensajeEnPaginas(mensaje);

    for (let parte of partes) {
        await mostrarPensamiento(delayPensamiento);
        await escribirMensaje(parte + "...   ");
        const tiempoVisible = calcularTiempoVisible(parte);
        await esperar(tiempoVisible);
    }

    mostrarSiguienteMensaje(); // Siguiente mensaje en cola
}

// Muestra puntos suspensivos como "pensamiento"
function mostrarPensamiento(duracion) {
    return new Promise((resolve) => {
        texto.textContent = "";
        cursor.style.display = "inline";
        burbuja.style.display = "block";

        let puntos = 0;
        const maxPuntos = 3;
        const intervalo = setInterval(() => {
            texto.textContent = '.'.repeat(puntos++ % (maxPuntos + 1));
        }, 200);

        setTimeout(() => {
            clearInterval(intervalo);
            resolve();
        }, duracion);
    });
}

// Escribe el mensaje con efecto de escritura
function escribirMensaje(mensaje) {
    return new Promise((resolve) => {
        texto.textContent = "";
        let i = 0;
        cursor.style.display = "inline";
        const escribir = setInterval(() => {
            texto.textContent += mensaje.charAt(i);
            i++;
            if (i >= mensaje.length) {
                clearInterval(escribir);
                cursor.style.display = "none";
                resolve();
            }
        }, velocidadEscritura);
    });
}

// Divide mensajes largos en partes
function dividirMensajeEnPaginas(mensaje) {
    const palabras = mensaje.split(" ");
    const partes = [];
    let actual = "";

    for (let palabra of palabras) {
        if ((actual + " " + palabra).length > maxCaracteresPorPagina) {
            partes.push(actual.trim());
            actual = palabra + " ";
        } else {
            actual += palabra + " ";
        }
    }
    if (actual.trim()) partes.push(actual.trim());

    return partes;
}

// Calcula tiempo de visibilidad del mensaje
function calcularTiempoVisible(mensaje) {
    const palabras = mensaje.split(" ").length;
    const tiempoPorPalabra = 300; // 0.3s por palabra
    return Math.max(tiempoMinimoVisible, palabras * tiempoPorPalabra);
}

// Helpers
function esperar(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function mostrarShinigami() {
    shinigami.style.opacity = "1";
    shinigami.style.transition = "opacity 0.5s ease-in";
    burbuja.style.display = "block";
}

function ocultarShinigami() {
    shinigami.style.opacity = "0";
    shinigami.style.transition = "opacity 0.5s ease-out";
    setTimeout(() => {
        burbuja.style.display = "none";
    }, 500);
}

// ************************ SOCKETS ************************ //

document.addEventListener("DOMContentLoaded", () => {
    const socket = new WebSocket(`ws://${window.location.host}/ws/notificaciones`);
    setupSocketListeners(socket)
})

function setupSocketListeners(socket) {
    socket.onopen = () => {
      console.log('Conectado al WebSocket');
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('Mensaje recibido:', data);
        let ele = document.querySelector(`.input_hoja[input_type='causa'][criminal_id='${data.criminal_id}']`)
        let ele2 = document.querySelector(`.input_hoja[input_type='detalles'][criminal_id='${data.criminal_id}']`)
        switch (data.proceso) {
            case "pendiente":
                gestionarColaMensajes(`${data.nombre_completo}, interesante`);
                break;
            case "asignado":
                ele = document.querySelector(`.input_hoja[input_type='causa'][criminal_id='${data.criminal_id}']`)
                selectnextInput(ele);
                ele.value = data.causa_muerte;
                break;
            case "detallado":
                ele2 = document.querySelector(`.input_hoja[input_type='detalles'][criminal_id='${data.criminal_id}']`)
                selectnextInput(ele2);
                ele2.value = data.detalles_muerte;
                break;
            case "muerte":
                ele = document.querySelector(`.input_hoja[input_type='causa'][criminal_id='${data.criminal_id}']`)
                ele2 = document.querySelector(`.input_hoja[input_type='detalles'][criminal_id='${data.criminal_id}']`)
                ele.setAttribute("disabled",true);
                ele2.setAttribute("disabled",true);
                ele.value = data.causa_muerte;
                ele2.value = data.detalles_muerte;
            default:
                break;
        }
    };

    socket.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    socket.onclose = () => {
        console.log('WebSocket cerrado');
    };
}