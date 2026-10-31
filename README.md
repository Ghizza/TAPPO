**[🇮🇹 Italiano](#italiano)** | **🇬🇧 [English](#english)**

## Italiano

**TAPPO — Tool per Alleggerire Pdf e Png Offline**

**TAPPO** è un'applicazione desktop scritta in Python con interfaccia `tkinter`, progettata per comprimere immagini **PNG** e documenti **PDF** in modo completamente **offline**, sfruttando la massima efficienza di strumenti CLI consolidati nel mondo open source.

### Caratteristiche Principali

- **100% Offline e Privato**: Nessun file viene caricato su server esterni; l'elaborazione avviene interamente sul tuo computer.
- **Compressione PNG avanzata**:
  - **Lossless** tramite `oxipng` (con livelli di ottimizzazione da `-o1` a `-o6` e opzione `Zopfli` spinta per la massima compressione).
  - **Lossy** tramite `pngquant` (con range di qualità personalizzabili e opzione di post-ottimizzazione con oxipng).
  - Rimozione opzionale dei metadati superflui (*strip*).
  - Anteprima visiva affiancata (Originale vs Compresso) con zoom dinamico o adattivo.
- **Compressione PDF flessibile**:
  - Sfrutta **Ghostscript** con vari preset di risoluzione e qualità `-dPDFSETTINGS` (`screen` a 72 dpi, `ebook` a 150 dpi, `printer`/`prepress` a 300 dpi).
- **Gestione intelligente degli strumenti esterni**:
  - L'app cerca gli eseguibili necessari (`oxipng`, `pngquant`, `ghostscript`) nella cartella locale `./bin`, nel `PATH` di sistema o nei percorsi di installazione predefiniti.
  - **Auto-aggiornamento e Download**: Include una scheda dedicata ("Strumenti") per verificare la presenza di nuove versioni online e scaricare/installare automaticamente i binari mancanti.

### Strumenti Esterni Richiesti

TAPPO funge da interfaccia grafica per tre eseguibili esterni che **non sono inclusi** nel repository e mantengono le rispettive licenze:

1. **`oxipng`**: Per la compressione lossless dei PNG ([rustutils.com/tools/oxipng](https://rustutils.com/tools/oxipng/)).
2. **`pngquant`**: Per la compressione lossy dei PNG ([pngquant.org](https://pngquant.org/)).
3. **`Ghostscript`**: Per la compressione e rasterizzazione dei PDF ([ghostscript.com](https://ghostscript.com/)).

### Come installarli

- **Metodo automatico (Consigliato)**: Posiziona l'app, avviala, vai sulla scheda **Strumenti** e clicca su *"Scarica e installa in bin"* per automatizzare il recupero dei file supportati.
- **Metodo manuale**: Crea una cartella denominata `bin` nella stessa directory di `tappo.py` e inserisci gli eseguibili necessari. Su Linux è possibile installarli anche tramite i gestori di pacchetti di sistema (`apt`, `dnf`, `pacman`).

### Requisiti e Dipendenze

- **Python 3.x** (consigliato Python 3.8 o superiore).
- **Dipendenze Python obbligatorie**: *Nessuna* (utilizza esclusivamente moduli nativi della libreria standard di Python).
- **Dipendenza Python opzionale**:
  - `Pillow` (`pip install pillow`): vivamente consigliata per abilitare anteprime PNG ridimensionate con algoritmi di interpolazione di qualità superiore (LANCZOS). Senza Pillow, l'app utilizzerà le funzioni native di `tkinter`.

### Avvio dell'Applicazione

Clona o scarica la repository, assicurati di trovarti nella cartella del progetto e avvia lo script con il comando:

- **Linux / macOS**:
  ```bash
  python3 tappo.py
  ```
- **Windows**:
  ```cmd
  python tappo.py
  ```

### Licenza

Questo progetto è distribuito sotto licenza MIT. Gli strumenti esterni utilizzati (`oxipng`, `pngquant`, `Ghostscript`) mantengono le proprie licenze e termini di utilizzo originali.

---

**[🇮🇹 Italiano](#italiano)** | **🇬🇧 [English](#english)**

## English

**TAPPO — Offline PDF and PNG Compression Tool**

**TAPPO** is a desktop application written in Python using `tkinter`, designed to compress **PNG** images and **PDF** documents completely **offline**, leveraging the performance of battle-tested open-source CLI tools.

### Key Features

- **100% Offline & Private**: No files are uploaded to external servers; all processing is executed locally on your machine.
- **Advanced PNG Compression**:
  - **Lossless** via `oxipng` (with optimization levels from `-o1` to `-o6` and an optional `Zopfli` pass for maximum compression).
  - **Lossy** via `pngquant` (customizable quality thresholds and optional post-optimization via oxipng).
  - Optional metadata stripping (*strip*).
  - Side-by-side visual preview (Original vs Compressed) with fit-to-box or 100% zoom controls.
- **Flexible PDF Compression**:
  - Powered by **Ghostscript** with multiple resolution presets via `-dPDFSETTINGS` (`screen` at 72 dpi, `ebook` at 150 dpi, `printer`/`prepress` at 300 dpi).
- **Smart External Tool Management**:
  - Automatically searches for required binaries (`oxipng`, `pngquant`, `ghostscript`) in `./bin`, system `PATH`, or standard install locations.
  - **Auto-update & Download**: Includes a dedicated "Tools" tab to check for updates online and automatically download/install missing binaries.

### External Tools Required

TAPPO serves as a GUI wrapper for three third-party executables that are **not bundled** in this repository and maintain their respective licenses:

1. **`oxipng`**: For lossless PNG compression ([rustutils.com/tools/oxipng](https://rustutils.com/tools/oxipng/)).
2. **`pngquant`**: For lossy PNG compression ([pngquant.org](https://pngquant.org/)).
3. **`Ghostscript`**: For PDF compression and rasterization ([ghostscript.com](https://ghostscript.com/)).

### Installation Options

- **Automatic (Recommended)**: Launch TAPPO, go to the **Tools** tab, and click *"Download and install to bin"* to fetch supported binaries automatically.
- **Manual**: Create a folder named `bin` in the same directory as `tappo.py` and copy the executables into it. On Linux, tools can also be installed using system package managers (`apt`, `dnf`, `pacman`).

### Requirements & Dependencies

- **Python 3.x** (Python 3.8+ recommended).
- **Required Python Libraries**: *None* (uses standard library modules only).
- **Optional Python Library**:
  - `Pillow` (`pip install pillow`): Recommended for high-quality preview resampling (LANCZOS). Without Pillow, previews fallback to native `tkinter` rendering.

### How to Run

Clone or download the repository, navigate to the project directory, and launch the application:

- **Linux / macOS**:
  ```bash
  python3 tappo.py
  ```
- **Windows**:
  ```cmd
  python tappo.py
  ```

### License

This project is licensed under the MIT License. External tools (`oxipng`, `pngquant`, `Ghostscript`) remain subject to their original respective licenses.