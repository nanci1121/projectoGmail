
import unittest
from unittest.mock import MagicMock, patch
import os
from descargar_adjuntos import AttachmentDownloader, GmailService

class TestGmailDownloader(unittest.TestCase):

    def setUp(self):
        # Mock del servicio para no disparar autenticación real durante inicialización
        self.mock_gmail_service = MagicMock(spec=GmailService)
        self.downloader = AttachmentDownloader(self.mock_gmail_service)

    def test_clean_filename(self):
        """Prueba que los nombres de archivo se limpien correctamente."""
        self.assertEqual(self.downloader._clean_filename("archivo:con:puntos.pdf"), "archivo_con_puntos.pdf")
        self.assertEqual(self.downloader._clean_filename("foto/vacaciones.jpg"), "foto_vacaciones.jpg")
        self.assertEqual(self.downloader._clean_filename("normal.pdf"), "normal.pdf")

    def test_list_labels(self):
        """Prueba la obtención de etiquetas."""
        self.mock_gmail_service.list_labels.return_value = [
            {"name": "INBOX"}, {"name": "TRASH"}
        ]
        labels = self.mock_gmail_service.list_labels()
        self.assertEqual(len(labels), 2)
        self.assertEqual(labels[0]['name'], "INBOX")

    @patch('descargar_adjuntos.os.path.exists')
    @patch('descargar_adjuntos.open', create=True)
    def test_save_file_collision(self, mock_open, mock_exists):
        """Prueba que se evite la sobrescritura de archivos (colisión de nombres)."""
        # Simulamos que el archivo ya existe la primera vez, pero no la segunda
        mock_exists.side_effect = [True, False]
        
        # Mock de la data del adjunto
        self.mock_gmail_service.get_attachment.return_value = {
            "data": "YmFzZTY0ZGF0YQ==" # "base64data"
        }

        # Ejecutamos el guardado
        # El nombre final debería tener un _1 antes de la extensión
        self.downloader._save_file("msg123", "att456", "test.pdf", "downloads")
        
        # Verificamos que se intentó abrir el archivo con el nombre modificado
        mock_open.assert_called_with("downloads/test_1.pdf", "wb")

if __name__ == "__main__":
    unittest.main()
