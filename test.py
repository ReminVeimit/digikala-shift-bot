import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

# --- تنظیمات شما ---
# روزهایی که می‌خواهید شیفت بردارید را اینجا بنویسید
MY_PREFERRED_DAYS = ["شنبه", "دوشنبه", "چهارشنبه"] 
# ------------------

def setup_driver():
    chrome_options = Options()
    # استفاده از پروفایل شخصی برای لاگین ماندن (مسیر پیش‌فرض ویندوز)
    user_data = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data')
    chrome_options.add_argument(f"user-data-dir={user_data}")
    chrome_options.add_argument("profile-directory=Default")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def run_bot():
    driver = setup_driver()
    driver.get("https://inshift.digikala.com/jobs")
    
    print("ربات شروع به کار کرد...")
    
    while True:
        try:
            driver.refresh()
            time.sleep(4) # فاصله برای جلوگیری از بلاک شدن
            
            # جستجو برای کارت‌های شیفت در صفحه
            shifts = driver.find_elements(By.CLASS_NAME, "shift-card") # کلاس را با Inspect چک کنید
            
            for shift in shifts:
                # بررسی اینکه آیا نام روز در کارت شیفت وجود دارد یا خیر
                for day in MY_PREFERRED_DAYS:
                    if day in shift.text:
                        reserve_btn = shift.find_element(By.TAG_NAME, "button")
                        reserve_btn.click()
                        print(f"شیفت {day} رزرو شد!")
                        # بعد از رزرو، می‌تونید break کنید یا ادامه بدید
                        
        except Exception as e:
            print("در حال جستجو برای شیفت‌های جدید...")
            time.sleep(2)

if __name__ == "__main__":
    run_bot()
