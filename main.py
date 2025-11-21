import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import csv
import os
import datetime

# --- PRÓBÁLJUK IMPORTÁLNI A DIAGRAM RAJZOLÓT ---
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None  # Ha nincs telepítve, kezeljük a hibát később


# --- 1. FELTÉTEL: Saját osztály (GYZS) ---
class Kiadas_GYZS:
    def __init__(self, megnevezes, osszeg, datum):
        self.megnevezes = megnevezes
        self.osszeg = osszeg
        self.datum = datum

    def __str__(self):
        return f"[{self.datum}] {self.megnevezes} - {self.osszeg} Ft"


class PenzugyiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Költségkövető App - GYZS")
        self.root.geometry("400x600")  # Még nagyobb a diagram gomb miatt

        self.kiadasok_lista = []

        # --- GRAFIKUS FELÜLET (GUI) ---

        # 1. Dátum
        tk.Label(root, text="Dátum (ÉÉÉÉ-HH-NN):").pack(pady=5)
        self.entry_datum = tk.Entry(root)
        self.entry_datum.pack(pady=5)
        self.entry_datum.insert(0, str(datetime.date.today()))

        # 2. Megnevezés
        tk.Label(root, text="Kiadás megnevezése:").pack(pady=5)
        self.entry_nev = tk.Entry(root)
        self.entry_nev.pack(pady=5)

        # 3. Összeg
        tk.Label(root, text="Összeg (Ft):").pack(pady=5)
        self.entry_osszeg = tk.Entry(root)
        self.entry_osszeg.pack(pady=5)

        # Gombok kerete (Felső sor)
        btn_frame_top = tk.Frame(root)
        btn_frame_top.pack(pady=10)

        # Hozzáadás
        self.btn_hozzaad = tk.Button(btn_frame_top, text="Hozzáadás", command=self.rogzites_GYZS)
        self.btn_hozzaad.pack(side=tk.LEFT, padx=5)

        # --- ÚJ GOMB: DIAGRAM ---
        # Különleges színnel kiemelve
        self.btn_diagram = tk.Button(btn_frame_top, text="📊 Diagram", command=self.diagram_keszites_GYZS, bg="#cff4fc")
        self.btn_diagram.pack(side=tk.LEFT, padx=5)

        # Lista
        self.listbox = tk.Listbox(root, width=60, height=10)
        self.listbox.pack(pady=10)

        # Fájlkezelő gombok kerete (Alsó sor)
        btn_frame_bottom = tk.Frame(root)
        btn_frame_bottom.pack(pady=10)

        self.btn_mentes = tk.Button(btn_frame_bottom, text="Mentés másként...", command=self.fajlba_iras_GYZS,
                                    bg="#d1e7dd")
        self.btn_mentes.pack(side=tk.LEFT, padx=10)

        self.btn_betoltes = tk.Button(btn_frame_bottom, text="Betöltés...", command=self.adatok_betoltese_GYZS,
                                      bg="#fff3cd")
        self.btn_betoltes.pack(side=tk.LEFT, padx=10)

        tk.Button(root, text="Kilépés", command=root.quit, bg="#f8d7da").pack(pady=10)

    # --- ADATFELVÉTEL (GYZS) ---
    def rogzites_GYZS(self):
        datum = self.entry_datum.get()
        nev = self.entry_nev.get()
        osszeg = self.entry_osszeg.get()

        if nev and osszeg and datum:
            try:
                osszeg = int(osszeg)
                uj_tetel = Kiadas_GYZS(nev, osszeg, datum)
                self.kiadasok_lista.append(uj_tetel)
                self.listbox.insert(tk.END, str(uj_tetel))

                self.entry_nev.delete(0, tk.END)
                self.entry_osszeg.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Hiba", "Az összeg csak szám lehet!")
        else:
            messagebox.showwarning("Hiányos adat", "Kérlek tölts ki minden mezőt!")

    # --- ÚJ FÜGGVÉNY: DIAGRAM KÉSZÍTÉS (GYZS) ---
    def diagram_keszites_GYZS(self):
        # 1. Ellenőrzés: Van-e matplotlib?
        if plt is None:
            messagebox.showerror("Hiba",
                                 "A diagramhoz telepíteni kell a matplotlib modult!\nParancs: pip install matplotlib")
            return

        # 2. Ellenőrzés: Van-e adat?
        if not self.kiadasok_lista:
            messagebox.showwarning("Üres", "Nincs megjeleníthető adat!")
            return

        # 3. Adatok előkészítése a diagramhoz
        kategoriak = []
        ertekek = []

        for tetel in self.kiadasok_lista:
            # Hozzáadjuk a neveket és összegeket a listákhoz
            # (Profi verzióban itt összegeznénk az azonos nevűeket, de ez így is működik)
            kategoriak.append(tetel.megnevezes)
            ertekek.append(tetel.osszeg)

        # 4. Diagram kirajzolása
        try:
            plt.figure(figsize=(8, 6))  # Ablak mérete
            # Kördiagram (Pie chart) készítése
            plt.pie(ertekek, labels=kategoriak, autopct='%1.1f%%', startangle=140)
            plt.title("Kiadások eloszlása - GYZS")  # Címben is a monogram
            plt.show()  # Ez dobja fel az ablakot
        except Exception as e:
            messagebox.showerror("Hiba", f"Hiba a diagram rajzolásakor: {e}")

    # --- FÁJLKEZELÉS (GYZS) ---
    def fajlba_iras_GYZS(self):
        fajl_utvonal = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV fájlok", "*.csv"), ("Minden fájl", "*.*")]
        )
        if fajl_utvonal:
            try:
                with open(fajl_utvonal, mode='w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    for tetel in self.kiadasok_lista:
                        writer.writerow([tetel.datum, tetel.megnevezes, tetel.osszeg])
                messagebox.showinfo("Siker", "Sikeres mentés!")
            except Exception as e:
                messagebox.showerror("Hiba", str(e))

    def adatok_betoltese_GYZS(self):
        fajl_utvonal = filedialog.askopenfilename(
            filetypes=[("CSV fájlok", "*.csv"), ("Minden fájl", "*.*")]
        )
        if fajl_utvonal:
            try:
                with open(fajl_utvonal, mode='r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    self.kiadasok_lista = []
                    self.listbox.delete(0, tk.END)
                    for row in reader:
                        if row and len(row) >= 3:
                            datum, nev, osszeg = row[0], row[1], int(row[2])
                            tetel = Kiadas_GYZS(nev, osszeg, datum)
                            self.kiadasok_lista.append(tetel)
                            self.listbox.insert(tk.END, str(tetel))
                messagebox.showinfo("Siker", "Adatok betöltve!")
            except Exception as e:
                messagebox.showerror("Hiba", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = PenzugyiApp(root)
    root.mainloop()