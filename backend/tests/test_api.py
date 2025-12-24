import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import os
import sys

# Añadir el path de backend para poder importar app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

client = TestClient(app)

def test_read_main():
    """Prueba que la página principal carga"""
    from fastapi.responses import HTMLResponse
    with patch('app.templates.TemplateResponse') as mock_template:
        mock_template.return_value = HTMLResponse(content="<html></html>", status_code=200)
        response = client.get("/")
        assert response.status_code == 200

def test_get_labels_error():
    """Prueba el manejo de errores al obtener etiquetas"""
    with patch('app.gmail_manager.get_labels') as mock_get:
        mock_get.side_effect = Exception("Gmail API Error")
        response = client.get("/api/labels")
        assert response.status_code == 200
        assert "error" in response.json()

def test_stop_download():
    """Prueba el endpoint de detener descarga"""
    response = client.get("/api/stop")
    assert response.status_code == 200
    assert response.json() == {"status": "stopping"}

def test_logout():
    """Prueba el endpoint de cerrar sesión"""
    with patch('app.gmail_manager.logout') as mock_logout:
        response = client.get("/api/logout")
        assert response.status_code == 200
        assert response.json() == {"status": "logged_out"}
        mock_logout.assert_called_once()
