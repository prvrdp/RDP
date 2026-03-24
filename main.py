import os, time, re, random, datetime, threading, sys, gc, tempfile, shutil
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- 🔥 ULTIMATE STABILITY CONFIG ---
TABS_PER_AGENT = 2       
PURGE_INTERVAL = 180     # Increased to 3 mins (More firing time, fewer restarts)
STRIKE_SPEED_MS = 180    

sys.stdout.reconfigure(encoding='utf-8')

def log_status(msg):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [Phoenix V103.8]: {msg}", flush=True)

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    
    # Modern iPhone 14 Pro User Agent for better React compatibility
    ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
    mobile_emulation = {
        "deviceMetrics": { "width": 393, "height": 852, "pixelRatio": 3.0 },
        "userAgent": ua
    }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    temp_dir = os.path.join(tempfile.gettempdir(), f"v103_force_{int(time.time())}")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="iPhone", fix_hairline=True)
    return driver

def inject_striker(driver, handle, tab_idx, target_name):
    """Switches to tab and forces a React state update."""
    driver.switch_to.window(handle)
    time.sleep(5) # Give the switch time to settle
    
    driver.execute_script(f"""
        const targetName = "{target_name}";
        const speed = {STRIKE_SPEED_MS};
        const emojis = ["👑", "⚡", "🔥", "🦈", "🦁", "💎", "⚔️", "🔱"];
        const underscores = "_".repeat(Math.max(5, 24 - (targetName.length - 4)));

        function startStriker() {{
            if (window.prvrStriker) clearInterval(window.prvrStriker);
            
            window.prvrStriker = setInterval(() => {{
                // Multi-selector for the most common IG DM box classes
                const box = document.querySelector('div[role="textbox"], [contenteditable="true"], .xat24cr, textarea');
                if (box) {{
                    const emoji = emojis[Math.floor(Math.random() * emojis.length)];
                    const salt = Math.random().toString(36).substring(7).toUpperCase();
                    const line = `【 ${{targetName}} 】 SAY P R V R बाप ${{emoji}} ${{underscores}}/`;
                    const block = Array(20).fill(line).join('\\n') + "\\n⚡ ID: " + salt;

                    // 1. Focus and Click to wake up React
                    box.focus();
                    box.click();

                    // 2. Insert text via execCommand
                    document.execCommand('insertText', false, block);
                    
                    // 3. Dispatch 'input' event (Crucial for Send button)
                    box.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    
                    // 4. Hit Enter
                    const enter = new KeyboardEvent('keydown', {{
                        bubbles: true, cancelable: true, key: 'Enter', code: 'Enter', keyCode: 13
                    }});
                    box.dispatchEvent(enter);
                    
                    // 5. Cleanup
                    setTimeout(() => {{ if(box) box.innerHTML = ""; }}, 10);
                }}
            }}, speed);
        }}

        // Check for box every 1s, then fire
        const checkExist = setInterval(() => {{
           const box = document.querySelector('div[role="textbox"], [contenteditable="true"]');
           if (box) {{
              clearInterval(checkExist);
              startStriker();
              console.log("TAB {tab_idx} FIRING");
           }}
        }}, 1000); 
    """)

def run_life_cycle(cookie, target_id, target_name):
    while True:
        driver = None
        try:
            log_status("🛠️ Initializing Engine V103.8...")
            driver = get_driver()
            driver.get("https://www.instagram.com/")
            
            sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
            driver.add_cookie({'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com'})
            
            # Navigate to accounts first to verify session
            driver.get("https://www.instagram.com/accounts/edit/")
            time.sleep(6)
            if "login" in driver.current_url.lower():
                log_status("❌ FATAL: Cookie Expired.")
                sys.exit(1)
            
            log_status("✅ Session Validated. Opening Streams...")
            for i in range(TABS_PER_AGENT):
                driver.execute_script(f"window.open('https://www.instagram.com/direct/t/{target_id}/', '_blank');")
                time.sleep(12) # ⏳ Slow stagger for GitHub CPU

            handles = driver.window_handles[1:]
            for idx, h in enumerate(handles):
                log_status(f"💉 Syncing Tab {idx+1}...")
                inject_striker(driver, h, idx + 1, target_name)
            
            # Stay alive for firing duration
            time.sleep(PURGE_INTERVAL)
                
        except Exception as e:
            log_status(f"⚠️ Error: {e}")
            time.sleep(5)
        finally:
            if driver: driver.quit()
            gc.collect()
            time.sleep(5)

def main():
    cookie = os.environ.get("INSTA_COOKIE")
    target_id = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "PRVR")
    if not cookie or not target_id: return
    run_life_cycle(cookie, target_id, target_name)

if __name__ == "__main__":
    main()
