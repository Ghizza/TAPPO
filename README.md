
# TAPPO

### Tool per Alleggerire PDF Pesanti Offline | Trim And Pack PDFs Offline

**[Italiano](#italiano) | [English](#english)**

---

## Italiano

TAPPO è un semplice compressore di file PDF scritto in Python con un'interfaccia grafica.

### Requisiti

Questa applicazione richiede l'installazione di **Ghostscript** sul sistema operativo dell'utente.  
Ghostscript è un interprete per i formati PostScript (PS) e PDF.

### Installazione di Ghostscript

#### Windows

1. Vai al sito ufficiale di Ghostscript: [https://ghostscript.com/download/gsdnld.html](https://ghostscript.com/download/gsdnld.html)
2. Scarica il pacchetto Windows a 64 bit (es: `gs###w64.exe`).
3. Esegui il programma di installazione e segui le istruzioni.

Per verificare che l'installazione sia avvenuta correttamente, apri il prompt dei comandi e digita:

```bash
gs --version
```

Dovresti vedere un numero di versione come risposta (es. `10.02.1`).  
In caso di errore, assicurati che l'opzione per aggiungere Ghostscript al PATH di sistema sia selezionata.

#### Linux

##### Debian/Ubuntu (e derivate)

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

Per verificare:

```bash
gs --version
```

Se Ghostscript non è disponibile nei repository, è possibile scaricare il pacchetto Snap: [https://ghostscript.com/releases/gsdnld.html](https://ghostscript.com/releases/gsdnld.html)

### Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](./LICENSE) per i dettagli.

---

**Nota:** TAPPO è in fase di sviluppo e diventerà un'applicazione per Windows (.exe) e per Linux (.appimage).

---

## English

TAPPO is a simple PDF file compressor written in Python with a graphical interface.

### Requirements

This application requires **Ghostscript** to be installed on the user's operating system.  
Ghostscript is an interpreter for PostScript (PS) and PDF formats.

### Ghostscript Installation

#### Windows

1. Go to the official Ghostscript website: [https://ghostscript.com/download/gsdnld.html](https://ghostscript.com/download/gsdnld.html)
2. Download the 64-bit Windows package (e.g., `gs###w64.exe`).
3. Run the installer and follow the instructions.

To verify that the installation was successful, open the command prompt and type:

```bash
gs --version
```

You should see a version number as response (e.g., `10.02.1`).  
In case of error, make sure the option to add Ghostscript to the system PATH is selected.

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

### License

This project is released under the MIT license. See the [LICENSE](./LICENSE) file for details.

---

**Note:** TAPPO is under development and will become a Windows application (.exe) and Linux application (.appimage).