#%%
import os
from cx_Freeze import setup,Executable

relative_path="C:/Users/garreaum/Documents/GitHub/eurofel_tools/src/"

files = [relative_path+"img/excel.ico"]



target = Executable(
    script=relative_path+"eurofel_v2.py",
    base="Win32GUI",
    icon=relative_path+"img/excel.ico"
)
setup(
    name="EuroPy",
    version="1.0",
    description="Eurofell Tools",
    author="Antoine Malmezac",
    options={"build_exe":{"include_files":files}},
    executables=[target]
)
# %%
