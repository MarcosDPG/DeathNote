var paginaActual = 0;
var hojas = []; // Aquí se guardarán las hojas HTML

document.addEventListener("DOMContentLoaded", function() {
    fetch_hojas().then(data => {
        if (data.length > 0) {
            cargarHojas(data);
        } else {
            crear_hoja({"id": "hoja" + (paginaActual + 1)});
        }
    }
    ).catch(error => {
        console.error("Error al cargar las hojas:", error);
        crear_hoja({"id": "hoja" + (paginaActual + 1)});
    });
});

send_data = function (currentInput) {}

function selectnextInput(currentInput) {
    const padre = currentInput.parentElement;
    if (currentInput.getAttribute("input_type") === "nombre") {
        nextInput = padre.querySelector(".input_hoja[input_type='causa']");
    } else {
        nextInput = padre.querySelector(".input_hoja[input_type='detalles']");
    }
    currentInput.setAttribute("disabled", true);
    if (nextInput) {
        nextInput.classList.remove('hidden');
        nextInput.focus();
        nextInput.select();
    }
}

function open_libro(obj) {
    document.getElementById("object_selected").classList.remove('hidden');
    document.getElementById("hojas").classList.remove('hidden');
    obj.classList.remove('animar-cerrar', 'animar-abrir');
    void obj.offsetWidth
    obj.classList.add('animar-abrir');
}
function close_libro(obj) {
    obj.classList.remove('animar-cerrar', 'animar-abrir');
    void obj.offsetWidth
    obj.classList.add('animar-cerrar');
    setTimeout(() => {
        document.getElementById("hojas").classList.add('hidden');
        document.getElementById("object_selected").classList.add('hidden');
    }, 1000);
}





function cambiarHoja(direccion) {
    if (hojas.length === 0) return;

    // Primero, eliminamos la clase 'hoja-actual' de la hoja actual
    const hojaAnterior = hojas[paginaActual];
    // Actualizamos la página actual
    paginaActual += direccion;
    // Comprobamos los límites del índice de la página
    if (paginaActual < 0) paginaActual=0;  // Si es menor que 0, no hacemos nada
    else if (paginaActual == hojas.length) {
        if (hojas[paginaActual-1].querySelector(".input_hoja[input_type='nombre']").disabled) {
            crear_hoja({"id": "hoja" + (paginaActual+1)});       
        } else {
            paginaActual = hojas.length - 1; // Si es mayor que el número de hojas, lo ajustamos
        }
    }
    // Seleccionamos la nueva hoja
    const nuevaHoja = hojas[paginaActual];

    //ANIMACIONES
    if (hojaAnterior === nuevaHoja) return; // Si la hoja no ha cambiado, no hacemos nada
    else  if (direccion > 0) {
        hojaAnterior.classList.remove('devolver-hoja');
        void hojaAnterior.offsetWidth; // Forzamos el reflow
        hojaAnterior.classList.add('pasar-hoja');
    } else {
        nuevaHoja.classList.remove('pasar-hoja');
        void nuevaHoja.offsetWidth; // Forzamos el reflow
        nuevaHoja.classList.add('devolver-hoja');
    }
}




function cargarHojas(contenidos) {
    contenidos.forEach((contenido, index) => {
        crear_hoja(contenido);
    });
    paginaActual = 0;
}

function crear_hoja(contenido={"id": "", "nombre": "", "causa": "", "detalles": ""}) {
    const contenedor = document.getElementById("hojas");
    const hoja = document.createElement("div");
    hoja.classList.add("hoja");
    hoja.id = contenido["id"];

    const nombre = document.createElement("textarea");
    nombre.classList.add("input_hoja");
    nombre.setAttribute("id_hoja", contenido["id"]);
    nombre.setAttribute("input_type", "nombre");
    nombre.setAttribute("placeholder", "Escribe el nombre de la persona aquí...");
    if (contenido["nombre"]) {
        nombre.setAttribute("disabled", true);
        nombre.value = contenido["nombre"];
    }

    const causa = document.createElement("textarea");
    causa.classList.add("hidden", "input_hoja");
    causa.setAttribute("id_hoja", contenido["id"]);
    causa.setAttribute("input_type", "causa");
    causa.setAttribute("placeholder", "Escribe la causa de la muerte aquí...");
    if (contenido["causa"]) {
        causa.setAttribute("disabled", true);
        causa.value = contenido["causa"];
        causa.classList.remove("hidden");
    }

    const detalles = document.createElement("textarea");
    detalles.classList.add("hidden", "input_hoja");
    detalles.setAttribute("id_hoja", contenido["id"]);
    detalles.setAttribute("input_type", "detalles");
    detalles.setAttribute("placeholder", "Escribe los detalles de la muerte aquí...");
    if (contenido["detalles"]) {
        detalles.setAttribute("disabled", true);
        detalles.value = contenido["detalles"];
        detalles.classList.remove("hidden");
    }

    // Agregamos los campos a la hoja
    hoja.appendChild(nombre);
    hoja.appendChild(causa);
    hoja.appendChild(detalles);

    // Añadimos la hoja al contenedor
    contenedor.insertBefore(hoja, contenedor.firstChild);

    // Guardamos la referencia de la hoja
    hojas.push(hoja);

    // Activamos los textarea
    hoja.querySelectorAll(".input_hoja").forEach(area => {
        area.addEventListener("input", function () {
            this.style.height = "auto";
            this.style.height = (this.scrollHeight) + "px";
        });
        area.addEventListener("keydown", function (e) {
            if (e.key === "Enter") {
                e.preventDefault();
                send_data(this);
                selectnextInput(this);
            }
        });
    });
}

function fetch_hojas() {
    return Promise.resolve([
        {"id": "hoja1", "nombre": "Nombre 1", "causa": "Causa 1", "detalles": "Detalles 1"}
    ]);
}