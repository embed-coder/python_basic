#!/usr/bin/python3
import os

def header():
    sHeader = "\
*****************************************************************************\n\
*                 --- Build Release for trane_bacnet app ---                *\n\
*            This sw will build all script and compile in one exe           *\n\
*            Require pyinstaller (pip install pyinstaller --user)           *\n\
*           NOTE: Uninstall PyQt4 if meet the exception from PyQt4          *\n\
*****************************************************************************\n"
    print(sHeader)

def main():
    # hotkey("win", "right")
    header()
    #if len(sys.argv) > 1:
    #    isRF = sys.argv[1]  # Re-flash or not?
    #else:
    #    isRF = '1'

    #if isRF == '1':
    #    os.system("START /WAIT qc-download-image.py ")

    # Increase version
    # f = open('VERSION')
    # VERSION = f.read()
    # f.close()
    # print('Current version:', VERSION)
    # verarr = VERSION.split(':')
    # numarr = verarr[1].split('.')
    # patch_num = int(numarr[2]) + 1
    # numarr[2] = str(patch_num)
    # verarr[1] = '.'.join(numarr)
    # VERSION = ':'.join(verarr)
    # print('Release version:', VERSION)
    # f = open('VERSION', 'w')
    # f.write(VERSION)
    # f.close()

    os.system("python3 -m PyInstaller -F trane_bacnet.py")
    #try:
    os.remove("trane_bacnet.spec")
    # os.system("RMDIR /S /Q build")
    # os.system("RMDIR /S /Q trane_bacnet_release")
    os.system("rm -rf build")
    os.system("rm -rf trane_bacnet_release")
    os.system("rm -rf __pycache__")
    os.rename("dist", "trane_bacnet_release")

    os.system("python3 -m PyInstaller -F bacnet_test.py")
    #try:
    os.remove("bacnet_test.spec")
    # os.system("RMDIR /S /Q build")
    # os.system("RMDIR /S /Q bacnet_test_release")
    os.system("rm -rf build")
    os.system("rm -rf bacnet_test_release")
    os.system("rm -rf __pycache__")
    os.rename("dist", "bacnet_test_release")

    #except:
    #    print("ERROR")

if __name__ == "__main__":
  main()
