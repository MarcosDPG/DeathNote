# 💀 DeathNote

Death Note es una aplicación web inspirada en el anime de Death Note. En esta plicación los usuarios pueden simular acciones vistas en la serie a través de la libreta, estas acciones son: escribir el nombre del criminal, subir una foto del mismo, especificar detalles de muerte y llevar un registro de los criminales. El proyecto busca proponer un frontend atractivo junto con un backend funcional y una base de datos funcional para almacenar notas.


## ⚒️ Tecnologías utilizadas

- 🌐 **HTML - CSS - JavaScript** — Para frontend
- 📦 **FastApi** - Para backend con Python
- 🐳 **Docker**
- 🔥 **Firebase**

## ⚙️ Instalación y ejecución local

1. Clona el repositorio:
    ```bash
    git clone https://github.com/MarcosDPG/DeathNote.git
    cd DeathNote
    ```
2. Crea un archivo `.env`:
    ```bash
    cp .env.example .env
    # Ajusta las variables de entorno en .env
    ```
3. Ejecuta con Docker:
    ```bash
    docker-compose up --build
    ```
4. Abre tu navegador en `http://localhost:8000`

## 🧪 Funcionalidades principales

- Interfaz visual inspirada en el anime Death Note
- Añadir criminales a la base de datos
- Libreta para escribir los nombres y detalles
- Computador para revisar criminales en la base de datos
- Guardado y consulta de entradas en la base de datos

## 📄 Licencia

MIT License
