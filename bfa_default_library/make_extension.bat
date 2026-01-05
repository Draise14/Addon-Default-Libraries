
:: Define where the Blender or Bforartists executable is and it's name

set PATH="C:\3D_Stuff\Bforartists 5.0.0\bforartists"

:: Make sure you run this script in the addon folder with it's contents, ei, where the __init__.py is.
cd /d %~dp0
%PATH% --command extension build
echo REPORT: Done! && color 0a
pause