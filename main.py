import os, time, re, random, datetime, threading, sys, gc, tempfile
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- 🚀 V112 SATURATION ENGINE ---
THREADS = 2 
STRIKE_SPEED_MS = 20  # 🔥 THE LIMIT: 20ms pulse (50 messages per second)
SESSION_MAX_SEC = 120    

def get_driver(agent_id):
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox") 
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-v8-idle-tasks")
    options.add_argument("--blink-settings=imagesEnabled=false")
    
    mobile = {
        "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
        "userAgent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
    }
    options.add_experimental_option("mobileEmulation", mobile)
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def run_life_cycle(agent_id, cookie, target_id, target_name):
    while True:
        driver = None
        try:
            driver = get_driver(agent_id)
            driver.get("https://www.instagram.com/")
            sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
            driver.add_cookie({'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com'})
            driver.get(f"https://www.instagram.com/direct/t/{target_id}/")
            time.sleep(8) # Allow full Lexical engine load

            # 🎯 CACHE THE BOX
            box = driver.find_element(By.XPATH, "//div[@role='textbox']|//textarea")

            # 🔥 THE SATURATION INJECTOR (Recursive Loop)
            # This starts a process INSIDE Chrome that Python doesn't need to manage.
            driver.execute_script(f"""
                const el = arguments[0];
                const targetName = "{target_name}";
                const speed = {STRIKE_SPEED_MS};
                const emojis = ["👑", "⚡", "🔥", "🦈", "🦁", "💎", "⚔️", "🔱"];
                
                if (window.prvrInterval) clearInterval(window.prvrInterval);

                window.prvrInterval = setInterval(() => {{
                    const emoji = emojis[Math.floor(Math.random() * emojis.length)];
                    const salt = Math.random().toString(36).substring(7).toUpperCase();
                    const line = `【 ${{targetName}} 】 SAY P R V R बाप ${{emoji}} ________________________/`;
                    const block = Array(20).fill(line).join('\\n') + "\\n⚡ ID: " + salt;

                    el.focus();
                    document.execCommand('insertText', false, block);
                    
                    // Native Dispatch (Instant)
                    const enter = new KeyboardEvent('keydown', {{
                        bubbles: true, cancelable: true, key: 'Enter', code: 'Enter', keyCode: 13
                    }});
                    el.dispatchEvent(enter);

                    // Immediate DOM Purge to keep RAM 0
                    setTimeout(() => {{ if(el) el.innerHTML = ""; }}, 5);
                }}, speed);
            """, box)

            print(f"[{agent_id}] 🔥 Saturation Engine Engaged at {STRIKE_SPEED_MS}ms", flush=True)
            
            # Python just hangs out and keeps the browser alive for 2 minutes
            time.sleep(SESSION_MAX_SEC)
                
        except Exception as e:
            print(f"⚠️ Error: {e}")
        finally:
            if driver: driver.quit()
            gc.collect()

def main():
    cookie = os.environ.get("INSTA_COOKIE", "")
    target_id = os.environ.get("TARGET_THREAD_ID", "")
    target_name = os.environ.get("TARGET_NAME", "PRVR")
    if not cookie or not target_id: return
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for i in range(THREADS): executor.submit(run_life_cycle, i+1, cookie, target_id, target_name)

if __name__ == "__main__": main()
