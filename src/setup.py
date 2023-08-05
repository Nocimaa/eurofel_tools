import sys
import os
from cx_Freeze import setup,Executable

files = ["img/excel.ico"]

target = Executable(
    script="eurofel_v2.py",
    base="Win32GUI-cpython-39-darwin",
    icon="img/excel.ico"
)
setup(
    name="EuroPy",
    version="1.0",
    description="Eurofell Tools",
    author="Antoine Malmezac",
    options={"build_exe":{"include_files":files}},
    executables=[target]
)