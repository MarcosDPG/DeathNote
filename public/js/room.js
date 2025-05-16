document.addEventListener("DOMContentLoaded", function() {
    const room = document.getElementById("room");
    const objectSelected = document.getElementById("object_selected");

    if (room && objectSelected) {
        //room.style.width = (window.innerWidth - objectSelected.offsetWidth) + "px";
    }
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