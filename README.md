# SACOM II2 — Your Personal LLM Wrapper App

Welcome to SACOM II2, a clean and modular AI assistant that runs on your own specified knowledge domains. It’s powered by FastAPI on the backend and a lightweight HTML/JavaScript frontend, making it easy to understand, extend, and customize.

At its core, it uses Google Gemini (Generative AI), but you can plug in any content—or even switch out the LLM—without much hassle.

---

##  Getting Started (Run It Locally)

### 1. Clone this repo
```bash
git clone <your-repo-url>
cd sacom-llm-app
```

### 2. Set up your Python environment
```bash
python -m venv backend/venv
# Then activate it:
# On Windows:
./backend/venv/Scripts/activate
# On macOS/Linux:
source backend/venv/bin/activate
```

### 3. Install backend dependencies
```bash
pip install -r requirements.txt
# Or manually:
pip install fastapi uvicorn pydantic pydantic-settings google-generativeai slowapi
```

### 4. Add your API key and active content domain
Create a `.env` file in the project root and add:
```
GOOGLE_API_KEY="your-gemini-api-key"
ACTIVE_DOMAIN="philosophy"  # or whatever content file you want to load
```
You can grab your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 5. Start the backend
```bash
uvicorn backend.main:app --reload
```

You should now see the FastAPI server running at:  
[http://127.0.0.1:8000](http://127.0.0.1:8000)

### 6. Open the frontend
Just open `frontend/index.html` in your browser — no build step, no bundling, just pure simplicity.

---

##  How It Works (Architecture Overview)

Here’s the idea:
-  Modular design— each file has a clear role:
  - `config.py` — handles your environment variables.
  - `content_service.py` — loads your domain-specific content.
  - `llm_service.py` — connects to Google Gemini (or any other LLM).
  - `main.py` — brings it all together and serves the API.
- Why environment variables?
  Keeps your secrets (like API keys) safe and makes switching domains simple.
- Rate limiting with `slowapi` — prevents abuse and helps control LLM usage costs.(Not more than 5 requests per minute)
- Frontend — plain HTML/CSS/JS. Easy to tweak, no complex build tools involved.

---

##  Changing the Knowledge Base (It's Super Easy)

Want the assistant to speak like a Stoic:

1. Add a new `.txt` file in the `content/` folder, e.g., `stoicism.txt`.
2. Set `ACTIVE_DOMAIN="stoicism"` in your `.env`.
3. Restart the server.

---

## Hosted Version

If deployed, you’ll find the live version here:  
`[YOUR_HOSTED_URL_HERE]`

---

##  Questions or Suggestions?

Feel free to open an issue or pull request.  
All contributions are welcome.
