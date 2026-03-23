# -*- coding: utf-8 -*-
# 🚀 PHOENIX V100.70 (PRVR-HYPER-INJECT)
# ⚡ SPEED: 180ms NATIVE JS PULSE | 5 TABS SIMULTANEOUS
# 🛡️ STABILITY: TAB-SPECIFIC LOGGING & COUNTER

import os, time, datetime, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ HYPER-INJECT CONFIG ---
TABS_PER_MACHINE = 5  
PULSE_DELAY = 180      
REFRESH_TIMER = 600    # 10 Minutes

def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.page_load_strategy = 'eager'
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_experimental_option("mobileEmulation", {"deviceName": "iPad Pro"})
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(options=options, service=service)

def inject_engine(driver, handle, tab_index, target_name, pulse):
    try:
        driver.switch_to.window(handle)
        driver.execute_script(f"""
            const targetName = "{target_name}";
            const emojis = ["👑", "⚡", "🔥", "🦈", "🦁", "💎", "⚔️", "🔱", "🧿", "🌪️", "🐍", "🦍"];
            
            if (window.prvrEngine) clearInterval(window.prvrEngine);

            window.prvrEngine = setInterval(() => {{
                const box = document.querySelector('div[role="textbox"], [contenteditable="true"]');
                if (box) {{
                    const emoji = emojis[Math.floor(Math.random() * emojis.length)];
                    const salt = Math.random().toString(36).substring(7).toUpperCase();
                    
                    const line = `【 ${{targetName}} 】 SAY P R V R बाप ${{emoji}} __________/`;
                    const block = Array(22).fill(line).join('\\n');
                    const finalText = block + "\\n⚡ TRACE-ID: " + salt;

                    box.focus();
                    document.execCommand('insertText', false, finalText);
                    box.dispatchEvent(new Event('input', {{ bubbles: true }}));

                    const sendBtn = document.querySelector('div.xjyslct');
                    if (sendBtn) {{
                        sendBtn.click();
                    }} else {{
                        const enter = new KeyboardEvent('keydown', {{
                            bubbles: true, cancelable: true, key: 'Enter', keyCode: 13
                        }});
                        box.dispatchEvent(enter);
                    }}
                    setTimeout(() => {{ if(box) box.innerHTML = ""; }}, 40);
                }}
            }}, {pulse});
        """)
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ✅ Tab {tab_index}: Engine Sync Success.")
    except Exception as e:
        print(f"⚠️ Tab {tab_index}: Injection Failed -> {e}")

def main():
    cookie = os.environ.get("INSTA_COOKIE")
    target = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "PRVR")
    
    if not cookie or not target:
        print("❌ CRITICAL: Secrets Missing")
        return

    driver = get_driver()
    start_time = time.time()
    
    try:
        driver.get("https://www.instagram.com/")
        driver.add_cookie({'name': 'sessionid', 'value': cookie.strip(), 'domain': '.instagram.com'})
        
        print(f"🚀 Launching {TABS_PER_MACHINE} Simultaneous Streams...")
        for i in range(TABS_PER_MACHINE):
            driver.execute_script(f"window.open('https://www.instagram.com/direct/t/{target}/', '_blank');")
            time.sleep(8) 

        handles = driver.window_handles[1:] 
        
        for idx, handle in enumerate(handles):
            inject_engine(driver, handle, idx + 1, target_name, PULSE_DELAY)

        while True:
            time.sleep(REFRESH_TIMER)
            uptime_min = int((time.time() - start_time) / 60)
            # Estimate: (60 seconds / 0.18 pulse) * 5 tabs * uptime
            total_est = int((60 / (PULSE_DELAY/1000)) * TABS_PER_MACHINE * uptime_min)
            
            print(f"\n📊 STATS: Uptime {uptime_min}m | Estimated Sent: {total_est}")
            print(f"♻️ Maintenance: Refreshing all 5 tabs...")
            
            for idx, handle in enumerate(handles):
                try:
                    driver.switch_to.window(handle)
                    driver.refresh()
                    time.sleep(12) 
                    inject_engine(driver, handle, idx + 1, target_name, PULSE_DELAY)
                except: continue

    except Exception as e:
        print(f"⚠️ Fatal: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
