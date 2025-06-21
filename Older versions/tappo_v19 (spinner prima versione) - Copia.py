#!/usr/bin/env python3

import customtkinter as ctk
import os
import platform
import shutil
import subprocess
import webbrowser
import threading
import time
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
    "spinner": "#0076d6", # Colore per lo spinner
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
        "text_color": APP_COLORS["border"]
    },
    
    "textbox": {
        "width": 650, 
        "height": 150,
        "font": (APP_FONTS["family"], 12),
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
# SPINNER COMPONENT
# ═══════════════════════════════════════════════════════════════════

class LoadingSpinner(ctk.CTkFrame):
    def __init__(self, master, size=50, **kwargs):
        super().__init__(master, **kwargs)
        
        self.size = size
        self.angle = 0
        self.is_running = False
        
        # Crea il canvas per disegnare lo spinner
        self.canvas = ctk.CTkCanvas(
            self, 
            width=size, 
            height=size, 
            bg=APP_COLORS["background"],
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Label per il testo
        self.status_label = ctk.CTkLabel(
            self,
            text="Compressione in corso...",
            font=(APP_FONTS["family"], APP_FONTS["size_normal"]),
            text_color=APP_COLORS["text_medium"]
        )
        self.status_label.pack(pady=(0, 10))
        
    def draw_spinner(self):
        """Disegna lo spinner sul canvas"""
        self.canvas.delete("all")
        
        center_x = self.size // 2
        center_y = self.size // 2
        radius = self.size // 3
        
        # Disegna 8 linee che formano lo spinner
        for i in range(8):
            angle = (self.angle + i * 45) % 360
            # Calcola l'opacità basata sulla posizione
            opacity = 1.0 - (i * 0.12)
            
            # Converti l'angolo in radianti
            import math
            angle_rad = math.radians(angle)
            
            # Calcola le coordinate della linea
            start_x = center_x + (radius * 0.6) * math.cos(angle_rad)
            start_y = center_y + (radius * 0.6) * math.sin(angle_rad)
            end_x = center_x + radius * math.cos(angle_rad)
            end_y = center_y + radius * math.sin(angle_rad)
            
            # Determina il colore basato sull'opacità
            color = self.blend_colors(APP_COLORS["spinner"], APP_COLORS["background"], opacity)
            
            self.canvas.create_line(
                start_x, start_y, end_x, end_y,
                fill=color, width=3, capstyle="round"
            )
    
    def blend_colors(self, color1, color2, ratio):
        """Miscela due colori hex basandosi su un ratio"""
        # Rimuovi il # se presente
        color1 = color1.lstrip('#')
        color2 = color2.lstrip('#')
        
        # Converti in RGB
        r1, g1, b1 = int(color1[0:2], 16), int(color1[2:4], 16), int(color1[4:6], 16)
        r2, g2, b2 = int(color2[0:2], 16), int(color2[2:4], 16), int(color2[4:6], 16)
        
        # Miscela i colori
        r = int(r1 * ratio + r2 * (1 - ratio))
        g = int(g1 * ratio + g2 * (1 - ratio))
        b = int(b1 * ratio + b2 * (1 - ratio))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def animate(self):
        """Anima lo spinner"""
        if self.is_running:
            self.angle = (self.angle + 45) % 360
            self.draw_spinner()
            self.after(100, self.animate)  # Aggiorna ogni 100ms
    
    def start(self):
        """Avvia l'animazione dello spinner"""
        self.is_running = True
        self.animate()
    
    def stop(self):
        """Ferma l'animazione dello spinner"""
        self.is_running = False

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
        
        # Variabili per il controllo dell'interfaccia
        self.is_compressing = False
        self.spinner_window = None
        self.compress_button = None

        # Setup interfaccia
        self.setup_main_frame()
        self.build_ui()

    def setup_main_frame(self):
        """Configura il frame principale e la griglia"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, padx=30, pady=30)

        # Configurazione griglia per il contenuto
        self.main_frame.grid_columnconfigure(0, weight=0)  # Labels
        self.main_frame.grid_columnconfigure(1, weight=0)  # Entries
        self.main_frame.grid_columnconfigure(2, weight=0)  # Buttons

    def build_ui(self):
        """Costruisce l'interfaccia utente"""
        self.show_main_content()

    def add_input_row(self, row, label_text, variable, browse_command=None):
        """Aggiunge una riga di input con label, entry e bottone opzionale"""
        ctk.CTkLabel(self.main_frame, text=label_text, **COMPONENT_STYLES['label']).grid(
            row=row, column=0, sticky="e", padx=(0, 15), pady=10
        )
        
        entry = ctk.CTkEntry(self.main_frame, textvariable=variable, **COMPONENT_STYLES['entry'])
        entry.grid(row=row, column=1, sticky="", padx=0, pady=10)
        
        if browse_command:
            button = ctk.CTkButton(self.main_frame, text="Sfoglia", command=browse_command, 
                         **COMPONENT_STYLES['button_primary'])
            button.grid(row=row, column=2, padx=(15, 0), pady=10)
            return entry, button
        return entry

    def show_main_content(self):
        """Mostra il contenuto principale dell'applicazione"""
        self.clear_main_frame()

        # Righe di input
        self.add_input_row(0, "Ghostscript", self.gs_path, self.browse_gs)
        self.add_input_row(1, "PDF originale", self.input_path, self.browse_input)
        self.add_input_row(2, "File compresso", self.output_path, self.browse_output)

        # Livello di compressione
        ctk.CTkLabel(self.main_frame, text="Livello di compressione", **COMPONENT_STYLES['label']).grid(
            row=3, column=0, sticky="e", padx=(0, 15), pady=(10, 10)
        )

        ctk.CTkOptionMenu(
            self.main_frame, variable=self.compression, values=list(COMPRESSION_LEVELS.keys()), 
            **COMPONENT_STYLES['option_menu']
        ).grid(row=3, column=1, sticky="", padx=0, pady=(10, 10))

        # Menu laterale
        self.create_side_menu()

        # Bottone comprimi PDF
        self.compress_button = ctk.CTkButton(
            self.main_frame, text="Comprimi PDF", command=self.compress_pdf,
            **COMPONENT_STYLES['button_compress']
        )
        self.compress_button.grid(row=5, column=0, columnspan=3, pady=(25, 0))

    def clear_main_frame(self):
        """Pulisce tutti i widget dal frame principale"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def create_side_menu(self):
        """Crea il menu laterale con i bottoni GUIDA e CREDITS"""
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.grid(row=3, column=2, padx=(15, 0), pady=(10, 10))

        ctk.CTkButton(frame, text="GUIDA", command=self.show_guide, 
                     width=40, **COMPONENT_STYLES['button_menu']).pack(side="left", padx=(0, 5))
        ctk.CTkButton(frame, text="CREDITS", command=self.show_credits, 
                     width=50, **COMPONENT_STYLES['button_menu']).pack(side="left")

    def create_info_screen(self, title, content, buttons):
        """Crea una schermata informativa generica"""
        self.clear_main_frame()

        # Titolo
        ctk.CTkLabel(self.main_frame, text=title, **COMPONENT_STYLES['title']).pack(pady=(0, 5))

        # Contenuto testuale
        text_widget = ctk.CTkTextbox(self.main_frame, **COMPONENT_STYLES['textbox'])
        text_widget.pack(pady=5, padx=10, fill="both", expand=True)
        text_widget.insert("0.0", content)
        text_widget.configure(state="disabled")

        # Frame per i bottoni
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=(5, 10))

        # Crea i bottoni dinamicamente
        for button_config in buttons:
            btn = ctk.CTkButton(
                button_frame, text=button_config['text'], 
                command=button_config['command'], **button_config['style']
            )
            btn.pack(side="left", padx=10)

    def create_loading_overlay(self):
        """Crea una finestra di caricamento modale"""
        self.spinner_window = ctk.CTkToplevel(self)
        self.spinner_window.title("Compressione in corso")
        self.spinner_window.configure(fg_color=APP_COLORS["background"])
        self.spinner_window.resizable(False, False)
        
        # Rendi la finestra modale
        self.spinner_window.transient(self)
        self.spinner_window.grab_set()
        
        # Centra la finestra di loading
        center_window_on_screen(self.spinner_window, 300, 150)
        
        # Crea lo spinner
        self.spinner = LoadingSpinner(
            self.spinner_window,
            size=60,
            fg_color="transparent"
        )
        self.spinner.pack(expand=True, fill="both")
        
        # Avvia l'animazione
        self.spinner.start()
        
        # Previeni la chiusura della finestra
        self.spinner_window.protocol("WM_DELETE_WINDOW", lambda: None)

    def hide_loading_overlay(self):
        """Nasconde la finestra di caricamento"""
        if self.spinner_window:
            self.spinner.stop()
            self.spinner_window.grab_release()
            self.spinner_window.destroy()
            self.spinner_window = None

    def show_guide(self):
        """Mostra la schermata della guida"""
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

        buttons = [
            {
                'text': 'Scarica Ghostscript',
                'command': self.open_ghostscript_download,
                'style': COMPONENT_STYLES['button_primary']
            },
            {
                'text': 'Indietro',
                'command': self.show_main_content,
                'style': COMPONENT_STYLES['button_secondary']
            }
        ]

        self.create_info_screen("Come usare TAPPO", guide_content, buttons)

    def show_credits(self):
        """Mostra la schermata dei credits"""
        credits_content = """───── TAPPO ─────

Tool per Alleggerire PDF Pesanti Offline

───── INFORMAZIONI ─────

• Versione: 2.0
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
• Indicatore di progresso durante la compressione

───── RINGRAZIAMENTI ─────

• Ghostscript Development Team
• Python Software Foundation
• CustomTkinter Community"""

        buttons = [
            {
                'text': 'Pagina GitHub',
                'command': self.open_github,
                'style': COMPONENT_STYLES['button_primary']
            },
            {
                'text': 'Indietro',
                'command': self.show_main_content,
                'style': COMPONENT_STYLES['button_secondary']
            }
        ]

        self.create_info_screen("TAPPO", credits_content, buttons)

    def open_ghostscript_download(self):
        """Apre la pagina di download di Ghostscript"""
        webbrowser.open("https://www.ghostscript.com/download/gsdnld.html")

    def open_github(self):
        """Apre la pagina GitHub del progetto"""
        webbrowser.open("https://github.com/Ghizza/TAPPO")

    def browse_gs(self):
        """Dialog per selezionare l'eseguibile Ghostscript"""
        if self.is_compressing:
            return
            
        if platform.system() == "Windows":
            filetypes = [("Eseguibili", "*.exe"), ("Tutti i files", "*.*")]
        else:
            filetypes = [("Tutti i files", "*.*")]

        file = filedialog.askopenfilename(title="Seleziona Ghostscript", filetypes=filetypes)
        if file:
            self.gs_path.set(file)

    def browse_input(self):
        """Dialog per selezionare il PDF di input"""
        if self.is_compressing:
            return
            
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
        if self.is_compressing:
            return
            
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

    def compression_worker(self, gs_path, input_pdf, output_pdf, quality, original_size):
        """Worker thread per eseguire la compressione"""
        try:
            # Costruisci comando
            command = self.build_compression_command(gs_path, input_pdf, output_pdf, quality)

            # Esegui compressione
            result = subprocess.run(
                command, check=True, capture_output=True, 
                text=True, timeout=300
            )

            # Valida risultato
            compressed_size = self.validate_compression_result(output_pdf)
            
            # Programma l'aggiornamento dell'UI nel thread principale
            self.after(0, lambda: self.compression_completed(
                input_pdf, output_pdf, original_size, compressed_size, None
            ))

        except Exception as e:
            # Programma la gestione dell'errore nel thread principale
            self.after(0, lambda: self.compression_completed(
                input_pdf, output_pdf, original_size, 0, e
            ))

    def compression_completed(self, input_pdf, output_pdf, original_size, compressed_size, error):
        """Callback chiamato quando la compressione è completata"""
        # Nascondi lo spinner
        self.hide_loading_overlay()
        
        # Riabilita l'interfaccia
        self.is_compressing = False
        if self.compress_button:
            self.compress_button.configure(state="normal", text="Comprimi PDF")

        if error:
            # Gestisci gli errori
            if isinstance(error, ValueError):
                messagebox.showerror("Errore", str(error))
            elif isinstance(error, subprocess.TimeoutExpired):
                messagebox.showerror("Errore", 
                    "Timeout: la compressione sta richiedendo troppo tempo.\n"
                    "Prova con un file più piccolo o un livello di compressione diverso.")
            elif isinstance(error, subprocess.CalledProcessError):
                error_msg = f"Errore nella compressione del PDF.\nCodice di errore: {error.returncode}"
                if hasattr(error, 'stderr') and error.stderr:
                    error_msg += f"\nDettagli: {error.stderr.strip()}"
                messagebox.showerror("Errore", error_msg)
            elif isinstance(error, RuntimeError):
                messagebox.showerror("Errore", str(error))
            elif isinstance(error, PermissionError):
                messagebox.showerror("Errore", "Permessi insufficienti per salvare il file.")
            elif isinstance(error, FileNotFoundError):
                messagebox.showerror("Errore", f"File non trovato: {error}")
            elif isinstance(error, OSError):
                messagebox.showerror("Errore", f"Errore del sistema operativo: {error}")
            else:
                messagebox.showerror("Errore", f"Errore imprevisto: {error}")
        else:
            # Mostra i risultati del successo
            self.show_compression_result(input_pdf, output_pdf, original_size, compressed_size)

    def compress_pdf(self):
        """Funzione principale per la compressione del PDF"""
        # Previeni multiple compressioni simultanee
        if self.is_compressing:
            return

        try:
            # Validazione input
            gs_path, input_pdf, output_pdf = self.validate_inputs()
            quality = COMPRESSION_LEVELS.get(self.compression.get(), "/printer")
            
            # Salva dimensione originale
            original_size = os.path.getsize(input_pdf)
            
            # Imposta stato di compressione
            self.is_compressing = True
            
            # Disabilita il bottone e cambia il testo
            if self.compress_button:
                self.compress_button.configure(state="disabled", text="Compressione...")
            
            # Mostra lo spinner
            self.create_loading_overlay()
            
            # Avvia la compressione in un thread separato
            compression_thread = threading.Thread(
                target=self.compression_worker,
                args=(gs_path, input_pdf, output_pdf, quality, original_size),
                daemon=True
            )
            compression_thread.start()

        except ValueError as e:
            self.is_compressing = False
            if self.compress_button:
                self.compress_button.configure(state="normal", text="Comprimi PDF")
            messagebox.showerror("Errore", str(e))
        except Exception as e:
            self.is_compressing = False
            if self.compress_button:
                self.compress_button.configure(state="normal", text="Comprimi PDF")
            messagebox.showerror("Errore", f"Errore imprevisto: {e}")

if __name__ == "__main__":
    app = TappoApp()
    app.mainloop()