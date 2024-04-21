import sys
import os
import platform
# import install_ffmpeg
import install_location

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


    
    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    shortcut_path = os.path.join(desktop_dir, "cerbogen_ui.lnk" if platform.system() == "Windows" else "cerbogen_ui.desktop")
    python_exe = sys.executable


    if platform.system() == "Windows":
        # Create Windows shortcut
        try:
            from win32com.client import Dispatch
        except ImportError:
            print("pywin32 not found. Install it to create shortcuts on Windows.")
            sys.exit(1)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "data", "img", "logo.ico")

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.TargetPath = python_exe
        shortcut.Arguments = ui_py_path
        shortcut.WorkingDirectory = os.path.dirname(ui_py_path)
        shortcut.IconLocation = icon_path
        shortcut.save()

    else:
        # Create shortcut for Linux and macOS
        with open(shortcut_path, 'w') as shortcut_file:
            shortcut_file.write("[Desktop Entry]\n")
            shortcut_file.write("Name=Cerbogen UI\n")
            shortcut_file.write("Exec={} {}\n".format(python_exe, ui_py_path))
            shortcut_file.write("Type=Application\n")
            shortcut_file.write("Terminal=false\n")
        os.chmod(shortcut_path, 0o755)  # Add execute permission for Linux/macOS

if __name__ == "__main__":
    
    install_pywin32()
    
