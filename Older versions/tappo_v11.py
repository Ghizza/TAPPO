#!/usr/bin/env python3

import customtkinter as ctk
import os
import platform
import shutil
import subprocess
import webbrowser
from tkinter import filedialog, messagebox

# === STILE GLOBALE: COLORI ===
APP_COLORS = {
    "background": "#002B36",
    "dark": "#002028", # +25% black
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


COMPRESSION_LEVELS = {
    "Bassa qualità (/screen) - File leggerissimo": "/screen",
    "Media qualità (/ebook) - File leggero": "/ebook",
    "Alta qualità (/printer) - File di medie dimensioni": "/printer",
    "Altissima qualità (/prepress) - File più pesante": "/prepress"
}

def find_ghostscript():
    """Trova automaticamente l'eseguibile di Ghostscript nel sistema"""
    system = platform.system()
    if system == "Windows":
        candidates = ["gswin64c.exe", "gswin32c.exe", "gs.exe"]
    else:
        candidates = ["gs"]
    
    # Cerca nei PATH del sistema
    for name in candidates:
        path = shutil.which(name)
        if path:
            return path
    
    # Cerca in percorsi comuni per sistemi Unix-like
    if system != "Windows":
        for path in ["/usr/bin/gs", "/usr/local/bin/gs", "/opt/local/bin/gs"]:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path
    
    return None  # Ghostscript non trovato

def center_window_on_screen(window, width, height):
    """Centra una finestra sullo schermo"""
    # Ottieni le dimensioni dello schermo
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Calcola la posizione per centrare la finestra
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Imposta la geometria
    window.geometry(f"{width}x{height}+{x}+{y}")

class InfoWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Info - Come usare TAPPO")
        self.configure(fg_color=APP_COLORS["background"])
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Centra la finestra sullo schermo
        center_window_on_screen(self, 600, 480)
        
        self.create_widgets()

    def create_widgets(self):
        title_label = ctk.CTkLabel(
            self,
            text="Come usare TAPPO",
            font=(APP_STYLE["font_family"], 20, "bold"),
            text_color=APP_COLORS["border"]
        )
        title_label.pack(pady=(20, 10))

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
            self,
            width=550,
            height=250,
            font=(APP_STYLE["font_family"], 12),
            fg_color=APP_COLORS["dark"],
            text_color=APP_COLORS["text_medium"],
            corner_radius=APP_STYLE["corner_radius"]
        )
        text_widget.pack(pady=10, padx=20)
        text_widget.insert("0.0", info_text)
        text_widget.configure(state="disabled")

        link_button = ctk.CTkButton(
            self,
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
        link_button.pack(pady=(5, 10))

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10)

        close_button = ctk.CTkButton(
            button_frame,
            text="Chiudi",
            command=self.destroy,
            fg_color=APP_COLORS["dark"],
            hover_color=APP_COLORS["hover"],
            text_color=APP_COLORS["text"],
            font=(APP_STYLE["font_family"], 13, "bold"),
            corner_radius=APP_STYLE["corner_radius"],
            border_width=APP_STYLE["border_width"],
            border_color=APP_COLORS["border"],
            width=150,
        )
        close_button.pack()

    def open_ghostscript_download(self):
        webbrowser.open("https://www.ghostscript.com/download/gsdnld.html")

class CreditsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Credits - Informazioni su TAPPO")
        self.configure(fg_color=APP_COLORS["background"])
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Centra la finestra sullo schermo
        center_window_on_screen(self, 500, 400)
        
        self.create_widgets()

    def create_widgets(self):
        title_label = ctk.CTkLabel(
            self,
            text="TAPPO",
            font=(APP_STYLE["font_family"], 20, "bold"),
            text_color=APP_COLORS["border"]
        )
        title_label.pack(pady=(20, 5))

        subtitle_label = ctk.CTkLabel(
            self,
            text="Tool per Alleggerire PDF Pesanti Offline",
            font=(APP_STYLE["font_family"], 14),
            text_color=APP_COLORS["text"]
        )
        subtitle_label.pack(pady=(0, 10))

        info_frame = ctk.CTkFrame(self, fg_color=APP_COLORS["dark"], corner_radius=10)
        info_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(info_frame, text="Versione: 1.0", font=(APP_STYLE["font_family"], 13), text_color=APP_COLORS["text"]).pack(pady=(2))
        ctk.CTkLabel(info_frame, text="Creato da: Stefano", font=(APP_STYLE["font_family"], 13), text_color=APP_COLORS["text"]).pack(pady=(2))
        ctk.CTkLabel(info_frame, text="Licenza: MIT License", font=(APP_STYLE["font_family"], 13), text_color=APP_COLORS["text"]).pack(pady=2)
        ctk.CTkLabel(info_frame, text="Tecnologie: Python, CustomTkinter, Ghostscript", font=(APP_STYLE["font_family"], 13), text_color=APP_COLORS["text"]).pack(pady=(2, 10))

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20)

        ctk.CTkButton(
            button_frame,
            text="Pagina GitHub",
            command=self.open_github,
            fg_color=APP_COLORS["dark"],
            hover_color=APP_COLORS["hover"],
            text_color=APP_COLORS["link_01"],
            font=(APP_STYLE["font_family"], 13, "bold"),
            corner_radius=APP_STYLE["corner_radius"],
            border_width=1,
            border_color=APP_COLORS["link_01"]
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="Chiudi",
            command=self.destroy,
            fg_color=APP_COLORS["dark"],
            hover_color=APP_COLORS["hover"],
            text_color=APP_COLORS["text"],
            font=(APP_STYLE["font_family"], 12, "bold"),
            corner_radius=APP_STYLE["corner_radius"],
            border_width=APP_STYLE["border_width"],
            border_color=APP_COLORS["border"]
        ).pack(side="left", padx=10)

    def open_github(self):
        # Cambia questo URL con il tuo repository effettivo
        webbrowser.open("https://github.com/Ghizza/TAPPO")

class TappoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TAPPO - Tool per Alleggerire PDF Pesanti Offline")
        self.configure(fg_color=APP_COLORS["background"], padx=20, pady=20)
        
        # Impedisce il ridimensionamento della finestra
        self.resizable(False, False)
        
        # Centra la finestra principale sullo schermo
        center_window_on_screen(self, 700, 280)
        
        # Imposta dimensioni minime e massime uguali per evitare il ridimensionamento
        self.minsize(700, 280)
        self.maxsize(700, 280)

        self.gs_path = ctk.StringVar(value=find_ghostscript() or "")
        self.input_path = ctk.StringVar()
        self.output_path = ctk.StringVar()
        self.compression = ctk.StringVar(value="Alta qualità (/printer) - File di medie dimensioni")

        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)

        label_style = {"font": ("Public Sans", 13, "bold"), "text_color": APP_COLORS["text"]}
        entry_style = {
            "width": 400, "font": ("Public Sans", 13),
            "fg_color": APP_COLORS["dark"], "text_color": APP_COLORS["text_light"],
            "border_color": APP_COLORS["border"], "corner_radius": 5, "border_width": 1,
        }
        button_style = {
            "fg_color": APP_COLORS["dark"], "hover_color": APP_COLORS["hover"],
            "text_color": APP_COLORS["link_01"], "corner_radius": 5,
            "font": ("Public Sans", 13, "bold"), "border_width": 1, "border_color": APP_COLORS["link_01"],
        }

        def add_row(row, label_text, variable, browse_command=None):
            ctk.CTkLabel(self, text=label_text, **label_style).grid(row=row, column=0, sticky="e", padx=10, pady=5)
            ctk.CTkEntry(self, textvariable=variable, **entry_style).grid(row=row, column=1, sticky="ew", padx=5)
            if browse_command:
                ctk.CTkButton(self, text="Sfoglia", command=browse_command, **button_style).grid(row=row, column=2, padx=5)

        add_row(0, "Ghostscript", self.gs_path, self.browse_gs)
        add_row(1, "PDF originale", self.input_path, self.browse_input)
        add_row(2, "File compresso", self.output_path, self.browse_output)

        ctk.CTkLabel(self, text="Livello di compressione", **label_style).grid(row=3, column=0, sticky="e", padx=10, pady=(20, 5))

        ctk.CTkOptionMenu(
            self, variable=self.compression, values=list(COMPRESSION_LEVELS.keys()), width=400,
            font=(APP_STYLE["font_family"], 13), fg_color=APP_COLORS["dark"], button_color=APP_COLORS["link_01"],
            button_hover_color=APP_COLORS["border"], text_color=APP_COLORS["text_light"],
            dropdown_fg_color=APP_COLORS["dark"], dropdown_text_color=APP_COLORS["text_light"],
            dropdown_hover_color=APP_COLORS["link_01"], corner_radius=APP_STYLE["corner_radius"]
        ).grid(row=3, column=1, sticky="w", padx=5, pady=(20, 6))

        self.create_side_menu()

        ctk.CTkButton(
            self, text="Comprimi PDF", command=self.compress_pdf,
            fg_color=APP_COLORS["dark"], hover_color=APP_COLORS["hover"],
            text_color=APP_COLORS["link_02"], font=(APP_STYLE["font_family"], 13, "bold"),
            corner_radius=APP_STYLE["corner_radius"], height=40, border_width=APP_STYLE["border_width"], border_color=APP_COLORS["link_02"]
        ).grid(row=4, column=0, columnspan=3, pady=15)

    def create_side_menu(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=3, column=2, padx=5, pady=(20, 5))

        ctk.CTkButton(
            frame, text="GUIDA", command=self.show_info,
            fg_color="transparent", hover_color=APP_COLORS["hover"],
            text_color=APP_COLORS["link_01"], font=(APP_STYLE["font_family"], 11, "bold"), width=40, height=24
        ).pack(side="left", padx=(0, 5))

        ctk.CTkButton(
            frame, text="CREDITS", command=self.show_credits,
            fg_color="transparent", hover_color=APP_COLORS["hover"],
            text_color=APP_COLORS["link_01"], font=(APP_STYLE["font_family"], 11, "bold"), width=50, height=24
        ).pack(side="left")

    def show_info(self):
        InfoWindow(self)

    def show_credits(self):
        CreditsWindow(self)

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
            # Suggerisci automaticamente il nome del file di output
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

        # Validazione input
        if not gs:
            messagebox.showerror("Errore", "Seleziona il percorso di Ghostscript.")
            return
        
        if not input_pdf:
            messagebox.showerror("Errore", "Seleziona un file PDF da comprimere.")
            return
            
        if not output_pdf:
            messagebox.showerror("Errore", "Specifica il percorso del file di output.")
            return

        # Verifica esistenza e validità dei file
        if not os.path.exists(gs):
            messagebox.showerror("Errore", "Ghostscript non trovato nel percorso specificato.")
            return
            
        if not os.path.exists(input_pdf):
            messagebox.showerror("Errore", "Il file PDF di input non esiste.")
            return
            
        if not input_pdf.lower().endswith('.pdf'):
            messagebox.showerror("Errore", "Il file di input deve essere un PDF.")
            return

        # Verifica che il file di input non sia vuoto
        try:
            input_size = os.path.getsize(input_pdf)
            if input_size == 0:
                messagebox.showerror("Errore", "Il file PDF di input è vuoto.")
                return
        except OSError as e:
            messagebox.showerror("Errore", f"Impossibile leggere il file di input: {e}")
            return

        # Verifica/crea directory di output
        output_dir = os.path.dirname(output_pdf)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError as e:
                messagebox.showerror("Errore", f"Impossibile creare la directory di output: {e}")
                return

        # Verifica permessi di scrittura
        try:
            # Test di scrittura nella directory di output
            test_dir = output_dir if output_dir else '.'
            test_file = os.path.join(test_dir, 'test_write_tappo.tmp')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
        except (OSError, IOError):
            messagebox.showerror("Errore", "Permessi insufficienti per scrivere nella directory di output.")
            return

        # Evita di sovrascrivere il file di input
        try:
            if os.path.abspath(input_pdf) == os.path.abspath(output_pdf):
                messagebox.showerror("Errore", "Il file di output non può essere uguale a quello di input.")
                return
        except OSError:
            pass  # Continua se non è possibile risolvere i percorsi assoluti

        # Comando Ghostscript
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
            # Esegui compressione con timeout di 5 minuti
            result = subprocess.run(
                command, 
                check=True, 
                capture_output=True, 
                text=True, 
                timeout=300  # 5 minuti
            )
            
            # Verifica che il file di output sia stato creato
            if not os.path.exists(output_pdf):
                messagebox.showerror("Errore", "Il file compresso non è stato creato.")
                return
                
            # Verifica che il file di output non sia vuoto
            compressed_size = os.path.getsize(output_pdf)
            if compressed_size == 0:
                messagebox.showerror("Errore", "Il file compresso è vuoto. Possibile errore durante la compressione.")
                if os.path.exists(output_pdf):
                    os.remove(output_pdf)  # Rimuovi il file vuoto
                return

            # Calcola statistiche
            original_size = os.path.getsize(input_pdf)
            saved_bytes = original_size - compressed_size
            saved_percent = (saved_bytes / original_size) * 100 if original_size > 0 else 0

            # Formatta le dimensioni in modo leggibile
            def format_size(bytes_size):
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if bytes_size < 1024.0:
                        return f"{bytes_size:.2f} {unit}"
                    bytes_size /= 1024.0
                return f"{bytes_size:.2f} TB"

            # Messaggio di successo
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
    
    app = TappoApp()
    app.mainloop()