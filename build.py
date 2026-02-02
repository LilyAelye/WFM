import sys
import subprocess
import importlib



REQUIRED_PACKAGES = [
    "flask",
    "colorama",
    "console-menu",
    "regex",
    "flask-socketio",
    "waitress",
    "threading",
    "psutil"
]

def pre_setupdep():
    def install(package):
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package
        ])

    for package in REQUIRED_PACKAGES:
        try:
            importlib.import_module(package.replace("-", "_"))
        except ImportError:
            print(f"Installing missing dependency: {package}")
            install(package)
    
    from consolemenu import clear_terminal
    clear_terminal()
