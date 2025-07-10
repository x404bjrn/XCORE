# ════════════════════════════════════════════════════════════════════ XCORE ══
# Copyright (C) 2025, Xeniorn | x404bjrn
# Lizenziert - siehe LICENSE Datei für Details
# ─────────────────────────────────────────────────────────────────────────────
# TODO: Docstring einarbeiten
# TODO: Übersetzungen hinzufügen
import os
import io
import glob
import shutil
import hashlib
import requests
import platform

from xcore_framework.config.env import RUNTIME_PACKAGE


class XCoreRuntimeManager:
    def __init__(self):
        self.runtime_name = None
        self.runtime_base = None
        self.runtime_version = None
        self.runtime_binary_path = None
        self.runtime_download_url = None
        self.runtime_cache_file = None
        self.runtime_checksum_file = None
        self.runtime_checksum_url = None

        self.system_architecture = {
            "x86_64": "x64", "amd64": "x64", "arm64": "aarch64"
        }.get(platform.machine().lower())

        self.system_os = {
            "windows": "win", "linux": "linux", "darwin": "mac"
        }.get(platform.system().lower())

        self.runtime_extension = {
            "windows": ".zip", "linux": ".tar.xz", "darwin": ".tar.xz"
        }.get(platform.system().lower())

        if not self.system_os or not self.system_architecture:
            raise Exception("[❌] Plattform oder Architektur nicht unterstützt.")


    def __verify_checksum(self):
        print("[🔐] Überprüfung der Datei-Integrität...")
        try:
            response = requests.get(self.runtime_checksum_url)

            if response.status_code != 200:
                print("[!] Keine gültige '.sha256.txt' Datei gefunden\n"
                      "[*] überspringe Check...")
                return True  # Kein Check, aber auch kein Abbruch

            checksum_text = response.text.strip()
            remote_hash = checksum_text.split()[0]

        except Exception as e:
            print(f"[!] SHA256 konnte nicht geladen werden: {e}")
            return True  # Check überspringen bei Fehler

        sha256 = hashlib.sha256()

        with open(self.runtime_cache_file, "rb") as f:
            for block in iter(lambda: f.read(65536), b""):
                sha256.update(block)

        local_hash = sha256.hexdigest()

        if remote_hash == local_hash:
            print("[✅] Checksumme OK!...")
            return True

        else:
            print(f"[❌] Checksumme stimmt nicht überein!\n"
                  f"[Erwartet]: {remote_hash}\n"
                  f"[Gefunden]: {local_hash}")
            return False


    def __download_with_progress(self, url, load_desc="[📦]  Download..."):
        from tqdm import tqdm

        if self.runtime_name:
            load_desc = f"[📦] Download ({self.runtime_name})..."

        response = requests.get(url, stream=True)
        total = int(response.headers.get('content-length', 0))

        if self.runtime_name == "Java JDK":
            # Bei (Java) JDK download
            with open(str(self.runtime_cache_file), "wb") as f, tqdm(
                total=total, unit="B", unit_scale=True, desc=load_desc
            ) as bar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))
        else:
            # Alle anderen Archivdownloads
            buffer = io.BytesIO()
            progress_bar = tqdm(total=total, unit='B', unit_scale=True, desc=load_desc)

            for data in response.iter_content(chunk_size=1024):
                buffer.write(data)
                progress_bar.update(len(data))

            progress_bar.close()
            buffer.seek(0)

            self.runtime_cache_file = buffer


    def download_and_extract(self):
        if not os.path.exists(self.runtime_base):
            os.makedirs(self.runtime_base, exist_ok=True)

        print(f"[📥] Lade ({self.runtime_name}) von: {self.runtime_download_url}")
        self.__download_with_progress(self.runtime_download_url)

        if self.runtime_name == "Java JDK":
            # Bei Java JDK Download Checksum Prüfung durchführen
            # TODO: Andere Runtimes auch mit Checksum Prüfung hinzufügen
            if not self.__verify_checksum():
                raise Exception("[!] Abbruch wegen fehlerhafter Datei!...")

        if self.runtime_download_url.endswith(".zip"):
            import zipfile
            with zipfile.ZipFile(self.runtime_cache_file) as z:
                z.extractall(self.runtime_base)

        elif self.runtime_extension == ".tar.xz" or self.runtime_extension == ".tar.gz":
            import tarfile
            ext = "xz"
            if self.runtime_download_url.endswith(".gz"):
                ext = "gz"

            with tarfile.open(fileobj=self.runtime_cache_file, mode=f"r:{ext}") as tar:
                tar.extractall(self.runtime_base)

                if self.runtime_name == "Node.js":
                    inner_dir = os.path.join(
                        self.runtime_base,
                        f"node-{self.runtime_version}-{self.system_os}-{self.system_architecture}"
                    )
                    if os.path.isdir(inner_dir):
                        for f in os.listdir(inner_dir):
                            shutil.move(os.path.join(inner_dir, f), self.runtime_base)
                        os.rmdir(inner_dir)
        else:
            raise Exception("[❌] Unbekanntes Archivformat...")


    def clean(self):
        if os.path.exists(self.runtime_base):
            print(f"[🧹] Entferne {self.runtime_name}-Runtime unter {self.runtime_base}")
            shutil.rmtree(self.runtime_base)
            print(f"[✅] {self.runtime_name}-Runtime erfolgreich entfernt...")

        else:
            print(f"[!] Keine {self.runtime_name}-Runtime zum Entfernen gefunden...")


class BashRuntimeManager(XCoreRuntimeManager):
    def __init__(self,
                 base=RUNTIME_PACKAGE["RUNTIME_BASH"],
                 version=RUNTIME_PACKAGE["RUNTIME_VERSION_BASH"],
                 name="Git Bash"):
        super().__init__()

        self.runtime_base = base
        self.runtime_version = version
        self.runtime_name = name
        self.runtime_binary_path = os.path.join(
            self.runtime_base, "usr", "bin", "sh.exe"
        )
        self.__get_download_url()


    def __get_download_url(self):
        filename = f".windows.1/MinGit-{self.runtime_version}-{self.system_architecture.replace('x', '')}-bit.zip"
        self.runtime_download_url = f"https://github.com/git-for-windows/git/releases/download/v{self.runtime_version}{filename}"


    def get_binary(self) -> str:
        if self.system_os == "win":
            if os.path.isfile(self.runtime_binary_path):
                return os.path.abspath(self.runtime_binary_path)

            print("[ℹ️] Bash nicht vorhanden!...\n"
                  "[⏬] Starte automatischen Download...")

            self.download_and_extract()

            if os.path.isfile(self.runtime_binary_path):
                print("[✅] Bash erfolgreich installiert!")
                return os.path.abspath(self.runtime_binary_path)

            raise FileNotFoundError("[❌] Bash konnte nicht installiert werden!...")

        elif self.system_os in ["linux", "mac"]:
            return "/bin/bash"

        else:
            raise Exception("[❌] System nicht unterstützt!...")


class JavaRuntimeManager(XCoreRuntimeManager):
    def __init__(self,
                 base=RUNTIME_PACKAGE["RUNTIME_JAVA"],
                 name="Java JDK"):
        super().__init__()

        self.runtime_base = base
        self.runtime_name = name
        self.runtime_cache_file = os.path.join(self.runtime_base, "jdk_download.tmp")
        self.runtime_checksum_file = os.path.join(self.runtime_base, "jdk.sha256")
        self.runtime_binary_path = []
        self.runtime_download_url = self.__get_download_url()
        self.runtime_checksum_url = self.__get_checksum_url()

        if self.system_os == "win":
            self.system_os = "windows"

        elif self.system_os == "linux":
            self.runtime_extension = ".tar.gz"

        elif self.system_os == "mac":
            self.runtime_extension = ".tar.gz"


    def __resolve_latest_jdk_download_url(self):
        api_url = "https://api.github.com/repos/adoptium/temurin20-binaries/releases/latest"
        response = requests.get(api_url)
        data = response.json()
        assets = data.get("assets", [])

        for asset in assets:
            name = asset["name"]
            if f"jdk_{self.system_architecture}_{self.system_os}" in name and name.endswith(".zip"):
                return asset["browser_download_url"]

        raise Exception("[❌] Es wurde keine passende JDK-Datei im Release gefunden!...")


    def __get_download_url(self):
        return self.__resolve_latest_jdk_download_url()


    def __get_checksum_url(self):
        return self.__get_download_url() + ".sha256.txt"


    def find_java_bin(self):
        candidates = glob.glob(os.path.join(self.runtime_base, "**", "bin", "java*"), recursive=True)
        java_bin = [f for f in candidates if os.path.basename(f) == "java" or os.path.basename(f) == "java.exe"]
        javac_bin = [f for f in candidates if os.path.basename(f) == "javac" or os.path.basename(f) == "javac.exe"]

        if not java_bin or not javac_bin:
            raise Exception("[❌] Java oder Javac wurde nicht gefunden!...")

        self.runtime_binary_path = [os.path.abspath(java_bin[0]), os.path.abspath(javac_bin[0])]


    def get_binary(self):
        try:
            self.find_java_bin()
            print(f"[✅] Java bereits vorhanden: {self.runtime_binary_path[0]}")

            return self.runtime_binary_path[0], self.runtime_binary_path[1]

        except:
            print("[ℹ️] Java nicht vorhanden!...\n"
                  "[⏬] Starte automatischen Download...")

        self.download_and_extract()
        os.remove(self.runtime_cache_file)

        self.find_java_bin()
        print(f"[✅] Java erfolgreich installiert: {self.runtime_binary_path[0]}")

        return self.runtime_binary_path[0], self.runtime_binary_path[1]


class NodeRuntimeManager(XCoreRuntimeManager):
    def __init__(self,
                 base=RUNTIME_PACKAGE["RUNTIME_NODE"],
                 version=RUNTIME_PACKAGE["RUNTIME_VERSION_NODE"],
                 name="Node.js"):
        super().__init__()

        self.runtime_base = base
        self.runtime_version = version
        self.runtime_name = name

        self.runtime_binary_path = os.path.join(
            self.runtime_base,
            f"node-{self.runtime_version}-{self.system_os}-{self.system_architecture}",
            "node.exe" if self.system_os == "win" else "bin/node"
        )
        self.__get_download_url()


    def __get_download_url(self):
        filename = f"node-{self.runtime_version}-{self.system_os}-{self.system_architecture}"
        url = f"https://nodejs.org/dist/{self.runtime_version}/{filename}{self.runtime_extension}"
        self.runtime_download_url = url


    def get_binary(self) -> str:
        if os.path.isfile(self.runtime_binary_path):
            return os.path.abspath(self.runtime_binary_path)

        print("[ℹ️] Node.js nicht vorhanden!...\n"
              "[⏬] Starte automatischen Download...")

        self.download_and_extract()

        if os.path.isfile(self.runtime_binary_path):
            print("[✅] Node.js erfolgreich installiert!")
            return os.path.abspath(self.runtime_binary_path)

        raise FileNotFoundError("[❌] Node.js konnte nicht installiert werden!...")


class PowerShellRuntimeManager(XCoreRuntimeManager):
    def __init__(self,
                 base=RUNTIME_PACKAGE["RUNTIME_POWERSHELL"],
                 version=RUNTIME_PACKAGE["RUNTIME_VERSION_POWERSHELL"],
                 name="PowerShell"):
        super().__init__()

        self.runtime_base = base
        self.runtime_version = version
        self.runtime_name = name

        self.runtime_binary_path = os.path.join(
            self.runtime_base,
            "pwsh.exe" if self.system_os == "win" else "pwsh"
        )
        self.__get_download_url()


    def __get_download_url(self):
        if self.system_os == "mac":
            self.system_os = "osx"

        if self.system_os == "mac" or self.system_os == "linux":
            self.runtime_extension = ".tar.gz"

        filename = f"PowerShell-{self.runtime_version}-{self.system_os}-{self.system_architecture}{self.runtime_extension}"
        url = f"https://github.com/PowerShell/PowerShell/releases/download/v{self.runtime_version}/{filename}"
        self.runtime_download_url = url


    def get_binary(self) -> str:
        if os.path.isfile(self.runtime_binary_path):
            return os.path.abspath(self.runtime_binary_path)

        print("[ℹ️] PowerShell nicht vorhanden!...\n"
              "[⏬] Starte automatischen Download...")

        self.download_and_extract()

        if os.path.isfile(self.runtime_binary_path):
            print("[✅] PowerShell erfolgreich installiert!...")
            return os.path.abspath(self.runtime_binary_path)

        raise FileNotFoundError("[❌] PowerShell konnte nicht installiert werden!...")
