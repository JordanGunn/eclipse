# ------------------------------------------------------------------------------
# GUI module for Eclipse
# Written by Sam May
# ------------------------------------------------------------------------------

# system imports
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkcalendar import Calendar
from multiprocessing import freeze_support
import os
import base64
import sys

# user imports
import eclipse_config
import eclipse_bridge

class ECLIPSE_GUI:

    def __init__(self):
        self.root = Tk()
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

        if not eclipse_config.NativeOS.IS_LINUX:
            icon_data = base64.b64decode(eclipse_config.BC_LOGO_B64)
            icon_path = os.path.join(os.getcwd(), "bc.ico")

            with open(icon_path, 'wb') as icon_file:
                icon_file.write(icon_data)

            frame.wm_iconbitmap(icon_path)
            os.remove(icon_path)

    def main_gui(self):
        navFrame = Frame(self.root)
        navFrame.grid(row=0, column=0, padx=50)

        #Delivery Button
        ttk.Button(
            navFrame, 
            width=30, 
            text="Delivery",
            command=lambda: self.deliveryWindow()
            ).grid(row=0, column=0, padx=10, pady=5, ipady=10)
        
        #LiDAR Button
        ttk.Button(
            navFrame, 
            width=30, 
            text="LiDAR"
            ).grid(row=0, column=1, padx=10, pady=5, ipady=10)
        
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
        
        
    def deliveryWindow(self):

        popup=Toplevel()
        self.open_popup_on_top_of_other_windows(popup)
        popup.resizable(False, False)
        self.set_icon(popup)
        popup.title("Delivery")
        popup.grab_set()
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Receiver Name - Name of the GeoBC staff member
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        receiverFrame = Frame(popup)
        receiverFrame.grid(row=0, column=0, padx=10, pady=5, sticky=W)
        ttk.Label(receiverFrame, text="Receiver name").grid(row=0, column=0, padx=5, sticky=W)
        
        receiverEntry = StringVar()
        ttk.Entry(
            receiverFrame,
            width=40,
            textvariable=receiverEntry
        ).grid(row=1, column=0, padx=5, pady=(0,5))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Date received - The date the drive was received
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        dateFrame = Frame(popup)
        dateFrame.grid(row=1, column=0, padx=10, pady=5, sticky=W)
        ttk.Label(dateFrame, text="Date received").grid(row=0, column=0, padx=5, sticky=W)
        
        calendar = Calendar(dateFrame, selectmode = 'day', date_pattern = 'yyyy-mm-dd')
        calendar.grid(row=1, column=0, padx=5, pady=(0,5))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Comments - Any additional comments from the user
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        commentFrame = Frame(popup)
        commentFrame.grid(row=2, column=0, padx=10, pady=5, sticky=W)
        ttk.Label(commentFrame, text="Comments").grid(row=0, column=0, padx=5, sticky=W)

        commentEntry = StringVar()
        ttk.Entry(
            commentFrame,
            width=55,
            textvariable=commentEntry
        ).grid(row=1, column=0, padx=5, pady=(0,5))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Submit Button - Saves and validates above info and sends to DB
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        submitFrame = ttk.Frame(popup)
        submitFrame.grid(row=3, column=0, padx=10, pady=5)
        submitClicked = IntVar()

        ttk.Button(
            submitFrame,
            text="Submit",
            command=lambda: self.deliveryValidation(receiverEntry, calendar, commentEntry, popup)
        ).grid(row=0, column=0)
            
    def deliveryValidation(self, receiverEntry, calendar, commentEntry, popup):
        receiverName = receiverEntry.get()
        dateReceived = calendar.get_date()
        comments = commentEntry.get()
        whitespaces = [" ", "\n"]

        try:

            # Receiver name ---------------------------------------------------------
            if receiverName == "":
                raise ValueError("Receiver name left blank! Please provide a receiver name.")
            
            isWhiteSpace = True
            for char in receiverName:
                if char in whitespaces:
                    continue
                else:
                    isWhiteSpace = False
                    break
            if isWhiteSpace:
                raise ValueError("Invalid receiver name! Please provide a valid receiver name.")
            
            eclipse_bridge.delivery(receiverName, dateReceived, comments)

        except ValueError as inputError:
            messagebox.showerror(
                "Input Error", 
                str(inputError)
                )
            self.open_popup_on_top_of_other_windows(popup)
            return
        
        popup.destroy()

        
    def path_select(self, pathSV):
        """
        Opens 'select folder' windows dialog,
        adds the selected folder to the relevant entrybox.
        """
        dirPath = filedialog.askdirectory(initialdir="/")
        pathSV.set(dirPath)

def main():
    gui = ECLIPSE_GUI()
    gui.root.mainloop()


if __name__ == '__main__':
    freeze_support()
    main()
