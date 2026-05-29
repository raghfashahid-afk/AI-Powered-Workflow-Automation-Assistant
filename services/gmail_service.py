import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CREDENTIALS_FILE = "credentials.json"
REDIRECT_URI = "http://localhost:8000/auth/gmail/callback"

# Temporary storage for dev/testing
flow_store = {}


def get_authorization_url():
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    flow_store["flow"] = flow
    return auth_url, state


def exchange_code_for_token(code: str):
    flow = flow_store.get("flow")
    if not flow:
        raise Exception("Flow not found. Please reconnect Gmail.")
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return {
        "token":         credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri":     credentials.token_uri,
        "client_id":     credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes":        list(credentials.scopes)
    }


def build_gmail_client(token_data: dict):
    creds = Credentials(
        token=token_data["token"],
        refresh_token=token_data["refresh_token"],
        token_uri=token_data["token_uri"],
        client_id=token_data["client_id"],
        client_secret=token_data["client_secret"],
        scopes=token_data["scopes"]
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("gmail", "v1", credentials=creds)


def fetch_emails(token_data: dict, max_results: int = 10):
    service = build_gmail_client(token_data)
    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()
        emails.append(parse_email(msg_data))
    return emails


def parse_email(msg_data: dict):
    headers = msg_data.get("payload", {}).get("headers", [])

    def get_header(name):
        for h in headers:
            if h["name"].lower() == name.lower():
                return h["value"]
        return ""

    return {
        "gmail_id": msg_data["id"],
        "sender":   get_header("From"),
        "subject":  get_header("Subject"),
        "date":     get_header("Date"),
        "snippet":  msg_data.get("snippet", ""),
        "body":     extract_body(msg_data.get("payload", {}))
    }


def extract_body(payload: dict):
    body = ""
    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data", "")
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                    break
    else:
        data = payload.get("body", {}).get("data", "")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    return body