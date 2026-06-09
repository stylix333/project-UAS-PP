# main.py
import tkinter as tk
from gui import KizunaApp

def main():
    root = tk.Tk()
    app = KizunaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
