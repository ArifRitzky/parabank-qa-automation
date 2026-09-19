from selenium.webdriver.common.by import By
import time

def test_login_parabank(driver, username, password):
    try:
        # Bersihkan semua sesi/cookies agar web kembali ke mode "belum login"
        driver.delete_all_cookies()
        
        # Navigate to home/login page
        driver.get("https://parabank.parasoft.com/parabank/index.htm")
        time.sleep(2)
        
        # Input credentials
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        time.sleep(1)
        
        # Execute login
        driver.find_element(By.CSS_SELECTOR, "input[value='Log In']").click()
        time.sleep(3)
        
        # Return structured outcome to API
        if "Log Out" in driver.page_source:
            return {"status": "PASS", "message": f"Login Berhasil untuk user: {username}"}
        # (kode sebelumnya...)
        else:
            # Arahkan ke folder screenshots
            nama_file = f"screenshots/fail_login_{int(time.time())}.png"
            driver.save_screenshot(nama_file)
            return {"status": "FAIL", "message": f"Login gagal. Bukti: {nama_file}"}
            
    except Exception as e:
        # Arahkan ke folder screenshots
        nama_file = f"screenshots/error_login_{int(time.time())}.png"
        driver.save_screenshot(nama_file)
        return {"status": "ERROR", "message": f"Skrip terhenti: {str(e)} | Bukti: {nama_file}"}