document.addEventListener('DOMContentLoaded', function() {
    espera.classList.remove('ocultar','mostrar');
    void espera.offsetWidth;
    espera.classList.add('ocultar');
});

window.addEventListener('pageshow', function(event) {
    let espera = document.getElementById('espera');

    // Si se viene del historial (como con la flecha "atrás")
    if (event.persisted) {
        espera.classList.remove('ocultar','mostrar');
        void espera.offsetWidth;
        espera.classList.add('ocultar');
    }
});

function onGoTo(ref) {
    let espera = document.getElementById('espera');
    espera.classList.remove('ocultar','mostrar');
    void espera.offsetWidth;
    espera.classList.add('mostrar');
    setTimeout(() => {
        window.location.href = ref
    }, 700);
}