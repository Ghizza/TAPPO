# 🗜️ Tappo (v1.1.0)
**Tool per Alleggerire Pdf e Png Offline**

**Tappo** è un'applicazione desktop scritta in Python con interfaccia `tkinter`[cite: 7], progettata per comprimere immagini **PNG** e documenti **PDF** in modo completamente **offline**[cite: 7], sfruttando la massima efficienza di strumenti CLI consolidati nel mondo open source.

L'interfaccia grafica adotta la palette di colori **Flexoki**[cite: 7], offrendo un design pulito, leggibile e moderno, con supporto nativo agli schermi HiDPI[cite: 7].

---

## 🚀 Caratteristiche Principali

* **100% Offline e Privato**: Nessun file viene caricato su server esterni; l'elaborazione avviene interamente sul tuo computer.
* **Compressione PNG avanzata**:
  * **Lossless** tramite `oxipng` (con livelli di ottimizzazione da `-o1` a `-o6` e opzione `Zopfli` spinta per la massima compressione)[cite: 7].
  * **Lossy** tramite `pngquant` (con range di qualità personalizzabili e opzione di post-ottimizzazione con oxipng)[cite: 7].
  * Rimozione opzionale dei metadati superflui (*strip*)[cite: 7].
  * Anteprima visiva affiancata (Originale vs Compresso) con zoom dinamico o adattivo[cite: 7].
* **Compressione PDF flessibile**:
  * Sfrutta **Ghostscript** con vari preset di risoluzione e qualità `-dPDFSETTINGS` (`screen` a 72 dpi, `ebook` a 150 dpi, `printer`/`prepress` a 300 dpi)[cite: 7].
* **Gestione intelligente degli strumenti esterni**:
  * L'app cerca gli eseguibili necessari (`oxipng`, `pngquant`, `ghostscript`) nella cartella locale `./bin`, nel `PATH` di sistema o nei percorsi di installazione predefiniti[cite: 7].
  * **Auto-aggiornamento e Download**: Include una scheda dedicata ("Strumenti") per verificare la presenza di nuove versioni online e scaricare/installare automaticamente i binari mancanti[cite: 7].

---

## 🛠️ Strumenti Esterni Richiesti

Tappo funge da interfaccia grafica per tre eseguibili esterni che **non sono inclusi** nel repository e mantengono le rispettive licenze[cite: 7]:

1. **`oxipng`**: Per la compressione lossless dei PNG (GitHub releases)[cite: 7].
2. **`pngquant`**: Per la compressione lossy dei PNG (pngquant.org)[cite: 7].
3. **`Ghostscript`** (`gswin64c.exe` / `gs`): Per la compressione e rasterizzazione dei PDF (ghostscript.com)[cite: 7].

### Come installarli
* **Metodo automatico (Consigliato)**: Posiziona l'app, avviala, vai sulla scheda **Strumenti** e clicca su *"Scarica e installa in bin"* per automatizzare il recupero dei file supportati[cite: 7].
* **Metodo manuale**: Crea una cartella denominata `bin` nella stessa directory di `tappo.py` e inserisci gli eseguibili necessari[cite: 7]. Su Linux è possibile installarli anche tramite i gestori di pacchetti di sistema (`apt`, `dnf`, `pacman`)[cite: 7].

---

## 📦 Requisiti e Dipendenze

* **Python 3.x** (consigliato Python 3.8 o superiore).
* **Dipendenze Python obbligatorie**: *Nessuna* (utilizza esclusivamente moduli nativi della libreria standard di Python)[cite: 7].
* **Dipendenza Python opzionale**: 
  * `Pillow` (`pip install pillow`)[cite: 7]: vivamente consigliata per abilitare anteprime PNG ridimensionate con algoritmi di interpolazione di qualità superiore (LANCZOS). Senza Pillow, l'app utilizzerà le funzioni native di `tkinter`[cite: 7].

---

## 🏃‍♂️ Avvio dell'Applicazione

Clona o scarica la repository, assicurati di trovarti nella cartella del progetto e avvia lo script con il comando:

* **Linux / macOS**:
  ```bash
  python3 tappo.py