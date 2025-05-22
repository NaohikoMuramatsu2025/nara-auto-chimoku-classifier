::call conda activate gdal_10
@echo off
cd /d "%~dp0\Python_SRC"
::python create_patches_winpath_final_clean_fixed.py

::python land_use_guess.py
python land_use_guess_fixed.py