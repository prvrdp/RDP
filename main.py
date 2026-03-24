import os, time, re, random, datetime, threading, sys, gc, tempfile, shutil
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- 🚀 V107 INTERNAL MEMORY STRIKER ---
THREADS = 2 
BURST_MIN = 0.01  # ⚡ 10ms (System Floor)
BURST_MAX = 0.03  # ⚡ 30ms
SESSION_MAX_SEC = 120    

sys.stdout.reconfigure(encoding='utf-8')
LAUNCH_LOCK = threading.Lock()

def get_driver(agent_id):
    with LAUNCH_LOCK:
        options = Options()
        options.add_argument("--headless=new") 
        options.add_argument("--no-sandbox") 
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--blink-settings=imagesEnabled=false")
        
        mobile = {
            "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
            "userAgent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
        }
        options.add_experimental_option("mobileEmulation", mobile)
        
        temp = os.path.join(tempfile.gettempdir(), f"v107_{agent_id}_{int(time.time())}")
        options.add_argument(f"--user-data-dir={temp}")
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

def run_life_cycle(agent_id, cookie, target_id, target_name):
    while True:
        driver = None
        session_start = time.time()
        try:
            print(f"[{agent_id}] 🚀 Launching Internal Engine...", flush=True)
            driver = get_driver(agent_id)
            driver.get("https://www.instagram.com/")
            
            sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
            driver.add_cookie({'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com'})
            
            driver.get(f"https://www.instagram.com/direct/t/{target_id}/")
            time.sleep(6) 

            while (time.time() - session_start) < SESSION_MAX_SEC:
                try:
                    box = driver.find_element(By.XPATH, "//div[@role='textbox']|//textarea")
                    
                    # 🔥 V107 ULTRA-FAST INJECTOR: Logic is now inside the Browser
                    driver.execute_script("""
                        const el = arguments[0];
                        const name = arguments[1];
                        const emojis = ["👑", "⚡", "🔥", "🦈", "🦁", "💎", "⚔️", "🔱"];
                        
                        // 🛠️ Internal Block Builder (Zero Latency)
                        const emoji = emojis[Math.floor(Math.random() * emojis.length)];
                        const salt = Math.random().toString(36).substring(7).toUpperCase();
                        const line = `【 ${name} 】 SAY P R V R बाप ${emoji} ________________________/`;
                        const block = Array(20).fill(line).join('\\n') + "\\n⚡ ID: " + salt;

                        el.focus();
                        document.execCommand('insertText', false, block);
                        
                        // Wipe memory 2ms after send
                        setTimeout(() => { if(el) el.innerHTML = ""; }, 2);
                    """, box, target_name)
                    
                    # ⚡ Native Send
                    box.send_keys(Keys.ENTER)
                    
                except:
                    break 
                
                # ⚡ Zero-Gravity Delay
                time.sleep(random.uniform(BURST_MIN, BURST_MAX))
                
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
        for i in range(THREADS):
            executor.submit(run_life_cycle, i+1, cookie, target_id, target_name)

if __name__ == "__main__":
    main()
