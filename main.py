# -*- coding: utf-8 -*-
import os, time, re, random, datetime, threading, sys, gc, tempfile, shutil
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ V101.2 HYPER-INJECT CONFIG ---
TABS_PER_MACHINE = 5    # 5 Simultaneous tabs
PURGE_INTERVAL = 120    # ♻️ Hard restart every 2 minutes to prevent lag
STRIKE_SPEED = 150      # 150ms JS Pulse (Recommended for 5-tab stability)

sys.stdout.reconfigure(encoding='utf-8')

def log_status(msg):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [Phoenix V101.2]: {msg}", flush=True)

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    
    # iPad Pro emulation for the fastest Lexical DOM response
    chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "iPad Pro"})
    
    temp_dir = os.path.join(tempfile.gettempdir(), f"v101_nuke_{int(time.time())}")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Apply your working Stealth configuration
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
    """Spawns 5 Tabs and injects the PRVR JS Striker into each."""
    log_status(f"🚀 Spawning {TABS_PER_MACHINE} Hyper-Tabs...")
    
    for i in range(TABS_PER_MACHINE):
        driver.execute_script(f"window.open('https://www.instagram.com/direct/t/{target_id}/', '_blank');")
        time.sleep(6) # Hydration stagger

    handles = driver.window_handles[1:]
    
    for idx, handle in enumerate(handles):
        driver.switch_to.window(handle)
        driver.execute_script(f"""
            const targetName = "{target_name}";
            const pulse = {STRIKE_SPEED};
            const emojis = ["👑", "⚡", "🔥", "🦈", "🦁", "💎", "⚔️", "🔱", "🧿", "🌪️"];
            
            // Auto-Align Underline Logic for the block
            const baseUnderlines = 20;
            const adjustment = targetName.length - 4;
            const numLines = Math.max(5, baseUnderlines - adjustment);
            const underscores = "_".repeat(numLines);

            window.strikeInterval = setInterval(() => {{
                // Optimized selector for Mobile/iPad interface
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

                    // Native Keyboard Dispatch for Enter
                    const enter = new KeyboardEvent('keydown', {{
                        bubbles: true, cancelable: true, key: 'Enter', code: 'Enter', keyCode: 13
                    }});
                    box.dispatchEvent(enter);

                    // Instant wipe to stop DOM bloat
                    setTimeout(() => {{ if(box) box.innerHTML = ""; }}, 10);
                }}
            }}, pulse);
        """)
    log_status(f"🔥 All tabs active. Firing at {STRIKE_SPEED}ms pulse.")

def main():
    cookie = os.environ.get("INSTA_COOKIE")
    target_id = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "PRVR")
    
    if not cookie or not target_id:
        print("❌ ERROR: Missing Secret Keys.")
        return

    global_start = time.time()
    while True:
        driver = None
        try:
            log_status("🛠️ Initializing Nuclear Cycle...")
            driver = get_driver()
            
            # Login Handshake
            driver.get("https://www.instagram.com/")
            sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
            driver.add_cookie({'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com'})
            
            # Deploy the JS Engine
            deploy_hyper_engine(driver, target_id, target_name)
            
            # Run for the duration of the Purge Interval
            time.sleep(PURGE_INTERVAL)
            
            log_status("♻️ PURGE INTERVAL REACHED: Flushing RAM and restarting...")
            
        except Exception as e:
            log_status(f"⚠️ SYSTEM REBOOT: {e}")
            time.sleep(10)
        finally:
            if driver: driver.quit()
            gc.collect()
            time.sleep(2)

if __name__ == "__main__":
    main()
