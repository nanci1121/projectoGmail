import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCOPES = os.getenv("GMAIL_SCOPES", "https://www.googleapis.com/auth/gmail.readonly").split(",")
CREDENTIALS_FILE = os.path.join(BASE_DIR, os.getenv("GMAIL_CREDENTIALS_FILE", "credentials.json"))
TOKEN_FILE = os.path.join(BASE_DIR, os.getenv("GMAIL_TOKEN_FILE", "token.json"))

class GmailWebManager:
    def __init__(self):
        self.creds = self._authenticate()
        self.service = build("gmail", "v1", credentials=self.creds)

    def _authenticate(self):
        creds = None
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
        return creds

    def logout(self):
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
        self.creds = None
        self.service = None

    def get_labels(self):
        if not self.creds or not self.service:
            self.creds = self._authenticate()
            self.service = build("gmail", "v1", credentials=self.creds)
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

class WebDownloader:
    def __init__(self, gmail_manager):
        self.gmail = gmail_manager
        self._stop_requested = False

    def stop(self):
        self._stop_requested = True

    def clean_filename(self, filename):
        invalid_chars = '\\/:*?"<>|'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename

    def download_attachments(self, query, download_dir, progress_callback=None):
        messages = self.gmail.search_messages(query)
        total = len(messages)
        downloaded_files = []

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        for i, message in enumerate(messages):
            if self._stop_requested:
                break
            msg = self.gmail.get_message_details(message["id"])
            files = self._process_payload(msg["payload"], message["id"], download_dir)
            downloaded_files.extend(files)
            
            if progress_callback:
                progress_callback(i + 1, total, files)

        return downloaded_files

    def _process_payload(self, payload, message_id, download_dir):
        parts = [payload]
        processed_files = []
        while parts:
            part = parts.pop()
            if 'parts' in part:
                parts.extend(part['parts'])
            
            if part.get("filename"):
                filename = self.clean_filename(part["filename"])
                if part["body"].get("attachmentId"):
                    path = self._save_file(message_id, part["body"]["attachmentId"], filename, download_dir)
                    if path:
                        processed_files.append(filename)
        return processed_files

    def _save_file(self, message_id, attachment_id, filename, download_dir):
        path = os.path.join(download_dir, filename)
        
        # Básica gestión de duplicados
        if os.path.exists(path):
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(download_dir, f"{base}_{counter}{ext}")):
                counter += 1
            filename = f"{base}_{counter}{ext}"
            path = os.path.join(download_dir, filename)

        attachment = self.gmail.get_attachment(message_id, attachment_id)
        file_data = base64.urlsafe_b64decode(attachment["data"].encode("UTF-8"))
        
        with open(path, "wb") as f:
            f.write(file_data)
        
        return path
