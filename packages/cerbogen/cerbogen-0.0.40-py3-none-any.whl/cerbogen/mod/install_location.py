import tkinter as tk
from tkinter import filedialog
import shutil
import os

def install_location():

    # Function to select an installation location
    def select_installation_location():
        # Prompt user to select an installation location
        install_location = filedialog.askdirectory()
        if install_location:
            install_location_entry.delete(0, tk.END)
            install_location_entry.insert(0, install_location)

    def install_cerbogen():
        # Get the installation location
        install_location = install_location_entry.get()

        # Check if the installation location is provided
        if install_location:
            try:
                # Get the absolute path of the current directory
                current_dir = os.path.abspath(os.path.dirname(__file__))
                
                # Construct the destination file path
                code_file = os.path.join(current_dir, "..", "cerbogen.pyw")
                
                print( code_file )

                # Copy the file
                shutil.copy(code_file, install_location)


                # Show success message
                tk.messagebox.showinfo("Success", f" Run Cerbogen.pyw file to use the generator ")
                exit(0)

            except Exception as e:
                # Show error message if copying fails
                tk.messagebox.showerror("Error", f"Failed to copy file: {str(e)}")
        else:
            # Show error message if the installation location is not provided
            tk.messagebox.showerror("Error", "Please select an installation location.")


    # Create main window
    root = tk.Tk()
    root.title("Cerbogen Installation")

    # Installation location frame
    install_frame = tk.Frame(root, padx=10, pady=10)
    install_frame.pack()

    install_label = tk.Label(install_frame, text="Select Installation Location:")
    install_label.grid(row=0, column=0)

    install_location_entry = tk.Entry(install_frame, width=50)
    install_location_entry.grid(row=0, column=1)

    install_button = tk.Button(install_frame, text="Browse", command=select_installation_location)
    install_button.grid(row=0, column=2)

    # Install button
    install_button = tk.Button(root, text="Install Cerbogen", command=install_cerbogen)
    install_button.pack(pady=10)

    root.mainloop()
