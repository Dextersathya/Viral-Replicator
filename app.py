import subprocess, socket, time, requests, ollama
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# ================= CONFIG =================
CHROME_PATH       = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
USER_DATA_DIR     = r"E:\New folder (7)\chrome_automation"
CHROMEDRIVER_PATH = r"E:\New folder (7)\chromedriver.exe"
TAVILY_API_KEY    = "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"
MODEL_NAME        = "gemma3:4b"
# ==========================================


# ---------- 1. Chrome debug helpers ----------
def is_chrome_running():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    res = s.connect_ex(("127.0.0.1", 9222))
    s.close()
    return res == 0

def start_chrome_if_needed():
    if is_chrome_running():
        print("✅ Chrome debugging session already running - connecting...")
    else:
        print("⏳ Starting new Chrome debugging session...")
        subprocess.Popen([
            CHROME_PATH,
            "--remote-debugging-port=9222",
            f"--user-data-dir={USER_DATA_DIR}"
        ])
        print("🕒 Waiting for Chrome to be ready...")
        time.sleep(10)

def attach_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("✅ Chrome connected!")
    return driver


# ---------- 2. AI helpers ----------
def get_trending_topic():
    print("🔍 Fetching trending AI topics ...")
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": "latest AI news 2025",
        "max_results": 3,
        "search_depth": "basic"
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        r.raise_for_status()
        results = r.json().get("results", [])
        if results:
            return results[0].get("title", "Latest AI trends 2025")
    except Exception as e:
        print("⚠️ Tavily error:", e)
    return "Latest AI trends 2025"

def make_post(topic):
    prompt = f"""
You are a viral LinkedIn creator.
Write ONE LinkedIn post (not 3 options) about:
"{topic}"

Structure:
- Hook (1–2 lines)
- Insight (3–4 lines)
- CTA (1 line)

Tone: conversational, human, with emojis.
Output ONLY the post text, nothing else.
"""
    try:
        res = ollama.chat(model=MODEL_NAME, messages=[{"role":"user","content":prompt}])
        return res["message"]["content"].strip()
    except Exception as e:
        print("⚠️ Ollama error:", e)
        return None


# ---------- 3. LinkedIn helpers ----------
def try_open_composer(driver):
    """
    Try ALL known LinkedIn composer entry points.
    Return True if opened, False otherwise.
    """
    driver.execute_script("window.scrollTo(0, 300);")
    time.sleep(2)

    selectors = [
        (By.CLASS_NAME, "share-box-feed-entry__trigger"),
        (By.XPATH, "//button[contains(., 'Start a post')]"),
        (By.XPATH, "//div[contains(., 'Start a post') and @role='button']"),
    ]

    for by, val in selectors:
        try:
            print(f"🔎 Trying selector: {val}")
            el = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((by, val))
            )
            el.click()
            print("✅ Composer opened.")
            return True
        except TimeoutException:
            continue
        except Exception:
            continue

    # fallback if UI changed
    print("⚠️ Could not find composer by selectors, trying direct URL...")
    driver.get("https://www.linkedin.com/feed/?launchComposer=true")
    time.sleep(5)

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox'][contenteditable='true']"))
        )
        print("✅ Composer opened via URL.")
        return True
    except TimeoutException:
        return False


def post_to_linkedin(driver, text):
    print("🌐 Opening LinkedIn feed...")
    driver.get("https://www.linkedin.com/feed/")
    time.sleep(5)

    if "authwall" in driver.current_url or "login" in driver.current_url:
        print("⚠️ Please login in Chrome, then press Enter here...")
        input()
        driver.get("https://www.linkedin.com/feed/")
        time.sleep(5)

    opened = try_open_composer(driver)
    if not opened:
        print("❌ Could not open composer.")
        return

    # === STEP: Type text using JavaScript (fixes Unicode/emoji issue) ===
    try:
        print("📝 Typing text into composer...")
        editor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='textbox'][contenteditable='true']"))
        )
        
        # Click to focus
        editor.click()
        time.sleep(1)
        
        # Use JavaScript to set innerHTML - handles emojis perfectly
        escaped_text = text.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
        js_script = f"""
        const editor = arguments[0];
        editor.focus();
        
        // Split text by newlines and create paragraph elements
        const lines = `{escaped_text}`.split('\\n');
        editor.innerHTML = '';
        
        lines.forEach((line, index) => {{
            if (line.trim()) {{
                const p = document.createElement('p');
                p.textContent = line;
                editor.appendChild(p);
            }} else if (index < lines.length - 1) {{
                const br = document.createElement('br');
                editor.appendChild(br);
            }}
        }});
        
        // Trigger input event to notify LinkedIn
        editor.dispatchEvent(new Event('input', {{ bubbles: true }}));
        """
        
        driver.execute_script(js_script, editor)
        time.sleep(2)
        
        print("📤 Clicking Post button...")
        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Post' or @aria-label='Post']"))
        )
        post_button.click()
        print("✅ Post successfully published!")
        time.sleep(3)  # Wait for post to complete
        
    except Exception as e:
        print("❌ Error typing/posting:", e)
        print("💡 Trying alternative method...")
        
        # Fallback: Try using pyperclip if available
        try:
            import pyperclip
            from selenium.webdriver.common.keys import Keys
            
            editor = driver.find_element(By.CSS_SELECTOR, "div[role='textbox'][contenteditable='true']")
            editor.click()
            time.sleep(1)
            
            # Copy to clipboard and paste
            pyperclip.copy(text)
            editor.send_keys(Keys.CONTROL, 'v')
            time.sleep(2)
            
            post_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Post' or @aria-label='Post']"))
            )
            post_button.click()
            print("✅ Post published using clipboard method!")
            
        except ImportError:
            print("❌ Fallback failed. Install pyperclip: pip install pyperclip")
        except Exception as e2:
            print("❌ Fallback also failed:", e2)

    input("⏸ Press Enter to close browser ...")
    driver.quit()


# ---------- 4. main ----------
if __name__ == "__main__":
    print("="*60)
    print("⚡ LINKEDIN VIRAL POSTER (Final Stable Version) ⚡")
    print("="*60)

    start_chrome_if_needed()
    driver = attach_driver()

    topic = get_trending_topic()
    print(f"🧠 Topic: {topic}")

    post = make_post(topic)
    if not post:
        print("❌ Post generation failed.")
        driver.quit()
    else:
        print("\n💬 Generated post\n" + "-"*60)
        print(post)
        print("-"*60)
        ans = input("👉 Post this to LinkedIn? (y/n): ").strip().lower()
        if ans == "y":
            post_to_linkedin(driver, post)
        else:
            print("❌ Skipped posting.")
            driver.quit()