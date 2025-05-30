var paginaActual = 0;
var hojas = []; // Aquí se guardarán las hojas HTML

document.addEventListener("DOMContentLoaded", function() {
    fetch_hojas();
});

function selectnextInput(currentInput) {
    const padre = currentInput.parentElement;
    if (currentInput.getAttribute("input_type") === "nombre") {
        nextInput = padre.querySelector(".input_hoja[input_type='causa']");
    } else {
        nextInput = padre.querySelector(".input_hoja[input_type='detalles']");
    }
    currentInput.setAttribute("disabled", true);
    if (nextInput) {
        nextInput.setAttribute("criminal_id", currentInput.getAttribute("criminal_id"));
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

function crear_hoja(contenido={"id": "", "criminal_id": "", "nombre_completo": "", "causa_muerte": "", "detalles_muerte": ""}) {
    const contenedor = document.getElementById("hojas");
    const hoja = document.createElement("div");
    hoja.classList.add("hoja");
    hoja.id = contenido["id"];

    const nombre = document.createElement("textarea");
    nombre.classList.add("input_hoja");
    nombre.setAttribute("id_hoja", contenido["id"]);
    nombre.setAttribute("criminal_id", contenido["criminal_id"]);
    nombre.setAttribute("input_type", "nombre");
    nombre.setAttribute("placeholder", "Escribe el nombre de la persona aquí...");

    const causa = document.createElement("textarea");
    causa.classList.add("hidden", "input_hoja");
    causa.setAttribute("id_hoja", contenido["id"]);
    causa.setAttribute("criminal_id", contenido["criminal_id"]);
    causa.setAttribute("input_type", "causa");
    causa.setAttribute("placeholder", "Escribe la causa de la muerte aquí...");

    const detalles = document.createElement("textarea");
    detalles.classList.add("hidden", "input_hoja");
    detalles.setAttribute("id_hoja", contenido["id"]);
    detalles.setAttribute("criminal_id", contenido["criminal_id"]);
    detalles.setAttribute("input_type", "detalles");
    detalles.setAttribute("placeholder", "Escribe los detalles de la muerte aquí...");


    if (contenido["nombre_completo"]) {
        nombre.setAttribute("disabled", true);
        nombre.value = contenido["nombre_completo"];
        if (contenido["causa_muerte"] !== "") {
            causa.setAttribute("disabled", true);
            causa.setAttribute("placeholder", "");
            causa.value = contenido["causa_muerte"];
            if (contenido["detalles_muerte"] !== "" || contenido["proceso"] === "muerto") {
                detalles.setAttribute("disabled", true);
                detalles.setAttribute("placeholder", "");
                detalles.value = contenido["detalles_muerte"];
            }
            detalles.classList.remove("hidden");
        }
        causa.classList.remove("hidden");
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
            if (e.key == "Enter") {
                e.preventDefault();
                send_data(this);
            }
        });
    });
}

function fetch_hojas() {
    fetch(window.location.origin + '/api/deathnote/hojas/', 
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            },
        }).then(res => {
            if (res.ok) {
                res.json().then(data => {
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
            } else {
                throw new Error("Error al cargar las hojas");
            }
        }
    );
}

function send_data(currentInput) {
    value = currentInput.value.trim();
    if (value === "") {
        alert("No puedes dejar el campo vacío");
        return;
    } else {
        const inputType = currentInput.getAttribute("input_type");
        switch (inputType) {
            case "nombre":
                requestIdByName(value).then(res => {
                    if (res.ok) {
                        res.json().then(data => {
                            let criminales = [];
                            let criminales_muertos = [];
                            let criminales_vivos = [];
                            let criminales_sin_foto = [];
                            data.forEach(criminal => {
                                if (criminal.estado === "vivo") {
                                    criminales_vivos.push(criminal);
                                } else {
                                    criminales_muertos.push(criminal);
                                }
                            });
                            criminales_vivos.forEach(criminal => {
                                if (criminal.foto_base64 === "no_foto") {
                                    criminales_sin_foto.push(criminal);
                                } else {
                                    criminales.push(criminal);
                                }
                            });
                            if (criminales.length > 0) {
                                let id = criminales[0].id;
                                currentInput.setAttribute("disabled", true);
                                currentInput.value = criminales[0].nombre_completo;
                                currentInput.setAttribute("criminal_id", id);
                                send_name(value, currentInput.getAttribute("criminal_id")).then(res => {
                                    if (res.ok) {
                                        selectnextInput(currentInput);
                                    } else {
                                        gestionarColaMensajes("Hmmm... Algo parece estar mal con el nombre que has escrito. ¿Podrías revisarlo?");
                                    }
                                });
                            } else {
                                if (criminales_sin_foto.length > 0) {
                                    gestionarColaMensajes("Hmmm... Parece que olvidaste el rostro de esta persona. ¿Podrías recordarlo mas tarde?");
                                }
                                if (criminales_muertos.length > 0) {
                                    gestionarColaMensajes("Estaria interesante matar a alguien que ya está muerto. ¿No crees?");
                                }
                            }
                        });
                    } else {
                        switch (res.status) {
                            case 400:
                                gestionarColaMensajes("Es un buen nombre para un futuro criminal jejeje");
                                break;
                        
                            default:
                                gestionarColaMensajes("Hmmm... Algo parece estar mal con el nombre que has escrito. ¿Podrías revisarlo?");
                                break;
                        }
                    }
                });
                break;
            case "causa":
                send_causa(value, currentInput.getAttribute("criminal_id")).then(res => {
                    if (res.ok) {
                        selectnextInput(currentInput);
                    } else {
                        gestionarColaMensajes("Hmmm... Algo parece estar mal con la causa de muerte que has escrito. ¿Podrías revisarlo?");
                    }
                });
                break;
            case "detalles":
                send_detalles(value, currentInput.getAttribute("criminal_id")).then(res => {
                    if (res.ok) {
                        selectnextInput(currentInput);
                    } else {
                        gestionarColaMensajes("Hmmm... Algo parece estar mal con los detalles de la muerte que has escrito. ¿Podrías revisarlo?");
                    }
                });
                break;
        
            default:
                break;
        }
    }
}

function requestIdByName(value) {
    return fetch(window.location.origin + `/api/criminales/nombre/${value}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
    });
}

function send_name(data, id) {
    return fetch(window.location.origin + `/api/deathnote/id/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({criminal_id: id})
    });
}

function send_causa(data, id) {
    return fetch(window.location.origin + `/api/deathnote/causa-muerte/`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({criminal_id: id, causa_muerte: data})
    });
}

function send_detalles(data, id) {
    return fetch(window.location.origin + `/api/deathnote/detalles/`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({criminal_id: id, detalles_muerte: data})
    });
}