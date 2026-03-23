import os, time, re, random, datetime, threading, sys, gc, tempfile, shutil
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- V102.6 TUNED CONFIGURATION ---
TABS_PER_AGENT = 3      
TOTAL_DURATION = 25000  
BURST_MIN = 0.05
BURST_MAX = 0.08
SESSION_MAX_SEC = 120    

sys.stdout.reconfigure(encoding='utf-8')
COUNTER_LOCK = threading.Lock()
GLOBAL_SENT = 0

def log_status(msg):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [Phoenix]: {msg}", flush=True)

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone 12 Pro"})
    
    temp_dir = os.path.join(tempfile.gettempdir(), f"v102_fix_{int(time.time())}")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Linux armv8l", fix_hairline=True)
    return driver

def find_mobile_box(driver):
    # Added .xat24cr which is the specific class Instagram uses for the DM box
    selectors = [
        "//div[@aria-label='Message...']",
        "//div[@role='textbox']",
        "//*[@class='xat24cr']",
        "//textarea"
    ]
    for xpath in selectors:
        try: return driver.find_element(By.XPATH, xpath)
        except: continue
    return None

def adaptive_inject(driver, element, text):
    """FORCED REACT INJECTION: Wakes up the Send button."""
    try:
        # 1. Click to focus (Crucial for mobile)
        element.click()
        
        # 2. Inject via Native Value Setter to bypass React block
        driver.execute_script("""
            var el = arguments[0];
            var txt = arguments[1];
            el.focus();
            // Use execCommand for text insertion but follow with Input events
            document.execCommand('insertText', false, txt);
            
            // Dispatch 'input' event so React sees the text
            var event = new Event('input', { bubbles: true });
            el.dispatchEvent(event);
        """, element, text)
        
        # 3. Hit Enter
        time.sleep(0.1)
        element.send_keys(Keys.ENTER)
        return True
    except: return False

def get_dynamic_block(target_name):
    emojis = ["👑", "⚡", "🔥", "🦈", "🦁", "💎", "⚔️", "🔱"]
    line = f"【 {target_name} 】 SAY P R V R बाप {random.choice(emojis)} ________________________/"
    block = "\n".join([line for _ in range(20)])
    return f"{block}\n⚡ ID: {random.randint(1000, 9999)}"

def main_cycle():
    cookie = os.environ.get("INSTA_COOKIE", "")
    target_id = os.environ.get("TARGET_THREAD_ID", "")
    target_name = os.environ.get("TARGET_NAME", "EZRA")
    
    global_start = time.time()
    while (time.time() - global_start) < TOTAL_DURATION:
        driver = None
        session_start = time.time()
        try:
            log_status("🚀 Launching Fix Engine...")
            driver = get_driver()
            driver.get("https://www.instagram.com/")
            
            sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
            driver.add_cookie({'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com'})
            
            # Navigate to direct chat
            driver.get(f"https://www.instagram.com/direct/t/{target_id}/")
            time.sleep(8) # Allow full hydration

            msg_box = find_mobile_box(driver)
            
            if msg_box:
                log_status("🔥 Box Found. Starting Firing...")
                while (time.time() - session_start) < SESSION_MAX_SEC:
                    final_text = get_dynamic_block(target_name)
                    if adaptive_inject(driver, msg_box, final_text):
                        with COUNTER_LOCK:
                            global GLOBAL_SENT
                            GLOBAL_SENT += 1
                    time.sleep(random.uniform(BURST_MIN, BURST_MAX))
            else:
                log_status("❌ Box not found. Check Thread ID.")
                
        except Exception as e:
            log_status(f"⚠️ Error: {e}")
        finally:
            log_status("♻️ Purging session...")
            if driver: driver.quit()
            gc.collect()

if __name__ == "__main__":
    main_cycle()
