import os
import time
import re
import random
import datetime
import threading
import sys
import gc
import tempfile
import subprocess
import shutil
from concurrent.futures import ThreadPoolExecutor

# 📦 SELENIUM & DRIVER TOOLS
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- V101.1 SINGLE AGENT CONFIG ---
THREADS = 1             # Locked to Single Agent
TABS_PER_AGENT = 5      # 5 Simultaneous Tabs in one browser
TOTAL_DURATION = 25000  # ~7 Hours

# ⚡ TARGET SPEED (Per Tab Switch)
BURST_MIN = 0.08
BURST_MAX = 0.10

# ♻️ RESTART CYCLES (2 Minutes)
SESSION_MAX_SEC = 120    

GLOBAL_SENT = 0
COUNTER_LOCK = threading.Lock()

sys.stdout.reconfigure(encoding='utf-8')

def log_status(msg):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [Agent 1]: {msg}", flush=True)

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    mobile_emulation = {
        "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
        "userAgent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
    }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    temp_dir = os.path.join(tempfile.gettempdir(), f"v101_single_{int(time.time())}")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Linux armv8l", 
        webgl_vendor="ARM",
        renderer="Mali-G76",
        fix_hairline=True,
    )
    return driver

def find_mobile_box(driver):
    selectors = ["//textarea", "//div[@role='textbox']", "//div[@contenteditable='true']", "//*[@class='xat24cr']"]
    for xpath in selectors:
        try: 
            return driver.find_element(By.XPATH, xpath)
        except: continue
    return None

def adaptive_inject(driver, element, text):
    try:
        driver.execute_script("arguments[0].focus();", element)
        driver.execute_script("document.execCommand('insertText', false, arguments[0]);", text)
        element.send_keys(Keys.ENTER)
        return True
    except: return False

def get_dynamic_block(target_name):
    """Generates a fresh 20-line block with a rotating emoji and auto-aligned underlines."""
    emojis = ["👑", "⚡", "🔥", "🦈", "🦁", "💎", "⚔️", "🔱", "🧿", "🌪️", "🐍", "🦍"]
    selected_emoji = random.choice(emojis)
    
    base_underlines = 24
    adjustment = len(target_name) - 4 
    num_underlines = max(5, base_underlines - adjustment)
    underlines = "_" * num_underlines

    line = f"【 {target_name} 】 SAY P R V R बाप {selected_emoji} {underlines}/"
    block = "\n".join([line for _ in range(20)])
    return f"{block}\n⚡ ID: {random.randint(1000, 9999)}"

def run_life_cycle(cookie, target_id, target_name):
    global_start = time.time()
    while (time.time() - global_start) < TOTAL_DURATION:
        driver = None
        session_start = time.time()
        try:
            log_status(f"🚀 Spawning Browser with {TABS_PER_AGENT} Hyper-Tabs...")
            driver = get_driver()
            driver.get("https://www.instagram.com/")
            
            sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
            driver.add_cookie({'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com'})
            
            # --- ⚡ DEPLOY TABS ---
            for i in range(TABS_PER_AGENT):
                driver.execute_script(f"window.open('https://www.instagram.com/direct/t/{target_id}/', '_blank');")
                time.sleep(6) 

            handles = driver.window_handles[1:] 
            
            # --- FIRING LOOP ---
            while (time.time() - session_start) < SESSION_MAX_SEC:
                if (time.time() - global_start) > TOTAL_DURATION: break
                
                for handle in handles:
                    driver.switch_to.window(handle)
                    msg_box = find_mobile_box(driver)
                    
                    if msg_box:
                        final_text = get_dynamic_block(target_name)
                        if adaptive_inject(driver, msg_box, final_text):
                            with COUNTER_LOCK:
                                global GLOBAL_SENT
                                GLOBAL_SENT += 1
                    
                    time.sleep(random.uniform(BURST_MIN, BURST_MAX))
                
        except Exception as e:
            log_status(f"⚠️ Runtime Error: {e}")
        finally:
            log_status("♻️ NUCLEAR PURGE: Resetting Browser session...")
            if driver: driver.quit()
            gc.collect()

def main():
    cookie = os.environ.get("INSTA_COOKIE", "")
    target_id = os.environ.get("TARGET_THREAD_ID", "")
    target_name = os.environ.get("TARGET_NAME", "EZRA") 
    
    if not cookie or not target_id:
        print("❌ Missing Secrets!")
        return

    run_life_cycle(cookie, target_id, target_name)

if __name__ == "__main__":
    main()
