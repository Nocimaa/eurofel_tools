#%%
import os
import sys
from cx_Freeze import setup,Executable

relative_path="C:/Users/ElisabethRibeiro/Documents/GitHub/eurofel_tools/src/"

python_install = os.path.dirname(sys.executable)

os.environ['TCL_LIBRARY'] = os.path.join(python_install, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(python_install, 'tcl', 'tk8.6')





files = [relative_path+"excel.ico",relative_path+"settings.erfl", relative_path+"country.json",
         (os.path.join(python_install, 'DLLs', 'tk86t.dll'), os.path.join('lib', 'tk86t.dll')),
         (os.path.join(python_install, 'DLLs', 'tcl86t.dll'), os.path.join('lib', 'tcl86t.dll'))]

base = 'Win32GUI'
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

target = Executable(
    script=relative_path+"eurofel_v2.py",
    base=base,
    icon=relative_path+"excel.ico",
    shortcut_name="EuroFel Utility",
    shortcut_dir=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
)
setup(
    name="EuroPy",
    version="1.0",
    description="Eurofell Tools",
    author="Antoine Malmezac",
    options={"build_exe":{"include_files":files,"includes":['tkinter','customtkinter','PIL','pandas','threading','fournisseur','magasin','verif','tarif']}},
    executables=[target]
)
# %%
