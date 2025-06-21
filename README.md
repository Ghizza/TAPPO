# TAPPO
### Tool per Alleggerire PDF Pesanti Offline 

TAPPO è un semplicissimo compressore di file PDF scritto in Python con un'interfaccia grafica.  

## 🛠️ Requisiti

Questa applicazione richiede l'installazione di **Ghostscript** sul sistema operativo dell'utente.  
Ghostscript è un interprete per i formati PostScript (PS) e PDF.

## Installazione di Ghostscript

### Windows

1. Vai al sito ufficiale di Ghostscript: [https://ghostscript.com/download/gsdnld.html](https://ghostscript.com/download/gsdnld.html)
2. Scarica il pacchetto Windows a 64 bit (es: `gs###w64.exe`).
3. Esegui il programma di installazione e segui le istruzioni.
4. Durante l'installazione, **assicurati che l'opzione per aggiungere Ghostscript al PATH di sistema sia selezionata**.

Per verificare che l'installazione sia avvenuta correttamente, apri il prompt dei comandi e digita:

```bash
gs --version
```

Dovresti vedere un numero di versione come risposta (es. `10.02.1`).

### Linux

#### Debian/Ubuntu (e derivate)

```bash
sudo apt update
sudo apt install ghostscript
```

#### Fedora

```bash
sudo dnf install ghostscript
```

#### Arch Linux / Manjaro

```bash
sudo pacman -S ghostscript
```

#### openSUSE

```bash
sudo zypper install ghostscript
```

Per verificare:

```bash
gs --version
```

Se Ghostscript non è disponibile nei repository o vuoi una versione più recente, puoi anche installarlo dai sorgenti ufficiali: [https://ghostscript.com/releases/](https://ghostscript.com/releases/)

---

TAPPO è in fase di sviluppo e diventerà un'applicazione per Windows (.exe) e per Linux (.appimage).
