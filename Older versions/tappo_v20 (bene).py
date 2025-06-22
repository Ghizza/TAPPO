#!/usr/bin/env python3

import customtkinter as ctk
import os
import platform
import shutil
import subprocess
import webbrowser
from tkinter import filedialog, messagebox

APP_COLORS = {
    "background": "#262626",
    "dark": "#191919",
    "hover": "#333333",
    "text": "#7f7f7f",
    "text_medium": "#cccccc",
    "text_light": "#d9d9d9",
    "border": "#666666",
    "link_01": "#0076d6", # 0076d6 IBM Blue
    "link_02": "#76b900", # 44d62c Razer Green # 76b900 NVIDIA
}

APP_FONTS = {
    "family": ("Segoe UI", "DejaVu Sans", "Liberation Sans", "Helvetica", "Arial", "sans-serif"),
    "size_small": 11,
    "size_normal": 13,
    "size_medium": 14,
    "size_large": 15,
}

# Definizione di tutti gli stili dei componenti
COMPONENT_STYLES = {
    "label": {
        "font": (APP_FONTS["family"], APP_FONTS["size_normal"], "bold"), 
        "text_color": APP_COLORS["text"]
    },
    
    "entry": {
        "width": 350, 
        "font": (APP_FONTS["family"], APP_FONTS["size_normal"]),
        "fg_color": APP_COLORS["dark"], 
        "text_color": APP_COLORS["text_light"],
        "border_color": APP_COLORS["border"], 
        "corner_radius": 5, 
        "border_width": 1,
    },
    
    "button_primary": {
        "fg_color": APP_COLORS["dark"], 
        "hover_color": APP_COLORS["hover"],
        "text_color": APP_COLORS["link_01"], 
        "corner_radius": 5,
        "font": (APP_FONTS["family"], APP_FONTS["size_medium"], "bold"), 
        "border_width": 1, 
        "border_color": APP_COLORS["link_01"],
        "width": 150
    },
    
    "button_secondary": {
        "fg_color": APP_COLORS["dark"], 
        "hover_color": APP_COLORS["hover"],
        "text_color": APP_COLORS["text"], 
        "corner_radius": 5,
        "font": (APP_FONTS["family"], APP_FONTS["size_normal"], "bold"), 
        "border_width": 1, 
        "border_color": APP_COLORS["border"],
        "width": 150
    },
    
    "button_compress": {
        "fg_color": APP_COLORS["dark"], 
        "hover_color": APP_COLORS["hover"],
        "text_color": APP_COLORS["link_02"], 
        "corner_radius": 5,
        "font": (APP_FONTS["family"], APP_FONTS["size_normal"], "bold"), 
        "border_width": 1, 
        "border_color": APP_COLORS["link_02"],
        "height": 36, 
        "width": 200
    },
    
    "button_menu": {
        "fg_color": "transparent", 
        "hover_color": APP_COLORS["hover"],
        "text_color": APP_COLORS["link_01"], 
        "font": (APP_FONTS["family"], APP_FONTS["size_small"], "bold"), 
        "height": 24
    },
    
    "option_menu": {
        "width": 350,
        "font": (APP_FONTS["family"], APP_FONTS["size_normal"]), 
        "fg_color": APP_COLORS["dark"], 
        "button_color": APP_COLORS["link_01"], 
        "button_hover_color": APP_COLORS["border"], 
        "text_color": APP_COLORS["text_light"], 
        "dropdown_fg_color": APP_COLORS["dark"], 
        "dropdown_text_color": APP_COLORS["text_light"], 
        "dropdown_hover_color": APP_COLORS["link_01"], 
        "corner_radius": 5
    },
    
    "title": {
        "font": (APP_FONTS["family"], APP_FONTS["size_large"], "bold"),
        "text_color": APP_COLORS["text"]
    },
    
    "textbox": {
        "width": 690, 
        "height": 170,
        "font": (APP_FONTS["family"], 13),
        "fg_color": APP_COLORS["dark"], 
        "text_color": APP_COLORS["text_medium"],
        "corner_radius": 5, 
        "wrap": "word"
    }
}

COMPRESSION_LEVELS = {
    "Bassa qualità (/screen) - File leggerissimo": "/screen",
    "Media qualità (/ebook) - File leggero": "/ebook",
    "Alta qualità (/printer) - File di medie dimensioni": "/printer",
    "Altissima qualità (/prepress) - File più pesante": "/prepress"
}

# ═══════════════════════════════════════════════════════════════════
# FUNZIONI DI UTILITÀ
# ═══════════════════════════════════════════════════════════════════

def find_ghostscript():
    """Trova l'eseguibile Ghostscript nel sistema"""
    system = platform.system()
    if system == "Windows":
        candidates = ["gswin64c.exe", "gswin32c.exe", "gs.exe"]
    else:
        candidates = ["gs"]

    # Cerca negli eseguibili del PATH
    for name in candidates:
        path = shutil.which(name)
        if path:
            return path

    # Cerca in percorsi comuni (solo su sistemi Unix-like)
    if system != "Windows":
        for path in ["/usr/bin/gs", "/usr/local/bin/gs", "/opt/local/bin/gs"]:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path

    return None

def center_window_on_screen(window, width, height):
    """Centra la finestra sullo schermo"""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def format_file_size(bytes_size):
    """Formatta la dimensione del file in formato leggibile"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

class TappoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TAPPO - Tool per Alleggerire PDF Pesanti Offline")
        self.configure(fg_color=APP_COLORS["background"])
        self.resizable(False, False)
        center_window_on_screen(self, 750, 320)

        # Variabili dell'applicazione
        self.gs_path = ctk.StringVar(value=find_ghostscript() or "")
        self.input_path = ctk.StringVar()
        self.output_path = ctk.StringVar()
        self.compression = ctk.StringVar(value="Alta qualità (/printer) - File di medie dimensioni")

        # Container principale che conterrà tutti i frame delle schermate
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Creazione dei frame per le diverse schermate
        self.main_content_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.guide_screen_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.credits_screen_frame = ctk.CTkFrame(self.container, fg_color="transparent")

        # Configurazione griglia per il frame principale (lasciato intatto)
        self.main_content_frame.grid_columnconfigure(0, weight=0) # Labels
        self.main_content_frame.grid_columnconfigure(1, weight=0) # Entries/Content
        self.main_content_frame.grid_columnconfigure(2, weight=0) # Buttons/Side Menu

        # Costruisci l'interfaccia utente per ogni schermata una volta sola all'avvio
        self.build_main_content_ui()
        self.build_guide_screen_ui()
        self.build_credits_screen_ui()

        # Mostra la schermata iniziale
        self.show_frame(self.main_content_frame)

    def show_frame(self, frame_to_show):
        """Nasconde tutti i frame e mostra quello selezionato."""
        for frame in [self.main_content_frame, self.guide_screen_frame, self.credits_screen_frame]:
            frame.grid_forget() # Rimuove il frame dalla griglia

        # Posiziona il frame desiderato nella griglia
        frame_to_show.grid(row=0, column=0, sticky="nsew") 
        # Assicurati che il frame interno possa espandersi per riempire il container
        frame_to_show.grid_columnconfigure(1, weight=1) # Rende la colonna dei contenuti espandibile

    def add_input_row(self, parent_frame, row, label_text, variable, browse_command=None):
        """Aggiunge una riga di input con label, entry e bottone opzionale al parent_frame specificato."""
        ctk.CTkLabel(parent_frame, text=label_text, **COMPONENT_STYLES['label']).grid(
            row=row, column=0, sticky="e", padx=(0, 15), pady=10
        )
        ctk.CTkEntry(parent_frame, textvariable=variable, **COMPONENT_STYLES['entry']).grid(
            row=row, column=1, sticky="", padx=0, pady=10
        )
        if browse_command:
            ctk.CTkButton(parent_frame, text="Sfoglia", command=browse_command, 
                         **COMPONENT_STYLES['button_primary']).grid(row=row, column=2, padx=(15, 0), pady=10)

    def build_main_content_ui(self):
        """Costruisce i widget per la schermata principale dell'applicazione."""
        # Righe di input
        self.add_input_row(self.main_content_frame, 0, "Ghostscript", self.gs_path, self.browse_gs)
        self.add_input_row(self.main_content_frame, 1, "PDF originale", self.input_path, self.browse_input)
        self.add_input_row(self.main_content_frame, 2, "File compresso", self.output_path, self.browse_output)

        # Livello di compressione
        ctk.CTkLabel(self.main_content_frame, text="Livello di compressione", **COMPONENT_STYLES['label']).grid(
            row=3, column=0, sticky="e", padx=(0, 15), pady=(10, 10)
        )

        ctk.CTkOptionMenu(
            self.main_content_frame, variable=self.compression, values=list(COMPRESSION_LEVELS.keys()), 
            **COMPONENT_STYLES['option_menu']
        ).grid(row=3, column=1, sticky="", padx=0, pady=(10, 10))

        # Menu laterale
        side_menu_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        side_menu_frame.grid(row=3, column=2, padx=(15, 0), pady=(10, 10))

        ctk.CTkButton(side_menu_frame, text="GUIDA", command=lambda: self.show_frame(self.guide_screen_frame), 
                     width=40, **COMPONENT_STYLES['button_menu']).pack(side="left", padx=(0, 5))
        ctk.CTkButton(side_menu_frame, text="CREDITS", command=lambda: self.show_frame(self.credits_screen_frame), 
                     width=50, **COMPONENT_STYLES['button_menu']).pack(side="left")

        # Bottone comprimi PDF
        ctk.CTkButton(
            self.main_content_frame, text="Comprimi PDF", command=self.compress_pdf,
            **COMPONENT_STYLES['button_compress']
        ).grid(row=5, column=0, columnspan=3, pady=(25, 0))

    def build_guide_screen_ui(self):
        """Costruisce i widget per la schermata della guida."""
        # Titolo centrato
        ctk.CTkLabel(self.guide_screen_frame, text="Come usare TAPPO", **COMPONENT_STYLES['title']).pack(pady=(0, 10))

        # Contenuto testuale
        guide_content = """───── INSTALLAZIONE GHOSTSCRIPT ─────

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
• La compressione varia in base al contenuto del PDF"""

        # Textbox centrata con larghezza massima (750 - 60 padding = 690)
        text_widget = ctk.CTkTextbox(self.guide_screen_frame, **COMPONENT_STYLES['textbox'])
        text_widget.pack(pady=(0, 15), expand=True, fill="both")
        text_widget.insert("0.0", guide_content)
        text_widget.configure(state="disabled")

        # Frame per i bottoni centrati
        button_frame = ctk.CTkFrame(self.guide_screen_frame, fg_color="transparent")
        button_frame.pack()

        ctk.CTkButton(button_frame, text='Scarica Ghostscript', command=self.open_ghostscript_download,
                      **COMPONENT_STYLES['button_primary']).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text='Indietro', command=lambda: self.show_frame(self.main_content_frame),
                      **COMPONENT_STYLES['button_secondary']).pack(side="left", padx=10)

    def build_credits_screen_ui(self):
        """Costruisce i widget per la schermata dei credits."""
        # Titolo centrato
        ctk.CTkLabel(self.credits_screen_frame, text="TAPPO", **COMPONENT_STYLES['title']).pack(pady=(0, 10))

        # Contenuto testuale
        credits_content = """───── TAPPO ─────

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
• CustomTkinter Community"""

        # Textbox centrata con larghezza massima (750 - 60 padding = 690)
        text_widget = ctk.CTkTextbox(self.credits_screen_frame, **COMPONENT_STYLES['textbox'])
        text_widget.pack(pady=(0, 15), expand=True, fill="both")
        text_widget.insert("0.0", credits_content)
        text_widget.configure(state="disabled")

        # Frame per i bottoni centrati
        button_frame = ctk.CTkFrame(self.credits_screen_frame, fg_color="transparent")
        button_frame.pack()

        ctk.CTkButton(button_frame, text='Pagina GitHub', command=self.open_github,
                      **COMPONENT_STYLES['button_primary']).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text='Indietro', command=lambda: self.show_frame(self.main_content_frame),
                      **COMPONENT_STYLES['button_secondary']).pack(side="left", padx=10)

    def open_ghostscript_download(self):
        """Apre la pagina di download di Ghostscript"""
        webbrowser.open("https://www.ghostscript.com/download/gsdnld.html")

    def open_github(self):
        """Apre la pagina GitHub del progetto"""
        webbrowser.open("https://github.com/Ghizza/TAPPO")

    def browse_gs(self):
        """Dialog per selezionare l'eseguibile Ghostscript"""
        if platform.system() == "Windows":
            filetypes = [("Eseguibili", "*.exe"), ("Tutti i files", "*.*")]
        else:
            filetypes = [("Tutti i files", "*.*")]

        file = filedialog.askopenfilename(title="Seleziona Ghostscript", filetypes=filetypes)
        if file:
            self.gs_path.set(file)

    def browse_input(self):
        """Dialog per selezionare il PDF di input"""
        file = filedialog.askopenfilename(
            title="Seleziona PDF da comprimere",
            filetypes=[("PDF files", "*.pdf"), ("Tutti i files", "*.*")]
        )
        if file:
            self.input_path.set(file)
            # Auto-genera il nome del file di output
            base, _ = os.path.splitext(file)
            self.output_path.set(base + " - compresso.pdf")

    def browse_output(self):
        """Dialog per selezionare il percorso di output"""
        file = filedialog.asksaveasfilename(
            title="Salva file compresso come",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("Tutti i files", "*.*")]
        )
        if file:
            self.output_path.set(file)

    def validate_inputs(self):
        """Valida tutti gli input necessari per la compressione"""
        gs = self.gs_path.get().strip()
        input_pdf = self.input_path.get().strip()
        output_pdf = self.output_path.get().strip()

        # Validazione Ghostscript
        if not gs:
            raise ValueError("Seleziona il percorso di Ghostscript.")
        if not os.path.exists(gs):
            raise ValueError("Ghostscript non trovato nel percorso specificato.")

        # Validazione file di input
        if not input_pdf:
            raise ValueError("Seleziona un file PDF da comprimere.")
        if not os.path.exists(input_pdf):
            raise ValueError("Il file PDF di input non esiste.")
        if not input_pdf.lower().endswith('.pdf'):
            raise ValueError("Il file di input deve essere un PDF.")

        # Validazione dimensioni file di input
        try:
            input_size = os.path.getsize(input_pdf)
            if input_size == 0:
                raise ValueError("Il file PDF di input è vuoto.")
        except OSError as e:
            raise ValueError(f"Impossibile leggere il file di input: {e}")

        # Validazione file di output
        if not output_pdf:
            raise ValueError("Specifica il percorso del file di output.")

        # Validazione directory di output
        output_dir = os.path.dirname(output_pdf)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError as e:
                raise ValueError(f"Impossibile creare la directory di output: {e}")

        # Test permessi di scrittura
        try:
            test_dir = output_dir if output_dir else '.'
            test_file = os.path.join(test_dir, 'test_write_tappo.tmp')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
        except (OSError, IOError):
            raise ValueError("Permessi insufficienti per scrivere nella directory di output.")

        # Validazione path identici
        try:
            if os.path.abspath(input_pdf) == os.path.abspath(output_pdf):
                raise ValueError("Il file di output non può essere uguale a quello di input.")
        except OSError:
            pass

        return gs, input_pdf, output_pdf

    def build_compression_command(self, gs_path, input_pdf, output_pdf, quality):
        """Costruisce il comando per Ghostscript"""
        return [
            gs_path,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={quality}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={output_pdf}",
            input_pdf
        ]

    def validate_compression_result(self, output_pdf):
        """Valida il risultato della compressione"""
        if not os.path.exists(output_pdf):
            raise RuntimeError("Il file compresso non è stato creato.")

        compressed_size = os.path.getsize(output_pdf)
        if compressed_size == 0:
            if os.path.exists(output_pdf):
                os.remove(output_pdf)
            raise RuntimeError("Il file compresso è vuoto. Possibile errore durante la compressione.")

        return compressed_size

    def show_compression_result(self, input_pdf, output_pdf, original_size, compressed_size):
        """Mostra i risultati della compressione"""
        saved_bytes = original_size - compressed_size
        saved_percent = (saved_bytes / original_size) * 100 if original_size > 0 else 0

        success_message = (
            f"File compresso salvato in:\n{output_pdf}\n\n"
            f"Dimensione originale: {format_file_size(original_size)}\n"
            f"Dimensione compressa: {format_file_size(compressed_size)}\n"
            f"Risparmio: {saved_percent:.1f}%"
        )

        if saved_percent < 0:
            success_message += "\n\nNota: Il file compresso è più grande dell'originale.\nProva un livello di compressione diverso."

        messagebox.showinfo("File compresso!", success_message)

    def compress_pdf(self):
        """Funzione principale per la compressione del PDF"""
        try:
            # Validazione input
            gs_path, input_pdf, output_pdf = self.validate_inputs()
            quality = COMPRESSION_LEVELS.get(self.compression.get(), "/printer")
            
            # Salva dimensione originale
            original_size = os.path.getsize(input_pdf)
            
            # Costruisci comando
            command = self.build_compression_command(gs_path, input_pdf, output_pdf, quality)

            # Esegui compressione
            result = subprocess.run(
                command, check=True, capture_output=True, 
                text=True, timeout=300
            )

            # Valida risultato
            compressed_size = self.validate_compression_result(output_pdf)
            
            # Mostra risultati
            self.show_compression_result(input_pdf, output_pdf, original_size, compressed_size)

        except ValueError as e:
            messagebox.showerror("Errore", str(e))
        except subprocess.TimeoutExpired:
            messagebox.showerror("Errore", 
                "Timeout: la compressione sta richiedendo troppo tempo.\n"
                "Prova con un file più piccolo o un livello di compressione diverso.")
        except subprocess.CalledProcessError as e:
            error_msg = f"Errore nella compressione del PDF.\nCodice di errore: {e.returncode}"
            if e.stderr:
                error_msg += f"\nDettagli: {e.stderr.strip()}"
            messagebox.showerror("Errore", error_msg)
        except RuntimeError as e:
            messagebox.showerror("Errore", str(e))
        except PermissionError:
            messagebox.showerror("Errore", "Permessi insufficienti per salvare il file.")
        except FileNotFoundError as e:
            messagebox.showerror("Errore", f"File non trovato: {e}")
        except OSError as e:
            messagebox.showerror("Errore", f"Errore del sistema operativo: {e}")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore imprevisto: {e}")

if __name__ == "__main__":
    app = TappoApp()
    app.mainloop()