import os
import json
import asyncio
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from web_logic import GmailWebManager, WebDownloader
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Gmail Downloader Web")

# Configuración de estáticos y plantillas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(FRONTEND_DIR, "templates"))

gmail_manager = GmailWebManager()
downloader = WebDownloader(gmail_manager)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/labels")
async def get_labels():
    try:
        labels = gmail_manager.get_labels()
        return sorted(labels, key=lambda x: x['name'])
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/download-progress")
async def download_progress(label_id: str = None):
    downloader._stop_requested = False
    query = "has:attachment -in:chats"
    if label_id and label_id != "0":
        # Buscamos el nombre de la etiqueta por ID
        labels = gmail_manager.get_labels()
        label_name = next((l['name'] for l in labels if l['id'] == label_id), None)
        if label_name:
            query += f' label:"{label_name}"'

    async def event_generator():
        download_dir = os.getenv("DOWNLOAD_DIR", "downloads")
        
        def progress_callback(current, total, files):
            # Esta función se llama desde la lógica síncrona
            pass

        messages = gmail_manager.search_messages(query)
        total = len(messages)
        
        yield f"data: {json.dumps({'type': 'start', 'total': total})}\n\n"

        for i, message in enumerate(messages):
            if downloader._stop_requested:
                yield f"data: {json.dumps({'type': 'stopped'})}\n\n"
                return

            msg = gmail_manager.get_message_details(message["id"])
            files = downloader._process_payload(msg["payload"], message["id"], download_dir)
            
            yield f"data: {json.dumps({
                'type': 'progress', 
                'current': i + 1, 
                'total': total, 
                'files': files
            })}\n\n"
            # Un pequeño delay para que la interfaz se vea fluida
            await asyncio.sleep(0.1)

        yield f"data: {json.dumps({'type': 'complete'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/api/stop")
async def stop_download():
    downloader.stop()
    return {"status": "stopping"}

@app.get("/api/logout")
async def logout():
    gmail_manager.logout()
    return {"status": "logged_out"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
