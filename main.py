# -*- coding: utf-8 -*-
import os, time, re, random, datetime, threading, sys, gc, tempfile, shutil
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ V101.5 STABLE CONFIGURATION ---
TABS_PER_MACHINE = 3    # Reduced to 3 for 100% stability
PURGE_INTERVAL = 120    # ♻️ Hard restart every 2 minutes
STRIKE_SPEED = 180      # 180ms JS Pulse (Server-Safe Speed)

sys.stdout.reconfigure(encoding='utf-8')

def log_status(msg):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [Phoenix V101.5]: {msg}", flush=True)

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    
    # 🛑 CRITICAL: Prevents Chrome from sleeping background tabs
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-background-timer-throttling")
    
    chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "iPad Pro"})
    
    temp_dir = os.path.join(tempfile.gettempdir(), f"v101_nuke_{int(time.time())}")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.set_page_load_timeout(35) # Prevent hanging on slow loads

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Linux armv8l", 
        webgl_vendor="ARM",
        renderer="Mali-G76",
        fix_hairline=True,
    )
    return driver

def deploy_hyper_engine(driver, target_id, target_name):
    """Spawns 3 Tabs with high-stagger hydration."""
    log_status(f"🌐 Initializing {TABS_PER_MACHINE} Hyper-Tabs...")
    
    for i in range(TABS_PER_MACHINE):
        tab_idx = i + 1
        log_status(f"🔄 Opening Tab {tab_idx}...")
        driver.execute_script(f"window.open('https://www.instagram.com/direct/t/{target_id}/', '_blank');")
        # ⏳ Give each tab 12 seconds to fully load the DM interface
        time.sleep(12) 

    handles = driver.window_handles[1:]
    
    for idx, handle in enumerate(handles):
        try:
            driver.switch_to.window(handle)
            time.sleep(2)
            
            log_status(f"💉 Injecting PRVR Engine into Tab {idx + 1}...")
            driver.execute_script(f"""
                const targetName = "{target_name}";
                const pulse = {STRIKE_SPEED};
                const emojis = ["👑", "⚡", "🔥", "🦈", "🦁", "💎", "⚔️", "🔱", "🧿", "🌪️"];
                
                const baseLines = 20;
                const adjustment = targetName.length - 4;
                const numUnderscores = Math.max(5, baseLines - adjustment);
                const underscores = "_".repeat(numUnderscores);

                if (window.strikeInterval) clearInterval(window.strikeInterval);

                window.strikeInterval = setInterval(() => {{
                    const box = document.querySelector('div[role="textbox"], [contenteditable="true"], textarea');
                    if (box) {{
                        const emoji = emojis[Math.floor(Math.random() * emojis.length)];
                        const salt = Math.random().toString(36).substring(7).toUpperCase();
                        
                        const line = `【 ${{targetName}} 】 SAY P R V R बाप ${{emoji}} ${{underscores}}/`;
                        const block = Array(22).fill(line).join('\\n');
                        const finalText = block + "\\n⚡ ID: " + salt;

                        box.focus();
                        document.execCommand('insertText', false, finalText);
                        box.dispatchEvent(new Event('input', {{ bubbles: true }}));

                        const enter = new KeyboardEvent('keydown', {{
                            bubbles: true, cancelable: true, key: 'Enter', code: 'Enter', keyCode: 13
                        }});
                        box.dispatchEvent(enter);

                        setTimeout(() => {{ if(box) box.innerHTML = ""; }}, 10);
                    }}
                }}, pulse);
            """)
        except Exception as e:
            log_status(f"❌ Tab {idx+1} Injection Failed: {e}")

    log_status(f"🔥 Stream Sync Complete. {len(handles)} Tabs Firing.")

def main():
    cookie = os.environ.get("INSTA_COOKIE")
    target_id = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "PRVR")
    
    if not cookie or not target_id:
        print("❌ ERROR: Missing Secret Keys.")
        return

    while True:
        driver = None
        try:
            log_status("🛠️ Starting New Nuclear Cycle...")
            driver = get_driver()
            
            driver.get("https://www.instagram.com/")
            sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
            driver.add_cookie({'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com'})
            
            deploy_hyper_engine(driver, target_id, target_name)
            
            # Wait 2 minutes for the tabs to blast
            time.sleep(PURGE_INTERVAL)
            
            log_status("♻️ REFRESH CYCLE: Nuking browser to clear DOM bloat...")
            
        except Exception as e:
            log_status(f"⚠️ REBOOTING ENGINE: {e}")
            time.sleep(10)
        finally:
            if driver: driver.quit()
            gc.collect()
            time.sleep(2)

if __name__ == "__main__":
    main()
