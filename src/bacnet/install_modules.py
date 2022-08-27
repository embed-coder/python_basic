#!/usr/bin/python3
import os

def check_install_modules():
    print("\
*****************************************************************************\n\
*    --- Require Python3 and pip were already installed on the system ---   *\n\
*****************************************************************************\n")

    os.system("python3 -m pip install --upgrade pip")
    os.system("python3 -m pip install pyinstaller")
    os.system("python3 -m pip install pyserial")
    os.system("python3 -m pip install paho-mqtt")
    # os.system("python3 -m pip install bacpypes")
    os.system("python3 -m pip install BAC0")
    os.system("python3 -m pip install pandas")

def main():
    check_install_modules()

if __name__ == "__main__":
    main()
