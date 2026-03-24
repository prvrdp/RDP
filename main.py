import os, time, re, random, datetime, threading, sys, gc, tempfile, shutil
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- 🔥 STABILITY CONFIG ---
TABS_PER_AGENT = 2       
PURGE_INTERVAL = 150     # Increased to 2.5 mins to allow for slower page loads
STRIKE_SPEED_MS = 180    

sys.stdout.reconfigure(encoding='utf-8')

def log_status(msg):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [Phoenix V103.7]: {msg}", flush=True)

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    
    mobile_emulation = {
        "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
    }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    temp_dir = os.path.join(tempfile.gettempdir(), f"v103_stable_{int(time.time())}")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="iPhone", fix_hairline=True)
    return driver

def inject_striker(driver, handle, tab_idx, target_name):
    driver.switch_to.window(handle)
    # This JS block now "Polles" (checks) for the textbox every 500ms before starting
    driver.execute_script(f"""
        const targetName = "{target_name}";
        const speed = {STRIKE_SPEED_MS};
        const emojis = ["👑", "⚡", "🔥", "🦈", "🦁", "💎", "⚔️", "🔱"];
        const underscores = "_".repeat(Math.max(5, 24 - (targetName.length - 4)));

        function startStriker() {{
            if (window.prvrStriker) clearInterval(window.prvrStriker);
            
            window.prvrStriker = setInterval(() => {{
                const box = document.querySelector('div[role="textbox"], [contenteditable="true"], .xat24cr');
                if (box) {{
                    const emoji = emojis[Math.floor(Math.random() * emojis.length)];
                    const salt = Math.random().toString(36).substring(7).toUpperCase();
                    const line = `【 ${{targetName}} 】 SAY P R V R बाप ${{emoji}} ${{underscores}}/`;
                    const block = Array(20).fill(line).join('\\n') + "\\n⚡ ID: " + salt;

                    box.focus();
                    document.execCommand('insertText', false, block);
                    box.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    
                    const enter = new KeyboardEvent('keydown', {{
                        bubbles: true, cancelable: true, key: 'Enter', code: 'Enter', keyCode: 13
                    }});
                    box.dispatchEvent(enter);
                    
                    setTimeout(() => {{ if(box) box.innerHTML = ""; }}, 10);
                }}
            }}, speed);
            console.log("🚀 STRIKER STARTED ON TAB {tab_idx}");
        }}

        // Wait for the DOM to be ready
        const checkExist = setInterval(() => {{
           const box = document.querySelector('div[role="textbox"], [contenteditable="true"], .xat24cr');
           if (box) {{
              clearInterval(checkExist);
              startStriker();
           }}
        }}, 1000); 
    """)

def run_life_cycle(cookie, target_id, target_name):
    while True:
        driver = None
        try:
            log_status("🛠️ Initializing Stable Engine...")
            driver = get_driver()
            driver.get("https://www.instagram.com/")
            
            sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
            driver.add_cookie({'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com'})
            
            driver.get("https://www.instagram.com/accounts/edit/")
            time.sleep(5)
            if "login" in driver.current_url.lower():
                log_status("❌ FATAL: Cookie Expired.")
                sys.exit(1)
            
            log_status("✅ Session Validated. Opening Hyper-Tabs...")
            for _ in range(TABS_PER_AGENT):
                driver.execute_script(f"window.open('https://www.instagram.com/direct/t/{target_id}/', '_blank');")
                time.sleep(10) # ⏳ Increased stagger to 10s for slower IG loading

            handles = driver.window_handles[1:]
            for idx, h in enumerate(handles):
                inject_striker(driver, h, idx + 1, target_name)
            
            # The Python script stays alive while the JS fires
            time.sleep(PURGE_INTERVAL)
                
        except Exception as e:
            log_status(f"⚠️ Error: {e}")
            time.sleep(5)
        finally:
            if driver: driver.quit()
            gc.collect()

def main():
    cookie = os.environ.get("INSTA_COOKIE")
    target_id = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "PRVR")
    if not cookie or not target_id: return
    run_life_cycle(cookie, target_id, target_name)

if __name__ == "__main__":
    main()
