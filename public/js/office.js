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
  const form = document.querySelector('#formulario-persona form'); 
  form.reset();
  form.removeAttribute('data-editando');
  form.removeAttribute('data-id');
  form.querySelector('button[type="submit"]').textContent = 'Guardar';
  document.getElementById('form-titulo').textContent = 'Registrar nueva persona';
  document.getElementById('formulario-persona').classList.add('oculto');
  document.getElementById('lista-personas').classList.remove('oculto');
}

async function guardarPersona(event) {
  event.preventDefault();
  const form = event.target;
  const nombre = form.nombre.value.trim();
  const archivo = form.imagen.files[0];
  const editando = form.getAttribute('data-editando') === 'true';

  const base64Foto = await fotoToBase64(archivo);
  if (editando) {
    actualizarData(form.getAttribute('data-id'), nombre, base64Foto);
  } else {
    crearData(nombre, base64Foto);
  }

  volverALista();
}

function fotoToBase64(foto) {
  return new Promise((resolve, reject) => {
    if (!foto) return resolve("no_foto");

    const reader = new FileReader();
    reader.onload = function () {
      const base64 = reader.result.split(',')[1];
      resolve(base64);
    };
    reader.onerror = function (error) {
      reject(error);
    };
    reader.readAsDataURL(foto);
  });
}


function actualizarData(id, nombre, foto_base64) {
  let res = {}
  res.nombre_completo = nombre;
  if (foto_base64 && foto_base64 !== "no_foto") {
    res.foto_base64 = foto_base64;
  }
  fetch(window.location.origin + '/api/criminales/' + id, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(res),
    })
    .then(response => {
      if (!response.ok) {
        alert('Error al actualizar la persona');
      } else {
        cargarCriminales();
      }
    })
}

function crearData(nombre, foto_base64) {
  let res = {}
  if (nombre === "") {
    alert("El nombre no puede estar vacío");
    return;
  }
  res.nombre_completo = nombre;
  res.foto_base64 = foto_base64;
  fetch(window.location.origin + '/api/criminales/registrar/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(res),
    })
    .then(response => {
      if (!response.ok) {
        alert('Error al registrar la persona');
        response.json().then(res => console.log(res));
      } else {
        cargarCriminales();
      }
    })
}

function editarPersona(id, nombre) {
  const formulario = document.querySelector('#formulario-persona form');
  formulario.nombre.value = nombre;
  formulario.setAttribute('data-id', id);
  formulario.setAttribute('data-editando', 'true');

  const titulo = document.getElementById('form-titulo');
  titulo.textContent = `Editando a ${nombre}`;

  const botonGuardar = formulario.querySelector('button[type="submit"]');
  botonGuardar.textContent = 'Actualizar';

  document.getElementById('lista-personas').classList.add('oculto');
  document.getElementById('formulario-persona').classList.remove('oculto');
}

async function cargarCriminales() {
  const listaContainer = document.getElementById('personas-lista');
  listaContainer.innerHTML = '<img class="cargando" src="public/assets/shinigami.gif" alt="Cargando...">';
  try {
    const response = await fetch( window.location.origin + '/api/criminales/');
    const data = await response.json();
    
    if (data.criminales && data.criminales.length > 0) {
      let res = "";
      data.criminales.forEach(criminal => {
        res += criminalHTML(criminal);
        listaContainer.innerHTML = res;
      });
    } else {
      listaContainer.innerHTML += '<p>No hay criminales registrados aún.</p>';
    }
  } catch (error) {
    console.error('Error al cargar criminales:', error);
    document.getElementById('lista-criminales').innerHTML += '<p>Error al cargar la lista de criminales.</p>';
  }
}

function criminalHTML(criminal) {
  if (criminal.foto_base64 && criminal.foto_base64 !== "no_foto") {
    imgElement = `<img src="data:image/jpeg;base64,${criminal.foto_base64}" class="criminal-img">`;
  } else {
    imgElement = '<div class="no-image">Sin imagen</div>';
  }
  if (criminal.estado === "vivo") {
    deathElement = "";
    deathElement2 = "";
  } else {
    deathElement = `<svg class="estado-muerto" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="red" width="48" height="48">
                      <path d="M32 2C19.85 2 10 11.85 10 24c0 6.53 2.76 12.42 7.18 16.57L17 48c0 1.1.9 2 2 2h6v4a2 2 0 0 0 4 0v-4h6v4a2 2 0 0 0 4 0v-4h6c1.1 0 2-.9 2-2l-.18-7.43C51.24 36.42 54 30.53 54 24 54 11.85 44.15 2 32 2zm-8 26a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm16 0a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/>
                  </svg>`;
    deathElement2 = `<span class="estado">Muerto</span>`;
  }
  return `<li class="persona-item">
              <div class="img-wrapper">
                  ${imgElement}
                  ${deathElement}
              </div>
              <div class="persona-texto">
                  <h3>${criminal.nombre_completo}</h3>
                  ${deathElement2}
              </div>
              <button class="editar-btn" onclick="editarPersona('${criminal.id}','${criminal.nombre_completo}')">🖉</button>
          </li>`
}

document.addEventListener('DOMContentLoaded', function() {
  cargarCriminales();
});