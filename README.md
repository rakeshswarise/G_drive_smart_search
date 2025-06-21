# 🔍 Gemini-Powered Smart Google Drive Search

This Python tool lets you **ask questions in natural language**, then uses **Google Drive API + Gemini AI** to:

- Extract **semantic keywords** from your question
- Search matching **Google Drive files**
- Read file contents (PDFs, Google Docs, and text files)
- Extract relevant **contextual snippets**
- Answer your question using **Gemini 1.5 Flash**

---

## 🚀 Features

- 🔐 Google OAuth-based Drive Access (Read-only)
- 🤖 Gemini-powered semantic keyword extraction
- 🧠 Snippet-based document comprehension
- 📄 Supports PDF, Google Docs, and plain text
- 💬 Natural language Q&A from your Drive documents

---

## 📁 File Structure

Google_Drive/
│
├── main.py # Main script to run smart Q&A
├── credentials.json # OAuth client secret from Google Cloud
├── token.json # Auto-generated access token after login
├── .env # Stores Gemini API key
├── .gitignore # Ignore secrets

yaml
Copy
Edit

---

## ⚙️ Setup Instructions

### 1. 🧱 Clone the Repo

```bash
git clone git@github.com:rakeshswarise/G_drive_smart_search.git
cd G_drive_smart_search
2. 🔑 Set Up Environment
Create a .env file:

env
Copy
Edit
GEMINI_API_KEY=your_gemini_api_key_here
To get a Gemini API key: https://aistudio.google.com/app/apikey

3. 📦 Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
If requirements.txt doesn't exist, install manually:

bash
Copy
Edit
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client google-generativeai python-dotenv PyMuPDF
4. 🔐 Set Up Google OAuth Credentials
Go to Google Cloud Console

Create a new project

Enable Google Drive API

Create OAuth credentials (Desktop app)

Download credentials.json and place it in the project root

▶️ Run the App
bash
Copy
Edit
python main.py
It will:

Authenticate via browser (only the first time)

Ask you to type a question

Find matching files in Drive

Extract content & snippets

Ask Gemini and return a precise answer

❓ Example Interaction
text
Copy
Edit
🔍 Enter your question (or 'exit'): What is the meeting agenda for Q2 marketing?

📁 Searching Google Drive using: ['meeting', 'agenda', 'Q2', 'marketing']

📄 File: Q2_Marketing_Meeting.pdf

📌 Extracted Snippets:
"""
... the agenda for Q2 marketing includes campaign planning, budget review, and performance metrics discussion ...
"""

🤖 Asking Gemini...

✅ Gemini Answer:
The **Q2 marketing meeting** agenda includes **campaign planning**, **budget review**, and **performance metrics discussion**.
🛡️ Security Notes
.env, token.json, and credentials.json are listed in .gitignore to avoid accidental commits.

Only readonly access is requested from your Google Drive.

📚 Tech Stack
🐍 Python 3.10+

🧠 Google Gemini (1.5 Flash)

☁️ Google Drive API (OAuth 2.0)

📄 PDF Parsing via PyMuPDF

🔍 Regex-based snippet extraction

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss the idea.

