# This is the standalone file, use it

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

from bs4 import BeautifulSoup

html = """


<a href="https://fuckingfast.co/dnhw0b3z4aog#Sekiro_-_Shadows_Die_Twice_--_fitgirl-repacks.site_--_.part01.rar" target="_blank" rel="noopener nofollow">Sekiro_-_Shadows_Die_Twice_–_fitgirl-repacks.site_–_.part01.rar</a><br>
<a href="https://fuckingfast.co/nki97hj7jk5m#Sekiro_-_Shadows_Die_Twice_--_fitgirl-repacks.site_--_.part02.rar" target="_blank" rel="noopener nofollow">Sekiro_-_Shadows_Die_Twice_–_fitgirl-repacks.site_–_.part02.rar</a><br>
<a href="https://fuckingfast.co/2n7evz7yrfwc#Sekiro_-_Shadows_Die_Twice_--_fitgirl-repacks.site_--_.part03.rar" target="_blank" rel="noopener nofollow">Sekiro_-_Shadows_Die_Twice_–_fitgirl-repacks.site_–_.part03.rar</a><br>
<a href="https://fuckingfast.co/0oftyxrw9izj#Sekiro_-_Shadows_Die_Twice_--_fitgirl-repacks.site_--_.part04.rar" target="_blank" rel="noopener nofollow">Sekiro_-_Shadows_Die_Twice_–_fitgirl-repacks.site_–_.part04.rar</a><br>
<a href="https://fuckingfast.co/yd5szfnpnsqq#Sekiro_-_Shadows_Die_Twice_--_fitgirl-repacks.site_--_.part05.rar" target="_blank" rel="noopener nofollow">Sekiro_-_Shadows_Die_Twice_–_fitgirl-repacks.site_–_.part05.rar</a><br>
<a href="https://fuckingfast.co/ozqp17cgqgap#Sekiro_-_Shadows_Die_Twice_--_fitgirl-repacks.site_--_.part06.rar" target="_blank" rel="noopener nofollow">Sekiro_-_Shadows_Die_Twice_–_fitgirl-repacks.site_–_.part06.rar</a><br>
<a href="https://fuckingfast.co/8mbzr8rrajjl#Sekiro_-_Shadows_Die_Twice_--_fitgirl-repacks.site_--_.part07.rar" target="_blank" rel="noopener nofollow">Sekiro_-_Shadows_Die_Twice_–_fitgirl-repacks.site_–_.part07.rar</a><br>
<a href="https://fuckingfast.co/320afrg3li5s#Sekiro_-_Shadows_Die_Twice_--_fitgirl-repacks.site_--_.part08.rar" target="_blank" rel="noopener nofollow">Sekiro_-_Shadows_Die_Twice_–_fitgirl-repacks.site_–_.part08.rar</a><br>
<a href="https://fuckingfast.co/fzpp2h1hvwut#Sekiro_-_Shadows_Die_Twice_--_fitgirl-repacks.site_--_.part09.rar" target="_blank" rel="noopener nofollow">Sekiro_-_Shadows_Die_Twice_–_fitgirl-repacks.site_–_.part09.rar</a><br>
<a href="https://fuckingfast.co/a7w1cp9ug5ec#Sekiro_-_Shadows_Die_Twice_--_fitgirl-repacks.site_--_.part10.rar" target="_blank" rel="noopener nofollow">Sekiro_-_Shadows_Die_Twice_–_fitgirl-repacks.site_–_.part10.rar</a><br>
<a href="https://fuckingfast.co/u5h0lai23ygv#Sekiro_-_Shadows_Die_Twice_--_fitgirl-repacks.site_--_.part11.rar" target="_blank" rel="noopener nofollow">Sekiro_-_Shadows_Die_Twice_–_fitgirl-repacks.site_–_.part11.rar</a><br>
<a href="https://fuckingfast.co/anmh1xvm1a8z#Sekiro_-_Shadows_Die_Twice_--_fitgirl-repacks.site_--_.part12.rar" target="_blank" rel="noopener nofollow">Sekiro_-_Shadows_Die_Twice_–_fitgirl-repacks.site_–_.part12.rar</a><br>
<a href="https://fuckingfast.co/a56s278uia3s#Sekiro_-_Shadows_Die_Twice_--_fitgirl-repacks.site_--_.part13.rar" target="_blank" rel="noopener nofollow">Sekiro_-_Shadows_Die_Twice_–_fitgirl-repacks.site_–_.part13.rar</a><br>
<a href="https://fuckingfast.co/2dlb7skgvj2w#Sekiro_-_Shadows_Die_Twice_--_fitgirl-repacks.site_--_.part14.rar" target="_blank" rel="noopener nofollow">Sekiro_-_Shadows_Die_Twice_–_fitgirl-repacks.site_–_.part14.rar</a><br>
<a href="https://fuckingfast.co/4sk0wp8qal9o#Sekiro_-_Shadows_Die_Twice_--_fitgirl-repacks.site_--_.part15.rar" target="_blank" rel="noopener nofollow">Sekiro_-_Shadows_Die_Twice_–_fitgirl-repacks.site_–_.part15.rar</a><br>
<a href="https://fuckingfast.co/e3i6zkwelhf9#fg-optional-bonus-content.bin" target="_blank" rel="noopener nofollow">fg-optional-bonus-content.bin</a><br>
<a href="https://fuckingfast.co/xlxrh5tc3epj#fg-selective-english.bin" target="_blank" rel="noopener nofollow">fg-selective-english.bin</a><br>
<a href="https://fuckingfast.co/hmfjqo5ai0sr#fg-selective-japanese.bin" target="_blank" rel="noopener nofollow">fg-selective-japanese.bin</a><br>

"""

def wait_for_downloads(download_dir, timeout=600):
    """
    Wait until all Chrome downloads in download_dir are complete.
    First waits for download to start, then waits for it to finish.
    """
    print("Waiting for download to start...")
    seconds = 0
    
    # First, wait for download to actually start (crdownload file appears)
    download_started = False
    while not download_started and seconds < 30:
        if any(f.endswith(".crdownload") for f in os.listdir(download_dir)):
            download_started = True
            print("Download started, monitoring progress...")
            break
        time.sleep(0.5)
        seconds += 0.5
    
    if not download_started:
        print("Download never started within 30 seconds.")
        return False
    
    # Now wait for download to complete with progress tracking
    last_size = 0
    stall_count = 0
    start_time = time.time()
    
    while seconds < timeout:
        crdownload_files = [f for f in os.listdir(download_dir) if f.endswith(".crdownload")]
        
        if not crdownload_files:
            elapsed_time = time.time() - start_time
            print(f"Download completed successfully in {elapsed_time:.1f} seconds.")
            return True
        
        # Enhanced progress tracking with speed calculation
        if crdownload_files:
            current_file = os.path.join(download_dir, crdownload_files[0])
            try:
                current_size = os.path.getsize(current_file)
                if current_size == last_size:
                    stall_count += 1
                    if stall_count > 30:  # 60 seconds of no progress
                        print("Download appears stalled. Moving on...")
                        return False
                else:
                    stall_count = 0
                    # Calculate download speed
                    elapsed = time.time() - start_time
                    speed_mbps = (current_size * 8) / (1024 * 1024 * elapsed) if elapsed > 0 else 0
                    print(f"Progress: {current_size / (1024*1024):.1f} MB | Speed: {speed_mbps:.1f} Mbps")
                last_size = current_size
            except:
                pass
        
        time.sleep(2)
        seconds += 2
    
    print("Timeout waiting for downloads to complete.")
    return False


soup = BeautifulSoup(html, "html.parser")
links = [a['href'] for a in soup.find_all('a', href=True)]

DOWNLOADS = r"C:\Users\Divyanshu\Saved Games\Sekiro"
if not os.path.exists(DOWNLOADS):
    os.mkdir(DOWNLOADS)

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": DOWNLOADS,
    "download.prompt_for_download": False,
    "profile.default_content_setting_values.automatic_downloads": 1
})
# Helps bypass some basic "Dummy" redirects
chrome_options.add_argument("--disable-blink-features=AutomationControlled") 

driver = webdriver.Chrome(options=chrome_options)
main_handle = driver.current_window_handle

try:
    # Starting from 0 to process all links (adjust if you need to skip)
    for i, link in enumerate(links, start=1):
        print(f"\n[Part {i}/{len(links)}] Loading: {link}")
        
        driver.get(link)
        
        # --- ANTI-DUMMY LOGIC ---
        # 1. Close any pop-up tabs that opened instantly
        for handle in driver.window_handles:
            if handle != main_handle:
                driver.switch_to.window(handle)
                driver.close()
        driver.switch_to.window(main_handle)

        # 2. Verify we aren't on a dummy redirect page
        if "fuckingfast.co" not in driver.current_url:
            print("Redirected to dummy site. Re-navigating...")
            driver.get(link)
            time.sleep(2)

        try:
            # 3. Use your original button logic
            # We wait up to 20s because some parts take time to "generate"
            wait = WebDriverWait(driver, 20)
            
            # Original XPath from your first script
            download_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[1]/button'))
            )
            
            # Clear overlays just in case (prevents "Click Intercepted" errors)
            driver.execute_script("document.querySelectorAll('div[style*=\"z-index\"]').forEach(el => el.remove());")
            
            # Perform the click
            driver.execute_script("arguments[0].click();", download_button)
            print(f"Button clicked for part {i}")
            
            # 4. Monitor the download progress
            if wait_for_downloads(DOWNLOADS):
                print(f"Part {i} finished.")
            else:
                print(f"Part {i} failed or timed out.")
                
        except Exception as e:
            print(f"Skip/Error on Part {i}: {e}")
            
        time.sleep(2) # Short breather between parts

finally:
    driver.quit()
    print("\nAll tasks finished.")



