# 🐞 BugHunt

![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green)

BugHunt adalah **alat CLI** untuk menguji koneksi **VLESS/Trojan** melalui **WebSocket**, 

---

## 📥 Instalasi & Cara Pakai

### 1. Instalasi
```bash
git clone https://github.com/Illhm/BugHunt
cd BugHunt
python3 main.py -h
```

### 2. Cek 1 Domain
```bash
python3 main.py -d example.com
```

### 3. Cek Banyak Domain (Dari File)
```bash
python3 main.py -f daftar-bug.txt
```

### 4. Opsi Tambahan
Atur timeout koneksi (default 10 detik):
```bash
python3 main.py -f daftar-bug.txt --timeout 5
```

---

## 🖥 Contoh Output
```
[*] Memulai scan 3 domain...
✓ example.com     | Terkoneksi
✗ bad-host.com    | Gagal
✓ cloud.isp.net   | Terkoneksi
```

---

## ⚠️ Catatan
- Tool ini **hanya melakukan handshake WebSocket** (cek koneksi, pastikan TANPA REGULER).

---

## 🖱️ Integrasi Aplikasi GUI
BugHunt juga dapat dijalankan melalui aplikasi desktop sederhana menggunakan **Tkinter**.
Aplikasi ini memungkinkan Anda memasukkan satu domain secara langsung atau memilih
file `.txt` yang berisi daftar domain/BUG yang akan dipindai.

### Menjalankan GUI
```bash
python3 gui.py
```

### Struktur Proyek
```
BugHunt/
├── main.py
├── gui.py
├── daftar-bug.txt
├── README.md
└── .github/
    └── workflows/
        └── ci.yml
```

