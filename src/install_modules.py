import os

def check_install_modules():
    print("\
*****************************************************************************\n\
*    --- Require Python3 and pip were already installed on the system ---   *\n\
*****************************************************************************\n")

    os.system("python3 -m pip install --upgrade pip")
    # os.system("python3 -m pip install Pillow")
    # os.system("python3 -m pip install openpyxl")
    # os.system("python3 -m pip install pyaudio")
    os.system("python3 -m pip install pyinstaller")
    os.system("python3 -m pip install pyserial")
    os.system("python3 -m pip install paho-mqtt")
    os.system("python3 -m pip install flask")
    os.system("python3 -m pip install pyopenssl")
    os.system("python3 -m pip install psutil")
    os.system("python3 -m pip install asyncio")
    os.system("python3 -m pip install asgiref")

def main():
    check_install_modules()

if __name__ == "__main__":
    main()
