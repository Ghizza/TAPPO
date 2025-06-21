# (rimuovi lo spazio su Linux)!/home/stefano/Dropbox/Projects/TAPPO/venv/bin/python3

import customtkinter as ctk
import os
import platform
import shutil
import subprocess
from tkinter import filedialog, messagebox

# Imposta modalità chiara e tema di base (stile personalizzato inline)
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COMPRESSION_LEVELS = {
    "Bassa qualità (/screen) - File leggerissimo": "/screen",
    "Media qualità (/ebook) - File leggero": "/ebook",
    "Alta qualità (/printer) - File di medie dimensioni": "/printer",
    "Altissima qualità (/prepress) - File più pesante": "/prepress"
}

def find_ghostscript():
    system = platform.system()
    if system == "Windows":
        candidates = ["gswin64c.exe", "gswin32c.exe", "gs.exe"]
    else:
        candidates = ["gs"]

    for name in candidates:
        path = shutil.which(name)
        if path:
            return path

    if system != "Windows":
        for path in ["/usr/bin/gs", "/usr/local/bin/gs"]:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path

    return None  # Ghostscript non trovato

class TappoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("T.A.P.P.O. - Tool per Alleggerire PDF Pesanti Offline")
        self.geometry("700x280")
        self.configure(fg_color="#2d2a2e")
        self.configure(padx=20, pady=20)

        self.gs_path = ctk.StringVar(value=find_ghostscript() or "")
        self.input_path = ctk.StringVar()
        self.output_path = ctk.StringVar()
        self.compression = ctk.StringVar(value="Alta qualità (/printer) - File di medie dimensioni")

        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)

        label_style = {
            "font": ("Public Sans", 13, "bold"),
            "text_color": "#c1c0c0"
        }
        entry_style = {
            "width": 400,
            "font": ("Public Sans", 13),
            "fg_color": "#19181a",
            "text_color": "#fcfcfa",
            "border_color": "#727072",
            "corner_radius": 5,
            "border_width": 1,
        }
        button_style = {
            "fg_color": "#19181a",
            "hover_color": "#403e41",
            "text_color": "#FF6188",
            "corner_radius": 5,
            "font": ("Public Sans", 13, "bold"),
            "border_width": 1,
            "border_color": "#FF6188",
        }

        def add_row(row, label_text, variable, browse_command=None):
            label = ctk.CTkLabel(self, text=label_text, **label_style)
            label.grid(row=row, column=0, sticky="e", padx=10, pady=6)

            entry = ctk.CTkEntry(self, textvariable=variable, **entry_style)
            entry.grid(row=row, column=1, sticky="ew", padx=5)

            if browse_command:
                button = ctk.CTkButton(self, text="Sfoglia", command=browse_command, **button_style)
                button.grid(row=row, column=2, padx=5)

        add_row(0, "Ghostscript", self.gs_path, self.browse_gs)
        add_row(1, "PDF originale", self.input_path, self.browse_input)
        add_row(2, "File compresso", self.output_path, self.browse_output)

        compression_label = ctk.CTkLabel(self, text="Livello di compressione", **label_style)
        compression_label.grid(row=3, column=0, sticky="e", padx=10, pady=(20, 6))

        combo = ctk.CTkOptionMenu(
            self,
            variable=self.compression,
            values=list(COMPRESSION_LEVELS.keys()),
            width=400,
            font=("Public Sans", 13),
            fg_color="#19181a",
            button_color="#FF6188",
            button_hover_color="#727072",
            text_color="#fcfcfa",
            dropdown_fg_color="#19181a",
            dropdown_text_color="#fcfcfa",
            dropdown_hover_color="#FF6188",
            corner_radius=5
        )
        combo.grid(row=3, column=1, sticky="w", padx=5, pady=(20, 6))

        compress_button = ctk.CTkButton(
            self,
            text="Comprimi PDF",
            command=self.compress_pdf,
            fg_color="#19181a",
            hover_color="#403e41",
            text_color="#A9DC76",
            font=("Public Sans", 13, "bold"),
            corner_radius=5,
            height=40,
            border_width=1,
            border_color="#A9DC76",
        )
        compress_button.grid(row=4, column=0, columnspan=3, pady=15)

    def browse_gs(self):
        file = filedialog.askopenfilename(title="Seleziona Ghostscript", filetypes=[("Eseguibili", "*.exe")])
        if file:
            self.gs_path.set(file)

    def browse_input(self):
        file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file:
            self.input_path.set(file)
            base, _ = os.path.splitext(file)
            self.output_path.set(base + " - compresso.pdf")

    def browse_output(self):
        file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file:
            self.output_path.set(file)

    def compress_pdf(self):
        gs = self.gs_path.get()
        input_pdf = self.input_path.get()
        output_pdf = self.output_path.get()
        quality = COMPRESSION_LEVELS.get(self.compression.get(), "/printer")

        if not os.path.exists(gs):
            messagebox.showerror("Errore", "Ghostscript non trovato.")
            return
        if not os.path.exists(input_pdf):
            messagebox.showerror("Errore", "Il file di input non esiste.")
            return

        command = [
            gs, "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={quality}", "-dNOPAUSE", "-dQUIET", "-dBATCH",
            f"-sOutputFile={output_pdf}", input_pdf
        ]

        try:
            subprocess.run(command, check=True)

            # Calcola dimensioni
            original_size = os.path.getsize(input_pdf)
            compressed_size = os.path.getsize(output_pdf)

            saved_bytes = original_size - compressed_size
            saved_percent = (saved_bytes / original_size) * 100 if original_size > 0 else 0

            messagebox.showinfo(
                "Successo",
                f"File compresso salvato in:\n{output_pdf}\n\n"
                f"Dimensione originale: {original_size / 1024:.2f} KB\n"
                f"Dimensione compressa: {compressed_size / 1024:.2f} KB\n"
                f"Risparmio: {saved_percent:.1f}%"
            )

        except subprocess.CalledProcessError:
            messagebox.showerror("Errore", "Errore nella compressione del PDF.")

if __name__ == "__main__":
    app = TappoApp()
    app.mainloop()
