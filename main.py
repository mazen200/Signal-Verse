import tkinter as tk
from gui import home_page

# Initialize Tkinter window
root = tk.Tk()
root.title("Signal Visualizer")
root.geometry("800x600")
root.configure(bg="#1569C7")

# Show home page
home_page(root)

root.mainloop()
