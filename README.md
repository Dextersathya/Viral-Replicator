
---

# ⚡ LinkedIn Viral Poster (Final Stable Version)

Automate your **LinkedIn content posting workflow** using AI!
This script generates a **viral-style LinkedIn post** about the **latest AI trends** and automatically posts it to your LinkedIn account — all in a human, conversational tone with emojis 🎯

---

## 🚀 Features

✅ **Auto-detects & connects** to an existing Chrome debugging session
✅ **Fetches latest AI news** using [Tavily API](https://tavily.com/)
✅ **Generates LinkedIn posts** using a local LLM model via [Ollama](https://ollama.ai/)
✅ **Automatically opens the LinkedIn composer** and posts your AI-generated content
✅ **Fallbacks and safety checks** (handles emoji text, clipboard paste, and login prompts)

---

## 🧠 Workflow Overview

1. **Launch / Attach to Chrome**

   * The script checks if Chrome is running in remote debugging mode.
   * If not, it launches Chrome with your specified profile.

2. **Fetch a Trending Topic**

   * Uses Tavily API to get the top trending AI-related topics.

3. **Generate a Viral Post**

   * Prompts an Ollama LLM (e.g., `gemma3:4b`) to write a short, catchy post.
   * Structure includes a **hook**, **insight**, and **CTA**.

4. **Auto-post to LinkedIn**

   * Logs into your LinkedIn session (if not already).
   * Opens the composer, injects the text, and publishes the post.

---

## 🧩 Requirements

### 🔹 Software

* Python 3.9+
* Google Chrome (with Remote Debugging enabled)
* ChromeDriver (matching your Chrome version)
* Ollama (for local model inference)

### 🔹 Python Libraries

Install dependencies:

```bash
pip install selenium requests ollama pyperclip
```

---

## ⚙️ Configuration

Edit these constants at the top of the script:

```python
CHROME_PATH       = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
USER_DATA_DIR     = r"E:\New folder (7)\chrome_automation"
CHROMEDRIVER_PATH = r"E:\New folder (7)\chromedriver.exe"
TAVILY_API_KEY    = "your_tavily_api_key_here"
MODEL_NAME        = "gemma3:4b"
```

### Notes:

* **USER_DATA_DIR**: A Chrome profile path that keeps you logged in to LinkedIn.
* **TAVILY_API_KEY**: Sign up at [Tavily](https://tavily.com/) for a free API key.
* **MODEL_NAME**: Any local Ollama model (e.g., `llama3`, `gemma3`, etc.).

---

## 🧭 How to Run

1. **Start the script:**

   ```bash
   python linkedin_poster.py
   ```

2. The script will:

   * Start Chrome (if needed)
   * Fetch AI trends
   * Generate a post using Ollama
   * Display the generated content

3. You’ll see a preview like this:

   ```
   🧠 Topic: AI Agents Revolutionizing Data Science
   💬 Generated post
   ------------------------------------------------------------
   🚀 The future of data science is autonomous! ...
   ------------------------------------------------------------
   👉 Post this to LinkedIn? (y/n):
   ```

4. Enter `y` to post automatically.

---

## 💡 Troubleshooting

| Issue                   | Solution                                                                      |
| ----------------------- | ----------------------------------------------------------------------------- |
| Chrome not connecting   | Make sure no other Chrome instance is using port 9222                         |
| LinkedIn asks for login | Log in manually once; your session will persist in USER_DATA_DIR              |
| Emojis not showing      | The script uses JS-based typing to preserve Unicode characters                |
| Post button not found   | LinkedIn UI might have changed — try updating `try_open_composer()` selectors |

---

## 🧰 Tech Stack

* **Python 3**
* **Selenium** – Web automation
* **Ollama** – Local AI text generation
* **Tavily API** – AI news retrieval
* **Chrome Debugging Protocol** – Seamless browser control

---

## 🛡️ Safety & Ethics

⚠️ This tool **automates social posting**. Please:

* Use it **responsibly** on your own account.
* Avoid spamming or posting misleading AI-generated content.
* Comply with [LinkedIn’s Terms of Service](https://www.linkedin.com/legal/user-agreement).

---

## ✨ Example Output

```
🚀 The AI world is changing faster than ever!  
From open-weight models to personalized copilots — 2025 is all about ownership.  

Don’t just consume AI tools — start **building with them**.  
The best opportunities come to those who experiment early.  

💬 What’s one AI trend you’re most excited about this year?
```

---

## 🧑‍💻 Author

**Dextersathya**
Python Developer | AI & ML Enthusiast
🔗 GitHub: [github.com/Dextersathya](https://github.com/Dextersathya)

---


