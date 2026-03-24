import os, time, re, random, datetime, threading, sys, gc, tempfile, shutil
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ V105 TURBO CONFIG ---
THREADS = 2              # 2 Browsers per runner
TOTAL_DURATION = 25000   

# 🔥 Target Speed: Dropped to absolute minimum Python latency
BURST_MIN = 0.01 
BURST_MAX = 0.04 

SESSION_MAX_SEC = 120    
GLOBAL_SENT = 0
COUNTER_LOCK = threading.Lock()
BROWSER_LAUNCH_LOCK = threading.Lock()

sys.stdout.reconfigure(encoding='utf-8')

def log_status(agent_id, msg):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] Agent {agent_id}: {msg}", flush=True)

def get_driver(agent_id):
    with BROWSER_LAUNCH_LOCK:
        time.sleep(1) # Reduced stagger
        chrome_options = Options()
        chrome_options.add_argument("--headless=new") 
        chrome_options.add_argument("--no-sandbox") 
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        # 💨 V105 Speed Hacks: Disable everything except the chat
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-remote-fonts")
        
        mobile_emulation = {
            "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
            "userAgent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
        }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        temp_dir = os.path.join(tempfile.gettempdir(), f"v105_{agent_id}_{int(time.time())}")
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Linux armv8l", fix_hairline=True)
        return driver

def find_mobile_box(driver):
    # Expanded selectors for faster detection
    selectors = ["//div[@role='textbox']", "//div[@contenteditable='true']", "//textarea", "//*[@class='xat24cr']"]
    for xpath in selectors:
        try: return driver.find_element(By.XPATH, xpath)
        except: continue
    return None

def adaptive_inject(driver, element, text):
    try:
        # Direct JS insertion is 100x faster than send_keys for long blocks
        driver.execute_script("arguments[0].focus();", element)
        driver.execute_script("document.execCommand('insertText', false, arguments[0]);", text)
        element.send_keys(Keys.ENTER)
        return True
    except: return False

def get_dynamic_block(target_name):
    emojis = ["👑", "⚡", "🔥", "🦈", "🦁", "💎", "⚔️", "🔱", "🧿", "🌪️"]
    selected_emoji = random.choice(emojis)
    underscores = "_" * max(5, 24 - (len(target_name) - 4))
    
    line = f"【 {target_name} 】 SAY P R V R बाप {selected_emoji} {underscores}/"
    block = "\n".join([line for _ in range(20)])
    return f"{block}\n⚡ ID: {random.randint(1000, 9999)}"

def run_life_cycle(agent_id, cookie, target_id, target_name):
    global_start = time.time()
    while (time.time() - global_start) < TOTAL_DURATION:
        driver = None
        session_start = time.time()
        try:
            log_status(agent_id, "🚀 Launching Turbo Agent...")
            driver = get_driver(agent_id)
            driver.get("https://www.instagram.com/")
            
            sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
            driver.add_cookie({'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com'})
            
            # Navigate directly to the chat
            driver.get(f"https://www.instagram.com/direct/t/{target_id}/")
            time.sleep(6) # Min hydration time

            msg_box = find_mobile_box(driver)
            if not msg_box:
                log_status(agent_id, "❌ Box not found, retrying...")
                continue
            
            while (time.time() - session_start) < SESSION_MAX_SEC:
                if (time.time() - global_start) > TOTAL_DURATION: break
                
                final_text = get_dynamic_block(target_name)
                
                if adaptive_inject(driver, msg_box, final_text):
                    with COUNTER_LOCK:
                        global GLOBAL_SENT
                        GLOBAL_SENT += 1
                
                # ⚡ Minimal sleep for Python thread yielding
                time.sleep(random.uniform(BURST_MIN, BURST_MAX))
                
        except Exception as e:
            log_status(agent_id, f"⚠️ Error: {e}")
        finally:
            if driver: driver.quit()
            gc.collect()
            time.sleep(2)

def main():
    cookie = os.environ.get("INSTA_COOKIE", "")
    target_id = os.environ.get("TARGET_THREAD_ID", "")
    target_name = os.environ.get("TARGET_NAME", "PRVR")
    
    if not cookie or not target_id: return

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for i in range(THREADS):
            executor.submit(run_life_cycle, i+1, cookie, target_id, target_name)

if __name__ == "__main__":
    main()
