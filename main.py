# main.py

import whois
from fastapi import FastAPI, HTTPException
from datetime import datetime

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Definisikan ambang batas hari untuk peringatan (misal: 30 hari)
ALERT_THRESHOLD_DAYS = 30


@app.get("/check")
def check_domain_expiry(domain: str):
    """
    Endpoint untuk memeriksa masa berlaku domain.
    """
    if not domain:
        raise HTTPException(
            status_code=400, detail="Parameter 'domain' tidak boleh kosong."
        )

    try:
        # Lakukan lookup WHOIS
        domain_info = whois.whois(domain)

        # Cek apakah ada tanggal kedaluwarsa
        if not domain_info.expiration_date:
            raise HTTPException(
                status_code=404,
                detail=f"Tidak dapat menemukan tanggal kedaluwarsa untuk {domain}.",
            )

        # WHOIS kadang mengembalikan list, jadi kita ambil elemen pertama jika itu list
        exp_date = domain_info.expiration_date
        if isinstance(exp_date, list):
            exp_date = exp_date[0]

        # Hitung sisa hari
        remaining_days = (exp_date - datetime.now()).days

        # Tentukan status berdasarkan ambang batas
        status = "AMAN"
        if remaining_days <= ALERT_THRESHOLD_DAYS:
            status = "SEGERA_PERPANJANG"

        # Kembalikan hasil dalam format JSON
        return {
            "domain": domain,
            "expiration_date": exp_date.strftime("%Y-%m-%d"),
            "days_remaining": remaining_days,
            "status": status,
            "last_checked": datetime.now().isoformat(),
        }

    except Exception as e:
        # Tangani error jika domain tidak ditemukan atau TLD tidak didukung
        raise HTTPException(status_code=500, detail=f"Terjadi error: {str(e)}")
