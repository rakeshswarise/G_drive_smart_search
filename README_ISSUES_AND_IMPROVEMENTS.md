
# Project Title

A brief description of what this project does and who it's for

# 🛠️ Gemini + Google Drive Q&A — Known Issues & Improvements

This document provides a practical analysis of what works well, what needs fixing, and areas for improvement in the current implementation of the **Gemini-powered Smart Document Search** tool.

---

## ✅ What Works Perfectly

### 🔐 Authentication
- Google OAuth 2.0 flow via `credentials.json` and `token.json` works as expected.
- Token refresh logic is handled correctly.

### 📂 Google Drive Integration
- Can successfully search files via `fullText contains` using semantic keywords.
- Supports the following file types:
  - ✅ PDF (`application/pdf`)
  - ✅ Google Docs (`application/vnd.google-apps.document`)
  - ✅ Plain text (`text/plain`, etc.)

### 🧠 Gemini AI Integration
- Uses Gemini 1.5 Flash to:
  - Extract semantic keywords
  - Generate answers based on document context
- Generates precise and relevant responses **if** keywords and snippets are valid.

---
 ### Improvements
✅ **Expected**: Show most relevant or recent documents first.

---

### ❗ Limited Snippet Extraction
- Extracts up to 10 snippets around keywords with a fixed 256-char buffer.
- Snippets may be cut off, overlap, or miss surrounding meaning.
