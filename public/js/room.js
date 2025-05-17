document.addEventListener("DOMContentLoaded", function() {
    fetchNoticias();
});

function cerrar_libro() {
    obj = document.getElementById("deathnote_object");
    if (obj.classList.contains('animar-abrir')) {
        close_libro(obj);   
    }
    setTimeout(() => {
        desactivar_libro(obj);
    }, 1100);
}

function activar_libro(obj) {
    obj.classList.remove('animar-salir', 'animar-entrar');
    void obj.offsetWidth
    obj.classList.add('animar-entrar');
    document.getElementById("object_selected").classList.add('active');
    document.getElementById("deathnote_object").classList.add('active');
}
function desactivar_libro(obj) {
    libro_estado = true;
    obj.classList.remove('animar-salir', 'animar-entrar', 'animar-cerrar');
    void obj.offsetWidth
    obj.classList.add('animar-salir');
    setTimeout(() => {
        document.getElementById("object_selected").classList.remove('active');
        document.getElementById("deathnote_object").classList.remove('active');
    }, 1000);
}
libro_estado = true;
document.getElementById("deathnote_object").addEventListener("click", function() {
    if (libro_estado) {
        activar_libro(this);
        libro_estado = false;
    } else {
        open_libro(this);
    }
});

function activar_portatil(obj) {
    obj.classList.remove('animar-cerrar-centrado', 'animar-abrir-centrado');
    void obj.offsetWidth
    obj.classList.add('animar-abrir-centrado');
}

function cerrar_portatil(event) {
    event.stopPropagation();
    obj = document.getElementById("portatil");
    obj.classList.remove('animar-cerrar-centrado', 'animar-abrir-centrado');
    void obj.offsetWidth
    obj.classList.add('animar-cerrar-centrado');
}

document.getElementById("portatil").addEventListener("click", function() {
    if (!this.classList.contains('animar-abrir-centrado')) {
        if (!libro_estado) {
            cerrar_libro();
            setTimeout(() => {
                activar_portatil(this);
            }, 1500);
        } else {
            activar_portatil(this);
        }
    }
});

function fetchNoticias() {
    let noticias = "";
    Promise.all([
        fetch(`${window.location.origin}/api/deathnote/hojas/`)
            .then(res => {
                if (!res.ok) throw new Error("Error al cargar las hojas");
                return res.json();
            }),
        fetch(`${window.location.origin}/api/criminales/muertos`)
            .then(res => {
                if (!res.ok) throw new Error("Error al obtener los criminales muertos");
                return res.json();
            })
    ])
    .then(([hojas, muertos]) => {
        let mapaMuertos = {};
        muertos.criminales.forEach(criminal => {
            mapaMuertos[criminal.id] = criminal;
        });

        hojas.forEach( h => {
            const criminal = mapaMuertos[h.criminal_id];
            if (criminal) {
                noticias += buildNoticia({ ...h, ...criminal });
            }
        });

        document.getElementById("personas").innerHTML = noticias;
    })
    .catch(error => {
        console.error("Error al cargar las noticias:", error);
    });
}

function buildNoticia(data) {
    let noticia = `'${data.causa_muerte}, es la primer hipotesis en este caso', dice el capitan de la policia.\n\n
    ${data.detalles_muerte}`;
    return `<li class="persona">
                <img src="data:image/jpeg;base64,${data.foto_base64}" alt="${data.nombre_completo}" class="persona-img">
                <div class="persona-info">
                    <h3 class="persona-nombre">${data.nombre_completo} fallecio</h3>
                    <p class="persona-detalle">${noticia}</p>
                </div>
            </li>`
}