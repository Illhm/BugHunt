import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from main import check_vless_connection, parse_vless_url, load_bugs_from_file


class BugHuntApp(tk.Tk):
    """GUI sederhana untuk menjalankan BugHunt."""

    def __init__(self):
        super().__init__()
        self.title("BugHunt GUI")
        self.geometry("500x400")
        self._create_widgets()

        # Gunakan template konfigurasi dari main.py
        self.proxy_template = parse_vless_url(
            "vless://8e1de14a-6873-4c92-b5bf-f9cb25aedb97@kang.cepu.us.kg:443?encryption=none&security=tls"
            "&sni=kang.cepu.us.kg&fp=randomized&type=ws&host=kang.cepu.us.kg&path=/146.235.18.248=45137#GUI"
        )

    def _create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Masukkan Domain atau Path File:").pack()
        self.entry = tk.Entry(frame, width=50)
        self.entry.pack(pady=5)

        btn_frame = tk.Frame(frame)
        btn_frame.pack()

        tk.Button(btn_frame, text="Pilih File", command=self._choose_file).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Mulai Scan", command=self._start_scan).pack(side=tk.LEFT, padx=5)

        self.output = scrolledtext.ScrolledText(self, width=60, height=15)
        self.output.pack(pady=10)

    def _choose_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, file_path)

    def _start_scan(self):
        target = self.entry.get().strip()
        if not target:
            messagebox.showwarning("Input", "Masukkan domain atau path file terlebih dahulu.")
            return

        if os.path.isfile(target):
            bugs = load_bugs_from_file(target)
        else:
            bugs = [target]

        if not bugs:
            messagebox.showinfo("Info", "Tidak ada domain ditemukan.")
            return

        self.output.delete("1.0", tk.END)
        for bug in bugs:
            proxy = self.proxy_template.copy()
            proxy["server"] = bug
            ok = check_vless_connection(proxy, timeout=10)
            status = "Terkoneksi" if ok else "Gagal"
            self.output.insert(tk.END, f"{bug} - {status}\n")


if __name__ == "__main__":
    app = BugHuntApp()
    app.mainloop()
