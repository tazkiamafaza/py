# ================= DATA (EDIT DI SINI) =================
judul1 = "Sistem Analisis Risiko Lingkungan Perkotaan"
judul2 = "Berdasarkan Kualitas Udara dan Timbunan Sampah di Indonesia"
kelompok = "Kelompok 7C"
asisten = "Faiza Mumtaz & Badra Allam Zonta"
dosen = "Asmuliardi Muluk, S.T., M.T."
tahun = "2026"
# =======================================================

LEBAR = 90  # lebar kertas (makin besar, makin lebar)


def baris(teks=""):
    # mencetak 1 baris di tengah, dengan garis | di kiri dan kanan
    print("|" + teks.center(LEBAR) + "|")


print("+" + "-" * LEBAR + "+")   # garis atas

baris()
baris()
baris()

# ---------- Judul ----------
baris("MINI PROJECT")
baris()
baris("PEMROGRAMAN KOMPUTER")
baris()
baris("(" + judul1)
baris(judul2 + ")")
baris()
baris()

# ---------- Kelompok ----------
baris("Oleh :")
baris()
baris(kelompok)
baris()
baris()

# ---------- Anggota ----------
baris("Anggota :")
baris()
baris("Khairunnisak             2610931027")
baris("Kayyisah Hulwatul Aini   2610932002")
baris("Monika Dwifa             2610933016")
baris("Tazkia Mafaza            2610933028")
baris()
baris()
baris()

# ---------- Asisten ----------
baris("Asisten Pembimbing :")
baris()
baris(asisten)
baris()
baris()
baris()

# ---------- Dosen ----------
baris("Dosen Pengampu :")
baris()
baris(dosen)
baris()
baris()
baris()
baris()

# ---------- Institusi ----------
baris("LABORATORIUM SISTEM INFORMASI DAN KEPUTUSAN")
baris("DEPARTEMEN TEKNIK INDUSTRI")
baris("FAKULTAS TEKNIK")
baris("UNIVERSITAS ANDALAS")
baris(tahun)

baris()
baris()
baris()

print("+" + "-" * LEBAR + "+")   # garis bawah

import csv
import os
import math

# Path file CSV menggunakan raw string (r"...")
file_csv = r"d:\KULIAH\PRAK PROKOM\MINI PROJECT\data_pemantauan_lingkungan.csv"

class AnalisisLingkungan:
    def __init__(self, file_csv=None):
        self.file_csv = file_csv if file_csv is not None else globals()["file_csv"]
        self.kolom_wajib = [
            "id_stasiun",
            "lokasi",
            "sumber_emisi_dominan",
            "indeks_kualitas_udara_aqi",
            "konsentrasi_pm25",
            "estimasi_sampah_harian_kg",
            "status_risiko_lingkungan",
        ]

    
    def baca_dan_validasi_csv(self):
        # 1. Cek apakah file CSV ada
        if not os.path.exists(self.file_csv):
            print(f"\n[ERROR] File CSV tidak ditemukan di: {self.file_csv}")
            return []

        data_valid = []

        # 2. Buka file CSV dengan delimiter titik koma (;) sesuai file
        with open(self.file_csv, mode="r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file, delimiter=";")

            # 3. Validasi header dan kolom wajib
            if not reader.fieldnames:
                print("\n[ERROR] Dataset tidak memiliki header!")
                return []

            for kolom in self.kolom_wajib:
                if kolom not in reader.fieldnames:
                    print(f"\n[ERROR] Kolom wajib '{kolom}' tidak ditemukan!")
                    print(f"Kolom tersedia: {reader.fieldnames}")
                    return []

            # 4. Baca dan validasi setiap baris mulai dari baris ke-2
            for nomor_baris, row in enumerate(reader, start=2):
                try:
                    id_stasiun = row["id_stasiun"].strip()
                    lokasi = row["lokasi"].strip()
                    sumber_emisi = row["sumber_emisi_dominan"].strip()
                    status_risiko = row["status_risiko_lingkungan"].strip()

                    aqi = float(row["indeks_kualitas_udara_aqi"])
                    pm25 = float(row["konsentrasi_pm25"])
                    sampah = float(row["estimasi_sampah_harian_kg"])

                    if id_stasiun == "" or lokasi == "":
                        print(f"Baris {nomor_baris} dilewati: ID stasiun atau lokasi kosong.")
                        continue

                    if aqi < 0 or pm25 < 0 or sampah < 0:
                        print(f"Baris {nomor_baris} dilewati: Nilai tidak boleh negatif.")
                        continue

                    data_valid.append({
                        "id_stasiun": id_stasiun,
                        "lokasi": lokasi,
                        "sumber_emisi": sumber_emisi,
                        "aqi": aqi,
                        "pm25": pm25,
                        "sampah": sampah,
                        "status_risiko": status_risiko,
                    })

                except ValueError:
                    print(f"Baris {nomor_baris} dilewati: Format angka tidak valid.")
                    continue

        return data_valid

    def proses_semua_lokasi(self, data_valid):
        if len(data_valid) == 0:
            print("\nTidak ada data valid yang dapat dianalisis.")
            return []
        
        # Mengelompokkan dan menjumlahkan nilai berdasarkan lokasi
        rekap_lokasi = {}
        daftar_lokasi = []

        for row in data_valid:
            lokasi = row["lokasi"]
            
            if lokasi not in rekap_lokasi:
                rekap_lokasi[lokasi] = {
                    "total_aqi": 0.0,
                    "jumlah_data" : 0,
                    "risiko_rendah": 0,
                    "total_pm25": 0.0,
                    "jumlah_data": 0,
                    "risiko_rendah": 0,
                }

            rekap_lokasi[lokasi]["total_aqi"] += row["aqi"]
            rekap_lokasi[lokasi]["total_pm25"] += row["pm25"]
            rekap_lokasi[lokasi]["jumlah_data"] += 1

            if row["status_risiko"].lower() == "rendah":
                rekap_lokasi[lokasi]["risiko_rendah"] += 1

        for lokasi, info in rekap_lokasi.items():
            n = info["jumlah_data"]

            # Menghitung rata-rata
            rata_aqi = info["total_aqi"] / n
            rata_pm25 = info["total_pm25"] / n

            # Menghitung variand AQI
            varians_aqi = sum((row["aqi"] - rata_aqi) ** 2 for row in data_valid if row["lokasi"] == lokasi) / n

            # Menghitung standar deviasi AQI
            std_dev_aqi = math.sqrt(varians_aqi)

            # Menentukan kategori kualitas udara
            if rata_aqi <= 50:
                kategori = "Baik (Sangat Segar)"
            elif rata_aqi <= 100:
                kategori = "Sedang (Cukup Nyaman)"
            else:
                kategori = "Kurang Sehat (Tinggi)"

            daftar_lokasi.append({
                    "lokasi": lokasi,
                    "rata_aqi": rata_aqi,
                    "rata_pm25": rata_pm25,
                    "risiko_rendah": info["risiko_rendah"],
                    "jumlah_data": n,
                    "kategori": kategori,
                    "varians_aqi": varians_aqi,
                    "std_dev_aqi": std_dev_aqi
                })

            # Mengurutkan dari rata-rata AQI terkecil ke terbesar
            jumlah_lokasi = len(daftar_lokasi)
        for i in range(jumlah_lokasi):
            for j in range(0, jumlah_lokasi - i - 1):
                if daftar_lokasi[j]["rata_aqi"] > daftar_lokasi[j + 1]["rata_aqi"]:
                    sementara = daftar_lokasi[j]
                    daftar_lokasi[j] = daftar_lokasi[j + 1]
                    daftar_lokasi[j + 1] = sementara

        return daftar_lokasi

    def tampilkan_hasil_analisis(self, tujuan_user="", sedang_sakit=False):
        """Menampilkan ringkasan AQI untuk satu lokasi atau seluruh lokasi."""
        data_valid = self.baca_dan_validasi_csv()
        hasil_lokasi = self.proses_semua_lokasi(data_valid)

        if len(hasil_lokasi) == 0:
            print("\nTidak ada data valid yang dapat dianalisis.")
            return

        print("\nASISTEN: Baik, sebentar saya proses data lingkungan dan menghitung rata-rata indeks AQI...")

        if tujuan_user != "":
            ditemukan = False
            for k in hasil_lokasi:
                if tujuan_user.lower() in k["lokasi"].lower():
                    ditemukan = True
                    print(f"\n--- INFO LOKASI TUJUAN KAMU: {k['lokasi'].upper()} ---")
                    print(f"Rata-rata Indeks Kualitas Udara (AQI) : {k['rata_aqi']:.2f} ({k['kategori']})")
                    print(f"Rata-rata Konsentrasi PM2.5           : {k['rata_pm25']:.2f}")
                    print(f"Titik Stasiun Risiko Rendah           : {k['risiko_rendah']} dari {k['jumlah_data']} stasiun")
                    if sedang_sakit and k["rata_aqi"] > 100:
                        print("Peringatan Kesehatan: Kamu sedang sakit dan lokasi ini memiliki AQI tinggi, harap berhati-hati!")
                    break
            if not ditemukan:
                print(f"\nASISTEN: Lokasi '{tujuan_user}' tidak tercatat spesifik di CSV. Berikut data lokasi yang tersedia:")
        else:
            print(f"\nTABEL RATA-RATA INDEKS KUALITAS UDARA (AQI) SELURUH LOKASI ({len(hasil_lokasi)} LOKASI):")
            print("=" * 115)
            print(f"{'No':<4} {'Lokasi / Lokasi':<18} {'Rata-rata AQI':<15}"
                  f"{'Varians AQI':<12} {'Std Dev AQI':<12} {'Rata PM2.5':<12} {'Status Udara'}")
            print("=" * 115)
            for i, k in enumerate(hasil_lokasi, start=1):
                print(f"{i:<4} {k['lokasi']:<18} {k['rata_aqi']:<15.2f} {k['varians_aqi']:<12.2f} {k['std_dev_aqi']:<12.2f} {k['rata_pm25']:<12.2f} {k['kategori']}")

                print("\n--- ANALISIS STATISTIK KUALITAS UDARA ---")
                print(f"varians AQI : {k['varians_aqi']:.2f}")
                print(f"standar deviasi AQI : {k['std_dev_aqi']:.2f}")
                print(f"variansi PM2.5 : {k['varians_pm25']:.2f}")
                print(f"standar deviasi PM2.5 : {k['std_dev_pm25']:.2f}")

        print("=" * 115)
        lokasi_tertinggi = hasil_lokasi[-1]
        print(f"Catatan: Sebaiknya hindari lokasi {lokasi_tertinggi['lokasi']} karena rata-rata AQI-nya paling tinggi yaitu {lokasi_tertinggi['rata_aqi']:.2f} ({lokasi_tertinggi['kategori']}).")
        print("-" * 115)
        print("ASISTEN: Selesai! Silakan pilih menu '6' jika ingin keluar dari program.")


def proses_semua_lokasi(data_valid):
    if len(data_valid) == 0:
        print("\nTidak ada data valid yang dapat dianalisis.")
        return []

    # Kelompokkan dan jumlahkan nilai berdasarkan lokasi
    rekap_lokasi = {}
    for row in data_valid:
        lokasi = row["lokasi"]
        if lokasi not in rekap_lokasi:
            rekap_lokasi[lokasi] = {
                "total_aqi": 0.0,
                "total_pm25": 0.0,
                "jumlah_data": 0,
                "risiko_rendah": 0,
            }

        rekap_lokasi[lokasi]["total_aqi"] += row["aqi"]
        rekap_lokasi[lokasi]["total_pm25"] += row["pm25"]
        rekap_lokasi[lokasi]["jumlah_data"] += 1

        if row["status_risiko"].lower() == "rendah":
            rekap_lokasi[lokasi]["risiko_rendah"] += 1

    # Hitung rata-rata AQI & PM2.5 untuk SEMUA lokasi
    daftar_lokasi = []
    for lokasi, info in rekap_lokasi.items():
        n = info["jumlah_data"]
        rata_aqi = info["total_aqi"] / n
        rata_pm25 = info["total_pm25"] / n

        if rata_aqi <= 50:
            kategori = "Baik (Sangat Segar)"
        elif rata_aqi <= 100:
            kategori = "Sedang (Cukup Nyaman)"
        else:
            kategori = "Kurang Sehat (Tinggi)"

        daftar_lokasi.append({
            "lokasi": lokasi,
            "rata_aqi": rata_aqi,
            "rata_pm25": rata_pm25,
            "risiko_rendah": info["risiko_rendah"],
            "jumlah_data": n,
            "kategori": kategori,
        })

    # Urutkan dari rata-rata AQI terkecil ke terbesar
    jumlah_lokasi = len(daftar_lokasi)
    for i in range(jumlah_lokasi):
        for j in range(0, jumlah_lokasi - i - 1):
            if daftar_lokasi[j]["rata_aqi"] > daftar_lokasi[j + 1]["rata_aqi"]:
                sementara = daftar_lokasi[j]
                daftar_lokasi[j] = daftar_lokasi[j + 1]
                daftar_lokasi[j + 1] = sementara

    return daftar_lokasi


def tampilkan_hasil_analisis(tujuan_user="", sedang_sakit=False):
    print("\nASISTEN: Baik, sebentar saya proses data lingkungan dan menghitung rata-rata indeks AQI...")
    analisis = AnalisisLingkungan()
    data_valid = analisis.baca_dan_validasi_csv()
    hasil_lokasi = analisis.proses_semua_lokasi(data_valid)

    if len(hasil_lokasi) == 0:
        return

    # Gunakan nama yang konsisten untuk daftar lokasi hasil pemrosesan
    hasil_lokasi = hasil_lokasi

    # Cek apakah lokasi yang diketik user ada di dalam daftar kota CSV
    if tujuan_user != "":
        ditemukan = False
        for k in hasil_lokasi:
            if tujuan_user.lower() in k["lokasi"].lower():
                ditemukan = True
                print(f"\n--- INFO LOKASI TUJUAN KAMU: {k['lokasi'].upper()} ---")
                print(f"Rata-rata Indeks Kualitas Udara (AQI) : {k['rata_aqi']:.2f} ({k['kategori']})")
                print(f"Rata-rata Konsentrasi PM2.5           : {k['rata_pm25']:.2f}")
                print(f"Titik Stasiun Risiko Rendah           : {k['risiko_rendah']} dari {k['jumlah_data']} stasiun")
                if sedang_sakit and k["rata_aqi"] > 100:
                    print("Peringatan Kesehatan: Kamu sedang sakit dan lokasi ini memiliki AQI tinggi, harap berhati-hati!")
                break
        if not ditemukan:
            print(f"\nASISTEN: Lokasi '{tujuan_user}' tidak tercatat spesifik di CSV, berikut data semua lokasi yang tersedia:")

    # Tampilkan tabel rata-rata AQI untuk SEMUA kota di file CSV
    else:
        print(f"\nTABEL RATA-RATA INDEKS KUALITAS UDARA (AQI) SELURUH LOKASI ({len(hasil_lokasi)} LOKASI):")
        print("=" * 115)
        print(f"{'No':<4} {'Lokasi / Lokasi':<18} {'Rata-rata AQI':<15} {'Varians AQI':<12} {'Std Dev AQI':<12} {'Rata PM2.5':<12} {'Status Udara'}")
        print("=" * 115)

        for i in range(len(hasil_lokasi)):
            k = hasil_lokasi[i]
            print(
                f"{i + 1:<4} {k['lokasi']:<18} {k['rata_aqi']:<15.2f} "
                f"{k['varians_aqi']:<12.2f} {k['std_dev_aqi']:<12.2f} {k['rata_pm25']:<12.2f} {k['kategori']}"
            )

    print(f"\n{'=' * 115}")

    # Catatan lokasi dengan AQI tertinggi di bagian akhir
    lokasi_tertinggi = hasil_lokasi[-1]
    print(
        f"Catatan: Sebaiknya hindari lokasi {lokasi_tertinggi['lokasi']} karena rata-rata AQI-nya paling tinggi yaitu {lokasi_tertinggi['rata_aqi']:.2f} ({lokasi_tertinggi['kategori']})."
    )
    print("-" * 115)
    print("ASISTEN: Selesai! Silakan pilih menu '6' jika ingin keluar dari program.")


def analisis_probabilitas(lokasi_tujuan):
    data_valid = AnalisisLingkungan().baca_dan_validasi_csv()

    if len(data_valid) == 0:
        print("Tidak ada data valid.")
        return

    jumlah_stasiun = 0
    stasiun_baik = 0
    total_aqi = 0

    for row in data_valid:
        if lokasi_tujuan.lower() in row["lokasi"].lower():
            jumlah_stasiun += 1
            total_aqi += row["aqi"]

            if row["aqi"] <= 50:
                stasiun_baik += 1

    if jumlah_stasiun == 0:
        print("Lokasi tidak ditemukan dalam dataset.")
        return

    probabilitas = (
        stasiun_baik / jumlah_stasiun
    ) * 100

    rata_aqi = total_aqi / jumlah_stasiun

    print("\n--- ANALISIS PROBABILITAS AQI ---")
    print(f"Lokasi : {lokasi_tujuan}")
    print(f"Jumlah stasiun : {jumlah_stasiun}")
    print(f"Stasiun dengan AQI baik : {stasiun_baik}")
    print(f"Rata-rata AQI : {rata_aqi:.2f}")
    print(f"Probabilitas AQI baik : {probabilitas:.2f}%")

    if probabilitas >= 80:
        print("Rekomendasi: Kualitas udara relatif baik.")
    elif probabilitas >= 50:
        print("Rekomendasi: Kualitas udara cukup bervariasi.")
    else:
        print("Rekomendasi: Perlu berhati-hati terhadap kualitas udara.")

    print(
        "\nHasil berdasarkan proporsi stasiun dalam dataset, "
        "bukan prediksi hari pemulihan."
    )

def sesi_percakapan():
    print("\n" + "-" * 65)
    # Pertanyaan 1: Apakah kamu mau bepergian?
    print("ASISTEN: Halo! Apakah kamu mau bepergian? (iya/tidak)")
    jawab_pergi = input("ANDA   : ").strip().lower()

    # JIKA JAWAB TIDAK
    if "tidak" in jawab_pergi:
        print("\nASISTEN: Baiklah. Apakah kamu mau melihat indeks cuaca / kualitas udara?")
        jawab_indeks = input("ANDA   : ").strip().lower()
    
        if "iya" in jawab_indeks: 
            lokasi_tujuan = input ("ASISTEN: Silakan ketik nama lokasi yang ingin dicek: ").strip()
            tampilkan_hasil_analisis(tujuan_user=lokasi_tujuan)
            print
        else:
            print("\nASISTEN: Baiklah kalau begitu. Silakan pilih menu '6' untuk keluar dari program.")

    # JIKA JAWAB IYA
    elif "iya" in jawab_pergi:
        # Pertanyaan 2: Apakah kamu sedang sakit?
        print("\nASISTEN: Apakah kamu sedang sakit? (iya/tidak)")
        jawab_sakit = input("ANDA   : ").strip().lower()
        status_sakit = True if ("iya" in jawab_sakit or "ya" in jawab_sakit) else False

        if status_sakit:
            print("ASISTEN: Semoga lekas sembuh ya! Mari kita cek kondisi udara agar perjalananmu tetap aman.")
        else:
            print("ASISTEN: Syukurlah kalau sehat! Mari kita cek kondisi udara untuk perjalananmu.")

        # Pertanyaan 3: Mau ke lokasi yang mana?
        print("\nASISTEN: Mau ke lokasi yang mana? (contoh: Surabaya, Balikpapan, Jakarta Selatan, Semarang, Yogyakarta, Denpasar, Medan, Bandung, Palembang, dan Makassar.)")
        lokasi_tujuan = input("ANDA   : ").strip()

        tampilkan_hasil_analisis(tujuan_user=lokasi_tujuan, sedang_sakit=status_sakit)

    else:
        print("\nASISTEN: Maaf, silakan jawab dengan 'iya' atau 'tidak'.")


class AkunPengguna:
    def __init__(self):
        self.users = {}
        self.user_aktif = None  # Penanda status login pengguna

    def registrasi(self):
        print("\n--- FORM REGISTRASI ---")
        username = input("Masukkan username baru: ").strip()
        if username == "":
            print("Username tidak boleh kosong!")
        elif username in self.users:
            print("Username sudah terdaftar!")
        else:
            password = input("Masukkan password baru (NIM/NIK): ").strip()
            self.users[username] = password
            print(f"Registrasi berhasil! Akun '{username}' telah dibuat.")

    def login(self):
        print("\n--- FORM LOGIN ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if username in self.users and self.users[username] == password:
            self.user_aktif = username
            print(f"\nLogin berhasil! Selamat datang, {username}.")
            print("Silahlan pilih menu '3' untuk rekomendasi tujuan.")
        else:
            print("Login gagal! Username atau password salah.")

    def tampilkan_hasil_analisis(self, tujuan_user="", sedang_sakit=False):
        """Mengakses tampilan hasil analisis melalui objek AnalisisLingkungan."""
        AnalisisLingkungan().tampilkan_hasil_analisis(tujuan_user, sedang_sakit)


def main():
    akun = AkunPengguna()

    while True:
        print("\n" + "=" * 52)
        print("   SISTEM ANALISIS LINGKUNGAN & REKOMENDASI LIBURAN")
        if akun.user_aktif:
            print(f"Status Login : Aktif ({akun.user_aktif})")
        else :
            print("Status Login : Belum Login")
        print("=" * 52)
        print("1. Registrasi Akun")
        print("2. Login")
        print("3. Rekomendasi Tujuan")
        print("4. Statistik Deskriptif (mean, varians,standar devisiasi)")
        print("5. Analisis Probabiltas Kualitas Udara")
        print("6. Keluar dari Program")
        print("=" * 52)

        pilihan = input("Pilih menu (1/2/3/4/5/6): ").strip()

        if pilihan == "1":
            akun.registrasi()

        elif pilihan == "2":
            akun.login()

        elif pilihan == "3":
            if akun.user_aktif is None:
                print("\n[PERINGATAN] Kamu harus Login terlebih dahulu di Menu 2 sebelum mengakses Tanya Jawab!")
            else:
                sesi_percakapan()

        elif pilihan == "4":
            tampilkan_hasil_analisis()

        elif pilihan == "5":
            if akun.user_aktif is None:
                print("\n[PERINGATAN] Kamu harus Login terlebih dahulu di Menu 2!")
            else:
                lokasi_tujuan = input("Masukkan nama lokasi yang diinginkan: ").strip()
                analisis_probabilitas(lokasi_tujuan)
                
        elif pilihan == "6":
            print("\nTerima kasih telah menggunakan program ini. Sampai jumpa!")
            break

        else:
            print("\nPilihan tidak valid! Silakan masukkan 1, 2, 3, 4, 5 atau 6.")


if __name__ == "__main__":
    main()