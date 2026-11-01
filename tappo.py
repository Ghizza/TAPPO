#!/usr/bin/env python3

import math
import os
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import webbrowser
import json
import glob
import platform
import zipfile
import tarfile
import urllib.request
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkfont

try:
    from PIL import Image, ImageTk
    _RES = getattr(Image, "Resampling", Image)
    HAVE_PIL = True
except Exception:
    HAVE_PIL = False

APP_NAME = "TAPPO"
APP_FULL = "Tool per Alleggerire Pdf e Png Offline"

IS_WIN = os.name == "nt"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIN_DIR = os.path.join(BASE_DIR, "bin")


# --- Palette Flexoki (https://stephango.com/flexoki): i soli colori usati dall'app
FLEXOKI = {
    "black":      "#100F0F",
    "base-950":   "#1C1B1A",
    "base-900":   "#282726",
    "base-850":   "#343331",
    "base-800":   "#403E3C",
    "base-700":   "#575653",
    "base-600":   "#6F6E69",
    "base-500":   "#878580",
    "base-300":   "#B7B5AC",
    "base-200":   "#CECDC3",
    "base-150":   "#DAD8CE",
    "base-100":   "#E6E4D9",
    "base-50":    "#F2F0E5",
    "paper":      "#FFFCF0",
    "red-600":    "#AF3029",
    "orange-600": "#BC5215",
    "yellow-600": "#AD8301",
    "green-600":  "#66800B",
    "cyan-600":   "#24837B",
    "blue-600":   "#205EA6",
    "purple-600": "#5E409D",
    "magenta-600": "#A02F6F",
    "red-400":    "#D14D41",
    "orange-400": "#DA702C",
    "yellow-400": "#D0A215",
    "green-400":  "#879A39",
    "cyan-400":   "#3AA99F",
    "blue-400":   "#4385BE",
    "purple-400": "#8B7EC8",
    "magenta-400": "#CE5D97",
}
F = FLEXOKI

# --- Ruoli dei colori nell'app: cambia il colore Flexoki assegnato a ciascun ruolo
COLORI = {
    # Sfondi
    "sfondo_app":            F["base-50"],    # finestra e pannelli
    "sfondo_campi":          F["paper"],      # menu a tendina, checkbox, radio, tabella, istruzioni
    "sfondo_istruzioni":     F["paper"],      # riquadro istruzioni (scheda Strumenti)
    "anteprima_sfondo":      F["base-200"],   # sfondo dei due riquadri con le immagini
    "anteprima_testo":       F["base-800"],   # scritta con dimensioni/zoom nell'anteprima

    # Testi
    "testo":                 F["black"],      # testo principale
    "testo_secondario":      F["base-600"],   # note, messaggi neutri
    "testo_disabilitato":    F["base-500"],   # controlli non attivi
    "ok":                    F["green-600"],  # risparmio ottenuto, stato "Aggiornato"
    "errore":                F["red-600"],    # nessun risparmio, errori, strumenti mancanti

    # Linee e bordi
    "linea":                 F["base-300"],

    # Pulsante primario (Apri PNG / Apri PDF / Ricontrolla)
    "primario":              F["blue-600"],
    "primario_hover":        F["blue-400"],
    "primario_premuto":      F["blue-400"],
    # Pulsante di salvataggio (Salva con nome)
    "salva":                 F["green-600"],
    "salva_hover":           F["green-400"],
    "salva_premuto":         F["green-400"],
    # Testo sui pulsanti colorati
    "testo_su_pulsante":     F["paper"],
    # Pulsanti secondari (Adatta al box, Zoom 100%, Scarica...)
    "secondario":            F["base-150"],
    "secondario_hover":      F["base-200"],
    "secondario_premuto":    F["base-300"],
    "secondario_testo":      F["black"],
    # Pulsanti disattivati
    "pulsante_disabilitato":       F["base-100"],
    "pulsante_disabilitato_testo": F["base-500"],

    # Checkbox e radio button
    "indicatore":            F["blue-600"],   # spunta / pallino
    "indicatore_bordo":      F["base-500"],

    # Linguette in alto
    "linguetta_inattiva":        F["base-150"],
    "linguetta_inattiva_testo":  F["base-800"],
    "linguetta_hover":           F["base-200"],
    "linguetta_attiva_testo":    F["paper"],
    "linguette_attive":          [F["cyan-600"],     # PNG
                                  F["magenta-600"],  # PDF
                                  F["yellow-600"]],  # Strumenti

    # Selezioni (testo selezionato, righe della tabella)
    "selezione":             F["base-200"],
    "selezione_testo":       F["black"],

    # Tabella strumenti
    "tabella_intestazione":       F["base-150"],
    "tabella_intestazione_testo": F["black"],

    # Barra di avanzamento
    "progress":              F["blue-600"],
    "progress_sfondo":       F["base-150"],
}
C = COLORI

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 960

FONT_SIZES = {"small": 9, "normal": 10, "large": 12}

PNGQUANT_WIN_LATEST = (2, 17, 0)


TOOLS = {
    "oxipng": {
        "title": "oxipng",
        "use": "PNG lossless",
        "names": ["oxipng.exe"] if IS_WIN else ["oxipng"],
        "url": "https://github.com/oxipng/oxipng/releases/latest",
    },
    "pngquant": {
        "title": "pngquant",
        "use": "PNG lossy",
        "names": ["pngquant.exe"] if IS_WIN else ["pngquant"],
        "url": "https://pngquant.org/",
    },
    "ghostscript": {
        "title": "Ghostscript",
        "use": "Compressione PDF",
        "names": ["gswin64c.exe", "gswin32c.exe"] if IS_WIN else ["gs"],
        "url": "https://ghostscript.com/releases/gsdnld.html",
    },
}

INSTALL_HELP = {
    "oxipng": {
        "win": (
            "WINDOWS\n"
            "1. Vai su https://github.com/oxipng/oxipng/releases/latest\n"
            "2. Scarica il file  oxipng-X.Y.Z-x86_64-pc-windows-msvc.zip\n"
            "3. Estrai  oxipng.exe  nella cartella bin di tappo:\n"
            "   {bin}\n"
        ),
        "linux": (
            "LINUX\n"
            "Opzione A (Debian/Ubuntu recenti):\n"
            "   sudo apt install oxipng\n\n"
            "Opzione B (Rust):\n"
            "   cargo install oxipng\n\n"
            "Opzione C (binario ufficiale):\n"
            "   scarica il .tar.gz per Linux da\n"
            "   https://github.com/oxipng/oxipng/releases/latest\n"
            "   copia il file 'oxipng' in:\n"
            "   {bin}\n"
            "   e rendilo eseguibile:  chmod +x oxipng\n"
        ),
    },
    "pngquant": {
        "win": (
            "WINDOWS\n"
            "1. Vai su https://pngquant.org/ e scarica la versione per Windows (zip)\n"
            "2. Estrai  pngquant.exe  nella cartella bin di tappo:\n"
            "   {bin}\n\n"
            "NOTA: l'exe per Windows sul sito ufficiale è la 2.17; la 3.x esiste solo per\n"
            "Linux e macOS. Su Windows TAPPO NON confronta pngquant con GitHub: usa la\n"
            "costante PNGQUANT_WIN_LATEST in cima al file (modificabile a mano), quindi\n"
            "la 2.17 risulta 'Aggiornata'. Per le funzioni usate da TAPPO le due versioni\n"
            "sono equivalenti.\n"
        ),
        "linux": (
            "LINUX\n"
            "   Debian/Ubuntu:  sudo apt install pngquant\n"
            "   Fedora:         sudo dnf install pngquant\n"
            "   Arch:           sudo pacman -S pngquant\n\n"
            "Oppure copia un binario compilato in:\n"
            "   {bin}\n"
            "e rendilo eseguibile:  chmod +x pngquant\n"
        ),
    },
    "ghostscript": {
        "win": (
            "WINDOWS\n"
            "1. Scarica l'installer (64 bit) da\n"
            "   https://ghostscript.com/releases/gsdnld.html\n"
            "2. Installalo: TAPPO trova da solo gswin64c.exe in\n"
            "   C:\\Program Files\\gs\\...\n"
            "3. In alternativa, per un uso 'portatile', copia nella cartella bin\n"
            "   ({bin})\n"
            "   gswin64c.exe e gsdll64.dll (e la cartella lib/resource di Ghostscript).\n"
        ),
        "linux": (
            "LINUX\n"
            "   Debian/Ubuntu:  sudo apt install ghostscript\n"
            "   Fedora:         sudo dnf install ghostscript\n"
            "   Arch:           sudo pacman -S ghostscript\n"
        ),
    },
}

PNG_PRESETS = {
    "Lossless - leggero (oxipng -o1)": {"mode": "lossless", "opt": 1},
    "Lossless - standard (oxipng -o3)": {"mode": "lossless", "opt": 3},
    "Lossless - massimo (oxipng -o6)": {"mode": "lossless", "opt": 6},
    "Lossy - alta qualità (pngquant 80-95)": {"mode": "lossy", "qmin": 80, "qmax": 95, "speed": 3},
    "Lossy - bilanciato (pngquant 65-80)": {"mode": "lossy", "qmin": 65, "qmax": 80, "speed": 3},
    "Lossy - forte (pngquant 45-65)": {"mode": "lossy", "qmin": 45, "qmax": 65, "speed": 3},
    "Lossy - estremo (pngquant 20-45)": {"mode": "lossy", "qmin": 20, "qmax": 45, "speed": 3},
}
DEFAULT_PNG_PRESET = "Lossless - standard (oxipng -o3)"
POST_OXIPNG_LEVEL = 3

PDF_PRESETS = [
    ("screen", "screen   -  72 dpi: file più piccolo, qualità bassa (solo lettura a schermo)"),
    ("ebook", "ebook    -  150 dpi: buon compromesso (consigliato)"),
    ("printer", "printer  -  300 dpi: qualità adatta alla stampa"),
    ("prepress", "prepress -  300 dpi: qualità massima, colori preservati"),
]


def enable_hidpi():
    if sys.platform != "win32":
        return
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def set_windows_app_id():
    if sys.platform != "win32":
        return
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("tappo.app")
    except Exception:
        pass


def apply_windows_icon_sizes(root, ico_path, warn):
    try:
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32
        user32.LoadImageW.restype = ctypes.c_void_p
        user32.LoadImageW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR, wintypes.UINT,
                                      ctypes.c_int, ctypes.c_int, wintypes.UINT]
        user32.SendMessageW.restype = ctypes.c_ssize_t
        user32.SendMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, ctypes.c_void_p]
        user32.GetParent.restype = wintypes.HWND
        user32.GetParent.argtypes = [wintypes.HWND]

        root.update_idletasks()
        child = root.winfo_id()
        hwnd = user32.GetParent(child) or child
        try:
            dpi = user32.GetDpiForWindow(hwnd) or 96
        except AttributeError:
            dpi = 96

        def metric(index):
            try:
                return user32.GetSystemMetricsForDpi(index, dpi)
            except AttributeError:
                return user32.GetSystemMetrics(index)

        SM_CXICON, SM_CXSMICON = 11, 49
        ICON_SMALL, ICON_BIG = 0, 1
        IMAGE_ICON, LR_LOADFROMFILE, WM_SETICON = 1, 0x10, 0x0080
        for which, size in ((ICON_SMALL, metric(SM_CXSMICON)), (ICON_BIG, metric(SM_CXICON))):
            handle = user32.LoadImageW(None, ico_path, IMAGE_ICON, size, size, LR_LOADFROMFILE)
            if handle:
                user32.SendMessageW(hwnd, WM_SETICON, which, handle)
            else:
                warn(f"Windows non riesce a caricare l'icona da {size}x{size} px")
    except Exception as e:
        warn(f"impossibile impostare le dimensioni dell'icona: {e}")


def set_app_icon(root):
    def warn(msg):
        print(f"[tappo] icona: {msg}", file=sys.stderr)

    ico = os.path.join(BASE_DIR, "tappo.ico")
    png = os.path.join(BASE_DIR, "tappo.png")
    done = False

    if IS_WIN:
        if not os.path.isfile(ico):
            warn(f"file non trovato: {ico}  (controlla che l'estensione non sia doppia, "
                 "es. tappo.ico.ico, con le estensioni nascoste di Windows)")
        else:
            with open(ico, "rb") as f:
                head = f.read(4)
            if head != b"\x00\x00\x01\x00":
                warn("tappo.ico non è un vero file .ico (forse è un PNG rinominato): "
                     "va convertito con un programma che esporta in formato ICO")
            else:
                try:
                    root.iconbitmap(default=ico)
                    root.iconbitmap(ico)
                    apply_windows_icon_sizes(root, ico, warn)
                    done = True
                except tk.TclError as e:
                    warn(f"Tk non riesce a leggere tappo.ico: {e}")

    if not done:
        if not os.path.isfile(png):
            warn(f"file non trovato: {png}")
        else:
            with open(png, "rb") as f:
                head = f.read(8)
            if head != b"\x89PNG\r\n\x1a\n":
                warn("tappo.png non è un vero PNG (estensione rinominata?)")
            else:
                try:
                    img = tk.PhotoImage(file=png)
                    root.iconphoto(True, img)
                    root._icon_ref = img
                except tk.TclError as e:
                    warn(f"Tk non riesce a leggere tappo.png: {e}")


UI_SCALE = 1.0


def sc(n):
    return int(round(n * UI_SCALE))


def mono_font(master):
    preferred = ["Consolas", "Cascadia Mono", "Cascadia Code", "DejaVu Sans Mono", "Liberation Mono",
                 "Ubuntu Mono", "Noto Sans Mono", "Menlo", "Monaco", "Lucida Console"]
    installed = set(tkfont.families(master))
    size = FONT_SIZES["normal"]
    for fam in preferred:
        if fam in installed:
            return tkfont.Font(master, family=fam, size=size)
    return tkfont.Font(master, family="TkFixedFont", size=size)


def hsize(n):
    if n >= 1024 * 1024:
        return f"{n / (1024 * 1024):.2f} MB"
    return f"{n / 1024:.1f} KB"


def run(cmd, timeout=600):
    kw = {}
    if IS_WIN:
        kw["creationflags"] = 0x08000000
    return subprocess.run(
        cmd, capture_output=True, text=True, errors="replace", timeout=timeout, **kw
    )


def find_binary(key):
    names = TOOLS[key]["names"]
    for name in names:
        p = os.path.join(BIN_DIR, name)
        if os.path.isfile(p):
            if not IS_WIN and not os.access(p, os.X_OK):
                try:
                    os.chmod(p, os.stat(p).st_mode | 0o111)
                except OSError:
                    pass
            if IS_WIN or os.access(p, os.X_OK):
                return p
    for name in names:
        p = shutil.which(name)
        if p:
            return p
    if IS_WIN and key == "ghostscript":
        for env in ("PROGRAMFILES", "PROGRAMFILES(X86)"):
            base = os.environ.get(env)
            if not base:
                continue
            for name in names:
                found = sorted(glob.glob(os.path.join(base, "gs", "gs*", "bin", name)), reverse=True)
                if found:
                    return found[0]
    return None


def parse_version(text):
    m = re.search(r"\d+(?:\.\d+)+", text or "")
    if not m:
        return None
    return tuple(int(x) for x in m.group(0).split("."))


def parse_gs_tag(tag):
    m = re.match(r"^gs(\d+)$", tag or "")
    if not m:
        return None
    d = m.group(1)
    if len(d) < 4:
        return None
    return (int(d[:-3]), int(d[-3:-1]), int(d[-1]))


def fmt_version(v):
    return ".".join(str(x) for x in v) if v else "-"


def fetch_json(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": APP_NAME, "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=8) as r:
        return json.loads(r.read().decode("utf-8"))


def latest_version(key):
    if key == "oxipng":
        data = fetch_json("https://api.github.com/repos/oxipng/oxipng/releases/latest")
        return parse_version(data.get("tag_name", ""))
    if key == "pngquant":
        if IS_WIN:
            return PNGQUANT_WIN_LATEST
        data = fetch_json("https://api.github.com/repos/kornelski/pngquant/tags")
        versions = [parse_version(t.get("name", "")) for t in data]
        versions = [v for v in versions if v]
        return max(versions) if versions else None
    data = fetch_json("https://api.github.com/repos/ArtifexSoftware/ghostpdl-downloads/releases/latest")
    return parse_gs_tag(data.get("tag_name", ""))


def check_tool(key):
    res = {"path": find_binary(key), "installed": None, "latest": None}
    if res["path"]:
        try:
            r = run([res["path"], "--version"], timeout=20)
            res["installed"] = parse_version((r.stdout or "") + (r.stderr or ""))
        except Exception:
            pass
    try:
        res["latest"] = latest_version(key)
    except Exception:
        pass
    return res


def tool_status(info):
    if not info["path"]:
        return "NON TROVATO", "warn"
    if info["latest"] is None:
        return "Installato (controllo online non riuscito)", "neutral"
    if info["installed"] is None:
        return "Installato (versione sconosciuta)", "neutral"
    if info["installed"] < info["latest"]:
        return "AGGIORNAMENTO DISPONIBILE", "warn"
    return "Aggiornato", "ok"


INSTALLER_DIR = os.path.join(BIN_DIR, "_installer")
IS_ARM = platform.machine().lower() in ("aarch64", "arm64")


class ManualInstall(Exception):

    def __init__(self, packages):
        super().__init__(", ".join(packages))
        self.packages = packages


def http_download(url, dest, log, label):
    req = urllib.request.Request(url, headers={"User-Agent": APP_NAME})
    with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as f:
        total = int(r.headers.get("Content-Length") or 0)
        done = 0
        last = -1
        while True:
            chunk = r.read(65536)
            if not chunk:
                break
            f.write(chunk)
            done += len(chunk)
            if total:
                pct = int(done * 100 / total)
                if pct != last:
                    last = pct
                    log(f"{label}: download {pct}%")


def github_asset(repo, patterns):
    data = fetch_json(f"https://api.github.com/repos/{repo}/releases/latest")
    for pat in patterns:
        for a in data.get("assets", []):
            if re.search(pat, a["name"]):
                return a["name"], a["browser_download_url"]
    raise RuntimeError("Nessun file compatibile con questo sistema nella release più recente.")


def extract_files(archive, want, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    extracted = []

    def write(base, fileobj):
        target = os.path.join(dest_dir, base)
        tmp_target = target + ".new"
        with open(tmp_target, "wb") as out:
            shutil.copyfileobj(fileobj, out)
        os.replace(tmp_target, target)
        if not IS_WIN:
            os.chmod(target, 0o755)
        extracted.append(target)

    if archive.endswith(".zip"):
        with zipfile.ZipFile(archive) as z:
            for info in z.infolist():
                base = os.path.basename(info.filename)
                if base and want(base):
                    with z.open(info) as f:
                        write(base, f)
    else:
        with tarfile.open(archive) as t:
            for m in t.getmembers():
                base = os.path.basename(m.name)
                if m.isfile() and base and want(base):
                    f = t.extractfile(m)
                    if f:
                        write(base, f)
    return extracted


def verify_binary(path):
    r = run([path, "--version"], timeout=30)
    if r.returncode != 0:
        raise RuntimeError(f"{os.path.basename(path)} scaricato ma non funziona su questo sistema.")
    return parse_version((r.stdout or "") + (r.stderr or ""))


def install_oxipng(log, tmp):
    arch = "aarch64" if (IS_ARM and not IS_WIN) else "x86_64"
    if IS_WIN:
        pats = [rf"{arch}-pc-windows-msvc\.zip$"]
    else:
        pats = [rf"{arch}-unknown-linux-musl\.tar\.gz$", rf"{arch}-unknown-linux-gnu\.tar\.gz$"]
    name, url = github_asset("oxipng/oxipng", pats)
    archive = os.path.join(tmp, name)
    http_download(url, archive, log, "oxipng")
    exe = TOOLS["oxipng"]["names"][0]
    files = extract_files(archive, lambda b: b.lower() == exe.lower(), BIN_DIR)
    if not files:
        raise RuntimeError(f"{exe} non trovato nell'archivio scaricato.")
    return f"oxipng {fmt_version(verify_binary(files[0]))} copiato in bin"


def install_pngquant(log, tmp):
    if not IS_WIN:
        raise ManualInstall(["pngquant"])
    archive = os.path.join(tmp, "pngquant-windows.zip")
    http_download("https://pngquant.org/pngquant-windows.zip", archive, log, "pngquant")
    files = extract_files(archive, lambda b: b.lower() == "pngquant.exe" or b.lower().endswith(".dll"), BIN_DIR)
    exe = [f for f in files if f.lower().endswith("pngquant.exe")]
    if not exe:
        raise RuntimeError("pngquant.exe non trovato nell'archivio scaricato.")
    return f"pngquant {fmt_version(verify_binary(exe[0]))} copiato in bin"


def install_ghostscript(log, tmp):
    if not IS_WIN:
        raise ManualInstall(["ghostscript"])
    name, url = github_asset("ArtifexSoftware/ghostpdl-downloads", [r"^gs\d+w64\.exe$"])
    os.makedirs(INSTALLER_DIR, exist_ok=True)
    dest = os.path.join(INSTALLER_DIR, name)
    http_download(url, dest, log, "Ghostscript")
    log("Ghostscript: avvio installer…")
    os.startfile(dest)
    return ("Installer di Ghostscript scaricato e avviato: completa l'installazione, "
            "poi premi 'Ricontrolla aggiornamenti'. TAPPO lo troverà da solo.")


INSTALLERS = {"oxipng": install_oxipng, "pngquant": install_pngquant, "ghostscript": install_ghostscript}


def linux_install_command(packages):
    ids = set()
    try:
        with open("/etc/os-release", encoding="utf-8") as f:
            for line in f:
                if line.startswith(("ID=", "ID_LIKE=")):
                    ids.update(line.split("=", 1)[1].strip().strip('"').lower().split())
    except OSError:
        return None
    pk = " ".join(packages)
    if ids & {"debian", "ubuntu"}:
        return f"sudo apt install {pk}"
    if ids & {"fedora", "rhel", "centos"}:
        return f"sudo dnf install {pk}"
    if "arch" in ids:
        return f"sudo pacman -S {pk}"
    if ids & {"suse", "opensuse", "opensuse-leap", "opensuse-tumbleweed"}:
        return f"sudo zypper install {pk}"
    return None


def run_oxipng(exe, src, dst, level, strip, zopfli):
    cmd = [exe, "-o", str(level), "--out", dst, "-q"]
    if strip:
        cmd += ["--strip", "safe"]
    if zopfli:
        cmd.append("--zopfli")
    cmd.append(src)
    r = run(cmd, timeout=3600 if zopfli else 600)
    if r.returncode != 0:
        raise RuntimeError("oxipng ha restituito un errore:\n" + (r.stderr or r.stdout or "").strip())
    if not os.path.exists(dst):
        shutil.copyfile(src, dst)


def run_pngquant(exe, src, dst, qmin, qmax, speed, strip):
    cmd = [exe, f"--quality={qmin}-{qmax}", "--speed", str(speed), "--force", "--output", dst]
    if strip:
        cmd.append("--strip")
    cmd += ["--", src]
    r = run(cmd)
    if r.returncode == 99:
        raise RuntimeError(
            "pngquant non riesce a raggiungere la qualità minima richiesta.\n"
            "Scegli un livello lossy meno spinto."
        )
    if r.returncode != 0 or not os.path.exists(dst):
        raise RuntimeError("pngquant ha restituito un errore:\n" + (r.stderr or r.stdout or "").strip())


def run_ghostscript(exe, src, dst, setting):
    cmd = [
        exe, "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4", f"-dPDFSETTINGS=/{setting}",
        "-dNOPAUSE", "-dQUIET", "-dBATCH", "-dSAFER", f"-sOutputFile={dst}", src,
    ]
    r = run(cmd, timeout=1800)
    if r.returncode != 0 or not os.path.exists(dst):
        raise RuntimeError("Ghostscript ha restituito un errore:\n" + (r.stderr or r.stdout or "").strip())


def save_result(out, src, title, ext, label):
    if not out or not os.path.exists(out):
        return
    stem = os.path.splitext(os.path.basename(src))[0]
    dst = filedialog.asksaveasfilename(
        title=title, defaultextension=ext,
        initialdir=os.path.dirname(src), initialfile=f"{stem}_tappo{ext}",
        filetypes=[(label, f"*{ext}")],
    )
    if not dst:
        return
    try:
        shutil.copyfile(out, dst)
        messagebox.showinfo(APP_NAME, f"File salvato:\n{dst}")
    except OSError as e:
        messagebox.showerror(APP_NAME, f"Impossibile salvare il file:\n{e}")


def result_text(orig, new):
    saved = orig - new
    pct = (saved / orig * 100) if orig else 0
    if saved > 0:
        return (f"Originale: {hsize(orig)}  →  Compresso: {hsize(new)}   |   "
                f"Risparmio: {hsize(saved)} ({pct:.1f}%)"), C["ok"]
    return (f"Originale: {hsize(orig)}  →  Compresso: {hsize(new)}   |   "
            f"Nessun risparmio (+{hsize(-saved)}): conviene tenere l'originale"), C["errore"]


class PngTab(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master, padding=8)
        self.app = app
        self.src = None
        self.out = None
        self.gen = 0
        self._job = None
        self._redraw_job = None
        self._cache = {}
        self._refs = {}
        self.fit_mode = True

        self.preset = tk.StringVar(value=DEFAULT_PNG_PRESET)
        self.strip = tk.BooleanVar(value=True)
        self.post = tk.BooleanVar(value=False)
        self.zopfli = tk.BooleanVar(value=False)

        top = ttk.Frame(self)
        top.pack(fill="x")
        ttk.Button(top, text="Apri PNG…", style="Primary.TButton", command=self.open_file).pack(side="left")
        self.lbl_file = ttk.Label(top, text="Nessun file caricato")
        self.lbl_file.pack(side="left", padx=12)
        self.btn_save = ttk.Button(top, text="Salva con nome…", style="Save.TButton",
                                   command=self.save_as, state="disabled")
        self.btn_save.pack(side="right")

        box = ttk.LabelFrame(self, text="Compressione", padding=8)
        box.pack(fill="x", pady=8)

        r0 = ttk.Frame(box)
        r0.pack(fill="x")
        ttk.Label(r0, text="Livello:").pack(side="left")
        cb = ttk.Combobox(r0, textvariable=self.preset, values=list(PNG_PRESETS), state="readonly", width=42)
        cb.pack(side="left", padx=6)
        cb.bind("<<ComboboxSelected>>", lambda e: self.options_changed())

        r1 = ttk.Frame(box)
        r1.pack(fill="x", pady=(8, 0))
        ttk.Checkbutton(r1, text="Rimuovi metadati", variable=self.strip,
                        command=self.options_changed).pack(side="left")
        self.chk_post = ttk.Checkbutton(r1, text="Poi ottimizza con oxipng", variable=self.post,
                                        command=self.options_changed)
        self.chk_post.pack(side="left", padx=16)
        self.chk_zopfli = ttk.Checkbutton(r1, text="Usa Zopfli (molto più lento, risparmia di più)",
                                          variable=self.zopfli, command=self.options_changed)
        self.chk_zopfli.pack(side="left")

        zb = ttk.Frame(self)
        zb.pack(fill="x", pady=(0, 4))
        ttk.Label(zb, text="Anteprima:").pack(side="left")
        ttk.Button(zb, text="Adatta al box", command=lambda: self.set_zoom(True)).pack(side="left", padx=(8, 4))
        ttk.Button(zb, text="Zoom 100%", command=lambda: self.set_zoom(False)).pack(side="left")
        self.lbl_zoom = ttk.Label(zb, text="", font=app.fonts["small"], foreground=C["testo_secondario"])
        self.lbl_zoom.pack(side="left", padx=12)

        panes = ttk.Frame(self)
        panes.pack(fill="both", expand=True)
        panes.columnconfigure(0, weight=1, uniform="p")
        panes.columnconfigure(1, weight=1, uniform="p")
        panes.rowconfigure(0, weight=1)

        self.lf_left = ttk.LabelFrame(panes, text="Originale", padding=4)
        self.lf_left.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        self.lf_right = ttk.LabelFrame(panes, text="Compresso (anteprima)", padding=4)
        self.lf_right.grid(row=0, column=1, sticky="nsew", padx=(4, 0))
        cv_opts = dict(bg=C["anteprima_sfondo"], highlightthickness=1, highlightbackground=C["linea"])
        self.cv_left = tk.Canvas(self.lf_left, **cv_opts)
        self.cv_right = tk.Canvas(self.lf_right, **cv_opts)
        self.cv_left.pack(fill="both", expand=True)
        self.cv_right.pack(fill="both", expand=True)
        self.cv_left.bind("<Configure>", self.schedule_redraw)
        self.cv_right.bind("<Configure>", self.schedule_redraw)

        self.lbl_info = ttk.Label(self, text="Apri un file PNG per iniziare.", anchor="w",
                                  font=app.fonts["normal_bold"], foreground=C["testo_secondario"])
        self.lbl_info.pack(fill="x", pady=(8, 0))

        self.update_option_states()

    def update_option_states(self):
        lossy = PNG_PRESETS[self.preset.get()]["mode"] == "lossy"
        self.chk_post.config(state="normal" if lossy else "disabled")
        oxipng_runs = (not lossy) or self.post.get()
        self.chk_zopfli.config(state="normal" if oxipng_runs else "disabled")

    def options_changed(self):
        self.update_option_states()
        self.schedule()

    def schedule(self):
        if not self.src:
            return
        if self._job:
            self.after_cancel(self._job)
        self._job = self.after(400, self.compress)

    def open_file(self):
        path = filedialog.askopenfilename(title="Apri PNG", filetypes=[("Immagini PNG", "*.png"), ("Tutti i file", "*.*")])
        if not path:
            return
        self.src = path
        self.out = None
        self.lbl_file.config(text=os.path.basename(path))
        self.lf_left.config(text=f"Originale - {hsize(os.path.getsize(path))}")
        self.lf_right.config(text="Compresso (anteprima)")
        self.btn_save.config(state="disabled")
        self.draw_all()
        self.compress()

    def compress(self):
        self._job = None
        if not self.src:
            return
        preset = PNG_PRESETS[self.preset.get()]
        lossy = preset["mode"] == "lossy"
        strip = self.strip.get()
        post = lossy and self.post.get()
        use_oxipng = (not lossy) or post
        zopfli = self.zopfli.get() and use_oxipng

        need = (["pngquant"] if lossy else []) + (["oxipng"] if use_oxipng else [])
        exes = {k: find_binary(k) for k in need}
        missing = [k for k, v in exes.items() if not v]
        if missing:
            self.set_info(f"Manca: {', '.join(missing)}. Vedi la scheda 'Strumenti' per installarlo.", C["errore"])
            return

        self.gen += 1
        g = self.gen
        tmp = self.app.tmpdir
        src_copy = os.path.join(tmp, f"in_{g}.png")
        self.btn_save.config(state="disabled")
        self.set_info("Compressione in corso…" + (" (Zopfli: può richiedere parecchio tempo)" if zopfli else ""),
                      C["testo_secondario"])
        orig_size = os.path.getsize(self.src)

        def work():
            shutil.copyfile(self.src, src_copy)
            out = os.path.join(tmp, f"out_{g}.png")
            if not lossy:
                run_oxipng(exes["oxipng"], src_copy, out, preset["opt"], strip, zopfli)
            else:
                mid = os.path.join(tmp, f"mid_{g}.png")
                run_pngquant(exes["pngquant"], src_copy, mid, preset["qmin"], preset["qmax"],
                             preset["speed"], strip)
                if post:
                    run_oxipng(exes["oxipng"], mid, out, POST_OXIPNG_LEVEL, strip, zopfli)
                else:
                    out = mid
            return out

        def done(res, err):
            if g != self.gen:
                return
            if err:
                self.out = None
                self.set_info(str(err).splitlines()[0] if str(err) else "Errore", C["errore"])
                messagebox.showerror(APP_NAME, str(err))
                return
            self.out = res
            new_size = os.path.getsize(res)
            txt, color = result_text(orig_size, new_size)
            self.set_info(txt, color)
            self.lf_right.config(text=f"Compresso (anteprima) - {hsize(new_size)}")
            self.btn_save.config(state="normal")
            self.draw_all()

        self.app.run_bg(work, done)

    def set_info(self, text, color):
        self.lbl_info.config(text=text, foreground=color)

    def save_as(self):
        save_result(self.out, self.src, "Salva PNG compresso", ".png", "Immagini PNG")

    def set_zoom(self, fit):
        self.fit_mode = fit
        self.draw_all()

    def schedule_redraw(self, _evt=None):
        if self._redraw_job:
            self.after_cancel(self._redraw_job)
        self._redraw_job = self.after(150, self.draw_all)

    def draw_all(self):
        self._redraw_job = None
        self.draw(self.cv_left, self.src, "l")
        self.draw(self.cv_right, self.out, "r")

    def _load(self, path):
        key = (path, os.path.getmtime(path))
        entry = self._cache.get(key)
        if entry is None:
            if len(self._cache) > 6:
                self._cache.clear()
            if HAVE_PIL:
                try:
                    im = Image.open(path)
                    im.load()
                    if im.mode not in ("RGB", "RGBA"):
                        im = im.convert("RGBA")
                    entry = ("pil", im)
                except Exception:
                    entry = None
            if entry is None:
                entry = ("tk", tk.PhotoImage(file=path))
            self._cache[key] = entry
        return entry

    def _render(self, path, cw, ch):
        kind, obj = self._load(path)
        iw, ih = obj.size if kind == "pil" else (obj.width(), obj.height())
        fit = min(cw / iw, ch / ih)
        scale = fit if self.fit_mode else min(1.0, fit)
        if kind == "pil":
            if abs(scale - 1.0) < 1e-6:
                im2 = obj
            else:
                size = (max(1, int(iw * scale)), max(1, int(ih * scale)))
                im2 = obj.resize(size, _RES.NEAREST if scale > 1 else _RES.LANCZOS)
            return ImageTk.PhotoImage(im2), iw, ih, scale
        if scale >= 1:
            z = max(1, int(scale))
            return (obj.zoom(z, z) if z > 1 else obj), iw, ih, float(z)
        f = math.ceil(1 / scale)
        return obj.subsample(f, f), iw, ih, 1.0 / f

    def draw(self, cv, path, tag):
        cv.delete("all")
        cw, ch = cv.winfo_width() - 4, cv.winfo_height() - 4
        if not path or cw < 20 or ch < 20 or not os.path.exists(path):
            if tag == "l":
                self.lbl_zoom.config(text="")
            return
        try:
            img, iw, ih, scale = self._render(path, cw, ch)
            self._refs[tag] = img
            cv.create_image(cv.winfo_width() // 2, cv.winfo_height() // 2, image=img)
            cv.create_text(8, 8, anchor="nw", fill=C["anteprima_testo"], font=self.app.fonts["small"],
                           text=f"{iw}×{ih} px  -  zoom {scale * 100:.0f}%")
            if tag == "l":
                if self.fit_mode:
                    self.lbl_zoom.config(text=f"Adattata al box (zoom {scale * 100:.0f}%)")
                elif scale < 1 - 1e-6:
                    self.lbl_zoom.config(text=f"100% non entra nel box: mostrata al {scale * 100:.0f}%")
                else:
                    self.lbl_zoom.config(text="Dimensioni reali (100%)")
        except tk.TclError:
            cv.create_text(cw // 2, ch // 2, fill=C["anteprima_testo"], font=self.app.fonts["small"],
                           text="Anteprima non disponibile per questo PNG\n(il file può comunque essere salvato)")


class PdfTab(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master, padding=8)
        self.app = app
        self.src = None
        self.out = None
        self.gen = 0
        self.setting = tk.StringVar(value="ebook")

        top = ttk.Frame(self)
        top.pack(fill="x")
        ttk.Button(top, text="Apri PDF…", style="Primary.TButton", command=self.open_file).pack(side="left")
        self.lbl_file = ttk.Label(top, text="Nessun file caricato")
        self.lbl_file.pack(side="left", padx=12)
        self.btn_save = ttk.Button(top, text="Salva con nome…", style="Save.TButton",
                                   command=self.save_as, state="disabled")
        self.btn_save.pack(side="right")

        box = ttk.LabelFrame(self, text="Livello di compressione (Ghostscript -dPDFSETTINGS)", padding=10)
        box.pack(fill="x", pady=12)
        for val, desc in PDF_PRESETS:
            ttk.Radiobutton(box, text=desc, value=val, variable=self.setting,
                            command=self.compress).pack(anchor="w", pady=2)

        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.progress.pack(fill="x", pady=(0, 8))

        ttk.Label(self, text="Nota: nessuna anteprima per i PDF. Controlla il risparmio e salva.",
                  font=app.fonts["small"], foreground=C["testo_secondario"]).pack(anchor="w")

        self.lbl_info = ttk.Label(self, text="Apri un file PDF per iniziare.", anchor="w",
                                  font=app.fonts["normal_bold"], foreground=C["testo_secondario"])
        self.lbl_info.pack(fill="x", side="bottom")

    def open_file(self):
        path = filedialog.askopenfilename(title="Apri PDF", filetypes=[("Documenti PDF", "*.pdf"), ("Tutti i file", "*.*")])
        if not path:
            return
        self.src = path
        self.out = None
        self.lbl_file.config(text=f"{os.path.basename(path)}  ({hsize(os.path.getsize(path))})")
        self.btn_save.config(state="disabled")
        self.compress()

    def compress(self):
        if not self.src:
            return
        exe = find_binary("ghostscript")
        if not exe:
            self.lbl_info.config(text="Ghostscript non trovato. Vedi la scheda 'Strumenti'.",
                                 foreground=C["errore"])
            return
        self.gen += 1
        g = self.gen
        setting = self.setting.get()
        tmp = self.app.tmpdir
        orig_size = os.path.getsize(self.src)
        self.btn_save.config(state="disabled")
        self.lbl_info.config(text=f"Compressione in corso ({setting})… può richiedere un po' di tempo.",
                             foreground=C["testo_secondario"])
        self.progress.start(12)

        def work():
            src_copy = os.path.join(tmp, f"in_{g}.pdf")
            out = os.path.join(tmp, f"out_{g}.pdf")
            shutil.copyfile(self.src, src_copy)
            run_ghostscript(exe, src_copy, out, setting)
            return out

        def done(res, err):
            if g != self.gen:
                return
            self.progress.stop()
            if err:
                self.out = None
                self.lbl_info.config(text="Errore durante la compressione.", foreground=C["errore"])
                messagebox.showerror(APP_NAME, str(err))
                return
            self.out = res
            txt, color = result_text(orig_size, os.path.getsize(res))
            self.lbl_info.config(text=txt, foreground=color)
            self.btn_save.config(state="normal")

        self.app.run_bg(work, done)

    def save_as(self):
        save_result(self.out, self.src, "Salva PDF compresso", ".pdf", "Documenti PDF")


class ToolsTab(ttk.Frame):
    def __init__(self, master, app):
        super().__init__(master, padding=8)
        self.app = app

        ttk.Label(self, text="Programmi esterni necessari", font=app.fonts["large_bold"]).pack(anchor="w")
        ttk.Label(self, text=f"TAPPO li cerca nella cartella:  {BIN_DIR}  (poi nel PATH di sistema).\n"
                             "Ad ogni avvio controlla se esistono versioni più recenti su Internet "
                             "(per il tuo sistema operativo).\n"
                             "Il pulsante «Scarica e installa» scarica da solo gli strumenti mancanti o "
                             "vecchi nella cartella bin.",
                  font=app.fonts["small"], foreground=C["testo_secondario"]).pack(anchor="w", pady=(0, 8))

        cols = ("tool", "uso", "stato", "inst", "ultima", "path")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=5, selectmode="browse")
        for c, t, w in (("tool", "Strumento", 100), ("uso", "Uso", 120), ("stato", "Stato", 240),
                        ("inst", "Installata", 80), ("ultima", "Disponibile", 90), ("path", "Percorso", 320)):
            self.tree.heading(c, text=t)
            self.tree.column(c, width=sc(w), anchor="w")
        self.tree.tag_configure("ok", foreground=C["ok"])
        self.tree.tag_configure("warn", foreground=C["errore"])
        self.tree.pack(fill="x")
        for k, t in TOOLS.items():
            self.tree.insert("", "end", iid=k, values=(t["title"], t["use"], "…", "-", "-", "-"))
        self.tree.selection_set("oxipng")

        btns = ttk.Frame(self)
        btns.pack(fill="x", pady=8)
        ttk.Button(btns, text="Ricontrolla aggiornamenti", style="Primary.TButton",
                   command=app.check_updates).pack(side="left")
        self.btn_install = ttk.Button(btns, text="Scarica e installa in bin", style="Primary.TButton",
                                      command=self.install_all)
        self.btn_install.pack(side="left", padx=6)
        ttk.Button(btns, text="Scarica (apre il browser)", style="Primary.TButton",
                   command=self.download).pack(side="left")
        ttk.Button(btns, text="Apri cartella bin", style="Primary.TButton",
                   command=self.open_bin).pack(side="left", padx=6)

        self.txt = tk.Text(self, height=14, wrap="word", state="disabled", font=mono_font(self),
                           bg=C["sfondo_istruzioni"], fg=C["testo"],
                           selectbackground=C["selezione"], selectforeground=C["selezione_testo"],
                           highlightthickness=1, highlightbackground=C["linea"], relief="flat",
                           padx=8, pady=8)
        self.txt.pack(fill="both", expand=True)
        self.show_help("oxipng")
        self.tree.bind("<<TreeviewSelect>>", lambda e: self.show_help(self.selected()))

    def selected(self):
        sel = self.tree.selection()
        return sel[0] if sel else "oxipng"

    def mark_checking(self):
        for k in TOOLS:
            self.set_row_status(k, "Controllo in corso…")

    def set_row_status(self, key, text):
        self.tree.set(key, "stato", text)
        self.tree.item(key, tags=())

    def install_all(self):
        results = self.app.check_results
        if results:
            targets = [k for k in TOOLS if tool_status(results[k])[1] != "ok"]
        else:
            targets = list(TOOLS)
        if not targets:
            messagebox.showinfo(APP_NAME, "Tutti gli strumenti risultano già aggiornati.")
            return
        self.btn_install.config(state="disabled")
        for k in targets:
            self.set_row_status(k, "In attesa…")
        tmp = self.app.tmpdir

        def work():
            outcome = {}
            for k in targets:
                def log(txt, k=k):
                    self.app.post_ui(lambda: self.set_row_status(k, txt))
                try:
                    outcome[k] = ("ok", INSTALLERS[k](log, tmp))
                except ManualInstall as e:
                    outcome[k] = ("manual", e.packages)
                except Exception as e:
                    outcome[k] = ("err", str(e))
            return outcome

        def done(outcome, err):
            self.btn_install.config(state="normal")
            self.app.check_updates()
            if err or not outcome:
                messagebox.showerror(APP_NAME, f"Operazione non riuscita:\n{err}")
                return
            lines = []
            manual = []
            for k, (kind, info) in outcome.items():
                title = TOOLS[k]["title"]
                if kind == "ok" and k == "ghostscript":
                    lines.append(f"{title}: {info}")
                elif kind == "manual":
                    manual += info
                elif kind == "err":
                    lines.append(f"{title}: errore - {info}")
            if manual:
                cmd = linux_install_command(manual)
                text = ("Per " + ", ".join(manual) + " non esiste un binario ufficiale scaricabile per Linux: "
                        "va installato (o aggiornato) con il gestore pacchetti.")
                if cmd:
                    self.app.clipboard_clear()
                    self.app.clipboard_append(cmd)
                    text += f"\n\nComando (copiato negli appunti):\n{cmd}"
                lines.append(text)
            if lines:
                messagebox.showinfo(APP_NAME, "\n\n".join(lines))

        self.app.run_bg(work, done)

    def update_rows(self, results):
        for k, info in results.items():
            text, tag = tool_status(info)
            self.tree.item(k, values=(
                TOOLS[k]["title"], TOOLS[k]["use"], text,
                fmt_version(info["installed"]), fmt_version(info["latest"]), info["path"] or "-",
            ), tags=(tag,))

    def help_text(self, key):
        h = INSTALL_HELP[key]
        os_part = h["win"] if IS_WIN else h["linux"]
        other = h["linux"] if IS_WIN else h["win"]
        return (f"{TOOLS[key]['title']} - {TOOLS[key]['use']}\n\n"
                + os_part.format(bin=BIN_DIR)
                + "\n--- altro sistema operativo ---\n"
                + other.format(bin=BIN_DIR))

    def show_help(self, key):
        self.txt.config(state="normal")
        self.txt.delete("1.0", "end")
        self.txt.insert("1.0", self.help_text(key))
        self.txt.config(state="disabled")

    def download(self):
        webbrowser.open(TOOLS[self.selected()]["url"])

    def open_bin(self):
        os.makedirs(BIN_DIR, exist_ok=True)
        try:
            if IS_WIN:
                os.startfile(BIN_DIR)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", BIN_DIR])
            else:
                subprocess.Popen(["xdg-open", BIN_DIR])
        except Exception as e:
            messagebox.showinfo(APP_NAME, f"Cartella bin:\n{BIN_DIR}\n\n({e})")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        global UI_SCALE
        UI_SCALE = max(1.0, float(self.tk.call("tk", "scaling")) * 72.0 / 96.0)
        self.title(f"{APP_NAME} - {APP_FULL}")
        w = min(WINDOW_WIDTH, self.winfo_screenwidth())
        h = min(WINDOW_HEIGHT, self.winfo_screenheight())
        self.geometry(f"{w}x{h}")
        self.minsize(min(sc(820), w), min(sc(620), h))
        self.configure(bg=C["sfondo_app"])
        set_app_icon(self)

        self.tmpdir = tempfile.mkdtemp(prefix="tappo_")
        self._q = queue.Queue()
        self.check_results = {}

        self.tab_pad = [sc(16), sc(6)]
        self.setup_fonts()
        self.setup_style()

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True)
        tab_png = PngTab(self.nb, self)
        tab_pdf = PdfTab(self.nb, self)
        self.tab_tools = ToolsTab(self.nb, self)
        labels = self.equal_width_labels(["PNG", "PDF", "Strumenti"])
        self.nb.add(tab_png, text=labels[0])
        self.nb.add(tab_pdf, text=labels[1])
        self.nb.add(self.tab_tools, text=labels[2])
        self.nb.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.on_tab_changed()

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.after(100, self._poll)
        self.after(300, self.check_updates)

    def setup_fonts(self):
        for name in ("TkDefaultFont", "TkTextFont", "TkMenuFont", "TkHeadingFont", "TkCaptionFont",
                     "TkSmallCaptionFont", "TkIconFont", "TkTooltipFont", "TkFixedFont"):
            try:
                tkfont.nametofont(name).configure(size=FONT_SIZES["normal"])
            except tk.TclError:
                pass
        fam = tkfont.nametofont("TkDefaultFont").cget("family")

        def mk(size, weight="normal"):
            return tkfont.Font(self, family=fam, size=FONT_SIZES[size], weight=weight)

        self.fonts = {
            "small": mk("small"),
            "normal": mk("normal"),
            "normal_bold": mk("normal", "bold"),
            "large_bold": mk("large", "bold"),
        }

    def equal_width_labels(self, labels):
        f = self.fonts["large_bold"]
        target = max(f.measure(t) for t in labels)
        space = max(1, f.measure(" "))
        out = []
        for t in labels:
            k = round((target - f.measure(t)) / space)
            left = k // 2
            out.append(" " * left + t + " " * (k - left))
        return out

    # --- stile (tutti i colori vengono dalla palette COLORI)
    def setup_style(self):
        st = self.style = ttk.Style(self)
        # 'clam' permette di colorare pulsanti, linguette e indicatori su tutti i sistemi
        if "clam" in st.theme_names():
            st.theme_use("clam")
        fn = self.fonts

        st.configure(".", background=C["sfondo_app"], foreground=C["testo"], bordercolor=C["linea"],
                     fieldbackground=C["sfondo_campi"], troughcolor=C["progress_sfondo"],
                     selectbackground=C["selezione"], selectforeground=C["selezione_testo"],
                     font=fn["normal"])
        st.map(".", foreground=[("disabled", C["testo_disabilitato"])])

        # menu a tendina: sfondo chiaro (anche la lista che si apre)
        st.configure("TCombobox", background=C["secondario"], arrowcolor=C["testo"], arrowsize=sc(16),
                     bordercolor=C["linea"], padding=sc(4))
        st.map("TCombobox",
               fieldbackground=[("readonly", C["sfondo_campi"]), ("disabled", C["sfondo_app"])],
               foreground=[("readonly", C["testo"])],
               selectbackground=[("readonly", C["sfondo_campi"])],
               selectforeground=[("readonly", C["testo"])],
               background=[("active", C["secondario_hover"])])
        self.option_add("*TCombobox*Listbox.background", C["sfondo_campi"])
        self.option_add("*TCombobox*Listbox.foreground", C["testo"])
        self.option_add("*TCombobox*Listbox.selectBackground", C["selezione"])
        self.option_add("*TCombobox*Listbox.selectForeground", C["selezione_testo"])
        self.option_add("*TCombobox*Listbox.font", fn["normal"])

        # checkbox e radio button: indicatore più grande, sfondo chiaro
        for name in ("TCheckbutton", "TRadiobutton"):
            st.configure(name, indicatorsize=sc(18), indicatormargin=[0, sc(2), sc(8), sc(2)],
                         indicatorbackground=C["sfondo_campi"], indicatorforeground=C["indicatore"],
                         upperbordercolor=C["indicatore_bordo"], lowerbordercolor=C["indicatore_bordo"],
                         padding=sc(3))
            st.map(name,
                   indicatorbackground=[("disabled", C["pulsante_disabilitato"]),
                                        ("pressed", C["sfondo_campi"])],
                   indicatorforeground=[("disabled", C["testo_disabilitato"])],
                   upperbordercolor=[("disabled", C["linea"])],
                   lowerbordercolor=[("disabled", C["linea"])],
                   foreground=[("disabled", C["testo_disabilitato"])])

        st.configure("TLabelframe", background=C["sfondo_app"], bordercolor=C["linea"])
        st.configure("TLabelframe.Label", background=C["sfondo_app"], foreground=C["testo"],
                     font=fn["normal_bold"])

        st.configure("Treeview", background=C["sfondo_campi"], fieldbackground=C["sfondo_campi"],
                     foreground=C["testo"], rowheight=sc(24), bordercolor=C["linea"], font=fn["normal"])
        st.map("Treeview", background=[("selected", C["selezione"])],
               foreground=[("selected", C["selezione_testo"])])
        st.configure("Treeview.Heading", background=C["tabella_intestazione"],
                     foreground=C["tabella_intestazione_testo"], relief="flat", font=fn["normal_bold"],
                     padding=sc(4))

        st.configure("Horizontal.TProgressbar", background=C["progress"], troughcolor=C["progress_sfondo"],
                     bordercolor=C["linea"], lightcolor=C["progress"], darkcolor=C["progress"])

        st.configure("TButton", padding=[sc(16), sc(8)], relief="flat", font=fn["normal_bold"])
        self._button_style("TButton", C["secondario"], C["secondario_hover"],
                           C["secondario_premuto"], C["secondario_testo"])
        self._button_style("Primary.TButton", C["primario"], C["primario_hover"],
                           C["primario_premuto"], C["testo_su_pulsante"])
        self._button_style("Save.TButton", C["salva"], C["salva_hover"],
                           C["salva_premuto"], C["testo_su_pulsante"])

        # (lightcolor/darkcolor = colore della linea: niente effetto rilievo, solo bordo piatto)
        st.configure("TNotebook", background=C["sfondo_app"], bordercolor=C["linea"],
                     lightcolor=C["linea"], darkcolor=C["linea"],
                     tabmargins=[sc(4), sc(4), 0, 0], tabposition="n")
        st.configure("TNotebook.Tab", font=fn["large_bold"], padding=self.tab_pad,
                     background=C["linguetta_inattiva"], foreground=C["linguetta_inattiva_testo"],
                     bordercolor=C["linea"], lightcolor=C["linea"], darkcolor=C["linea"])

    def _button_style(self, name, bg, hover, pressed, fg):
        st = self.style
        st.configure(name, background=bg, foreground=fg, bordercolor=bg, lightcolor=bg,
                     darkcolor=bg, focuscolor=bg)
        dis, dis_fg = C["pulsante_disabilitato"], C["pulsante_disabilitato_testo"]
        st.map(name,
               background=[("disabled", dis), ("pressed", pressed), ("active", hover)],
               foreground=[("disabled", dis_fg)],
               bordercolor=[("disabled", dis), ("pressed", pressed), ("active", hover)],
               lightcolor=[("disabled", dis), ("pressed", pressed), ("active", hover)],
               darkcolor=[("disabled", dis), ("pressed", pressed), ("active", hover)])

    def on_tab_changed(self, _evt=None):
        colors = C["linguette_attive"]
        color = colors[self.nb.index(self.nb.select()) % len(colors)]
        self.style.map("TNotebook.Tab",
                       background=[("selected", color), ("active", C["linguetta_hover"])],
                       foreground=[("selected", C["linguetta_attiva_testo"])],
                       bordercolor=[("selected", C["linea"]), ("!selected", C["linea"])],
                       lightcolor=[("selected", C["linea"]), ("!selected", C["linea"])],
                       darkcolor=[("selected", C["linea"]), ("!selected", C["linea"])],
                       focuscolor=[("selected", color), ("!selected", C["linguetta_inattiva"])],
                       padding=[("selected", self.tab_pad)],
                       expand=[("selected", [0, 0, 0, 0])])

    def run_bg(self, work, done):
        def target():
            try:
                res, err = work(), None
            except Exception as e:
                res, err = None, e
            self._q.put((done, res, err))
        threading.Thread(target=target, daemon=True).start()

    def post_ui(self, fn):
        self._q.put((lambda res, err: fn(), None, None))

    def _poll(self):
        try:
            while True:
                done, res, err = self._q.get_nowait()
                done(res, err)
        except queue.Empty:
            pass
        self.after(100, self._poll)

    def check_updates(self):
        self.tab_tools.mark_checking()

        def work():
            return {k: check_tool(k) for k in TOOLS}

        def done(results, err):
            if err:
                return
            self.check_results = results
            self.tab_tools.update_rows(results)

        self.run_bg(work, done)

    def on_close(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)
        self.destroy()


def main():
    enable_hidpi()
    set_windows_app_id()
    os.makedirs(BIN_DIR, exist_ok=True)
    App().mainloop()


if __name__ == "__main__":
    main()