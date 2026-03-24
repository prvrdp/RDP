# -*- coding: utf-8 -*-
# 🚀 PHOENIX V100.40 (JS-HYPER-INJECT + DYNAMIC BLOCKS)
# ⚡ SPEED: 100ms NATIVE JS PULSE | 5 TABS PER RUNNER

import os, time, random, sys, re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- ⚡ CONFIG ---
TABS_PER_MACHINE = 5  
PULSE_DELAY = 100  # 100ms - 120ms stable range

def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.page_load_strategy = 'eager'
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--blink-settings=imagesEnabled=false")
    
    # iPad Pro emulation for the fastest Lexical DOM response
    options.add_experimental_option("mobileEmulation", {"deviceName": "iPad Pro"})
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(options=options, service=service)

def main():
    cookie = os.environ.get("INSTA_COOKIE")
    target = os.environ.get("TARGET_THREAD_ID")
    target_name = os.environ.get("TARGET_NAME", "EZRA")
    machine_id = os.environ.get("MACHINE_ID", "1")

    if not cookie or not target:
        print("❌ Missing Secrets!")
        return

    driver = get_driver()
    try:
        # 1. Login Handshake
        driver.get("https://www.instagram.com/")
        sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
        driver.add_cookie({'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com'})
        
        # 2. Launch Hyper-Tabs
        print(f"🚀 MACHINE {machine_id}: Launching {TABS_PER_MACHINE} Hyper-Tabs for {target_name}...")
        for i in range(TABS_PER_MACHINE):
            driver.execute_script(f"window.open('https://www.instagram.com/direct/t/{target}/', '_blank');")
            time.sleep(5) # Stagger for DOM hydration

        handles = driver.window_handles[1:] 
        
        # 3. ⚡ THE INJECTION: Deploy High-Speed Block Engine
        for handle in handles:
            driver.switch_to.window(handle)
            driver.execute_script("""
                const name = arguments[0];
                const delay = arguments[1];
                
                function getBlock(targetName) {
                    const emojis = ["👑", "⚡", "🔥", "🦈", "🦁", "💎", "⚔️", "🔱", "🧿", "🌪️", "🐍", "🦍"];
                    const emo = emojis[Math.floor(Math.random() * emojis.length)];
                    const line = `【 ${targetName} 】 SAY P R V R बाप ${emo} ____________________/`;
                    let fullBlock = "";
                    for(let i=0; i<20; i++) { fullBlock += line + "\\n"; }
                    return fullBlock + "\\n⚡ ID: " + Math.random().toString(36).substring(7);
                }

                console.log("🚀 JS-BLOCK-ENGINE DEPLOYED");
                
                setInterval(() => {
                    const box = document.querySelector('div[role="textbox"], [contenteditable="true"]');
                    if (box) {
                        const finalText = getBlock(name);

                        // High-Speed Lexical Injection
                        box.focus();
                        document.execCommand('insertText', false, finalText);
                        box.dispatchEvent(new Event('input', { bubbles: true }));

                        // Native Keyboard Dispatch
                        const enter = new KeyboardEvent('keydown', {
                            bubbles: true, cancelable: true, key: 'Enter', code: 'Enter', keyCode: 13
                        });
                        box.dispatchEvent(enter);

                        // Prevent DOM heavy-load (Instant Clear)
                        setTimeout(() => { if(box.innerHTML.length > 0) box.innerHTML = ""; }, 2);
                    }
                }, delay);
            """, target_name, PULSE_DELAY)
        
        print(f"🔥 MACHINE {machine_id}: {TABS_PER_MACHINE} TABS FIRING BLOCKS AT {PULSE_DELAY}ms.")
        
        # 4. Keep alive and monitor
        while True:
            time.sleep(60)
            driver.switch_to.window(handles[0])
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    except Exception as e:
        print(f"⚠️ FATAL: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
