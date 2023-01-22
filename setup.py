import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning
# Run : python setup.py build

additional_modules = []

build_exe_options = {"includes": additional_modules,
                     "packages": ["sqlite3", "cryptography", "webbrowser", "pyperclip", "tkinter"],
                     "include_files": ['data.db']}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="Password Storer",
      version="1.0",
      description="Password Storer",
      options={"build_exe": build_exe_options},
      executables=[Executable(script="main.py", base=base)])