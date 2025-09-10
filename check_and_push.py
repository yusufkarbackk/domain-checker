# check_and_push.py

import whois
import requests
from datetime import datetime

# --- KONFIGURASI ---
# Ganti dengan nama domain yang ingin Anda cek
DOMAIN_TO_CHECK = "mybaticloud.com"

# Ganti dengan URL LENGKAP yang Anda dapatkan dari Uptime Kuma
# Pastikan Anda menyalinnya dengan benar!
UPTIME_KUMA_PUSH_URL = "http://localhost:3001/api/push/S7BGLhSPhL"

# Ambang batas hari untuk status menjadi "down" (misal: 30 hari)
ALERT_THRESHOLD_DAYS = 30
# --- SELESAI KONFIGURASI ---


def main():
    """
    Fungsi utama untuk cek domain dan kirim status ke Uptime Kuma.
    """
    try:
        # Lakukan lookup WHOIS
        domain_info = whois.whois(DOMAIN_TO_CHECK)

        # Ambil tanggal kedaluwarsa
        exp_date = domain_info.expiration_date
        if isinstance(exp_date, list):
            exp_date = exp_date[0]

        # Hitung sisa hari
        remaining_days = (exp_date - datetime.now()).days
        exp_date_str = exp_date.strftime("%Y-%m-%d")

        # Tentukan status dan pesan
        if remaining_days > ALERT_THRESHOLD_DAYS:
            status = "up"
            message = (
                f"AMAN - Kedaluwarsa pada {exp_date_str} ({remaining_days} hari lagi)"
            )
        else:
            status = "down"  # Status akan merah jika sisa hari <= 30
            message = f"PERINGATAN - Kedaluwarsa pada {exp_date_str} ({remaining_days} hari lagi!)"

    except Exception as e:
        status = "down"
        message = f"Error: Gagal memeriksa domain - {e}"

    # Siapkan URL akhir untuk di-push ke Uptime Kuma
    final_push_url = (
        f"{UPTIME_KUMA_PUSH_URL}?status={status}&msg={requests.utils.quote(message)}"
    )

    # Kirim status ke Uptime Kuma
    try:
        print(f"Mengirim status ke Kuma: {message}")
        response = requests.get(final_push_url)
        response.raise_for_status()  # Akan error jika status code bukan 200
        print("Berhasil mengirim status.")
    except requests.exceptions.RequestException as e:
        print(f"Gagal mengirim status ke Uptime Kuma: {e}")


if __name__ == "__main__":
    main()
