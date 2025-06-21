import os
import io
import fitz  # PyMuPDF
import re
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import google.generativeai as genai

# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not found in .env")
    exit()

genai.configure(api_key=GEMINI_API_KEY)
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# ✨ Semantic keyword extractor using Gemini
def semantic_keywords_gemini(query):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
You are an NLP assistant.

Extract the top 15 **Semantic, Contextual, Surface keywords** from the question below that can be used to search documents. Remove stopwords and select meaningful, relevant words or short phrases.

Query: "{query}"

Respond as a Python list: ["keyword1", "keyword2", ...]
"""
    try:
        response = model.generate_content(prompt)
        match = re.findall(r'\[.*?\]', response.text)
        if match:
            return eval(match[0])  # Convert string list to actual list
    except Exception as e:
        print(f"Gemini keyword error: {e}")
    return []

def search_files(service, keywords):
    if not keywords:
        return []
    query_parts = [f"fullText contains '{kw}'" for kw in keywords]
    query = " or ".join(query_parts)
    try:
        results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
        return results.get('files', [])
    except Exception as e:
        print(f"❌ Drive search error: {e}")
        return []

def download_file(service, file_id):
    request = service.files().get_media(fileId=file_id)
    file_stream = io.BytesIO()
    downloader = MediaIoBaseDownload(file_stream, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return file_stream.getvalue()

def extract_pdf_text(pdf_bytes):
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "\n".join(page.get_text("text") for page in doc)
        doc.close()
        return text
    except Exception as e:
        return f"Error extracting PDF: {e}"

def extract_google_doc_text(service, file_id):
    try:
        request = service.files().export(fileId=file_id, mimeType="text/plain")
        content = request.execute()
        return content.decode("utf-8", errors="ignore")
    except Exception as e:
        return f"Error extracting Google Doc: {e}"

def extract_text_from_bytes(file_bytes):
    try:
        return file_bytes.decode("utf-8", errors="ignore")
    except Exception as e:
        return f"Error decoding: {e}"

def extract_snippets(text, keywords, buffer=256, max_snips=10):
    if not keywords:
        return "No keywords found."

    pattern = "|".join(sorted([re.escape(k) for k in keywords], key=len, reverse=True))
    matches = list(re.finditer(pattern, text, re.IGNORECASE))

    snippets = []
    for match in matches[:max_snips]:
        start = max(match.start() - buffer // 2, 0)
        end = min(match.end() + buffer // 2, len(text))
        while start > 0 and text[start - 1].isalnum():
            start -= 1
        while end < len(text) and text[end].isalnum():
            end += 1
        snippets.append(text[start:end].strip())

    return "\n...\n".join(snippets) if snippets else "No direct keyword match found."

def ask_gemini(question, context):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
You are a precise document analysis assistant.

Based *only* on the provided "Document Context," answer the "User Question."

User Question: "{question}"
Document Context:
\"\"\"{context}\"\"\"

Instructions:
1. If the answer is directly and clearly available in the context, extract it.
2. If the answer contains specific details (like times, names, dates), highlight them using **bold**.
3. If the context contains information relevant to the question but not a direct answer, synthesize a concise answer from the relevant information.
4. If no relevant information is found in the context, reply with: "Not found in this document context."
5. Do not invent information or use external knowledge.
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {e}"

def main():
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    while True:
        query = input("\n🔍 Enter your question (or 'exit'): ").strip()
        if query.lower() == "exit":
            break

        keywords = semantic_keywords_gemini(query)
        if not keywords:
            print("❌ Couldn’t extract semantic keywords. Try again.")
            continue

        print(f"📁 Searching Google Drive using: {', '.join(keywords)}")
        files = search_files(service, keywords)

        if not files:
            print("❌ No matching files found.")
            continue

        for file in files:
            print(f"\n📄 File: {file['name']} ({file['mimeType']})")
            try:
                if file["mimeType"] == "application/pdf":
                    content = extract_pdf_text(download_file(service, file["id"]))
                elif file["mimeType"] == "application/vnd.google-apps.document":
                    content = extract_google_doc_text(service, file["id"])
                elif file["mimeType"].startswith("text/"):
                    content = extract_text_from_bytes(download_file(service, file["id"]))
                else:
                    print("⛔ Unsupported file format.")
                    continue
            except Exception as e:
                print(f"⚠️ Error reading file: {e}")
                continue

            context = extract_snippets(content, keywords)
            print(f"\n📌 Extracted Snippets:\n\"\"\"\n{context}\n\"\"\"")

            print("\n🤖 Asking Gemini...")
            answer = ask_gemini(query, context)
            print(f"\n✅ Gemini Answer:\n{answer}")

if __name__ == "__main__":
    main()
