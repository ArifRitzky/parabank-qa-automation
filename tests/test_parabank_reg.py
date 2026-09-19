from selenium.webdriver.common.by import By
import time
import random

# Fungsi menerima "driver" dari luar
def test_registrasi_parabank(driver):
    try:
        driver.get("https://parabank.parasoft.com/parabank/register.htm")
        time.sleep(2)
        
        username_tester = f"qa_tester_{random.randint(1000, 9999)}"
        password_tester = "Password123!"
        
        driver.find_element(By.ID, "customer.firstName").send_keys("Budi")
        driver.find_element(By.ID, "customer.lastName").send_keys("QA")
        driver.find_element(By.ID, "customer.address.street").send_keys("Jl. Sudirman No 1")
        driver.find_element(By.ID, "customer.address.city").send_keys("Jakarta")
        driver.find_element(By.ID, "customer.address.state").send_keys("DKI")
        driver.find_element(By.ID, "customer.address.zipCode").send_keys("12345")
        driver.find_element(By.ID, "customer.phoneNumber").send_keys("08123456789")
        driver.find_element(By.ID, "customer.ssn").send_keys("32010123")
        
        driver.find_element(By.ID, "customer.username").send_keys(username_tester)
        driver.find_element(By.ID, "customer.password").send_keys(password_tester)
        driver.find_element(By.ID, "repeatedPassword").send_keys(password_tester)
        time.sleep(2)
        
        driver.find_element(By.CSS_SELECTOR, "input[value='Register']").click()
        time.sleep(3)
        
        if "Your account was created successfully" in driver.page_source:
            return {
                "status": "PASS", 
                "message": f"Registrasi Berhasil! Username: {username_tester}",
                "data": {"username": username_tester, "password": password_tester}
            }
        else:
            # Mengarahkan screenshot ke folder screenshots saat FAIL
            nama_file = f"screenshots/fail_reg_{int(time.time())}.png"
            driver.save_screenshot(nama_file)
            return {"status": "FAIL", "message": f"Validasi gagal. Bukti: {nama_file}", "data": None}
        
    except Exception as e:
        # Mengarahkan screenshot ke folder screenshots saat ERROR
        nama_file = f"screenshots/error_reg_{int(time.time())}.png"
        driver.save_screenshot(nama_file)
        return {"status": "ERROR", "message": f"Skrip terhenti: {str(e)} | Bukti: {nama_file}", "data": None}