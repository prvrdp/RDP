# -*- coding: utf-8 -*-
import os, time, re, random, datetime, threading, sys, gc, tempfile, shutil
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ V101 CONFIGURATION ---
TABS_PER_AGENT = 3       # Optimized to 3 simultaneous streams
TOTAL_DURATION = 250000  
PURGE_INTERVAL = 120     # ♻️ Rebuild browser every 2 minutes
STRIKE_SPEED = 180       # 180ms JS Pulse

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
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    
    # iPad Pro emulation for optimized Lexical DOM
    chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "iPad Pro"})
    
    temp_dir = os.path.join(tempfile.gettempdir(), f"v101_nuke_{int(time.time())}")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win32", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL", fix_hairline=True)
    return driver

def deploy_js_engine(driver, target_id, target_name):
    """Spawns 3 Tabs and injects the high-speed engine."""
    for i in range(TABS_PER_AGENT):
        driver.execute_script(f"window.open('https://www.instagram.com/direct/t/{target_id}/', '_blank');")
        time.sleep(10) # 10s stagger for safe page hydration

    handles = driver.window_handles[1:]
    for idx, handle in enumerate(handles):
        driver.switch_to.window(handle)
        driver.execute_script(f"""
            const targetName = "{target_name}";
            const pulse = {STRIKE_SPEED};
            const emojis = ["👑", "⚡", "🔥", "🦈", "🦁", "💎", "⚔️", "🔱", "🧿", "🌪️"];
            
            const baseUnderlines = 20;
            const adjustment = targetName.length - 4;
            const numLines = Math.max(5, baseUnderlines - adjustment);
            const underscores = "_".repeat(numLines);

            window.strikeInterval = setInterval(() => {{
                const box = document.querySelector('div[role="textbox"], [contenteditable="true"], .xat24cr');
                if (box) {{
                    const emoji = emojis[Math.floor(Math.random() * emojis.length)];
                    const salt = Math.random().toString(36).substring(7).toUpperCase();
                    
                    const line = `【 ${{targetName}} 】 SAY P R V R बाप ${{emoji}} ${{underscores}}/`;
                    const finalText = Array(22).fill(line).join('\\n') + "\\n⚡ ID: " + salt;

                    box.focus();
                    document.execCommand('insertText', false, finalText);
                    box.dispatchEvent(new Event('input', {{ bubbles: true }}));

                    const sendBtn = document.querySelector('div.xjyslct') || 
                                    Array.from(document.querySelectorAll('div[role="button"]')).find(el => el.innerText === 'Send');
                    
                    if (sendBtn) {{
                        sendBtn.click();
                    }} else {{
                        const enter = new KeyboardEvent('keydown', {{bubbles: true, cancelable: true, key: 'Enter', keyCode: 13}});
                        box.dispatchEvent(enter);
                    }}
                    
                    // Instant DOM reset
                    setTimeout(() => {{ if(box) box.innerHTML = ""; }}, 40);
                }}
            }}, pulse);
        """)
    log_status(f"🚀 3 Tabs Synced. Firing at {STRIKE_SPEED}ms.")

def main():
    cookie = os.environ.get("INSTA_COOKIE")
    target_id = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "PRVR")
    
    if not cookie or not target_id:
        print("❌ ERROR: Set INSTA_COOKIE and TARGET_THREAD_ID in Secrets.")
        return

    global_start = time.time()
    while (time.time() - global_start) < TOTAL_DURATION:
        driver = None
        try:
            log_status("🛠️ Rebuilding environment...")
            driver = get_driver()
            driver.get("https://www.instagram.com/")
            
            sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
            driver.add_cookie({'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com'})
            
            deploy_js_engine(driver, target_id, target_name)
            
            time.sleep(PURGE_INTERVAL)
            log_status("♻️ NUCLEAR PURGE: Cleaning up and restarting cycle...")
            
        except Exception as e:
            log_status(f"⚠️ Error: {e}")
            time.sleep(10)
        finally:
            if driver: driver.quit()
            gc.collect()
            time.sleep(2)

if __name__ == "__main__":
    main()
