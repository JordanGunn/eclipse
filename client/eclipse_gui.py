# ------------------------------------------------------------------------------
# GUI module for Eclipse
# Written by Sam May
# ------------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from multiprocessing import freeze_support
import eclipse_config

import os
import base64
import sys


class ECLIPSE_GUI:

    def __init__(self):
        self.root = tk.Tk()
        self.open_root_gui_on_top()
        self.set_icon(self.root)
        self.root.title("Eclipse Client")
        self.root.resizable(width=False, height=False)
        self.main_gui()

    def open_root_gui_on_top(self):
        """
        Open the ECLIPSE GUI window on top of other windows,
        but allow other windows to be placed on top
        after it's opened.
        """
        # Open window on top of others
        self.root.attributes('-topmost', True)
        self.root.update()
        # Allow other windows to go on top of it afterwards
        self.root.attributes('-topmost', False)

    def open_popup_on_top_of_other_windows(self, popup):
        # Open window on top of others
        popup.attributes('-topmost', True)
        popup.update()
        # Allow other windows to go on top of it afterwards
        popup.attributes('-topmost', False)

    def set_icon(self, frame):

        if not eclipse_config.IS_LINUX:
            icon_data = base64.b64decode(eclipse_config.BC_LOGO_B64)
            icon_path = os.path.join(os.getcwd(), "bc.ico")

            with open(icon_path, 'wb') as icon_file:
                icon_file.write(icon_data)

            frame.wm_iconbitmap(icon_path)
            os.remove(icon_path)

    def main_gui(self):
        navFrame = tk.Frame(self.root)
        navFrame.grid(row=0, column=0, padx=50)

        #Delivery Button
        ttk.Button(
            navFrame, 
            width=30, 
            text="Delivery"
            ).grid(row=0, column=0, padx=5, pady=5, ipady=10)
        
        #LiDAR Button
        ttk.Button(
            navFrame, 
            width=30, 
            text="LiDAR"
            ).grid(row=0, column=1, padx=5, pady=5, ipady=10)
        
        #NAS Box Button
        ttk.Button(
            navFrame, 
            width=30, 
            text="NAS Box"
            ).grid(row=1, column=0, padx=5, pady=(0,5), ipady=10)
        
        #NAS Box Button
        ttk.Button(
            navFrame, 
            width=30, 
            text="NAS Box"
            ).grid(row=1, column=1, padx=5, pady=(0,5), ipady=10)
        
def main():
    gui = ECLIPSE_GUI()
    gui.root.mainloop()


if __name__ == '__main__':
    freeze_support()
    main()
