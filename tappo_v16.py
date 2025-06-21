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
    "link_01": "#0076d6",
    "link_02": "#44d62c",
}

APP_STYLE = {
    "corner_radius": 5,
    "border_width": 1
}

COMPRESSION_LEVELS = {
    "Bassa qualit\u00e0 (/screen) - File leggerissimo": "/screen",
    "Media qualit\u00e0 (/ebook) - File leggero": "/ebook",
    "Alta qualit\u00e0 (/printer) - File di medie dimensioni": "/printer",
    "Altissima qualit\u00e0 (/prepress) - File pi\u00f9 pesante": "/prepress"
}

def center_window_on_screen(window, width, height):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

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

        self.gs_path = ctk.StringVar(value=find_ghostscript() or "")
        self.input_path = ctk.StringVar()
        self.output_path = ctk.StringVar()
        self.compression = ctk.StringVar(value="Alta qualit\u00e0 (/printer) - File di medie dimensioni")

        self.setup_main_frame()
        self.build_ui()

    def setup_main_frame(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
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
                "fg_color": APP_COLORS["dark"], "text_color": APP_COLORS["text_light"],
                "border_color": APP_COLORS["border"], "corner_radius": 5, "border_width": 1,
            },
            'button': {
                "fg_color": APP_COLORS["dark"], "hover_color": APP_COLORS["hover"],
                "text_color": APP_COLORS["link_01"], "corner_radius": 5,
                "font": ("Segoe UI", 13, "bold"), "border_width": 1, 
                "border_color": APP_COLORS["link_01"],
            }
        }

    def add_input_row(self, row, label_text, variable, browse_command=None):
        styles = self.get_ui_styles()
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
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        styles = self.get_ui_styles()
        self.add_input_row(0, "Ghostscript", self.gs_path, self.browse_gs)
        self.add_input_row(1, "PDF originale", self.input_path, self.browse_input)
        self.add_input_row(2, "File compresso", self.output_path, self.browse_output)

        ctk.CTkLabel(self.main_frame, text="Livello di compressione", **styles['label']).grid(
            row=3, column=0, sticky="e", padx=(0, 5), pady=(10, 10)
        )
        ctk.CTkOptionMenu(
            self.main_frame, variable=self.compression, values=list(COMPRESSION_LEVELS.keys()), 
            width=350, font=("Segoe UI", 13), fg_color=APP_COLORS["dark"], 
            button_color=APP_COLORS["link_01"], button_hover_color=APP_COLORS["border"], 
            text_color=APP_COLORS["text_light"], dropdown_fg_color=APP_COLORS["dark"], 
            dropdown_text_color=APP_COLORS["text_light"], dropdown_hover_color=APP_COLORS["link_01"], 
            corner_radius=APP_STYLE["corner_radius"]
        ).grid(row=3, column=1, sticky="", padx=5, pady=(10, 10))

        compress_button = ctk.CTkButton(
            self.main_frame, text="Comprimi PDF", command=self.compress_pdf,
            fg_color=APP_COLORS["dark"], hover_color=APP_COLORS["hover"],
            text_color=APP_COLORS["link_02"], font=("Segoe UI", 13, "bold"),
            corner_radius=APP_STYLE["corner_radius"], height=40, width=200,
            border_width=APP_STYLE["border_width"], border_color=APP_COLORS["link_02"]
        )
        compress_button.grid(row=5, column=0, columnspan=3, pady=(25, 0))

    def browse_gs(self):
        filetypes = [("Eseguibili", "*.exe"), ("Tutti i files", "*.*")] if platform.system() == "Windows" else [("Tutti i files", "*.*")]
        file = filedialog.askopenfilename(title="Seleziona Ghostscript", filetypes=filetypes)
        if file:
            self.gs_path.set(file)

    def browse_input(self):
        file = filedialog.askopenfilename(title="Seleziona PDF da comprimere", filetypes=[("PDF files", "*.pdf"), ("Tutti i files", "*.*")])
        if file:
            self.input_path.set(file)
            base, _ = os.path.splitext(file)
            self.output_path.set(base + " - compresso.pdf")

    def browse_output(self):
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
