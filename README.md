
# TAPPO

### Tool per Alleggerire PDF Pesanti Offline | Trim And Pack PDFs Offline

**[Italiano](#italiano)** | **[English](#english)**

---

## Italiano

TAPPO è un semplice compressore di file PDF scritto in Python con un'interfaccia grafica.

![Screenshot](screenshots/tappo_1.2.0_screenshot_windows.png)

### Requisiti

Questa applicazione richiede l'installazione di **Ghostscript** sul sistema operativo dell'utente.  
Ghostscript è un interprete per i formati PostScript (PS) e PDF.

#### Installazione di Ghostscript

##### Windows

1. Vai al sito ufficiale di Ghostscript: [https://ghostscript.com/download/gsdnld.html](https://ghostscript.com/download/gsdnld.html)
2. Scarica il pacchetto Windows a 64 bit (es: `gs###w64.exe`).
3. Esegui il programma di installazione e segui le istruzioni.

Per verificare che l'installazione sia avvenuta correttamente, apri il prompt dei comandi e digita:
```bash
gs --version
```
Dovresti vedere un numero di versione come risposta (es. `10.02.1`).  
In caso di errore, assicurati che l'opzione per aggiungere Ghostscript al PATH di sistema sia selezionata.

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

Per verificare:
```bash
gs --version
```

Se Ghostscript non è disponibile nei repository, è possibile scaricare il pacchetto Snap: [https://ghostscript.com/releases/gsdnld.html](https://ghostscript.com/releases/gsdnld.html)

#### Requisiti Python

```bash
pip install -r requirements.txt
```

### Problemi noti

- Corretta assegnazione dell'[icona .png nell'AppImage](https://github.com/Ghizza/TAPPO/issues/2)

### Contributi

Contributi benvenuti! Vedi [CONTRIBUTING.md](./CONTRIBUTING.md) per le linee guida.

### Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](./LICENSE) per i dettagli.

---

## English

TAPPO is a simple PDF file compressor written in Python with a graphical user interface.

![Screenshot](screenshots/tappo_1.2.0_screenshot_windows.png)

## Requirements

This application requires **Ghostscript** to be installed on the user's operating system.  
Ghostscript is an interpreter for PostScript (PS) and PDF formats.

### Installing Ghostscript

#### Windows

1. Go to the official Ghostscript website: [https://ghostscript.com/download/gsdnld.html](https://ghostscript.com/download/gsdnld.html)
2. Download the 64-bit Windows package (e.g., `gs###w64.exe`).
3. Run the installer and follow the instructions.

To verify the installation was successful, open the command prompt and type:
```bash
gs --version
```
You should see a version number as a response (e.g., `10.02.1`).  
If you get an error, make sure the option to add Ghostscript to the system PATH is selected.

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

To verify:
```bash
gs --version
```

If Ghostscript is not available in the repositories, you can download the Snap package: [https://ghostscript.com/releases/gsdnld.html](https://ghostscript.com/releases/gsdnld.html)

### Python Requirements

```bash
pip install -r requirements.txt
```

## Known Issues

- Correct assignment of the [].png icon](https://github.com/Ghizza/TAPPO/issues/2) in the AppImage

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

This project is released under the MIT License. See the [LICENSE](./LICENSE) file for details.
