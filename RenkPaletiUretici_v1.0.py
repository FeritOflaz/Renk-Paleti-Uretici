import tkinter as tk
from tkinter import colorchooser, messagebox, filedialog
import random

def generate_palette_from_color(base_color):
    # Ana renkten 5 ton türet
    r, g, b = tuple(int(base_color[i:i + 2], 16) for i in (0, 2, 4))
    shades = []
    for i in range(5):
        factor = 1 - (i - 2) * 0.15
        nr = int(max(0, min(255, r * factor)))
        ng = int(max(0, min(255, g * factor)))
        nb = int(max(0, min(255, b * factor)))
        shades.append(f"#{nr:02X}{ng:02X}{nb:02X}")
    return shades

def random_color():
    return f"#{random.randint(0, 0xFFFFFF):06X}"

class ColorPaletteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Renk Paleti Üretici v1.0")
        self.root.geometry("900x550")
        self.root.configure(bg="#2b2b2b")
        self.palette = []

        self.setup_ui()
        self.load_default_palette()  # Uygulama açılışında siyah tonları

    def setup_ui(self):
        # Üst çerçeve (başlık + butonlar)
        top_frame = tk.Frame(self.root, bg="#2b2b2b")
        top_frame.pack(fill="x", pady=10, padx=10)

        title_label = tk.Label(top_frame, text="🎨 Renk Paleti Üretici", fg="white", bg="#2b2b2b", font=("Segoe UI", 14, "bold"))
        title_label.pack(side="left", padx=10)

        select_color_btn = tk.Button(top_frame, text="🎨 Ana Renk Seç", bg="#3a7bd5", fg="white", font=("Segoe UI", 10, "bold"),
                                     relief="flat", padx=15, pady=5, command=self.choose_color)
        select_color_btn.pack(side="right", padx=5)

        random_btn = tk.Button(top_frame, text="🎲 Rastgele Üret", bg="#3a7bd5", fg="white", font=("Segoe UI", 10, "bold"),
                               relief="flat", padx=15, pady=5, command=self.generate_random_palette)
        random_btn.pack(side="right", padx=5)

        # Palet kutuları
        self.palette_frame = tk.Frame(self.root, bg="#2b2b2b")
        self.palette_frame.pack(pady=5, padx=15, fill="both", expand=True)

        self.color_panels = []
        for _ in range(5):
            panel = tk.Frame(self.palette_frame, bg="#3a3a3a", bd=2, relief="flat")
            panel.pack(side="left", expand=True, fill="both", padx=8, pady=10)
            color_box = tk.Frame(panel, bg="#444", height=360, width=120)
            color_box.pack(pady=(10, 5), padx=10, fill="both", expand=True)
            hex_label = tk.Label(panel, text="#FFFFFF", fg="white", bg="#3a3a3a", font=("Consolas", 10))
            hex_label.pack(pady=5)
            hex_label.bind("<Button-1>", self.copy_to_clipboard)
            self.color_panels.append({"box": color_box, "hex": hex_label})

        # Alt kısım (kaydet + içe aktar + powered by)
        bottom_frame = tk.Frame(self.root, bg="#2b2b2b")
        bottom_frame.pack(fill="x", pady=8, padx=15)

        save_btn = tk.Button(bottom_frame, text="💾 Paleti Kaydet", bg="#3a7bd5", fg="white", font=("Segoe UI", 10, "bold"),
                             relief="flat", padx=15, pady=5, command=self.save_palette)
        save_btn.pack(side="left", padx=5)

        load_btn = tk.Button(bottom_frame, text="📂 Paleti İçe Aktar", bg="#3a7bd5", fg="white", font=("Segoe UI", 10, "bold"),
                             relief="flat", padx=15, pady=5, command=self.load_palette)
        load_btn.pack(side="left", padx=5)

        powered = tk.Label(bottom_frame, text="Powered by Ferit Oflaz", fg="#8f8f8f", bg="#2b2b2b", font=("Segoe UI", 8, "italic"))
        powered.pack(side="right", padx=10)

    def update_ui_palette(self):
        for i, item in enumerate(self.color_panels):
            hex_val = self.palette[i] if i < len(self.palette) else "#000000"
            item["box"].configure(bg=hex_val)
            item["hex"].configure(text=hex_val)
            item["hex"].configure(fg="white")  # Her zaman beyaz metin

    def generate_random_palette(self):
        self.palette = [random_color() for _ in range(5)]
        self.update_ui_palette()

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Renk Seç")[1]
        if color_code:
            self.palette = generate_palette_from_color(color_code.lstrip('#'))
            self.update_ui_palette()

    def copy_to_clipboard(self, event):
        hex_value = event.widget.cget("text")
        self.root.clipboard_clear()
        self.root.clipboard_append(hex_value)
        messagebox.showinfo("Kopyalandı", f"{hex_value} panoya kopyalandı!")

    def save_palette(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Metin Dosyası", "*.txt")])
        if file:
            with open(file, "w") as f:
                for color in self.palette:
                    f.write(color + "\n")
            messagebox.showinfo("Kaydedildi", "Renk paleti başarıyla kaydedildi!")

    def load_palette(self):
        file = filedialog.askopenfilename(filetypes=[("Metin Dosyası", "*.txt")])
        if file:
            with open(file, "r") as f:
                colors = [line.strip() for line in f.readlines() if line.strip().startswith("#")]
            if len(colors) == 5:
                self.palette = colors
                self.update_ui_palette()
                messagebox.showinfo("Yüklendi", "Palet başarıyla içe aktarıldı!")
            else:
                messagebox.showwarning("Hatalı Palet", "Geçerli bir palet dosyası değil!")

    def load_default_palette(self):
        # Açılışta siyah tonları göster
        self.palette = ["#000000", "#202020", "#404040", "#606060", "#808080"]
        self.update_ui_palette()

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorPaletteApp(root)
    root.mainloop()
