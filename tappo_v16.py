<<<<<<< HEAD
=======
#!/usr/bin/env python3

>>>>>>> 2b623e89c17a016c77ffecccdd9f14aea38e7e5b
import customtkinter as ctk
import os
import platform
import shutil
import subprocess
import webbrowser
<<<<<<< HEAD
from tkinter import filedialog, messagebox

APP_COLORS = {
    "background": "#262626",
    "dark": "#191919",
    "hover": "#333333",
    "text": "#7f7f7f",
    "text_medium": "#cccccc",
    "text_light": "#d9d9d9",
    "border": "#666666",
    "link_01": "#0076d6",
    "link_02": "#44d62c",
}

APP_STYLE = {
=======
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
>>>>>>> 2b623e89c17a016c77ffecccdd9f14aea38e7e5b
    "corner_radius": 5,
    "border_width": 1
}

COMPRESSION_LEVELS = {
<<<<<<< HEAD
    "Bassa qualit\u00e0 (/screen) - File leggerissimo": "/screen",
    "Media qualit\u00e0 (/ebook) - File leggero": "/ebook",
    "Alta qualit\u00e0 (/printer) - File di medie dimensioni": "/printer",
    "Altissima qualit\u00e0 (/prepress) - File pi\u00f9 pesante": "/prepress"
}

def center_window_on_screen(window, width, height):
=======
    "Bassa qualità (/screen) - File leggerissimo": "/screen",
    "Media qualità (/ebook) - File leggero": "/ebook",
    "Alta qualità (/printer) - File di medie dimensioni": "/printer",
    "Altissima qualità (/prepress) - File più pesante": "/prepress"
}

def register_custom_font():
    """Registra il font personalizzato per la distribuzione dell'app"""
    font_path = Path(__file__).parent / "fonts" / "PublicSans-VariableFont_wght.ttf"
    if not font_path.exists():
        print(f"[ERRORE] Font non trovato: {font_path}")
        return

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
>>>>>>> 2b623e89c17a016c77ffecccdd9f14aea38e7e5b
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

<<<<<<< HEAD
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

def format_file_size(bytes_size):
=======
def format_file_size(bytes_size):
    """Formatta la dimensione del file in formato leggibile"""
>>>>>>> 2b623e89c17a016c77ffecccdd9f14aea38e7e5b
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

<<<<<<< HEAD
        self.gs_path = ctk.StringVar(value=find_ghostscript() or "")
        self.input_path = ctk.StringVar()
        self.output_path = ctk.StringVar()
        self.compression = ctk.StringVar(value="Alta qualit\u00e0 (/printer) - File di medie dimensioni")

=======
        # Variabili dell'applicazione
        self.gs_path = ctk.StringVar(value=find_ghostscript() or "")
        self.input_path = ctk.StringVar()
        self.output_path = ctk.StringVar()
        self.compression = ctk.StringVar(value="Alta qualità (/printer) - File di medie dimensioni")

        # Setup interfaccia
>>>>>>> 2b623e89c17a016c77ffecccdd9f14aea38e7e5b
        self.setup_main_frame()
        self.build_ui()

    def setup_main_frame(self):
<<<<<<< HEAD
=======
        """Configura il frame principale e la griglia"""
>>>>>>> 2b623e89c17a016c77ffecccdd9f14aea38e7e5b
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
<<<<<<< HEAD
        self.main_frame.grid(row=0, column=0, sticky="n", padx=0, pady=30)

        self.main_frame.grid_columnconfigure(0, weight=0)
        self.main_frame.grid_columnconfigure(1, weight=0)
        self.main_frame.grid_columnconfigure(2, weight=0)

    def build_ui(self):
        self.show_main_content()

    def get_ui_styles(self):
        return {
            'label': {
                "font": ("Segoe UI", 13, "bold"), 
                "text_color": APP_COLORS["text"]
            },
            'entry': {
                "width": 350, "font": ("Segoe UI", 13),
=======
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

        # Configurazione griglia per centrare il contenuto
        self.main_frame.grid_columnconfigure(0, weight=0)  # Labels
        self.main_frame.grid_columnconfigure(1, weight=0)  # Entries
        self.main_frame.grid_columnconfigure(2, weight=0)  # Buttons

    def build_ui(self):
        """Costruisce l'interfaccia utente"""
        self.show_main_content()

    def get_ui_styles(self):
        """Restituisce i dizionari di stile per i componenti UI"""
        return {
            'label': {
                "font": ("Public Sans", 13, "bold"), 
                "text_color": APP_COLORS["text"]
            },
            'entry': {
                "width": 350, "font": ("Public Sans", 13),
>>>>>>> 2b623e89c17a016c77ffecccdd9f14aea38e7e5b
                "fg_color": APP_COLORS["dark"], "text_color": APP_COLORS["text_light"],
                "border_color": APP_COLORS["border"], "corner_radius": 5, "border_width": 1,
            },
            'button': {
                "fg_color": APP_COLORS["dark"], "hover_color": APP_COLORS["hover"],
                "text_color": APP_COLORS["link_01"], "corner_radius": 5,
<<<<<<< HEAD
                "font": ("Segoe UI", 13, "bold"), "border_width": 1, 
=======
                "font": ("Public Sans", 13, "bold"), "border_width": 1, 
>>>>>>> 2b623e89c17a016c77ffecccdd9f14aea38e7e5b
                "border_color": APP_COLORS["link_01"],
            }
        }

    def add_input_row(self, row, label_text, variable, browse_command=None):
<<<<<<< HEAD
        styles = self.get_ui_styles()
=======
        """Aggiunge una riga di input con label, entry e bottone opzionale"""
        styles = self.get_ui_styles()
        
>>>>>>> 2b623e89c17a016c77ffecccdd9f14aea38e7e5b
        ctk.CTkLabel(self.main_frame, text=label_text, **styles['label']).grid(
            row=row, column=0, sticky="e", padx=(0, 5), pady=10
        )
        ctk.CTkEntry(self.main_frame, textvariable=variable, **styles['entry']).grid(
            row=row, column=1, sticky="", padx=10, pady=10
        )
        if browse_command:
            ctk.CTkButton(self.main_frame, text="Sfoglia", command=browse_command, 
                         **styles['button']).grid(row=row, column=2, padx=(5, 0), pady=10)

    def show_main_content(self):
<<<<<<< HEAD
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        styles = self.get_ui_styles()
=======
        """Mostra il contenuto principale dell'applicazione"""
        self.clear_main_frame()
        styles = self.get_ui_styles()

        # Righe di input
>>>>>>> 2b623e89c17a016c77ffecccdd9f14aea38e7e5b
        self.add_input_row(0, "Ghostscript", self.gs_path, self.browse_gs)
        self.add_input_row(1, "PDF originale", self.input_path, self.browse_input)
        self.add_input_row(2, "File compresso", self.output_path, self.browse_output)

<<<<<<< HEAD
        ctk.CTkLabel(self.main_frame, text="Livello di compressione", **styles['label']).grid(
            row=3, column=0, sticky="e", padx=(0, 5), pady=(10, 10)
        )
        ctk.CTkOptionMenu(
            self.main_frame, variable=self.compression, values=list(COMPRESSION_LEVELS.keys()), 
            width=350, font=("Segoe UI", 13), fg_color=APP_COLORS["dark"], 
=======
        # Livello di compressione
        ctk.CTkLabel(self.main_frame, text="Livello di compressione", **styles['label']).grid(
            row=3, column=0, sticky="e", padx=(0, 5), pady=(10, 10)
        )

        ctk.CTkOptionMenu(
            self.main_frame, variable=self.compression, values=list(COMPRESSION_LEVELS.keys()), 
            width=350, font=(APP_STYLE["font_family"], 13), fg_color=APP_COLORS["dark"], 
>>>>>>> 2b623e89c17a016c77ffecccdd9f14aea38e7e5b
            button_color=APP_COLORS["link_01"], button_hover_color=APP_COLORS["border"], 
            text_color=APP_COLORS["text_light"], dropdown_fg_color=APP_COLORS["dark"], 
            dropdown_text_color=APP_COLORS["text_light"], dropdown_hover_color=APP_COLORS["link_01"], 
            corner_radius=APP_STYLE["corner_radius"]
        ).grid(row=3, column=1, sticky="", padx=5, pady=(10, 10))

<<<<<<< HEAD
        compress_button = ctk.CTkButton(
            self.main_frame, text="Comprimi PDF", command=self.compress_pdf,
            fg_color=APP_COLORS["dark"], hover_color=APP_COLORS["hover"],
            text_color=APP_COLORS["link_02"], font=("Segoe UI", 13, "bold"),
=======
        # Menu laterale
        self.create_side_menu()

        # Bottone comprimi PDF
        compress_button = ctk.CTkButton(
            self.main_frame, text="Comprimi PDF", command=self.compress_pdf,
            fg_color=APP_COLORS["dark"], hover_color=APP_COLORS["hover"],
            text_color=APP_COLORS["link_02"], font=(APP_STYLE["font_family"], 13, "bold"),
>>>>>>> 2b623e89c17a016c77ffecccdd9f14aea38e7e5b
            corner_radius=APP_STYLE["corner_radius"], height=40, width=200,
            border_width=APP_STYLE["border_width"], border_color=APP_COLORS["link_02"]
        )
        compress_button.grid(row=5, column=0, columnspan=3, pady=(25, 0))

<<<<<<< HEAD
    def browse_gs(self):
        filetypes = [("Eseguibili", "*.exe"), ("Tutti i files", "*.*")] if platform.system() == "Windows" else [("Tutti i files", "*.*")]
=======
    def clear_main_frame(self):
        """Pulisce tutti i widget dal frame principale"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def create_side_menu(self):
        """Crea il menu laterale con i bottoni GUIDA e CREDITS"""
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.grid(row=3, column=2, padx=(5, 0), pady=(10, 10))

        menu_button_style = {
            "fg_color": "transparent", "hover_color": APP_COLORS["hover"],
            "text_color": APP_COLORS["link_01"], 
            "font": (APP_STYLE["font_family"], 11, "bold"), "height": 24
        }

        ctk.CTkButton(frame, text="GUIDA", command=self.show_guide, 
                     width=40, **menu_button_style).pack(side="left", padx=(0, 5))
        ctk.CTkButton(frame, text="CREDITS", command=self.show_credits, 
                     width=50, **menu_button_style).pack(side="left")

    def create_info_screen(self, title, content, buttons):
        """Crea una schermata informativa generica"""
        self.clear_main_frame()

        # Titolo
        title_label = ctk.CTkLabel(
            self.main_frame, text=title,
            font=(APP_STYLE["font_family"], 16, "bold"),
            text_color=APP_COLORS["border"]
        )
        title_label.pack(pady=(0, 5))

        # Contenuto testuale
        text_widget = ctk.CTkTextbox(
            self.main_frame, width=650, height=150,
            font=(APP_STYLE["font_family"], 12),
            fg_color=APP_COLORS["dark"], text_color=APP_COLORS["text_medium"],
            corner_radius=APP_STYLE["corner_radius"], wrap="word"
        )
        text_widget.pack(pady=5, padx=10, fill="both", expand=True)
        text_widget.insert("0.0", content)
        text_widget.configure(state="disabled")

        # Frame per i bottoni
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=(5, 10))

        # Crea i bottoni dinamicamente
        for button_config in buttons:
            btn = ctk.CTkButton(
                button_frame, **button_config['style'], 
                text=button_config['text'], command=button_config['command']
            )
            btn.pack(side="left", padx=10)

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

        button_style_primary = {
            "fg_color": APP_COLORS["dark"], "hover_color": APP_COLORS["hover"],
            "text_color": APP_COLORS["link_01"], "font": (APP_STYLE["font_family"], 13, "bold"),
            "corner_radius": APP_STYLE["corner_radius"], "border_width": 1,
            "border_color": APP_COLORS["link_01"], "width": 150
        }

        button_style_secondary = {
            "fg_color": APP_COLORS["dark"], "hover_color": APP_COLORS["hover"],
            "text_color": APP_COLORS["text"], "font": (APP_STYLE["font_family"], 13, "bold"),
            "corner_radius": APP_STYLE["corner_radius"], "border_width": APP_STYLE["border_width"],
            "border_color": APP_COLORS["border"], "width": 150
        }

        buttons = [
            {
                'text': 'Scarica Ghostscript',
                'command': self.open_ghostscript_download,
                'style': button_style_primary
            },
            {
                'text': 'Indietro',
                'command': self.show_main_content,
                'style': button_style_secondary
            }
        ]

        self.create_info_screen("Come usare TAPPO", guide_content, buttons)

    def show_credits(self):
        """Mostra la schermata dei credits"""
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

        button_style_primary = {
            "fg_color": APP_COLORS["dark"], "hover_color": APP_COLORS["hover"],
            "text_color": APP_COLORS["link_01"], "font": (APP_STYLE["font_family"], 13, "bold"),
            "corner_radius": APP_STYLE["corner_radius"], "border_width": 1,
            "border_color": APP_COLORS["link_01"], "width": 150
        }

        button_style_secondary = {
            "fg_color": APP_COLORS["dark"], "hover_color": APP_COLORS["hover"],
            "text_color": APP_COLORS["text"], "font": (APP_STYLE["font_family"], 13, "bold"),
            "corner_radius": APP_STYLE["corner_radius"], "border_width": APP_STYLE["border_width"],
            "border_color": APP_COLORS["border"], "width": 150
        }

        buttons = [
            {
                'text': 'Pagina GitHub',
                'command': self.open_github,
                'style': button_style_primary
            },
            {
                'text': 'Indietro',
                'command': self.show_main_content,
                'style': button_style_secondary
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
        if platform.system() == "Windows":
            filetypes = [("Eseguibili", "*.exe"), ("Tutti i files", "*.*")]
        else:
            filetypes = [("Tutti i files", "*.*")]

>>>>>>> 2b623e89c17a016c77ffecccdd9f14aea38e7e5b
        file = filedialog.askopenfilename(title="Seleziona Ghostscript", filetypes=filetypes)
        if file:
            self.gs_path.set(file)

    def browse_input(self):
<<<<<<< HEAD
        file = filedialog.askopenfilename(title="Seleziona PDF da comprimere", filetypes=[("PDF files", "*.pdf"), ("Tutti i files", "*.*")])
        if file:
            self.input_path.set(file)
=======
        """Dialog per selezionare il PDF di input"""
        file = filedialog.askopenfilename(
            title="Seleziona PDF da comprimere",
            filetypes=[("PDF files", "*.pdf"), ("Tutti i files", "*.*")]
        )
        if file:
            self.input_path.set(file)
            # Auto-genera il nome del file di output
>>>>>>> 2b623e89c17a016c77ffecccdd9f14aea38e7e5b
            base, _ = os.path.splitext(file)
            self.output_path.set(base + " - compresso.pdf")

    def browse_output(self):
<<<<<<< HEAD
        file = filedialog.asksaveasfilename(title="Salva file compresso come", defaultextension=".pdf", filetypes=[("PDF files", "*.pdf"), ("Tutti i files", "*.*")])
        if file:
            self.output_path.set(file)

    def compress_pdf(self):
        try:
            gs = self.gs_path.get().strip()
            input_pdf = self.input_path.get().strip()
            output_pdf = self.output_path.get().strip()
            quality = COMPRESSION_LEVELS.get(self.compression.get(), "/printer")

            if not gs or not os.path.exists(gs):
                raise ValueError("Ghostscript non trovato.")
            if not input_pdf or not os.path.exists(input_pdf):
                raise ValueError("PDF originale non valido.")
            if not output_pdf:
                raise ValueError("Percorso di output mancante.")

            original_size = os.path.getsize(input_pdf)
            command = [gs, "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", f"-dPDFSETTINGS={quality}", "-dNOPAUSE", "-dQUIET", "-dBATCH", f"-sOutputFile={output_pdf}", input_pdf]

            subprocess.run(command, check=True, capture_output=True, timeout=300)
            if not os.path.exists(output_pdf):
                raise RuntimeError("Il file compresso non \u00e8 stato creato.")
            compressed_size = os.path.getsize(output_pdf)
            saved = original_size - compressed_size
            percent = (saved / original_size) * 100 if original_size > 0 else 0
            message = f"File salvato in: {output_pdf}\n\nOriginale: {format_file_size(original_size)}\nCompresso: {format_file_size(compressed_size)}\nRisparmio: {percent:.1f}%"
            messagebox.showinfo("Compressione completata", message)
        except Exception as e:
            messagebox.showerror("Errore", str(e))

if __name__ == "__main__":
    app = TappoApp()
    app.mainloop()
=======
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
    register_custom_font()
    app = TappoApp()
    app.mainloop()
>>>>>>> 2b623e89c17a016c77ffecccdd9f14aea38e7e5b
