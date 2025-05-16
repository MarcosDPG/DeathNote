from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get("/", response_class=HTMLResponse)
def read_html():
    html_path = Path("public/index.html")
    return HTMLResponse(content=html_path.read_text(), status_code=200)

@app.get("/room", response_class=HTMLResponse)
def read_html():
    html_path = Path("public/room.html")
    return HTMLResponse(content=html_path.read_text(), status_code=200)

@app.get("/office", response_class=HTMLResponse)
def read_html():
    html_path = Path("public/office.html")
    return HTMLResponse(content=html_path.read_text(), status_code=200)