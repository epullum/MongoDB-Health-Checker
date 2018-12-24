import monitorUI as mui
import tkinter as tk

#Function to build the application GUI.
def main():
    myGui = tk.Tk()
    myGui.title("MongoDB Health Checker")
    mui.Gui(myGui)
    myGui.mainloop()




#Calls the main function to start the application.
main()