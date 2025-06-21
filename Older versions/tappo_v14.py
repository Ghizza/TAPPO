#!/usr/bin/env python3

import customtkinter as ctk
import os
import platform
import shutil
import subprocess
import webbrowser
import tkinter.font as tkFont
from tkinter import filedialog, messagebox
from pathlib import Path

APP_COLORS = {
    "background": "#002B36",
    "dark": "#002028",
    "hover": "#073642",
    "text": "#839496",
    "text_medium": "#93A1A1",
    "text_light": "#FDF6E3",
    "border": "#586E75",
    "link_01": "#268BD2",
    "link_02": "#B58900",
}

APP_STYLE = {
    "font_family": "Public Sans",
    "corner_radius": 5,
    "border_width": 1
}

def register_custom_font():
    font_path = Path(__file__).parent / "fonts" / "PublicSans-VariableFont_wght.ttf"
    if not font_path.exists():
        print(f"[ERRORE] Font non trovato: {font_path}")
        return

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
        for path in ["/usr/bin/gs", "/usr/local/bin/gs", "/opt/local/bin/gs"]:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path

    return None

def center_window_on_screen(window, width, height):
    window.update_idletasks()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")

class TappoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TAPPO - Tool per Alleggerire PDF Pesanti Offline")
        self.configure(fg_color=APP_COLORS["background"])

        self.resizable(False, False)
        center_window_on_screen(self, 750, 320)

        self.gs_path = ctk.StringVar(value=find_ghostscript() or "")
        self.input_path = ctk.StringVar()
        self.output_path = ctk.StringVar()
        self.compression = ctk.StringVar(value="Alta qualità (/printer) - File di medie dimensioni")

        # Configurazione griglia principale
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

        # Configurazione griglia del main_frame per centrare il contenuto
        self.main_frame.grid_columnconfigure(0, weight=0)  # Labels
        self.main_frame.grid_columnconfigure(1, weight=1)  # Entries (centrate)
        self.main_frame.grid_columnconfigure(2, weight=0)  # Buttons

        self.build_ui()

    def build_ui(self):
        self.show_main_content()

    def show_main_content(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        label_style = {"font": ("Public Sans", 13, "bold"), "text_color": APP_COLORS["text"]}
        entry_style = {
            "width": 350, "font": ("Public Sans", 13),
            "fg_color": APP_COLORS["dark"], "text_color": APP_COLORS["text_light"],
            "border_color": APP_COLORS["border"], "corner_radius": 5, "border_width": 1,
        }
        button_style = {
            "fg_color": APP_COLORS["dark"], "hover_color": APP_COLORS["hover"],
            "text_color": APP_COLORS["link_01"], "corner_radius": 5,
            "font": ("Public Sans", 13, "bold"), "border_width": 1, "border_color": APP_COLORS["link_01"],
        }

        def add_row(row, label_text, variable, browse_command=None):
            ctk.CTkLabel(self.main_frame, text=label_text, **label_style).grid(
                row=row, column=0, sticky="e", padx=(0, 15), pady=8
            )
            ctk.CTkEntry(self.main_frame, textvariable=variable, **entry_style).grid(
                row=row, column=1, sticky="", padx=5, pady=8
            )
            if browse_command:
                ctk.CTkButton(self.main_frame, text="Sfoglia", command=browse_command, **button_style).grid(
                    row=row, column=2, padx=(15, 0), pady=8
                )

        add_row(0, "Ghostscript", self.gs_path, self.browse_gs)
        add_row(1, "PDF originale", self.input_path, self.browse_input)
        add_row(2, "File compresso", self.output_path, self.browse_output)

        # Livello di compressione
        ctk.CTkLabel(self.main_frame, text="Livello di compressione", **label_style).grid(
            row=3, column=0, sticky="e", padx=(0, 15), pady=(25, 8)
        )

        ctk.CTkOptionMenu(
            self.main_frame, variable=self.compression, values=list(COMPRESSION_LEVELS.keys()), width=350,
            font=(APP_STYLE["font_family"], 13), fg_color=APP_COLORS["dark"], button_color=APP_COLORS["link_01"],
            button_hover_color=APP_COLORS["border"], text_color=APP_COLORS["text_light"],
            dropdown_fg_color=APP_COLORS["dark"], dropdown_text_color=APP_COLORS["text_light"],
            dropdown_hover_color=APP_COLORS["link_01"], corner_radius=APP_STYLE["corner_radius"]
        ).grid(row=3, column=1, sticky="", padx=5, pady=(25, 8))

        # Menu laterale (GUIDA e CREDITS)
        self.create_side_menu()

        # Bottone comprimi PDF - centrato su tutte le colonne
        compress_button = ctk.CTkButton(
            self.main_frame, text="Comprimi PDF", command=self.compress_pdf,
            fg_color=APP_COLORS["dark"], hover_color=APP_COLORS["hover"],
            text_color=APP_COLORS["link_02"], font=(APP_STYLE["font_family"], 13, "bold"),
            corner_radius=APP_STYLE["corner_radius"], height=40, width=200,
            border_width=APP_STYLE["border_width"], border_color=APP_COLORS["link_02"]
        )
        compress_button.grid(row=5, column=0, columnspan=3, pady=(25, 0))

    def create_side_menu(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.grid(row=3, column=2, padx=(15, 0), pady=(25, 8))

        ctk.CTkButton(
            frame, text="GUIDA", command=self.show_guide,
            fg_color="transparent", hover_color=APP_COLORS["hover"],
            text_color=APP_COLORS["link_01"], font=(APP_STYLE["font_family"], 11, "bold"), width=40, height=24
        ).pack(side="left", padx=(0, 5))

        ctk.CTkButton(
            frame, text="CREDITS", command=self.show_credits,
            fg_color="transparent", hover_color=APP_COLORS["hover"],
            text_color=APP_COLORS["link_01"], font=(APP_STYLE["font_family"], 11, "bold"), width=50, height=24
        ).pack(side="left")

    def show_guide(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Titolo con padding ridotto
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Come usare TAPPO",
            font=(APP_STYLE["font_family"], 16, "bold"),  # Ridotto da 20 a 16
            text_color=APP_COLORS["border"]
        )
        title_label.pack(pady=(5, 5))  # Ridotto padding superiore da 10 a 5

        info_text = """───── INSTALLAZIONE GHOSTSCRIPT ─────

⚠ TAPPO richiede che Ghostscript sia installato sul sistema.

• SU WINDOWS:
- Scarica Ghostscript dal link in basso

• SU LINUX:
- Debian/Ubuntu: sudo apt install ghostscript
- Arch Linux: sudo pacman -S ghostscript
- Fedora: sudo dnf install ghostscript

───── COME USARE TAPPO ─────

• Seleziona il percorso di Ghostscript (se non rilevato automaticamente)
• Scegli il file PDF da comprimere
• Specifica dove salvare il PDF compresso
• Seleziona il livello di compressione desiderato
• Clicca su "Comprimi PDF"

───── LIVELLI DI COMPRESSIONE ─────

• Bassa qualità: Massima compressione, qualità ridotta
• Media qualità: Buon compromesso per lettura digitale
• Alta qualità: Buona qualità per stampa normale
• Altissima qualità: Qualità professionale per stampa

───── NOTE ─────

• I tempi di elaborazione dipendono dalla dimensione del file
• Il file originale non viene modificato
• La compressione varia in base al contenuto del PDF
"""

        text_widget = ctk.CTkTextbox(
            self.main_frame,
            width=650,
            height=150,
            font=(APP_STYLE["font_family"], 12),
            fg_color=APP_COLORS["dark"],
            text_color=APP_COLORS["text_medium"],
            corner_radius=APP_STYLE["corner_radius"],
            wrap="word"
        )
        text_widget.pack(pady=5, padx=10, fill="both", expand=True)
        text_widget.insert("0.0", info_text)
        text_widget.configure(state="disabled")

        # Frame per i pulsanti affiancati
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=(5, 10))

        link_button = ctk.CTkButton(
            button_frame,
            text="Scarica Ghostscript",
            command=self.open_ghostscript_download,
            fg_color=APP_COLORS["dark"],
            hover_color=APP_COLORS["hover"],
            text_color=APP_COLORS["link_01"],
            font=(APP_STYLE["font_family"], 13, "bold"),
            corner_radius=APP_STYLE["corner_radius"],
            border_width=1,
            border_color=APP_COLORS["link_01"],
            width=150,
        )
        link_button.pack(side="left", padx=10)

        close_button = ctk.CTkButton(
            button_frame,
            text="Indietro",
            command=self.show_main_content,
            fg_color=APP_COLORS["dark"],
            hover_color=APP_COLORS["hover"],
            text_color=APP_COLORS["text"],
            font=(APP_STYLE["font_family"], 13, "bold"),
            corner_radius=APP_STYLE["corner_radius"],
            border_width=APP_STYLE["border_width"],
            border_color=APP_COLORS["border"],
            width=150,
        )
        close_button.pack(side="left", padx=10)

    def show_credits(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Titolo con padding ridotto (stesso della guida)
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="TAPPO",
            font=(APP_STYLE["font_family"], 16, "bold"),  # Ridotto da 20 a 16
            text_color=APP_COLORS["border"]
        )
        title_label.pack(pady=(5, 5))  # Ridotto padding superiore da 10 a 5

        info_text = """───── TAPPO ─────

Tool per Alleggerire PDF Pesanti Offline

───── INFORMAZIONI ─────

• Versione: 1.0
• Creato da: Stefano
• Licenza: MIT License
• Tecnologie: Python, CustomTkinter, Ghostscript

───── DESCRIZIONE ─────

TAPPO è un'applicazione desktop open source che permette di comprimere 
file PDF riducendone le dimensioni mantenendo una qualità accettabile.

Il software utilizza Ghostscript come motore di compressione e offre 
diversi livelli di qualità per soddisfare diverse esigenze di utilizzo.

───── CARATTERISTICHE ─────

• Interface utente intuitiva e moderna
• Supporto per diversi livelli di compressione
• Elaborazione locale (nessun caricamento online)
• Multipiattaforma (Windows, Linux, macOS)
• Codice sorgente completamente disponibile

───── RINGRAZIAMENTI ─────

• Ghostscript Development Team
• Python Software Foundation
• CustomTkinter Community
"""

        text_widget = ctk.CTkTextbox(
            self.main_frame,
            width=650,
            height=150,
            font=(APP_STYLE["font_family"], 12),
            fg_color=APP_COLORS["dark"],
            text_color=APP_COLORS["text_medium"],
            corner_radius=APP_STYLE["corner_radius"],
            wrap="word"
        )
        text_widget.pack(pady=5, padx=10, fill="both", expand=True)
        text_widget.insert("0.0", info_text)
        text_widget.configure(state="disabled")

        # Frame per i pulsanti affiancati
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=(5, 10))

        github_button = ctk.CTkButton(
            button_frame,
            text="Pagina GitHub",
            command=self.open_github,
            fg_color=APP_COLORS["dark"],
            hover_color=APP_COLORS["hover"],
            text_color=APP_COLORS["link_01"],
            font=(APP_STYLE["font_family"], 13, "bold"),
            corner_radius=APP_STYLE["corner_radius"],
            border_width=1,
            border_color=APP_COLORS["link_01"],
            width=150,
        )
        github_button.pack(side="left", padx=10)

        close_button = ctk.CTkButton(
            button_frame,
            text="Indietro",
            command=self.show_main_content,
            fg_color=APP_COLORS["dark"],
            hover_color=APP_COLORS["hover"],
            text_color=APP_COLORS["text"],
            font=(APP_STYLE["font_family"], 13, "bold"),
            corner_radius=APP_STYLE["corner_radius"],
            border_width=APP_STYLE["border_width"],
            border_color=APP_COLORS["border"],
            width=150,
        )
        close_button.pack(side="left", padx=10)

    def open_ghostscript_download(self):
        webbrowser.open("https://www.ghostscript.com/download/gsdnld.html")

    def open_github(self):
        webbrowser.open("https://github.com/Ghizza/TAPPO")

    def browse_gs(self):
        if platform.system() == "Windows":
            filetypes = [("Eseguibili", "*.exe"), ("Tutti i files", "*.*")]
        else:
            filetypes = [("Tutti i files", "*.*")]

        file = filedialog.askopenfilename(title="Seleziona Ghostscript", filetypes=filetypes)
        if file:
            self.gs_path.set(file)

    def browse_input(self):
        file = filedialog.askopenfilename(
            title="Seleziona PDF da comprimere",
            filetypes=[("PDF files", "*.pdf"), ("Tutti i files", "*.*")]
        )
        if file:
            self.input_path.set(file)
            base, _ = os.path.splitext(file)
            self.output_path.set(base + " - compresso.pdf")

    def browse_output(self):
        file = filedialog.asksaveasfilename(
            title="Salva file compresso come",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("Tutti i files", "*.*")]
        )
        if file:
            self.output_path.set(file)

    def compress_pdf(self):
        gs = self.gs_path.get().strip()
        input_pdf = self.input_path.get().strip()
        output_pdf = self.output_path.get().strip()
        quality = COMPRESSION_LEVELS.get(self.compression.get(), "/printer")

        if not gs:
            messagebox.showerror("Errore", "Seleziona il percorso di Ghostscript.")
            return

        if not input_pdf:
            messagebox.showerror("Errore", "Seleziona un file PDF da comprimere.")
            return

        if not output_pdf:
            messagebox.showerror("Errore", "Specifica il percorso del file di output.")
            return

        if not os.path.exists(gs):
            messagebox.showerror("Errore", "Ghostscript non trovato nel percorso specificato.")
            return

        if not os.path.exists(input_pdf):
            messagebox.showerror("Errore", "Il file PDF di input non esiste.")
            return

        if not input_pdf.lower().endswith('.pdf'):
            messagebox.showerror("Errore", "Il file di input deve essere un PDF.")
            return

        try:
            input_size = os.path.getsize(input_pdf)
            if input_size == 0:
                messagebox.showerror("Errore", "Il file PDF di input è vuoto.")
                return
        except OSError as e:
            messagebox.showerror("Errore", f"Impossibile leggere il file di input: {e}")
            return

        output_dir = os.path.dirname(output_pdf)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError as e:
                messagebox.showerror("Errore", f"Impossibile creare la directory di output: {e}")
                return

        try:
            test_dir = output_dir if output_dir else '.'
            test_file = os.path.join(test_dir, 'test_write_tappo.tmp')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
        except (OSError, IOError):
            messagebox.showerror("Errore", "Permessi insufficienti per scrivere nella directory di output.")
            return

        try:
            if os.path.abspath(input_pdf) == os.path.abspath(output_pdf):
                messagebox.showerror("Errore", "Il file di output non può essere uguale a quello di input.")
                return
        except OSError:
            pass

        command = [
            gs,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={quality}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output_pdf}",
            input_pdf
        ]

        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                timeout=300
            )

            if not os.path.exists(output_pdf):
                messagebox.showerror("Errore", "Il file compresso non è stato creato.")
                return

            compressed_size = os.path.getsize(output_pdf)
            if compressed_size == 0:
                messagebox.showerror("Errore", "Il file compresso è vuoto. Possibile errore durante la compressione.")
                if os.path.exists(output_pdf):
                    os.remove(output_pdf)
                return

            original_size = os.path.getsize(input_pdf)
            saved_bytes = original_size - compressed_size
            saved_percent = (saved_bytes / original_size) * 100 if original_size > 0 else 0

            def format_size(bytes_size):
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if bytes_size < 1024.0:
                        return f"{bytes_size:.2f} {unit}"
                    bytes_size /= 1024.0
                return f"{bytes_size:.2f} TB"

            success_message = (
                f"File compresso salvato in:\n{output_pdf}\n\n"
                f"Dimensione originale: {format_size(original_size)}\n"
                f"Dimensione compressa: {format_size(compressed_size)}\n"
                f"Risparmio: {saved_percent:.1f}%"
            )

            if saved_percent < 0:
                success_message += "\n\nNota: Il file compresso è più grande dell'originale.\nProva un livello di compressione diverso."

            messagebox.showinfo("File compresso!", success_message)

        except subprocess.TimeoutExpired:
            messagebox.showerror("Errore", "Timeout: la compressione sta richiedendo troppo tempo.\nProva con un file più piccolo o un livello di compressione diverso.")
        except subprocess.CalledProcessError as e:
            error_msg = f"Errore nella compressione del PDF.\nCodice di errore: {e.returncode}"
            if e.stderr:
                error_msg += f"\nDettagli: {e.stderr.strip()}"
            messagebox.showerror("Errore", error_msg)
        except PermissionError:
            messagebox.showerror("Errore", "Permessi insufficienti per salvare il file.")
        except FileNotFoundError as e:
            messagebox.showerror("Errore", f"File non trovato: {e}")
        except OSError as e:
            messagebox.showerror("Errore", f"Errore del sistema operativo: {e}")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore imprevisto: {e}")

if __name__ == "__main__":
    register_custom_font()
    app = TappoApp()
    app.mainloop()