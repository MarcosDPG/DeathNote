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
        activar_portatil(this);
    }
});

// portatil js

function mostrarFormulario() {
  document.getElementById('lista-personas').classList.add('oculto');
  document.getElementById('formulario-persona').classList.remove('oculto');
}

function volverALista() {
  document.getElementById('formulario-persona').classList.add('oculto');
  document.getElementById('lista-personas').classList.remove('oculto');
}

function guardarPersona(event) {
  event.preventDefault();
  const form = event.target;
  const nombre = form.nombre.value;
  const archivo = form.imagen.files[0];
  const editando = form.getAttribute('data-editando') === 'true';

  const base64Foto = fotoToBase64(archivo);
  if (editando) {
    actualizarData(form.getAttribute('data-id'), nombre, base64Foto);
  } else {
    alert(`Persona guardada: ${nombre}` + (archivo ? " (con imagen)" : ""));
  }

  form.reset();
  form.removeAttribute('data-editando');
  form.removeAttribute('data-id');
  form.querySelector('button[type="submit"]').textContent = 'Guardar';
  document.getElementById('form-titulo').textContent = 'Registrar nueva persona';

  volverALista();
}

function fotoToBase64(foto){
  if (foto) {
    const reader = new FileReader();
    reader.onload = function() {
      base64Foto = reader.result.split(',')[1];
    };
    reader.readAsDataURL(foto);
  }
}

function actualizarData(id, nombre, foto_base64) {}

function editarPersona(id, nombre) {
  const formulario = document.querySelector('#formulario-persona form');
  formulario.nombre.value = nombre;
  formulario.setAttribute('data-id', id);
  formulario.setAttribute('data-editando', 'true');
  formulario.setAttribute('data-id', nombre);

  const titulo = document.getElementById('form-titulo');
  titulo.textContent = `Editando a ${nombre}`;

  const botonGuardar = formulario.querySelector('button[type="submit"]');
  botonGuardar.textContent = 'Actualizar';

  document.getElementById('lista-personas').classList.add('oculto');
  document.getElementById('formulario-persona').classList.remove('oculto');
}

