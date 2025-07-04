#!/usr/bin/env python3
import customtkinter as ctk
import sys
import os
import platform
import shutil
import subprocess
import webbrowser
import threading
from tkinter import filedialog, messagebox, PhotoImage

if platform.system() == "Windows":
    import ctypes
    from ctypes import windll, byref, sizeof, c_int

# ==================== ICON & DPI CONFIGURATION ====================
def configure_windows_dpi_and_icon(app):
    """Configura DPI awareness e icona per Windows"""
    try:
        # Configurazione DPI avanzata (Full DPI awareness)
        windll.shcore.SetProcessDpiAwareness(2)
        windll.user32.SetProcessDPIAware()
        
        # Caricamento icona ad alta risoluzione
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "tappo_icon.ico")
        
        if os.path.exists(icon_path):
            # Metodo standard per l'icona
            app.iconbitmap(default=icon_path)
            
            # Metodo avanzato per forzare l'icona ad alta risoluzione
            hwnd = windll.user32.GetParent(app.winfo_id())
            WM_SETICON = 0x80
            ICON_BIG = 1
            LR_LOADFROMFILE = 0x10
            LR_DEFAULTSIZE = 0x40
            
            hicon = windll.user32.LoadImageW(
                0, icon_path, 1, 0, 0, LR_LOADFROMFILE | LR_DEFAULTSIZE
            )
            
            if hicon:
                windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hicon)
            
            # Imposta AppUserModelID per la taskbar
            windll.shell32.SetCurrentProcessExplicitAppUserModelID('tappo.app.1.1.0')
            
    except Exception as e:
        print(f"[WARNING] Icon/DPI configuration failed: {e}")

APP_COLORS = {
    "background": "#262626",
    "dark": "#191919",
    "hover": "#333333",
    "text": "#7f7f7f",
    "text_medium": "#cccccc",
    "text_light": "#d9d9d9",
    "border": "#666666",
    "link_01": "#367bf0",
    "link_02": "#ffbb11",
}

APP_FONTS = {
    "family": ("Segoe UI", "DejaVu Sans", "Liberation Sans", "Helvetica", "Arial", "sans-serif"),
    "size_small": 11,
    "size_normal": 13,
    "size_medium": 14,
    "size_large": 15,
}

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
        "font": (APP_FONTS["family"], APP_FONTS["size_medium"], "bold"),
        "border_width": 1,
        "border_color": APP_COLORS["border"],
        "width": 150
    },
    
    "button_compress": {
        "fg_color": APP_COLORS["dark"],
        "hover_color": APP_COLORS["hover"],
        "text_color": APP_COLORS["link_02"],
        "corner_radius": 5,
        "font": (APP_FONTS["family"], APP_FONTS["size_large"], "bold"),
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
        "border_spacing": 10,
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

def format_file_size(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

class LoadingDialog:
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("")
        self.dialog.geometry("350x80")
        self.dialog.resizable(False, False)
        self.dialog.configure(fg_color=APP_COLORS["background"])
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 175
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 40
        self.dialog.geometry(f"350x80+{x}+{y}")
        
        self.label = ctk.CTkLabel(
            self.dialog, 
            text="- Compressione in corso -",
            font=(APP_FONTS["family"], APP_FONTS["size_medium"], "bold"),
            text_color=APP_COLORS["text_light"]
        )
        self.label.pack(expand=True)
        
        self.running = True
        self.animation_step = 0
        self.animate_text()
    
    def animate_text(self):
        if not self.running:
            return
        
        animations = [
        "[     Compressione in corso     ]",
        "|[    Compressione in corso    ]|",
        "||[   Compressione in corso   ]||",
        "|||[  Compressione in corso  ]|||",
        "||||[ Compressione in corso ]||||",
        "|||[  Compressione in corso  ]|||",
        "||[   Compressione in corso   ]||",
        "|[    Compressione in corso    ]|",
        ]
        
        self.label.configure(text=animations[self.animation_step])
        self.animation_step = (self.animation_step + 1) % len(animations)
        
        self.dialog.after(300, self.animate_text)
    
    def close(self):
        self.running = False
        if self.dialog.winfo_exists():
            self.dialog.grab_release()
            self.dialog.destroy()

class TappoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configura DPI e icona solo su Windows
        if platform.system() == "Windows":
            configure_windows_dpi_and_icon(self)
        elif platform.system() == "Linux":
            try:
                from tkinter import PhotoImage  # Assicurati che sia importato in cima al file
                base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
                icon_path = os.path.join(base_path, "tappo_icon.png")
                if os.path.exists(icon_path):
                    icon_img = PhotoImage(file=icon_path)
                    self.iconphoto(True, icon_img)
            except Exception as e:
                print(f"[WARNING] Impossibile impostare l'icona su Linux: {e}")

        # Il resto del tuo __init__ rimane uguale
        self.title("TAPPO - Tool per Alleggerire PDF Pesanti Offline")
        self.configure(fg_color=APP_COLORS["background"])
        self.resizable(False, False)
        center_window_on_screen(self, 750, 320)

        gs_found = find_ghostscript()
        if gs_found:
            self.gs_path = ctk.StringVar(value=gs_found)
        else:
            self.gs_path = ctk.StringVar(value="Ghostscript non trovato -> Leggi la GUIDA qui sotto!")
        
        self.input_path = ctk.StringVar()
        self.output_path = ctk.StringVar()
        self.compression = ctk.StringVar(value="Alta qualità (/printer) - File di medie dimensioni")

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_content_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.guide_screen_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.credits_screen_frame = ctk.CTkFrame(self.container, fg_color="transparent")

        self.main_content_frame.grid_columnconfigure(0, weight=0)
        self.main_content_frame.grid_columnconfigure(1, weight=0)
        self.main_content_frame.grid_columnconfigure(2, weight=0)

        self.build_main_content_ui()
        self.build_guide_screen_ui()
        self.build_credits_screen_ui()

        self.show_frame(self.main_content_frame)

    def show_frame(self, frame_to_show):
        for frame in [self.main_content_frame, self.guide_screen_frame, self.credits_screen_frame]:
            frame.grid_forget()

        frame_to_show.grid(row=0, column=0, sticky="nsew")
        frame_to_show.grid_columnconfigure(1, weight=1)

    def add_input_row(self, parent_frame, row, label_text, variable, browse_command=None):
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
        self.add_input_row(self.main_content_frame, 0, "Ghostscript", self.gs_path, self.browse_gs)
        self.add_input_row(self.main_content_frame, 1, "PDF originale", self.input_path, self.browse_input)
        self.add_input_row(self.main_content_frame, 2, "File compresso", self.output_path, self.browse_output)

        ctk.CTkLabel(self.main_content_frame, text="Livello di compressione", **COMPONENT_STYLES['label']).grid(
            row=3, column=0, sticky="e", padx=(0, 15), pady=(10, 10)
        )

        ctk.CTkOptionMenu(
            self.main_content_frame, variable=self.compression, values=list(COMPRESSION_LEVELS.keys()),
            **COMPONENT_STYLES['option_menu']
        ).grid(row=3, column=1, sticky="", padx=0, pady=(10, 10))

        side_menu_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        side_menu_frame.grid(row=3, column=2, padx=(15, 0), pady=(10, 10))

        ctk.CTkButton(side_menu_frame, text="GUIDA", command=lambda: self.show_frame(self.guide_screen_frame),
                     width=40, **COMPONENT_STYLES['button_menu']).pack(side="left", padx=(0, 5))
        ctk.CTkButton(side_menu_frame, text="CREDITS", command=lambda: self.show_frame(self.credits_screen_frame),
                     width=50, **COMPONENT_STYLES['button_menu']).pack(side="left")

        ctk.CTkButton(
            self.main_content_frame, text="Comprimi PDF", command=self.compress_pdf,
            **COMPONENT_STYLES['button_compress']
        ).grid(row=5, column=0, columnspan=3, pady=(25, 0))

    def build_guide_screen_ui(self):
        ctk.CTkLabel(self.guide_screen_frame, text="Come usare TAPPO", **COMPONENT_STYLES['title']).pack(pady=(0, 10))

        guide_content = """——— INSTALLAZIONE GHOSTSCRIPT ———

Questa applicazione richiede l'installazione di Ghostscript sul sistema operativo dell'utente.
Ghostscript è un interprete per i formati PostScript (PS) e PDF, disponibile sotto licenza AGPL.

• SU WINDOWS:
    - Scarica Ghostscript dal link in basso (AGPL Release)

• SU LINUX:
    - Debian/Ubuntu: sudo apt install ghostscript
    - Arch Linux: sudo pacman -S ghostscript
    - Fedora: sudo dnf install ghostscript

——— COME USARE TAPPO ———

• Seleziona il percorso di Ghostscript (se non rilevato automaticamente)
• Scegli il file PDF da comprimere
• Specifica dove salvare il PDF compresso
• Seleziona il livello di compressione desiderato
• Clicca su "Comprimi PDF"

——— LIVELLI DI COMPRESSIONE ———

• Bassa qualità: Massima compressione, qualità ridotta
• Media qualità: Buon compromesso per lettura digitale
• Alta qualità: Buona qualità per stampa normale
• Altissima qualità: Qualità professionale per stampa

——— NOTE ———

• I tempi di elaborazione dipendono dalla dimensione del file
• Il file originale non viene modificato
• La compressione varia in base al contenuto del PDF"""

        text_widget = ctk.CTkTextbox(self.guide_screen_frame, **COMPONENT_STYLES['textbox'])
        text_widget.pack(pady=(0, 15), expand=True, fill="both")
        text_widget.insert("0.0", guide_content)
        text_widget.configure(state="disabled")

        button_frame = ctk.CTkFrame(self.guide_screen_frame, fg_color="transparent")
        button_frame.pack()

        ctk.CTkButton(button_frame, text='Scarica Ghostscript', command=self.open_ghostscript_download,
                      **COMPONENT_STYLES['button_primary']).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text='Indietro', command=lambda: self.show_frame(self.main_content_frame),
                      **COMPONENT_STYLES['button_secondary']).pack(side="left", padx=10)

    def build_credits_screen_ui(self):
        ctk.CTkLabel(self.credits_screen_frame, text="TAPPO - Tool per Alleggerire PDF Pesanti Offline", **COMPONENT_STYLES['title']).pack(pady=(0, 10))

        credits_content = """• Versione: 1.0.1
• Creato da: Ghizza
• Licenza: MIT License
• Tecnologie: Python, CustomTkinter, Ghostscript

——

TAPPO è un'applicazione desktop open source che permette di comprimere file PDF riducendone le dimensioni mantenendo una qualità accettabile.
Il software utilizza Ghostscript come motore di compressione e offre diversi livelli di qualità per soddisfare diverse esigenze di utilizzo.

──

• Supporto per diversi livelli di compressione
• Elaborazione locale (nessun caricamento online)
• Multipiattaforma (Windows, Linux, macOS)
• Codice sorgente completamente disponibile

──

Ringraziamenti:

• Ghostscript Development Team
• Python Software Foundation
• CustomTkinter Community
• E.T. (https://github.com/et994)"""

        text_widget = ctk.CTkTextbox(self.credits_screen_frame, **COMPONENT_STYLES['textbox'])
        text_widget.pack(pady=(0, 15), expand=True, fill="both")
        text_widget.insert("0.0", credits_content)
        text_widget.configure(state="disabled")

        button_frame = ctk.CTkFrame(self.credits_screen_frame, fg_color="transparent")
        button_frame.pack()

        ctk.CTkButton(button_frame, text='Pagina GitHub', command=self.open_github,
                      **COMPONENT_STYLES['button_primary']).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text='Indietro', command=lambda: self.show_frame(self.main_content_frame),
                      **COMPONENT_STYLES['button_secondary']).pack(side="left", padx=10)

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

    def validate_inputs(self):
        gs = self.gs_path.get().strip()
        input_pdf = self.input_path.get().strip()
        output_pdf = self.output_path.get().strip()

        if not gs or gs == "Ghostscript non trovato -> Leggi la GUIDA qui sotto!":
            raise ValueError("Seleziona il percorso di Ghostscript.")
        if not os.path.exists(gs):
            raise ValueError("Ghostscript non trovato nel percorso specificato.")

        if not input_pdf:
            raise ValueError("Seleziona un file PDF da comprimere.")
        if not os.path.exists(input_pdf):
            raise ValueError("Il file PDF di input non esiste.")
        if not input_pdf.lower().endswith('.pdf'):
            raise ValueError("Il file di input deve essere un PDF.")

        try:
            input_size = os.path.getsize(input_pdf)
            if input_size == 0:
                raise ValueError("Il file PDF di input è vuoto.")
        except OSError as e:
            raise ValueError(f"Impossibile leggere il file di input: {e}")

        if not output_pdf:
            raise ValueError("Specifica il percorso del file di output.")

        output_dir = os.path.dirname(output_pdf)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError as e:
                raise ValueError(f"Impossibile creare la directory di output: {e}")

        try:
            test_dir = output_dir if output_dir else '.'
            test_file = os.path.join(test_dir, 'test_write_tappo.tmp')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
        except (OSError, IOError):
            raise ValueError("Permessi insufficienti per scrivere nella directory di output.")

        try:
            if os.path.abspath(input_pdf) == os.path.abspath(output_pdf):
                raise ValueError("Il file di output non può essere uguale a quello di input.")
        except OSError:
            pass

        return gs, input_pdf, output_pdf

    def build_compression_command(self, gs_path, input_pdf, output_pdf, quality):
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
        if not os.path.exists(output_pdf):
            raise RuntimeError("Il file compresso non è stato creato.")

        compressed_size = os.path.getsize(output_pdf)
        if compressed_size == 0:
            if os.path.exists(output_pdf):
                os.remove(output_pdf)
            raise RuntimeError("Il file compresso è vuoto. Possibile errore durante la compressione.")

        return compressed_size

    def show_compression_result(self, input_pdf, output_pdf, original_size, compressed_size):
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

    def compress_pdf_worker(self, gs_path, input_pdf, output_pdf, quality, original_size, loading_dialog):
        try:
            command = self.build_compression_command(gs_path, input_pdf, output_pdf, quality)
            
            result = subprocess.run(
                command, check=True, capture_output=True, 
                text=True, timeout=300
            )
            
            compressed_size = self.validate_compression_result(output_pdf)
            
            self.after(0, lambda: self.compression_completed(
                loading_dialog, input_pdf, output_pdf, original_size, compressed_size
            ))
            
        except Exception as e:
            self.after(0, lambda: self.compression_error(loading_dialog, e))
    
    def compression_completed(self, loading_dialog, input_pdf, output_pdf, original_size, compressed_size):
        loading_dialog.close()
        self.show_compression_result(input_pdf, output_pdf, original_size, compressed_size)
    
    def compression_error(self, loading_dialog, error):
        loading_dialog.close()
        
        if isinstance(error, subprocess.TimeoutExpired):
            messagebox.showerror("Errore", 
                "Timeout: la compressione sta richiedendo troppo tempo.\n"
                "Prova con un file più piccolo o un livello di compressione diverso.")
        elif isinstance(error, subprocess.CalledProcessError):
            error_msg = f"Errore nella compressione del PDF.\nCodice di errore: {error.returncode}"
            if error.stderr:
                error_msg += f"\nDettagli: {error.stderr.strip()}"
            messagebox.showerror("Errore", error_msg)
        elif isinstance(error, (RuntimeError, ValueError)):
            messagebox.showerror("Errore", str(error))
        elif isinstance(error, PermissionError):
            messagebox.showerror("Errore", "Permessi insufficienti per salvare il file.")
        elif isinstance(error, FileNotFoundError):
            messagebox.showerror("Errore", f"File non trovato: {error}")
        elif isinstance(error, OSError):
            messagebox.showerror("Errore", f"Errore del sistema operativo: {error}")
        else:
            messagebox.showerror("Errore", f"Errore imprevisto: {error}")

    def compress_pdf(self):
        try:
            gs_path, input_pdf, output_pdf = self.validate_inputs()
            quality = COMPRESSION_LEVELS.get(self.compression.get(), "/printer")
            original_size = os.path.getsize(input_pdf)
            
            loading_dialog = LoadingDialog(self)
            
            thread = threading.Thread(
                target=self.compress_pdf_worker,
                args=(gs_path, input_pdf, output_pdf, quality, original_size, loading_dialog),
                daemon=True
            )
            thread.start()
            
        except ValueError as e:
            messagebox.showerror("Errore", str(e))

if __name__ == "__main__":
    app = TappoApp()
    app.mainloop()