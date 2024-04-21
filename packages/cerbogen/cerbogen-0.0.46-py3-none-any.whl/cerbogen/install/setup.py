import sys
import os
import platform
# import install_ffmpeg
from .install_location import install_location

def install_pywin32():
    if platform.system() == "Windows":
        try:
            import win32com.client
        except ImportError:
            print("pywin32 not found. Installing...")
            try:
                import pip
                pip.main(["install", "pywin32"])
            except Exception as e:
                print("Error installing pywin32:", e)
                sys.exit(1)


if __name__ == "__main__":
    
    install_pywin32()
    install_location()


