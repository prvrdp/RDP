import os
import time
import random
import datetime
import threading
import sys
import gc
import tempfile
from concurrent.futures import ThreadPoolExecutor

# 📦 SELENIUM & DRIVER TOOLS
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- 🔥 SPEED & CYCLE CONFIGURATION ---
THREADS = 2             
TOTAL_DURATION = 25000  

# ⚡ EXTREME TIMING SETTINGS
JS_DELAY = 50           # 50ms between messages (Ultra-Speed)
REFRESH_CYCLE = 120     # Refresh page every 2 minutes (120 seconds)

sys.stdout.reconfigure(encoding='utf-8')
DRIVER_PATH = None
INSTALL_LOCK = threading.Lock()

def log_status(agent_id, msg):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] Agent {agent_id}: {msg}", flush=True)

def get_driver(agent_id):
    global DRIVER_PATH
    with INSTALL_LOCK:
        if DRIVER_PATH is None:
            log_status(agent_id, "📦 Installing Chrome Driver...")
            DRIVER_PATH = ChromeDriverManager().install()

    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    
    mobile_emulation = {
        "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
        "userAgent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
    }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    temp_dir = os.path.join(tempfile.gettempdir(), f"automa_{agent_id}_{int(time.time())}")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")

    service = Service(DRIVER_PATH)
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

def run_prvr_engine(agent_id, cookie, target_id, target_name):
    driver = None
    global_start = time.time()
    
    try:
        log_status(agent_id, "🚀 Launching Browser...")
        driver = get_driver(agent_id)
        driver.get("https://www.instagram.com/")
        
        sid = cookie.replace("sessionid=", "").strip().split(";")[0]
        driver.add_cookie({'name': 'sessionid', 'value': sid, 'domain': '.instagram.com'})
        
        # --- ♻️ THE 2-MINUTE REFRESH LOOP ---
        while (time.time() - global_start) < TOTAL_DURATION:
            try:
                driver.get(f"https://www.instagram.com/direct/t/{target_id}/")
                log_status(agent_id, "⏳ Loading Chat...")
                time.sleep(12) # Wait for IG to render

                js_payload = f"""
                (async function() {{
                    const targetName = "{target_name}";
                    const delay = {JS_DELAY};
                    const emojis = ["👑", "⚡", "🔥", "🦈", "🦁", "💎", "⚔️", "🔱", "🧿", "🌪️", "🐍", "🦍"];

                    function getMessageBox() {{
                        return document.querySelector('textarea') || 
                               document.querySelector('[role="textbox"]') || 
                               document.querySelector('[contenteditable="true"]') ||
                               document.querySelector('.xat24cr');
                    }}

                    // Infinite rapid-fire loop
                    while (true) {{
                        try {{
                            const msgBox = getMessageBox();
                            if (!msgBox) {{
                                await new Promise(r => setTimeout(r, 1000));
                                continue;
                            }}

                            const emoji = emojis[Math.floor(Math.random() * emojis.length)];
                            const traceID = Math.random().toString(36).substring(2, 9).toUpperCase();
                            
                            // 👇 REDUCED UNDERLINE LENGTH HERE 👇
                            const line = `【 ${{targetName}} 】 SAY P R V R बाप ${{emoji}} __________/`;
                            const block = Array(30).fill(line).join('\\n');
                            const finalMsg = block + "\\n⚡ ID: " + traceID;

                            msgBox.focus();
                            document.execCommand('insertText', false, finalMsg);
                            msgBox.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            
                            // Tiny pause to let IG React register the text
                            await new Promise(r => setTimeout(r, 20)); 
                            
                            const sendBtn = document.querySelector('div.xjyslct') || 
                                            Array.from(document.querySelectorAll('div[role="button"]')).find(el => el.textContent.trim().toLowerCase() === 'send') ||
                                            Array.from(document.querySelectorAll('button')).find(el => el.textContent.trim().toLowerCase() === 'send');
                            
                            if (sendBtn) {{ sendBtn.click(); }} 
                            else {{
                                const enterEvent = new KeyboardEvent('keydown', {{ bubbles: true, cancelable: true, keyCode: 13, key: 'Enter' }});
                                msgBox.dispatchEvent(enterEvent);
                            }}

                            await new Promise(r => setTimeout(r, delay));
                            console.clear();
                        }} catch (e) {{ 
                            console.error("JS Loop Error", e); 
                        }}
                    }}
                }})();
                """

                log_status(agent_id, f"🔥 Firing 30-Line Blocks at {JS_DELAY}ms...")
                driver.execute_script(js_payload)

                # Let JS spam for exactly 2 minutes (120 seconds)
                time.sleep(REFRESH_CYCLE)
                
                log_status(agent_id, "♻️ 2-Min Cycle Complete. Flushing RAM and Refreshing...")
                driver.refresh()
                gc.collect() 
                
            except Exception as loop_err:
                log_status(agent_id, f"⚠️ Cycle Error: {loop_err}. Retrying in 10s...")
                time.sleep(10)

    except Exception as e:
        log_status(agent_id, f"❌ Fatal Crash: {e}")
    finally:
        if driver: driver.quit()
        gc.collect()

def main():
    cookie = os.environ.get("INSTA_COOKIE", "")
    target_id = os.environ.get("TARGET_THREAD_ID", "")
    target_name = os.environ.get("TARGET_NAME", "PRVR") 
    
    if not cookie or not target_id:
        print("❌ Missing Secrets (INSTA_COOKIE or TARGET_THREAD_ID)!")
        return

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for i in range(THREADS):
            executor.submit(run_prvr_engine, i+1, cookie, target_id, target_name)

if __name__ == "__main__":
    main()
