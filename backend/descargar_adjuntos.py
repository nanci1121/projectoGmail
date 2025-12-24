
import os
import base64
import sys
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# 1. CARGA DE CONFIGURACIÓN (.env)
load_dotenv()

SCOPES = os.getenv("GMAIL_SCOPES", "https://www.googleapis.com/auth/gmail.readonly").split(",")
CREDENTIALS_FILE = os.getenv("GMAIL_CREDENTIALS_FILE", "credentials.json")
TOKEN_FILE = os.getenv("GMAIL_TOKEN_FILE", "token.json")
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")

# 2. ADAPTADORES (Infraestructura)
class GmailService:
    def __init__(self, credentials_file, token_file, scopes):
        self.creds = self._authenticate(credentials_file, token_file, scopes)
        self.service = build("gmail", "v1", credentials=self.creds)

    def _authenticate(self, credentials_file, token_file, scopes):
        creds = None
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, scopes)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
                creds = flow.run_local_server(port=0)
            with open(token_file, "w") as token:
                token.write(creds.to_json())
        return creds

    def list_labels(self):
        results = self.service.users().labels().list(userId="me").execute()
        return results.get("labels", [])

    def search_messages(self, query):
        messages = []
        result = self.service.users().messages().list(userId="me", q=query).execute()
        messages.extend(result.get("messages", []))

        while "nextPageToken" in result:
            page_token = result["nextPageToken"]
            result = self.service.users().messages().list(userId="me", q=query, pageToken=page_token).execute()
            messages.extend(result.get("messages", []))
        return messages

    def get_message_details(self, message_id):
        return self.service.users().messages().get(userId="me", id=message_id).execute()

    def get_attachment(self, message_id, attachment_id):
        return self.service.users().messages().attachments().get(
            userId="me", messageId=message_id, id=attachment_id
        ).execute()

# 3. CASOS DE USO (Lógica de Negocio)
class AttachmentDownloader:
    def __init__(self, gmail_service):
        self.gmail = gmail_service

    def _clean_filename(self, filename):
        invalid_chars = '\\/:*?"<>|'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename

    def download_from_query(self, query, download_dir):
        messages = self.gmail.search_messages(query)
        print(f"Se encontraron {len(messages)} correos con archivos adjuntos.")
        
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        for message in messages:
            msg = self.gmail.get_message_details(message["id"])
            self._process_payload(msg["payload"], message["id"], download_dir)

    def _process_payload(self, payload, message_id, download_dir):
        parts = [payload]
        while parts:
            part = parts.pop()
            if 'parts' in part:
                parts.extend(part['parts'])
            
            if part.get("filename"):
                filename = self._clean_filename(part["filename"])
                if part["body"].get("attachmentId"):
                    self._save_file(message_id, part["body"]["attachmentId"], filename, download_dir)

    def _save_file(self, message_id, attachment_id, filename, download_dir):
        path = os.path.join(download_dir, filename)
        
        # Evitar duplicados: si el archivo ya existe, no lo volvemos a descargar
        if os.path.exists(path):
            print(f"Saltando (ya existe): {filename}")
            return path

        attachment = self.gmail.get_attachment(message_id, attachment_id)
        file_data = base64.urlsafe_b64decode(attachment["data"].encode("UTF-8"))
        
        with open(path, "wb") as f:
            f.write(file_data)
        
        sys.stdout.reconfigure(errors='replace')
        print(f"Descargado: {filename} -> {path}")
        return path

# 4. INTERFAZ DE USUARIO / APP CORE
def main():
    try:
        gmail = GmailService(CREDENTIALS_FILE, TOKEN_FILE, SCOPES)
        downloader = AttachmentDownloader(gmail)

        print("\n--- Carpetas de Gmail disponibles ---")
        labels = gmail.list_labels()
        label_map = {i: label['name'] for i, label in enumerate(labels, 1)}
        print("0: [TODOS LOS CORREOS]")
        for i, name in label_map.items():
            print(f"{i}: {name}")

        choice = input("\nSelecciona el número de la carpeta (o 0 para todo): ").strip()
        query = "has:attachment -in:chats"
        if choice.isdigit() and int(choice) in label_map:
            query += f' label:"{label_map[int(choice)]}"'

        downloader.download_from_query(query, DOWNLOAD_DIR)

    except HttpError as error:
        print(f"Ocurrió un error de API: {error}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()
