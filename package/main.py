# main.py

import whois
from fastapi import FastAPI, HTTPException
from datetime import datetime
from mangum import Mangum  # <-- TAMBAHKAN BARIS INI

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Definisikan ambang batas hari untuk peringatan (misal: 30 hari)
ALERT_THRESHOLD_DAYS = 30

@app.get("/check")
def check_domain_expiry(domain: str):
    # ... (TIDAK ADA PERUBAHAN DI DALAM FUNGSI INI) ...
    if not domain:
        raise HTTPException(status_code=400, detail="Parameter 'domain' tidak boleh kosong.")
    try:
        domain_info = whois.whois(domain)
        if not domain_info.expiration_date:
            raise HTTPException(status_code=404, detail=f"Tidak dapat menemukan tanggal kedaluwarsa untuk {domain}.")
        exp_date = domain_info.expiration_date
        if isinstance(exp_date, list):
            exp_date = exp_date[0]
        remaining_days = (exp_date - datetime.now()).days
        status = "AMAN"
        if remaining_days <= ALERT_THRESHOLD_DAYS:
            status = "SEGERA_PERPANJANG"
        return {
            "domain": domain,
            "expiration_date": exp_date.strftime("%Y-%m-%d"),
            "days_remaining": remaining_days,
            "status": status,
            "last_checked": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi error: {str(e)}")

# ↓↓↓ TAMBAHKAN BARIS INI DI PALING BAWAH ↓↓↓
handler = Mangum(app)