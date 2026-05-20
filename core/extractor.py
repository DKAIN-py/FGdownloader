import os
import sys
import shutil
import subprocess
import re
from PySide6.QtCore import QObject, Signal

class ExtractWorker(QObject):
    progress_update = Signal(str, int)  
    extraction_finished = Signal(str)   
    extraction_error = Signal(str, str) 

    def __init__(self, first_part_path, extract_dir, game_title):
        super().__init__()
        self.first_part_path = first_part_path
        self.extract_dir = extract_dir
        self.game_title = game_title
        
        # Resolve backend utility dynamically based on host OS
        self.unrar_cmd = self._resolve_unrar_backend()

    def _resolve_unrar_backend(self):
        """
        Determines the correct unrar execution string based on platform.
        """
        # If running on Linux (or macOS)
        if sys.platform.startswith("linux") or sys.platform == "darwin":
            # Look for 'unrar' in the system PATH environment
            system_unrar = shutil.which("unrar")
            if system_unrar:
                return system_unrar
            else:
                # If missing, throw an error early instructing how to fix it
                raise FileNotFoundError(
                    "Native 'unrar' binary not found on your system. "
                    "Please install it using your package manager (e.g., sudo pacman -S unrar)."
                )
        
        # Default Windows fallback configuration
        else:
            return os.path.join(os.path.dirname(__file__), "bin", "UnRAR.exe")

    def start_extraction(self):
        if not os.path.exists(self.first_part_path):
            self.extraction_error.emit(self.game_title, f"Source file missing: {self.first_part_path}")
            return

        os.makedirs(self.extract_dir, exist_ok=True)
        self.progress_update.emit("Extracting archive...", 0)

        # Build execution array command using resolved execution string
        cmd = [self.unrar_cmd, "x", "-o+", "-p-", self.first_part_path, self.extract_dir]

        try:
            # Hide console window only on Windows environments
            startupinfo = None
            if sys.platform.startswith("win"):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                startupinfo=startupinfo,
                encoding="utf-8",
                errors="replace"
            )

            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                
                match = re.search(r"(\d+)%", line)
                if match:
                    percentage = int(match.group(1))
                    self.progress_update.emit(f"Extracting package... {percentage}%", percentage)

            if process.returncode == 0:
                self.progress_update.emit("Extraction complete!", 100)
                self.extraction_finished.emit(self.game_title)
            else:
                self.extraction_error.emit(self.game_title, f"UnRAR exited with error code {process.returncode}")

        except Exception as e:
            self.extraction_error.emit(self.game_title, str(e))