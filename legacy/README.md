# TAPPO 1.2.0 – Legacy

### Tool per Alleggerire PDF Pesanti Offline | Trim And Pack PDFs Offline

**[Italiano](#italiano)** | **[English](#english)**

---

## Italiano

Questa cartella contiene il codice sorgente della versione originale **TAPPO 1.2.0**, un semplice compressore di file PDF scritto in Python con interfaccia grafica.

Questa versione è stata successivamente sostituita da una riscrittura completa dell'applicazione, che mantiene il nome TAPPO e introduce anche la compressione dei file PNG.

La versione originale viene conservata per motivi di compatibilità e per consentire agli utenti di continuare a utilizzarla.

![Screenshot](../tappo_1.2.0_screenshot_windows.png)

### Requisiti

Questa applicazione richiede l'installazione di **Ghostscript** sul sistema operativo dell'utente.  
Ghostscript è un interprete per i formati PostScript (PS) e PDF.

#### Installazione di Ghostscript

##### Windows

1. Vai al sito ufficiale di Ghostscript: [https://ghostscript.com/download/gsdnld.html](https://ghostscript.com/download/gsdnld.html)
2. Scarica il pacchetto Windows a 64 bit (es: `gs###w64.exe`).
3. Esegui il programma di installazione e segui le istruzioni.

##### Linux

###### Debian/Ubuntu (e derivate)

```bash
sudo apt update
sudo apt install ghostscript
```

###### Fedora

```bash
sudo dnf install ghostscript
```

###### Arch Linux / Manjaro

```bash
sudo pacman -S ghostscript
```

###### openSUSE

```bash
sudo zypper install ghostscript
```

Se Ghostscript non è disponibile nei repository, è possibile consultare la pagina ufficiale: [Ghostscript Downloads](https://ghostscript.com/releases/gsdnld.html).

#### Requisiti Python

Dalla cartella `legacy`:

```bash
pip install -r requirements.txt
```

### Problemi noti

- Corretta assegnazione dell'[icona .png nell'AppImage](https://github.com/Ghizza/TAPPO/issues/2).

### Contributi

La versione legacy non è più quella principale del progetto. Per informazioni sui contributi, consulta il file [CONTRIBUTING.md](../CONTRIBUTING.md) nella directory principale.

### Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](../LICENSE) nella directory principale per i dettagli.

---

## English

This folder contains the source code of the original **TAPPO 1.2.0**, a simple PDF file compressor written in Python with a graphical user interface.

This version was subsequently replaced by a complete rewrite of the application, which retains the TAPPO name and also introduces PNG file compression.

The original version is preserved for compatibility purposes and to allow existing users to continue using it.

![Screenshot](../tappo_1.2.0_screenshot_windows.png)

### Requirements

This application requires **Ghostscript** to be installed on the user's operating system.  
Ghostscript is an interpreter for PostScript (PS) and PDF formats.

### Installing Ghostscript

#### Windows

1. Go to the official Ghostscript website: [https://ghostscript.com/download/gsdnld.html](https://ghostscript.com/download/gsdnld.html).
2. Download the 64-bit Windows package (e.g., `gs###w64.exe`).
3. Run the installer and follow the instructions.

#### Linux

##### Debian/Ubuntu (and derivatives)

```bash
sudo apt update
sudo apt install ghostscript
```

##### Fedora

```bash
sudo dnf install ghostscript
```

##### Arch Linux / Manjaro

```bash
sudo pacman -S ghostscript
```

##### openSUSE

```bash
sudo zypper install ghostscript
```

If Ghostscript is not available in the repositories, refer to the official page: [Ghostscript Downloads](https://ghostscript.com/releases/gsdnld.html).

### Python Requirements

From the `legacy` directory:

```bash
pip install -r requirements.txt
```

### Known Issues

- Correct assignment of the [.png icon in the AppImage](https://github.com/Ghizza/TAPPO/issues/2).

### Contributing

This legacy version is no longer the main version of the project. For contribution guidelines, see the [CONTRIBUTING.md](../CONTRIBUTING.md) file in the repository root.

### License

This project is released under the MIT License. See the [LICENSE](../LICENSE) file in the repository root for details.
