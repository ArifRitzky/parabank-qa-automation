from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from selenium import webdriver
import time

from tests.test_parabank_reg import test_registrasi_parabank
from tests.test_parabank_login import test_login_parabank

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run-test")
def trigger_all_tests():
    # 1. Manajer membuka Chrome SATU KALI saja
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    semua_laporan = []
    
    try:
        # 2. Menyuruh pekerja pertama jalan dengan memberikan 'driver'
        hasil_reg = test_registrasi_parabank(driver)
        
        semua_laporan.append({
            "id": "TC-REG-01",
            "modul": "Registrasi (CIF)",
            "status": hasil_reg["status"],
            "message": hasil_reg["message"]
        })
        
        # 3. Cek apakah Registrasi sukses? Jika ya, lanjut Login!
        if hasil_reg["status"] == "PASS":
            user_baru = hasil_reg["data"]["username"]
            pass_baru = hasil_reg["data"]["password"]
            
            hasil_login = test_login_parabank(driver, user_baru, pass_baru)
            
            semua_laporan.append({
                "id": "TC-LOG-01",
                "modul": "Login System",
                "status": hasil_login["status"],
                "message": hasil_login["message"]
            })
        else:
            semua_laporan.append({
                "id": "TC-LOG-01",
                "modul": "Login System",
                "status": "SKIPPED",
                "message": "Dilewati karena Registrasi gagal."
            })
            
    finally:
        # 4. Manajer menutup Chrome
        time.sleep(2)
        driver.quit()
        
    return semua_laporan